from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import os

app = FastAPI()

# permitir requests desde Jupyter
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class Prompt(BaseModel):
    message: str

@app.post("/generate")
def generate(prompt: Prompt):

    completion = client.chat.completions.create(
        model="gpt-4.1-mini",   # o gpt-4.1, gpt-5.1, etc.
        messages=[
            {"role": "user", "content": prompt.message}
        ]
    )

    response = completion.choices[0].message.content
    return {"response": response}
