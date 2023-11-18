#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  main.py
#  Scribbler version 1.0
#  Created by Ingenuity i/o on 2023/10/20
#

import sys
import ingescape as igs

# Initialize OpenCV drawing variables
import cv2
import numpy as np
import pickle
import base64
import numpy as np
from PIL import Image
import io
import base64
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageDraw
from tkinter import Tk, Canvas, ALL
from PIL import Image, ImageDraw

drawing = False
point = (-1, -1)

# Initialize the canvas and PIL image
canvas = None
image = Image.new("RGB", (500, 500), "white")
draw = ImageDraw.Draw(image)


scribble_path = "/home/pinconp/Images/ingescape/scribble_transparent.jpg"


def get_scribble():
    global drawing, point

    # Mouse callback for drawing
    def mouse_draw(event, x, y, flags, param):
        global drawing, point
        img_white_bg = param[0]
        if event == cv2.EVENT_LBUTTONDOWN:
            drawing = True
            point = (x, y)
        elif event == cv2.EVENT_LBUTTONUP:
            drawing = False
            cv2.line(img_white_bg, point, (x, y), (0, 0, 0), 3)
        elif event == cv2.EVENT_MOUSEMOVE and drawing:
            cv2.line(img_white_bg, point, (x, y), (0, 0, 0), 3)
            point = (x, y)

    # Initialize OpenCV drawing variables
    drawing = False
    point = (-1, -1)

    # Create a white canvas with 3 channels
    canvas_white_bg = np.ones((512, 512, 3), np.uint8) * 255

    # Show canvas for scribbling
    cv2.namedWindow("Canvas")
    cv2.imshow("Canvas", canvas_white_bg)
    cv2.waitKey(1)
    cv2.setMouseCallback("Canvas", mouse_draw, [canvas_white_bg])

    while True:
        cv2.imshow("Canvas", canvas_white_bg)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # Cleanup
    cv2.destroyAllWindows()

    # Create a transparent canvas from the black and white one
    canvas_transparent = np.zeros((512, 512, 4), np.uint8)
    canvas_transparent[:, :, :3] = canvas_white_bg
    canvas_transparent[:, :, 3] = 255  # set alpha channel to fully opaque
    black_pixels = np.all(canvas_white_bg == [0, 0, 0], axis=-1)
    # set alpha channel to fully opaque for black pixels
    canvas_transparent[black_pixels, 3] = 255
    # set alpha channel to transparent for non-black pixels
    canvas_transparent[~black_pixels, 3] = 0

    return canvas_white_bg


# inputs
def input_callback(iop_type, name, value_type, value, my_data):
    if value_type == igs.IMPULSION_T:
        scribble = get_scribble()
        igs.output_set_data("scribble", pickle.dumps(255 - scribble))

        # Convert the NumPy array to a PIL image
        image = Image.fromarray(scribble, "RGB")

        # Save the PIL image locally in PNG format in cas the user want to display it later
        image.save(scribble_path)
        igs.output_set_string("scribble_path", scribble_path)


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
        """Allows a pop up window to open so the user can scribble. The scribbling is then returned."""
    )
    igs.log_set_console(True)
    igs.log_set_file(True, None)
    igs.set_command_line(sys.executable + " " + " ".join(sys.argv))

    igs.input_create("start", igs.IMPULSION_T, None)

    igs.output_create("scribble", igs.DATA_T, None)
    igs.output_create("scribble_path", igs.STRING_T, None)

    igs.observe_input("start", input_callback, None)

    igs.start_with_device(sys.argv[2], int(sys.argv[3]))

    input()

    igs.stop()
