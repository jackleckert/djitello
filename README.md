# djitello with LLMs

A repository that enables to text or tell commands to a DJI Tello drone. The commands include ```taking off```,```landing```, ```moving in any direction```,```rotating clockwise or anticlockwise```, or doing a ```flip```.

## Installation
Clone the repo locally and install all dependencies in a new environment:
```
git clone https://github.com/jackleckert/djitello
cd djitello/DJITelloPy
pip install -e .
```
You will require to ```brew install portaudio``` and ```pip install openai pyaudio SpeechRecognition```.

In the ```.env``` file, paste your OpenAI API key that you can retrieve from [here](https://platform.openai.com/settings/organization/api-keys).

## Runing
Run ```python drone_prompt_controller.py```.

From there you'll be able to choose whether to text or speak with the drone, and execute any command.
