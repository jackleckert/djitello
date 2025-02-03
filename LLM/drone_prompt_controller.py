import json
import os
from openai import OpenAI
import speech_recognition as sr

import sys
djitellopy = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'DJITelloPy'))
if djitellopy not in sys.path:
    sys.path.append(djitellopy)
from djitellopy import Tello
from command_mapping import *


def convert_prompt_to_commands(client, prompt: str) -> list:
    """
    Calls an LLM to convert a natural language prompt into a JSON list of drone commands.
    
    """
    system_prompt = (
        "You are an assistant that translates natural language instructions into "
        "a JSON list of Tello drone commands and parameters. Valid commands are: takeoff, land, "
        "move_up, move_down, move_left, move_right, move_forward, move_back, "
        "rotate_clockwise, rotate_counter_clockwise, flip_left, flip_right, flip_forward, flip_back. "
        "Valid parameters are: the distance to move in cm (integer between 20-500cm, could be given in meters by user), the angle to rotate in degrees (integer 1-360)."
        "For each command, output a dictionary with keys 'command' and 'parameter'. "
        "Ensure only valid JSON is output."
    )
    user_prompt = f"Instruction: {prompt}"
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0  # Use temperature=0 for determinism
    )
    
    reply = response.choices[0].message.content.strip()
    print("LLM reply was:")
    print(reply)

    if reply.startswith("```"):
        lines = reply.splitlines()
        if len(lines) >= 3 and lines[0].startswith("```"):
            reply = "\n".join(lines[1:-1]).strip()
    try:
        commands = json.loads(reply)
        if isinstance(commands, str):
            commands = json.loads(commands)
        return commands
    except Exception as e:
        print("Failed to parse JSON from LLM reply:", e)
        return []

def get_drone_instruction(prompt: str, using_text: bool = True) -> str:
    """
    Gets the drone command instruction from the user.
    If using_text is True, it reads from standard input.
    Otherwise, it listens to audio via the microphone and converts it to text using the
    speech_recognition library and Google Speech Recognition.
    """
    if using_text:
        return input(prompt)
    else:
        if sr is None:
            print("Speech recognition module not available. Please install SpeechRecognition.")
            return ""
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening... Please speak your instruction.")
            audio = recognizer.listen(source, timeout=5)
        try:
            text = recognizer.recognize_google(audio)
            print("You said:", text)
            return text
        except sr.UnknownValueError:
            print("Speech Recognition could not understand audio.")
            return ""
        except sr.RequestError as e:
            print("Could not request results from Speech Recognition service; {0}".format(e))
            return ""

def main():
    
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    tello = Tello()
    tello.connect()
    print("Drone connected.")
    print("Battery level:", tello.get_battery())

    mode = ""
    while mode not in ["1", "2"]:
        mode = input("Select input mode: 1 for text input, 2 for speech input: ")
    using_text = (mode == "1")
    
    print("Enter your drone command instruction or say/type 'exit' to quit.")

    while True:
        
        instruction = get_drone_instruction(">> ", using_text)
        if instruction.lower() == "exit":
            break
        commands = convert_prompt_to_commands(client, instruction)
        print("LLM converted to commands:", commands)

        for cmd in commands:
            command_name = cmd.get("command")
            parameter = cmd.get("parameter", None)
            if command_name in COMMAND_MAPPING:
                try:
                    print(f"Executing {command_name} with parameter {parameter}")
                    COMMAND_MAPPING[command_name](tello, parameter)
                except Exception as e:
                    print(f"Error executing command {command_name}: {e}")
            else:
                print(f"Unknown or unsupported command: {command_name}")

    tello.end()

if __name__ == "__main__":
    main() 