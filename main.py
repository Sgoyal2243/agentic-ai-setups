from pydantic import BaseModel
from groq import Groq
from fastapi import FastAPI, Request
import requests

app = FastAPI()

# Telegram token and endpoint
TOKEN = "8750372549:AAGclv8--6edwlE_UYHGJhZ875esi2PgW3s"
TELEGRAM_API = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

# Initialize Groq client
client = Groq(api_key="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")

class Message(BaseModel):
    content: str

@app.post("/hello")
def hello_agent(message: Message):
    print(message)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",  # fast and free model
        messages=[
            {"role": "user", "content": message.content}
        ]
    )

    return {
        "response": response.choices[0].message.content

    }

@app.get("/helloget")
def hello_get_agent():
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",  # fast and free model
        messages=[
            {"role": "user", "content": "what is today's date"}
        ]
    )

    return {
        "response": response.choices[0].message.content
    }

@app.post(f"/webhook/{TOKEN}")
async def telegram_webhook(request: Request):
    update = await request.json()
    message = update.get("message")
    if not message:
        return {"ok": True}

    chat_id = message["chat"]["id"]
    user_text = message.get("text", "")
    user_id = str(message["from"]["id"])

    print(f"Received message from user {user_id}: {user_text}")
    # Send user input to AI agent
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # fast and free model
            messages=[
                {"role": "user", "content": user_text}
            ]
        )
        ai_reply = response.choices[0].message.content
    except Exception as e:
        ai_reply = f"Error: {e}"

    # Send response back to Telegram
    requests.post(
        TELEGRAM_API,
        json={"chat_id": chat_id, "text": ai_reply}
    )

    return {"ok": True}


@app.get(f"/webhook")
async def telegram_get(request: Request):
     return {
        "response": "hi"
    }
