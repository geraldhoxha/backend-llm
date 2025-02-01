from fastapi import FastAPI
from routers.client import client

app = FastAPI()
app.include_router(client)

@app.get("/")
async def home():
    return {"page": "main", "response": "Hello Home"}

@app.get("/health")
async def healthcheck():
    return {"status": "Healthy"}