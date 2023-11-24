# IngeSketch

## Presentation

IngeSketch is a project made for UPSSITECH Engineering School's third year. This project is part of the multimodal HMI course. The primary goal of this project was to design a project utilizing Ingescape Circle, a software suite that specializes in Systems Engineering, Software Interoperability and Human-System Integration. The sole requirement was to include the Whiteboard, utilized here as the print of the conversational agent and display screen, as the central element of the project.

Our two-member team, Pierre PINCON and Dorian SAURAT, chose to create a tool which's main objective is to allow users to create "text-to-image" or "image-to-image" visuals as desired using a broadcasting model through the whiteboard. This has been made possible through the can communicate with the agent either orally or in writing in English.

## Functionalities

The final system provides numerous functions, as outlined below:

- Image-to-image generation: the user can draw a shape on a canvas with or without describing roughly what they want to draw. The system will then generate an image based on the user's input.
- Text-to-image generation: the user can describe what they want to draw in English. The system will then generate an image based on the user's input. For this they simply need to not draw anything on the canvas.
- The user can communicate with the system either orally or in writing in English and ask it to perform a specific action. The system will then perform the requested action. The following actions can be done :
  - Redrawing : this makes it so the model generates another image based on the same user's input. The prompt and user's scribble stay unchanged.
  - Doing the sketch again : this makes it so the user can draw again on the canvas. The prompt stays unchanged.
  - Changing the prompt : this makes it so the user can change the prompt. The scribble stays unchanged.
  - Showing the sketch : this makes it so the user's sketch is displayed on top on the image generated by the model.

## Getting Started

### Dependencies

The dependancies are listed in the requirements.txt file.

### Installation

For the libraries:

```bash
pip install -r requirements.txt
```

For the diffusion model:

```
python3 model_downloader.py
```

If the model fails to download, you can download it manually [here](https://huggingface.co/runwayml/stable-diffusion-v1-5/resolve/main/v1-5-pruned-emaonly.ckpt?download=true) and put it in the "models" folder within the ImageGenerator agent.

### Usage

The conversational agent is the brain behind the system, when the systems is launched, a window will pop up :

- Write/Say "I want to draw" to enter the loop. Anything else won't be recognized if you don't state this or a similar sentence.
- The agent will then ask you what you want to draw. You can either write or say what you want to draw. If you want to draw a specific thing, you can say/write it. If you don't know what you want to draw, you can say/write "No clue" or a similar sentence, the system will use a default prompt for this case. The agent will ask you to draw something.
- A new window will pop up, you can draw what you want to draw. When you're done, you can press on "q" to close the window. After about 20 seconds, the system will generate an image based on your drawing and the prompt you gave. The image will be displayed on the whiteboard.

<!--

## Demonstration

![Opening/Closing demo](demo/OuvertureFermeture.mp4)

![Gatebell demo](demo/AppelEntrant.mp4)
-->
