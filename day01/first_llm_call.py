"""Chapter 1: your first LLM calls.  Run: python first_llm_call.py"""
import requests

from llm_config import MODEL, OPTIONS  # choose the model in llm_config.py

OLLAMA_URL = "http://localhost:11434/api/chat"


def chat(messages: list[dict], temperature: float = 0.2) -> str:
    resp = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "messages": messages,
            "stream": False,
            "options": {**OPTIONS, "temperature": temperature},
        },
        timeout=300,
    )
    data = resp.json()
    if "error" in data:
        return f"[Ollama error] {data['error']}"
    return data["message"]["content"]


if __name__ == "__main__":
    print(chat([{"role": "user", "content": "Explain a REST API in one sentence."}]))

    messages = [
        {"role": "system", "content": "You are a senior Java architect. Answer in 2 short bullet points."},
        {"role": "user", "content": "When should I use Kafka instead of a REST call?"},
    ]
    answer = chat(messages)
    print(answer)

    messages.append({"role": "assistant", "content": answer})
    messages.append({"role": "user", "content": "Now give one risk of using Kafka."})
    print(chat(messages))

for i in range(3):
    print(chat([{"role": "user", "content": "Give me a name for a banking app."}], temperature=1.0))