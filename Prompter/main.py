#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  main.py
#  Prompter version 1.0
#  Created by Ingenuity i/o on 2023/10/24
#

import sys
import ingescape as igs
import tkinter as tk
from tkinter import simpledialog
import base64
import io
from PIL import Image
import matplotlib.pyplot as plt
import base64
import io
import json
from difflib import get_close_matches
import random
import speech_recognition as sr
from tkinter import simpledialog, messagebox,Button

import tkinter as tk
from tkinter import simpledialog
from tkinter import PhotoImage
from PIL import Image, ImageTk






# Load the synonyms from the JSON file
with open("synonyms.json", "r") as f:
    synonyms_data = json.load(f)

synonyms_for_redraw = synonyms_data.get("Redraw", [])

synonyms_for_scribble = synonyms_data.get("Show drawing", [])

synonyms_for_no_clue = synonyms_data.get("No clue", [])

synonyms_for_change_prompt = synonyms_data.get("Change the prompt", [])

synonyms_for_new_prompt = synonyms_data.get("New prompt ?", [])

synonyms_for_redo_sketch = synonyms_data.get("Redo the sketch", [])

synonyms_for_want_anything = synonyms_data.get("Want anything ?", [])

synonyms_for_prompt_used = synonyms_data.get("What's the prompt you used ?", [])

synonyms_for_want_draw = synonyms_data.get("I want to draw", [])

synonyms_for_no = synonyms_data.get("No", [])

synonyms_assemble = (
    synonyms_for_redraw
    + synonyms_for_scribble
    + synonyms_for_no_clue
    + synonyms_for_change_prompt
    + synonyms_for_new_prompt
    + synonyms_for_redo_sketch
    + synonyms_for_want_anything
    + synonyms_for_prompt_used
    + synonyms_for_want_draw
    + synonyms_for_no
)

def speech_recognition():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Veuillez dire quelque chose :")

        # recognizer.adjust_for_ambient_noise(source)

        try:
        
            # Record audio for a max of 5 seconds after speech has been detected
            # If no speech is detected for 5 seconds, then it will timeout
            audio_data = recognizer.listen(
                source, timeout=5, phrase_time_limit=5)

            text = recognizer.recognize_google(audio_data, language='en-US')
            print(f"Vous avez dit : {text}")
            return text
        except Exception as e:
            print(e)


def prompt_engineer(prompt):
    if is_synonym(prompt, synonyms_for_no_clue):
        prompt = "pretty, stunning, gorgeous, magnificent, marvelous, splendid, breathtaking, aesthetically pleasing, photogenic, refined, photorealistic, official art, unity 8k wallpaper, ultra detailed, beautiful and aesthetic, masterpiece, best quality, by Greg Rutkowski"
    else:
        prompt = prompt
    return prompt


def output_chat_message(message):
    igs.service_call("Whiteboard", "chat", message, "")
    user_input = get_user_input(message)
    return user_input


def find_best_match(usr_question, question):
    # print(question.shape)
    matches = get_close_matches(usr_question, question, n=1)
    return matches[0] if matches else None


# Function to check if a given word or phrase is in the list of synonyms
def is_synonym(word, synonyms):
    word_lower = word.lower()
    synonyms_lower = [s.lower() for s in synonyms]
    return word_lower in synonyms_lower


"""def get_user_input(windown_title="Input"):
    root = tk.Tk()
    root.withdraw()  # Cache la fenêtre principale de tkinter
    user_input = simpledialog.askstring(windown_title, "")
    return user_input"""


def get_user_input(window_title="Input"):
    # Initialize the root Tkinter widget
    root = tk.Tk()
    root.title(window_title)

    # Set the window size to 300x200 pixels
    root.geometry('500x100')  # Width x Height
    
    # Load the image using Pillow
    pil_image = Image.open("microphone.png")
    pil_image = pil_image.resize((50, 50), Image.Resampling.LANCZOS)  # Resize the image to 50x50 pixels

    # Convert the PIL image to a Tkinter-compatible photo image
    tk_image = ImageTk.PhotoImage(pil_image)
    # Configure the button with the image and command to call speech_recognition function
    button = Button(root, image=tk_image, command=lambda: simpledialog.askstring(window_title, "Enter something or press the button:"))
    button.image = tk_image  # Keep a reference so it's not garbage collected
    button.pack()

    # Function to be called when button is clicked, replacing the entry with the speech_recognition's return value
    def on_button_click():
        entry_var.set(speech_recognition())  # Calls speech_recognition and sets its return value to entry_var
        root.quit()  # Closes the Tkinter window

    button.config(command=on_button_click)

    # Set up the Entry widget variable and pack it
    entry_var = tk.StringVar()
    entry = tk.Entry(root, textvariable=entry_var)
    entry.pack()

    # Button to submit the entry
    submit_button = Button(root, text="Submit", command=root.quit)
    submit_button.pack()

    # Run the Tkinter loop until the user provides an input or clicks the speech_recognition button
    root.mainloop()

    # After the mainloop ends, fetch the entry's value (which might have been altered by the button)
    user_input = entry_var.get()
    root.destroy()  # Clean up the Tkinter root from memory
    return user_input


