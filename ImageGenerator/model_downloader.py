import os
import requests

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
