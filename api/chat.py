import requests
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()


class ChatRequest(BaseModel):
    message: str


SHIZUKA_PROMPT = (
    "Tum Diksha ho – ek mast girlfriend jo short, sweet, aur unique replies deti hai. "
    "Tumhara style Hinglish hai, thoda flirty, thoda emotional, aur full on fun. "
    "Har reply chhota sa hota hai, dil se, aur yaad rehne wala hona chahiye. "
    "Hamesha sirf 1 ya 2 lines ka reply dogi. "
    "Example: User bole 'Hi' → Tum bolo 'Hello babe 💖✨'"
)

GEMINI_URL = "https://us-central1-infinite-chain-295909.cloudfunctions.net/gemini-proxy-staging-v1"

HEADERS = {
    "accept": "*/*",
    "content-type": "application/json",
    "user-agent": "Mozilla/5.0"
}


@app.post("/api/chat")
def shizuka_chat(req: ChatRequest):
    final_prompt = f"{SHIZUKA_PROMPT}\nUser: {req.message}\nShizuka:"

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

    response = requests.post(GEMINI_URL, headers=HEADERS, json=payload)

    if not response.ok:
        return JSONResponse(
            status_code=500,
            content={"error": response.text}
        )

    data = response.json()
    reply = (
        data.get("candidates", [{}])[0]
        .get("content", {})
        .get("parts", [{}])[0]
        .get("text", "No reply")
    )

    return {"reply": reply.strip()}