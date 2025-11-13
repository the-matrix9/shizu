import requests
from fastapi import FastAPI

app = FastAPI()

SHIZUKA_PROMPT = (
    "Tum Diksha ho – ek mast girlfriend ho. "
    "Hinglish me short, cute, flirty, emotional replies deti ho. "
    "Hamesha sirf 1–2 lines me jawab dogi. "
    "Example: User bole 'Hi' → Tum bolo 'Hello babe 💖✨'"
)

GEMINI_URL = "https://us-central1-infinite-chain-295909.cloudfunctions.net/gemini-proxy-staging-v1"


@app.get("/api/chat")
def shizuka(msg: str = "Hi"):
    prompt = f"{SHIZUKA_PROMPT}\nUser: {msg}\nShizuka:"

    payload = {
        "model": "gemini-2.0-flash-lite",
        "input": prompt           # <- REAL FIX 🔥
    }

    r = requests.post(GEMINI_URL, json=payload)

    if not r.ok:
        return {"error": r.text}

    data = r.json()

    # OUTPUT FIX
    reply = data.get("output_text", "").strip()

    return {"reply": reply}