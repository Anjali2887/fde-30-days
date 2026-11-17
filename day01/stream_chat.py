"""Day 2: streaming - print the answer word by word as it is generated.  Run: python stream_chat.py"""
import json

import requests

from llm_config import MODEL, OPTIONS  # choose the model in llm_config.py

OLLAMA_URL = "http://localhost:11434/api/chat"


def stream_chat(messages: list[dict]) -> str:
    pieces = []
    with requests.post(
        OLLAMA_URL,
        json={"model": MODEL, "messages": messages, "stream": True, "options": {**OPTIONS, "temperature": 0.2}},
        stream=True,  # read the response as it arrives, line by line
        timeout=300,
    ) as resp:
        for line in resp.iter_lines():
            if not line:
                continue
            chunk = json.loads(line)  # each line is one small JSON object
            if "error" in chunk:
                print("\n[Ollama error]", chunk["error"])
                break
            piece = chunk.get("message", {}).get("content", "")
            print(piece, end="", flush=True)
            pieces.append(piece)
            if chunk.get("done"):
                break
    print()
    return "".join(pieces)


if __name__ == "__main__":
    answer = stream_chat([{"role": "user", "content": "Explain Kafka to a Java developer in 3 sentences."}])
    print(f"\n[{len(answer.split())} words received]")
