"""Day 2: compare a weak prompt with a well-built one.  Run: python prompt_lab.py"""
import requests

from llm_config import MODEL, OPTIONS  # choose the model in llm_config.py

OLLAMA_URL = "http://localhost:11434/api/chat"

INCIDENT = (
    "At 02:10 the payments service began returning HTTP 503 errors. "
    "About 4,200 UPI payments failed over 35 minutes. A database connection pool "
    "was exhausted after a config change set max connections from 100 to 10. "
    "The change was rolled back at 02:45 and payments recovered."
)


def ask(system: str, user: str) -> str:
    messages = [{"role": "system", "content": system}] if system else []
    messages.append({"role": "user", "content": user})
    resp = requests.post(
        OLLAMA_URL,
        json={"model": MODEL, "messages": messages, "stream": False, "options": {**OPTIONS, "temperature": 0}},
        timeout=300,
    )
    data = resp.json()
    if "error" in data:
        return f"[Ollama error] {data['error']}"
    return data["message"]["content"]


# Weak prompt: no role, no format, no audience
WEAK = ("", f"Summarise this: {INCIDENT}")

# Strong prompt: role + task + context + format
STRONG = (
    "You are a site reliability engineer writing for a bank's operations manager.",
    "Summarise the incident below in exactly 3 bullet points: Impact, Cause, Fix. "
    "Each bullet under 15 words, plain English, no jargon.\n\n"
    f"Incident:\n{INCIDENT}",
)

if __name__ == "__main__":
    print("=== WEAK PROMPT ===")
    print(ask(*WEAK))
    print("\n=== STRONG PROMPT ===")
    print(ask(*STRONG))
