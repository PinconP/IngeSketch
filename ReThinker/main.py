#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  main.py
#  ReThinker version 1.0
#  Created by Ingenuity i/o on 2023/10/26
#

import sys
import ingescape as igs
import pickle
class scribble_prompt:
    def __init__(self, scribble=None, prompt=None):
        self.scribble = scribble
        self.prompt = prompt

#inputs
def input_callback_prompt(iop_type, name, value_type, value, my_data):
    if value_type == igs.STRING_T:
        pp.prompt = value
        print(value)
        
def input_callback_scribble(iop_type, name, value_type, value, my_data):
    if value_type == igs.DATA_T:
        pp.scribble = pickle.loads(value)

def input_callback_impusle(iop_type, name, value_type, value, my_data):
    if value_type == igs.IMPULSION_T:
        print(pp.prompt)
        igs.output_set_string("prompt", pp.prompt)
        igs.output_set_data("scribble", pickle.dumps(pp.scribble))

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
    igs.definition_set_description("""Stores a prompt and a scribble, and returns it when asked to.""")
    igs.log_set_console(True)
    igs.log_set_file(True, None)
    igs.set_command_line(sys.executable + " " + " ".join(sys.argv))

    igs.input_create("prompt", igs.STRING_T, None)
    igs.input_create("greenlight", igs.IMPULSION_T, None)
    igs.input_create("scribble", igs.DATA_T, None)

    igs.output_create("prompt", igs.STRING_T, None)
    igs.output_create("scribble", igs.DATA_T, None)
    pp = scribble_prompt()
    igs.observe_input("prompt", input_callback_prompt, None)
    igs.observe_input("greenlight", input_callback_impusle, None)
    igs.observe_input("scribble", input_callback_scribble, None)

    igs.start_with_device(sys.argv[2], int(sys.argv[3]))

    input()

    igs.stop()

