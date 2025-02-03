from fastapi import FastAPI
from routers.client import client

app = FastAPI()
app.include_router(client)

# Endpoint for health check
@app.get("/health")
async def healthcheck():
    return {"status": "Healthy"}