"""Day 1 stretch (light version): bank ticket triage with structured JSON output.
Run: python ticket_triage.py
"""
from typing import Literal

import requests
from pydantic import BaseModel, ValidationError

from llm_config import MODEL, OPTIONS  # choose the model in llm_config.py

OLLAMA_URL = "http://localhost:11434/api/chat"


class Triage(BaseModel):
    category: Literal["card", "payments", "login", "fraud", "other", "account"]
    priority: Literal["low", "medium", "high"]
    summary: str


SYSTEM = (
    "You triage customer support tickets for a retail bank. "
    "Fraud or money already lost is always high priority. Reply only with JSON."
    "For answering any process related ticket refer process documents."
    "New password setting is allowed only if password gets expired."
)


def triage(ticket: str) -> Triage:
    resp = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "messages": [
                {"role": "system", "content": SYSTEM},
                {"role": "user", "content": ticket},
            ],
            "stream": False,
            "format": Triage.model_json_schema(),
            "options": {**OPTIONS, "temperature": 0},
        },
        timeout=300,
    )
    data = resp.json()
    if "error" in data:
        raise RuntimeError(data["error"])
    return Triage.model_validate_json(data["message"]["content"])


if __name__ == "__main__":
    tickets = [
        "I can't log in since this morning, it says my password expired.",
        "There are two payments of Rs 18,000 I never made on my card!",
        "How do I change the address on my account?",
        "My account is not showing correct balance",
        "I am not able to setup UPI payment for my bank account",
        "I need to change my account password but not able to proceed",
        "I need to attach a nominee with my account",
        "Need new chequebook",
        ""
    ]
    for t in tickets:
        try:
            r = triage(t)
            print(f"{r.priority.upper():6} {r.category:9} {r.summary}")
        except (ValidationError, RuntimeError) as e:
            print("Problem:", e)
