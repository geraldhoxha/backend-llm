from fastapi import FastAPI
from routes.endpoint import router

app = FastAPI()
app.include_router(router)

# Endpoint for health check
@app.get("/health")
async def health_check():
    return {"status": "Healthy"}
