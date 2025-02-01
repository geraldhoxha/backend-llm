from fastapi import APIRouter

client = APIRouter(prefix="/prompt")

@client.post("/client")
async def prompt():
    return {"response": "Hello World"}