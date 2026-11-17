"""One place to choose the model - like application.properties in Spring.
Every course file imports MODEL and OPTIONS from here, so you switch models by editing only this file.
"""

# Your setup: llama3.2 (3B) on your laptop's CPU.
# num_gpu 0 stops Ollama using the graphics chip, which produced garbled answers on your laptop.
MODEL = "llama3.2"
OPTIONS = {"num_gpu": 0}

# If your laptop feels too slow, use the smaller model instead (less accurate):
# MODEL = "llama3.2:1b"
