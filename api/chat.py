import requests
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

SHIZUKA_PROMPT = (
    "Tum Diksha ho – ek mast girlfriend jo short, sweet, aur unique replies deti hai. "
    "Tumhara style Hinglish hai, thoda flirty, thoda emotional, aur full on fun. "
    "Har reply chhota sa hota hai, dil se, aur yaad rehne wala hona chahiye."
)

GEMINI_URL = "https://us-central1-infinite-chain-295909.cloudfunctions.net/gemini-proxy-staging-v1"

HEADERS = {"accept": "*/*", "content-type": "application/json"}


@app.api_route("/api/chat", methods=["GET"])
async def shizuka_chat(msg: str = "Hi"):
    final_prompt = f"{SHIZUKA_PROMPT}\nUser: {msg}\nShizuka:"

    payload = {
        "model": "gemini-2.0-flash-lite",
        "contents": [{"parts": [{"text": final_prompt}]}]
    }

    r = requests.post(GEMINI_URL, headers=HEADERS, json=payload)

    data = r.json()
    reply = (
        data.get("candidates", [{}])[0]
        .get("content", {})
        .get("parts", [{}])[0]
        .get("text", "No reply")
    )

    return {"reply": reply.strip()}