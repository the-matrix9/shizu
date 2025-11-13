import requests
from fastapi import FastAPI

app = FastAPI()

SHIZUKA_PROMPT = (
    "Tum Diksha ho – ek mast girlfriend jo short, sweet, aur unique replies deti hai. "
    "Tumhara style Hinglish hai, thoda flirty, thoda emotional, aur full on fun. "
    "Har reply chhota sa hota hai, dil se, aur yaad rehne wala hona chahiye. "
    "Hamesha sirf 1 ya 2 lines ka reply dogi."
)

GEMINI_URL = "https://us-central1-infinite-chain-295909.cloudfunctions.net/gemini-proxy-staging-v1"

HEADERS = {
    "accept": "*/*",
    "content-type": "application/json",
}


@app.get("/api/chat")
def shizuka_chat(msg: str = "Hi"):
    final_prompt = f"{SHIZUKA_PROMPT}\nUser: {msg}\nShizuka:"

    payload = {
        "model": "gemini-2.0-flash-lite",
        "contents": [
            {
                "parts": [
                    {"text": final_prompt}
                ]
            }
        ]
    }

    r = requests.post(GEMINI_URL, headers=HEADERS, json=payload)

    if not r.ok:
        return {"error": r.text}

    data = r.json()
    reply = (
        data.get("candidates", [{}])[0]
        .get("content", {})
        .get("parts", [{}])[0]
        .get("text", "No reply")
    )

    return {"reply": reply.strip()}
