# ReadMe for ReThinker agent

## Overview

ReThinker is a Python-based agent created Pierre Pinçon and Dorian Saurat for Ingeniuty I/O's course at UPSSITECH's engineering school, designed as a way to get the scribble and/or the prompt whenever an impuslion is received. Its goal is to temporize the system and avoid the data to be sent in the "wrong" order.

## Inputs

- **Scribble**: The scribble is received and stored.
- **Prompt**: The prompt is received and stored.
- **Impulsion**: When received, tells to the agent to set the scribble and the prompt as outputs.

## Outputs

- **Scribble**: When asked, the scribble is set as output.
- **Prompt**: When asked, the prompt is set as output.

## Requirements

- Python 3
- `ingescape`

## Installation

To install Scribbler, ensure that Python 3 is installed along with the required modules listed above. Clone or download the repository and run the `main.py` script.

## Usage

Run the script using the following command syntax:
`python3 main.py [agent_name] [network_device] [port]`
Replace `[agent_name]`, `[network_device]`, and `[port]` with appropriate values based on your setup.

## Network Device Compatibility

Scribbler is designed to work with various network devices. Ensure the network device is correctly specified when running the script.
