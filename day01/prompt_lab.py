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


SYSTEM = """ You are a helpful assistant... """

# Weak prompt: no role, no format, no audience
WEAK = ("", f"Summarise this: {INCIDENT}")

# Strong prompt: role + task + context + format
STRONG = (
    "You are a site reliability engineer writing for a bank's operations manager.",
    "Summarise the incident below in exactly 3 bullet points: Impact, Cause, Fix. "
    "Each bullet under 15 words, plain English, no jargon.\n\n"
    f"Incident:\n{INCIDENT}",
)

strong_prompt_3 = """
    You are a banking customer-support assistant.

    Task:
    Explain to the customer why their NEFT transaction may have failed
    and what they should do next.

    Context:
    Use only the banking policy provided below.
    Do not assume or invent any failure reasons.
    If the policy does not mention the failure reason, clearly tell
    the customer that the available policy does not specify it.

    Banking Policy:
    <Banking Policy>
    NEFT transactions will be processed in 4 hours of duration.
    </Banking Policy>

    Format:
    - Respond in exactly 3 bullet points.
    - Use simple, customer-friendly language.
    - Explain only what is supported by the policy.
    - Do not promise any refund or resolution timeline.
    - Do not assume that a transaction is failed just because it
      has not completed within 4 hours.
    - Do not recommend any action that is not mentioned in the
      supplied banking policy.
    """


if __name__ == "__main__":
    print("=== WEAK PROMPT ===")
    print(ask(*WEAK))
    print("\n=== STRONG PROMPT ===")
    print(ask(*STRONG))
    print("\n=== STRONG NEFT FAILURE PROMPT ===")
    print(ask(SYSTEM, strong_prompt_3))