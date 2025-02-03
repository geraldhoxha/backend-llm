from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from model.model import model_dep, Prompt, NUM_STEPS
from io import BytesIO
import asyncio

router = APIRouter(prefix="/model", tags=["Model"])


# Endpoint to generate an image from text
@router.post("/generate")
async def generate(model: model_dep, prompt: Prompt):
    """
    This endpoint calls the model function in a background thread (to avoid blocking)
    and returns the generated image as a streamed PNG response
    """
    try:
        # Define a lambda function to run the model inference.
        func = lambda text: model(text, num_inference_steps=NUM_STEPS).images[0]
        image = await asyncio.to_thread(func, prompt.text)
        buffer = BytesIO()
        image.save(buffer, format="PNG")
        
        # Reset the buffer's pointer to the beginning so it can be read from
        buffer.seek(0)
        
        # Stream the generated image to the client
        return StreamingResponse(buffer, media_type="image/png")
    
    except Exception as e:
        # Raise 500 HTTPException if any error occurs
        raise HTTPException(status_code=500, detail=str(e))