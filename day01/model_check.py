"""Model health check (v2): simple questions with known answers, run against each model.
A tiny "eval" - the same idea FDEs use to judge any model.  Run: python model_check.py
"""
import requests

OLLAMA_URL = "http://localhost:11434/api/chat"

TESTS = [
    ("What is 2 + 2? Reply with only the number.", "4"),
    ("What does REST stand for? Reply with only the full form.", "representational state transfer"),
    ("What is the capital of France? Reply with one word.", "paris"),
    ("Which is bigger, 9 or 12? Reply with only the number.", "12"),
]

# (label, model name, extra options)
RUNS = [
    ("cloud, free tier", "gpt-oss:20b-cloud", {}),
    ("local 3B, CPU only", "llama3.2", {"num_gpu": 0}),
    ("local 1B, CPU only", "llama3.2:1b", {"num_gpu": 0}),
]


def ask(model: str, prompt: str, extra: dict) -> tuple[bool, str]:
    """Returns (ok, text). ok is False when Ollama sends back an error."""
    resp = requests.post(
        OLLAMA_URL,
        json={
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False,
            "options": {"temperature": 0, **extra},
        },
        timeout=300,
    )
    data = resp.json()
    if "error" in data:
        return False, data["error"]
    return True, data["message"]["content"].strip()


if __name__ == "__main__":
    for label, model, extra in RUNS:
        passed = 0
        print(f"\n=== {model} ({label}) ===")
        for prompt, expected in TESTS:
            ok, text = ask(model, prompt, extra)
            if not ok:
                status = "ERROR"  # an error is never a pass
            elif expected in text.lower():
                status = "PASS"
                passed += 1
            else:
                status = "FAIL"
            print(f"{status:5} | {prompt[:40]:40} | {text[:60]}")
        print(f"Score: {passed}/{len(TESTS)}")
