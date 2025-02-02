import json
import os
from openai import OpenAI

import sys
djitellopy = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'DJITelloPy'))
if djitellopy not in sys.path:
    sys.path.append(djitellopy)
from djitellopy import Tello
from command_mapping import *

def convert_prompt_to_commands(client, prompt: str) -> list:
    """
    Calls an LLM to convert a natural language prompt into a JSON list of drone commands.

    The LLM is instructed to return a JSON array like:
    [
        {"command": "takeoff", "parameters": val},
        {"command": "move_forward", "parameters": val},
        {"command": "land", "parameters": val}
    ]
    """
    system_prompt = (
        "You are an assistant that translates natural language instructions into "
        "a JSON list of Tello drone commands and parameters. Valid commands are: takeoff, land, "
        "move_up, move_down, move_left, move_right, move_forward, move_back, "
        "rotate_clockwise, rotate_counter_clockwise, flip_left, flip_right, flip_forward, flip_back. "
        "Valid parameters are: the distance to move in cm (integer), the angle to rotate in degrees (integer)."
        "For each command, output a dictionary with keys 'command' and 'parameter'. "
        "Ensure only valid JSON is output."
    )
    user_prompt = f"Instruction: {prompt}"
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    
    # Call the OpenAI API (or another provider's LLM interface)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0  # Use temperature=0 for determinism
    )
    
    reply = response.choices[0].message.content.strip()
    try:
        commands = json.loads(reply)
        return commands
    except Exception as e:
        print("Failed to parse JSON from LLM reply:", e)
        print("LLM reply was:")
        print(reply)
        return []

def main():
    # Initialize the Tello drone and switch to SDK mode.
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    tello = Tello()
    tello.connect()
    print("Drone connected.")

    print("Type your drone command instruction or 'exit' to quit.")

    while True:
        user_input = input(">> ")
        if user_input.lower() == "exit":
            break

        # Convert natural language prompt into a list of commands
        commands = convert_prompt_to_commands(client, user_input)
        print("LLM converted to commands:", commands)

        # Execute each command
        for cmd in commands:
            command_name = cmd.get("command")
            parameter = cmd.get("parameter", None)
            if command_name in COMMAND_MAPPING:
                try:
                    print(f"Executing {command_name} with parameters {parameter}")
                    COMMAND_MAPPING[command_name](tello, parameter)
                except Exception as e:
                    print(f"Error executing command {command_name}: {e}")
            else:
                print(f"Unknown or unsupported command: {command_name}")

    # Ensure the drone is closed down nicely.
    tello.end()

if __name__ == "__main__":
    main() 