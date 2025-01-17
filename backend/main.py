import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List



class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = None

class Items(BaseModel):
    items: List[Item]


app = FastAPI()

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

@app.get("/items", response_model=Items)
async def read_items():
    return Items(items=db["items"])

@app.post("/items", response_model=Item)
async def create_item(item: Item):
    db["items"].append(item)
    return item

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)