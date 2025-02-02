from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from model.model import model_dep, Prompt, NUM_STEPS
from io import BytesIO
import asyncio

router = APIRouter(prefix="/model", tags=["Model"])

@router.post("/generate")
async def generate(model: model_dep, prompt: Prompt):
    try:
        # Run model on a thread to move the blocking execution to a
        # background thread
        func = lambda text: model(text, num_inference_steps=NUM_STEPS).images[0]
        image = await asyncio.to_thread(func, prompt.text)
        buffer = BytesIO()
        image.save(buffer, format="PNG")
        
        buffer.seek(0)
        
        return StreamingResponse(buffer, media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))