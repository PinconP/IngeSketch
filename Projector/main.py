#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  main.py
#  Projector version 1.0
#  Created by Ingenuity i/o on 2023/10/28
#

import sys
import ingescape as igs
import io
import base64
from PIL import Image
import contextlib
import pickle


def image_to_base64(image_path):
    # Open image file
    with Image.open(image_path) as image:
        """# Make sure the image has an alpha (transparency) channel
        if image.mode != 'RGBA':
            print("Nuh-uh")
            print(image.mode)
            image = image.convert('RGBA')

        # Convert white pixels to transparent pixels
        data = image.getdata()
        newData = []
        for item in data:
            if item[0] == 255 and item[1] == 255 and item[2] == 255:
                newData.append((255, 255, 255, 0))
            else:
                newData.append(item)
        
        image.putdata(newData)"""

        # Convert the image to bytes
        image_bytes_io = io.BytesIO()
        image.save(image_bytes_io, format='PNG')
        
        # Get the byte array
        image_byte_array = image_bytes_io.getvalue()

        # Encode image as base64
        image_base64 = base64.b64encode(image_byte_array).decode('utf-8')

        return image_base64


#inputs
def input_callback_path(iop_type, name, value_type, value, my_data):
    # if value_type == igs.STRING_T and name == "path":
    path = value
    print(path)
        
    # Encode the byte array as Base64
    image_base64 = image_to_base64(path)

    # Your arguments list
    arguments_list = (image_base64, 10.0, 10.0, 512.0, 512.0)
    igs.service_call("Whiteboard", "addImage", arguments_list, "")
    
    
def input_callback_image(iop_type, name, value_type, value, my_data):
    """if value_type == igs.DATA_T and name == "image":"""
    image = pickle.loads(value)
        
    # Create a bytes buffer to save the image
    buffer = io.BytesIO()

    # Save the PIL image to the buffer in JPEG format
    image.save(buffer, format='JPEG')

    # Get the byte array
    image_byte_array = buffer.getvalue()

    # Encode as Base64
    image_base64 = base64.b64encode(image_byte_array).decode('utf-8')
        
    arguments_list = (image_base64, 10.0, 10.0, 512.0, 512.0)
        
        
    # arguments_list = (pickle.dumps(process_output), 256.0, 256.0, 512.0, 512.0)
    igs.service_call("Whiteboard", "addImage", arguments_list, "")   
        
    
    
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
    igs.definition_set_description("""Takes an image, either as a base64 input or a string corresponding to the absolute path of the picture, and displays it on the witheboard.""")
    igs.log_set_console(True)
    igs.log_set_file(True, None)
    igs.set_command_line(sys.executable + " " + " ".join(sys.argv))

    igs.input_create("path", igs.STRING_T, None)
    igs.input_create("image", igs.DATA_T, None)

    igs.observe_input("path", input_callback_path, None)
    igs.observe_input("image", input_callback_image, None)

    igs.start_with_device(sys.argv[2], int(sys.argv[3]))

    input()

    igs.stop()

