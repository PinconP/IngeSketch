#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  main.py
#  ImageGenerator version 1.0
#  Created by Ingenuity i/o on 2023/10/20
#

import sys
import ingescape as igs
import random
import numpy as np
import cv2
import torch
from pytorch_lightning import seed_everything
from share import *
import config
from annotator.util import resize_image, HWC3, nms
from annotator.hed import HEDdetector
from annotator.pidinet import PidiNetDetector
from cldm.model import create_model, load_state_dict
from cldm.ddim_hacked import DDIMSampler
import einops
import pickle
import numpy as np
from PIL import Image
import io
import os
from transformers import AutoModel, AutoTokenizer
import requests


class scribididle:
    def __init__(self, scribble=None, prompt=None):
        self.scribble = scribble
        self.prompt = prompt


# The path where the checkpoint is going to be saved
output_path = "./models/v1-5-pruned-emaonly.ckpt"

if not os.path.exists(output_path):
    # URL of the .ckpt file
    checkpoint_url = "https://huggingface.co/runwayml/stable-diffusion-v1-5/resolve/main/v1-5-pruned-emaonly.ckpt?download=true"
    # The path where the checkpoint is going to be saved
    output_path = "./models/v1-5-pruned-emaonly.ckpt"

    # Downloading the checkpoint
    response = requests.get(checkpoint_url)
    response.raise_for_status()  # This will raise an error if the download failed

    # Saving the file
    with open(output_path, "wb") as file:
        file.write(response.content)

    print(f"Checkpoint saved to {output_path}")


# Initialize variables
preprocessor = None
model_name = "control_v11p_sd15_scribble"
model = create_model(f"./models/{model_name}.yaml").cpu()
model.load_state_dict(
    load_state_dict("./models/v1-5-pruned-emaonly.ckpt", location="cuda"), strict=False
)
"""model.load_state_dict(
    load_state_dict(f"./models/{model_name}.pth", location="cuda"), strict=False
)"""
model = model.cuda()
ddim_sampler = DDIMSampler(model)


def process(
    det,
    input_image,
    prompt,
    a_prompt,
    n_prompt,
    num_samples,
    image_resolution,
    detect_resolution,
    ddim_steps,
    guess_mode,
    strength,
    scale,
    seed,
    eta,
):
    global preprocessor
    if "HED" in det:
        if not isinstance(preprocessor, HEDdetector):
            preprocessor = HEDdetector()

    if "PIDI" in det:
        if not isinstance(preprocessor, PidiNetDetector):
            preprocessor = PidiNetDetector()

    with torch.no_grad():
        input_image = HWC3(input_image)

        if det == "None":
            detected_map = input_image.copy()
        else:
            detected_map = preprocessor(resize_image(input_image, detect_resolution))
            detected_map = HWC3(detected_map)

        img = resize_image(input_image, image_resolution)
        H, W, C = img.shape

        detected_map = cv2.resize(detected_map, (W, H), interpolation=cv2.INTER_LINEAR)
        detected_map = nms(detected_map, 127, 1.0)
        detected_map = cv2.GaussianBlur(detected_map, (0, 0), 1.0)
        detected_map[detected_map > 4] = 255
        detected_map[detected_map < 255] = 0

        control = torch.from_numpy(detected_map.copy()).float().cuda() / 255.0
        control = torch.stack([control for _ in range(num_samples)], dim=0)
        control = einops.rearrange(control, "b h w c -> b c h w").clone()

        if seed == -1:
            seed = random.randint(0, 65535)
        seed_everything(seed)

        if config.save_memory:
            model.low_vram_shift(is_diffusing=False)

        cond = {
            "c_concat": [control],
            "c_crossattn": [
                model.get_learned_conditioning([prompt + ", " + a_prompt] * num_samples)
            ],
        }
        un_cond = {
            "c_concat": None if guess_mode else [control],
            "c_crossattn": [model.get_learned_conditioning([n_prompt] * num_samples)],
        }
        shape = (4, H // 8, W // 8)

        if config.save_memory:
            model.low_vram_shift(is_diffusing=True)

        model.control_scales = (
            [strength * (0.825 ** float(12 - i)) for i in range(13)]
            if guess_mode
            else ([strength] * 13)
        )
        # Magic number. IDK why. Perhaps because 0.825**12<0.01 but 0.826**12>0.01

        samples, intermediates = ddim_sampler.sample(
            ddim_steps,
            num_samples,
            shape,
            cond,
            verbose=False,
            eta=eta,
            unconditional_guidance_scale=scale,
            unconditional_conditioning=un_cond,
        )

        if config.save_memory:
            model.low_vram_shift(is_diffusing=False)

        x_samples = model.decode_first_stage(samples)
        x_samples = (
            (einops.rearrange(x_samples, "b c h w -> b h w c") * 127.5 + 127.5)
            .cpu()
            .numpy()
            .clip(0, 255)
            .astype(np.uint8)
        )

        results = [x_samples[i] for i in range(num_samples)]
    return [detected_map] + results


negative_prompt = "ugly, tiling, poorly drawn, out of frame, extra limbs, blurry, bad, blurred, watermark, grainy, signature, cut off, draft, text, logo"


# inputs
def input_callback_prompt(iop_type, name, value_type, value, my_data):
    if value_type == igs.STRING_T:
        pp.prompt = value
        print(value)
        if pp.prompt == "No clue":
            pp.prompt = "pretty, stunning, gorgeous, magnificent, marvelous, splendid, breathtaking, aesthetically pleasing, photogenic, refined, photorealistic, official art, unity 8k wallpaper, ultra detailed, beautiful and aesthetic, masterpiece,best quality, greg rutkowski"


def input_callback_scribble(iop_type, name, value_type, value, my_data):
    if value_type == igs.DATA_T:
        pp.scribble = pickle.loads(value)
    if pp.prompt is not None and pp.scribble is not None:
        input_merger(pp.prompt, pp.scribble)


def input_merger(prompt, scribble):
    process_output = process(
        "HED",
        scribble,
        prompt,
        "",
        negative_prompt,
        1,
        512,
        512,
        40,
        False,
        1.0,
        9.0,
        -1,
        1.0,
    )

    # Convert the NumPy array to a PIL image
    image = Image.fromarray(process_output[1], "RGB")
    image.save("/home/pinconp/Images/ingescape/output_model.jpg")

    print(type(image))
    igs.output_set_data("image_generated", pickle.dumps(image))

    print("Ready")


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("usage: python3 main.py agent_name network_device port")
        devices = igs.net_devices_list()
        print("Please restart with one of these devices as network_device argument:")
        for device in devices:
            print(f" {device}")
        exit(0)
    igs.agent_set_name(sys.argv[1])
    igs.definition_set_version("1.0")
    igs.definition_set_description(
        """Generates an image from a scribble and a prompt if one is provided."""
    )
    igs.log_set_console(True)
    igs.log_set_file(True, None)
    igs.set_command_line(sys.executable + " " + " ".join(sys.argv))
    igs.input_create("prompt", igs.STRING_T, None)
    igs.input_create("scribble", igs.DATA_T, None)

    igs.output_create("image_generated", igs.DATA_T, None)

    pp = scribididle()
    igs.observe_input("prompt", input_callback_prompt, None)
    igs.observe_input("scribble", input_callback_scribble, None)

    igs.start_with_device(sys.argv[2], int(sys.argv[3]))
    print("Initialization done, waiting for input...")

    input()

    igs.stop()
