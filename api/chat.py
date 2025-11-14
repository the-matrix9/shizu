import requests
import urllib.parse
from fastapi import FastAPI

app = FastAPI()

class ShizukaChat:
    def __init__(self):
        self.base_url = "https://text.pollinations.ai/"
        self.headers = {
            "accept": "*/*",
            "user-agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36"
        }

        # Shizuka's inbuilt vibe 🩷
        self.inbuilt_prompt = (
            "Tum Shizuka ho – ek mast girlfriend jo short, sweet, aur unique replies deti hai. "
            "Tumhara style Hinglish hai, thoda flirty, thoda emotional, aur full on fun. "
            "Har reply chhota, dil se, aur yaad rehne wala hona chahiye. "
            "Jab bhi user baat kare, Shizuka apne andaaz mein pyar aur swag ke sath jawab degi. "
            "Hamesha sirf 1 ya 2 lines ka reply dogi. "
            "Example: User bole 'Hi' → Tum bolo 'Hello babe 💖✨'"
        )

    def chat(self, user_msg: str):
        final_prompt = f"{self.inbuilt_prompt}\nUser: {user_msg}\nShizuka:"
        encoded_prompt = urllib.parse.quote(final_prompt)

        url = f"{self.base_url}{encoded_prompt}"
        response = requests.get(url, headers=self.headers)

        if not response.ok:
            return f"Error: {response.status_code}, {response.text}"

        return response.text.strip()


shizuka_ai = ShizukaChat()

@app.get("/api/chat")
def shizuka(msg: str = "Hi"):
    reply = shizuka_ai.chat(msg)
    return {"reply": reply}