def replace_white_pixels(img_scribble_path, sd_generated_path, output_path):
    # Open both images
    with Image.open(sd_generated_path) as img_generated, Image.open(
        img_scribble_path
    ) as img_scribble:
        # Ensure both images are the same size
        if img_scribble.size != img_generated.size:
            print("The images must be the same size.")
            return

        # Get pixel data
        data1 = img_scribble.getdata()
        data2 = img_generated.getdata()

        # Initialize new data array
        new_data = []

        for i in range(len(data1)):
            pixel1 = data1[i]
            pixel2 = data2[i]

            # If the pixel in the first image is white
            if pixel1[0] >= 200 and pixel1[1] >= 200 and pixel1[2] >= 200:
                new_data.append(pixel2)  # Take pixel from the second image
            else:
                new_data.append(pixel1)  # Keep pixel from the first image

        # Apply new data
        img_scribble.putdata(new_data)

        # Save new image
        img_scribble.save(output_path)
        print(f"Saved superposed image as {output_path}")


# inputs
def input_callback(iop_type, name, value_type, value, my_data):
    if value_type == igs.IMPULSION_T and name == "greenlight":
        igs.service_call("Whiteboard", "chat", "Hello citizen of the Earth", "")
        
        
        looper = True
        while looper:
            user_input = output_chat_message(random.choice(synonyms_for_want_anything))
            igs.output_set_string("chat_message", user_input)
            user_input = find_best_match(user_input, synonyms_assemble)
            print(user_input)

            if isinstance(user_input, str):
                if is_synonym(user_input, synonyms_for_want_draw):
                    prompt_before_remodel = output_chat_message("What would you like to draw ?")
                    prompt = prompt_engineer(prompt_before_remodel)

                    igs.output_set_string("prompt", prompt)
                    igs.output_set_string("chat_message", prompt_before_remodel)

                    igs.output_set_impulsion("greenlight")
                if True==True: # TODO: Replace by a condition that allows to enter here only when there already are pictures on the Whiteboard
                    if is_synonym(user_input, synonyms_for_redraw):
                        igs.output_set_impulsion("greenlight_redraw")

                    elif is_synonym(user_input, synonyms_for_scribble):
                        print("if entered")

                        replace_white_pixels(
                            "/home/pinconp/Images/ingescape/scribble_transparent.jpg",
                            "/home/pinconp/Images/ingescape/output_model.jpg",
                            "/home/pinconp/Images/ingescape/scribble_transparent_over_generated.jpg",
                        )
                        igs.output_set_string(
                            "scribble_path",
                            "/home/pinconp/Images/ingescape/scribble_transparent_over_generated.jpg",
                        )

                    elif is_synonym(user_input, synonyms_for_redo_sketch):
                    # elif user_input == "Redo the sketch":
                        igs.output_set_string("prompt", prompt)
                        igs.output_set_impulsion("greenlight")

                    elif is_synonym(user_input, synonyms_for_change_prompt):
                        prompt_before_remodel = output_chat_message(
                            random.choice(synonyms_for_new_prompt)
                        )
                        prompt = prompt_engineer(prompt_before_remodel)

                        igs.output_set_string("prompt", prompt)
                        igs.output_set_string("chat_message", prompt_before_remodel)
                        igs.output_set_impulsion("greenlight_redraw")

                    elif is_synonym(user_input, synonyms_for_prompt_used):
                        prompt_used = 'The prompt I used was : "' + prompt + '"'
                        igs.service_call("Whiteboard", "chat", prompt_used, "")

                    elif is_synonym(user_input, synonyms_for_no):
                        looper = False
            else:
                igs.service_call(
                    "Whiteboard",
                    "chat",
                    "You're either having a stroke or I fail to recognize what you told me.",
                    "",
                )


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
        """Most basic conversationnal agent that could exist."""
    )
    igs.log_set_console(True)
    igs.log_set_file(True, None)
    igs.set_command_line(sys.executable + " " + " ".join(sys.argv))

    igs.input_create("greenlight", igs.IMPULSION_T, None)

    igs.output_create("scribble_path", igs.STRING_T, None)
    igs.output_create("prompt", igs.STRING_T, None)
    igs.output_create("chat_message", igs.STRING_T, None)
    igs.output_create("greenlight", igs.IMPULSION_T, None)
    igs.output_create("greenlight_redraw", igs.IMPULSION_T, None)

    igs.observe_input("greenlight", input_callback, None)

    igs.start_with_device(sys.argv[2], int(sys.argv[3]))

    input()

    igs.stop()
