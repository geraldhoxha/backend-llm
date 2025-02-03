from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from models.models import Prompt, URLS
import httpx

client = APIRouter(prefix="/prompts")

# Asynchronous function to call LLM api from the services.
async def async_api_call(url: str, text: str):
    # Async http client
    async with httpx.AsyncClient() as async_client:
        try:
            response = await async_client.post(url,
                            headers={"Content-Type": "application/json"},
                            json={"text": text},
                            timeout=120.0, # seconds
                            )

            # raise an exception for statuses 40x - 50x
            await response.raise_for_status()
            
            # Async generator tp stream response bytes
            async def stream_byres():
                async for chunk in await response.aiter_bytes():
                    yield chunk
                    
            return stream_byres()
        
        # Catch HTTP status errors (4xx and 5xx) and print error details
        except httpx.HTTPStatusError as status_error:
            raise HTTPException(status_code=status_error.response.status_code, detail="Image generation failed")
        except httpx.RequestError as request_error:
            raise HTTPException(status_code=500, detail="Image server unavailable")
        
        # Catch any other exceptions and raise them as HTTPExceptions
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


# Define an endpoint to handle text-to-image generation.
@client.post("/txt2image")
async def prompt(prompt: Prompt):
    resp = await async_api_call(URLS.text2image, prompt.text)
    # Stream the generated image to the client
    return StreamingResponse(resp, media_type="image/png")