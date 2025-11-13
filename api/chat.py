import requests
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

SHIZUKA_PROMPT = (
    "Tum Diksha ho – ek mast girlfriend jo short, sweet, aur unique replies deti hai. "
    "Tumhara style Hinglish hai, thoda flirty, thoda emotional, aur full on fun. "
    "Har reply chhota sa hota hai, dil se, aur yaad rehne wala hona chahiye. "
    "Hamesha sirf 1 ya 2 lines ka reply dogi."
)

GEMINI_URL = "https://us-central1-infinite-chain-295909.cloudfunctions.net/gemini-proxy-staging-v1"

HEADERS = {"accept": "*/*", "content-type": "application/json"}


@app.api_route("/api/chat", methods=["GET", "POST", "OPTIONS"])
async def shizuka_chat(request: Request):
    """
    GET  -> /api/chat?msg=Hello
    POST -> JSON body: {"message": "Hello"}
    OPTIONS -> returns allowed methods (for CORS / preflight)
    """
    if request.method == "OPTIONS":
        return JSONResponse({"ok": True, "methods": ["GET", "POST", "OPTIONS"]})

    # get message from GET query or POST json
    msg = None
    if request.method == "GET":
        msg = request.query_params.get("msg") or request.query_params.get("message") or "Hi"
    else:
        try:
            body = await request.json()
            msg = body.get("message") or body.get("msg") or "Hi"
        except Exception:
            # fallback if body not JSON
            msg = "Hi"

    final_prompt = f"{SHIZUKA_PROMPT}\nUser: {msg}\nShizuka:"

    payload = {
        "model": "gemini-2.0-flash-lite",
        "contents": [{"parts": [{"text": final_prompt}]}]
    }

    try:
        r = requests.post(GEMINI_URL, headers=HEADERS, json=payload, timeout=20)
    except Exception as e:
        return JSONResponse({"error": f"Upstream request failed: {e}"}, status_code=502)

    if not r.ok:
        return JSONResponse({"error": r.text}, status_code=502)

    data = r.json()
    reply = (
        data.get("candidates", [{}])[0]
        .get("content", {})
        .get("parts", [{}])[0]
        .get("text", "No reply")
    )

    return JSONResponse({"reply": reply.strip()})