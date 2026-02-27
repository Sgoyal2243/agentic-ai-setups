from fastapi import FastAPI
from pydantic import BaseModel
from groq import Groq
import os

app = FastAPI()

# Initialize Groq client
client = Groq(api_key=os.getenv('GROQ_API_KEY'))

class Message(BaseModel):
    content: str

@app.post("/hello")
def hello_agent(message: Message):
    response = client.chat.completions.create(
        model="llama3-8b-8192",  # fast and free model
        messages=[
            {"role": "user", "content": message.content}
        ]
    )

    return {
        "response": response.choices[0].message.content

    }

@app.get("/helloget")
def hello_get_agent():
    return {
        "response": "hanji"

    }

