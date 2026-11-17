"""One place to choose the model - like application.properties in Spring.
Every course file imports MODEL and OPTIONS from here, so you switch models by editing only this file.
"""

# Option A (default): free Ollama cloud model. Runs on Ollama's servers, not your laptop.
MODEL = "llama3.2"
OPTIONS = {}

# Option B: if the cloud says "add usage credits" or "limit reached",
# put a # in front of the two lines above and remove the # from the two lines below.
# This runs llama3.2 (3B) on your laptop's CPU. num_gpu 0 stops it using the graphics chip,
# which is what produced the garbled answers on your laptop.
# MODEL = "llama3.2"
# OPTIONS = {"num_gpu": 0}
