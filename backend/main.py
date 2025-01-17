import os
from dotenv import load_dotenv
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from groq import Groq
import requests
from bs4 import BeautifulSoup

class Input(BaseModel):
    link: str
    prompt: str


load_dotenv()
app = FastAPI()

client = Groq(
    # This is the default and can be omitted
    api_key=os.environ.get("GROQ_API_KEY"),
)

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db ={
    "items": []}
@app.get("/")
async def root():
    return {"message": "Hello World"}



@app.post("/chat")
async def chat_bot(input: Input):
    website = requests.get(input.link)
    soup = BeautifulSoup(website.text, "html.parser")
    body_content = soup.body.get_text(separator="\n", strip=True) # Extract plain text
    
    response = client.chat.completions.create(
    messages=[
       {
            "role": "system",
            "content": "You are a helpful assistant. From website response answer the question. The website content is: " + body_content
        },
        {
            "role": "user",
            "content": input.prompt
        }
    ],
    model="llama-3.3-70b-versatile",
    )
    return response.choices[0].message.content
    

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)