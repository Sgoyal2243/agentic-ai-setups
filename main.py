from fastapi import FastAPI
from pydantic import BaseModel
from groq import Groq

app = FastAPI()

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




