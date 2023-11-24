# ReadMe for Scribbler agent

## Overview

Scribbler is a Python-based agent created Pierre Pinçon and Dorian Saurat for Ingeniuty I/O's course at UPSSITECH's engineering school, designed to provide a simple and intuitive interface for users to draw scribbles on a digital canvas. This agent leverages OpenCV for drawing, NumPy for array manipulations, and PIL for image processing.

## Features

- **Drawing Canvas**: Utilizes OpenCV to create an interactive canvas where users can draw with their mouse.
- **Transparent Scribble Generation**: Converts the drawn scribbles into a transparent image format.
- **PIL Image Processing**: Utilizes PIL to handle image conversions and save the scribbles in a desired format.
- **Network Device Integration**: Works with network devices, allowing for broader application use.

## Requirements

- Python 3
- OpenCV (`cv2`)
- NumPy
- PIL (Python Imaging Library)
- Tkinter (for file dialogs)
- `ingescape`

## Installation

To install Scribbler, ensure that Python 3 is installed along with the required modules listed above. Clone or download the repository and run the `main.py` script.

## Usage

Run the script using the following command syntax:
`python3 main.py [agent_name] [network_device] [port]`
Replace `[agent_name]`, `[network_device]`, and `[port]` with appropriate values based on your setup.

### Drawing Interface

Upon triggering the input, a window titled 'Canvas' will pop up. You can draw on this canvas using your mouse. Press 'q' to quit the drawing interface.

### Outputs

- **Scribble Image**: The drawn scribble is saved as a transparent image.
- **Scribble Path**: The path to the saved scribble image is outputted for later access.

## Network Device Compatibility

Scribbler is designed to work with various network devices. Ensure the network device is correctly specified when running the script.

## Limitations

- The application currently only supports basic drawing and does not have features like undo for example.
