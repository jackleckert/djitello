# djitello with LLMs

A repository that enables to text or tell commands to a DJI Tello drone. The commands include ```taking off```,```landing```, ```moving in any direction```,```rotating clockwise or anticlockwise```, or doing a ```flip```.

## Installation
Clone the repo locally and install all dependencies in an environment with ```python>=3.10```:
```
git clone --recurse-submodules https://github.com/jackleckert/djitello
cd djitello/DJITelloPy
pip install -e .
```
You will require to ```brew install portaudio``` and ```pip install openai pyaudio SpeechRecognition```.

In the ```.env``` file, paste your OpenAI API key that can be retrieved from [here](https://platform.openai.com/settings/organization/api-keys).

## Runing
Run ```python drone_prompt_controller.py``` from the ```LLM``` folder.

From there you'll be able to choose whether to text or speak with the drone, and execute any command.
