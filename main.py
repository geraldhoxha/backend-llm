from fastapi import FastAPI
from routers.client import client

app = FastAPI()
app.include_router(client)

@app.get("/health")
async def healthcheck():
    return {"status": "Healthy"}