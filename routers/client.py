from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from models.models import Prompt, URLS
import httpx

client = APIRouter(prefix="/prompts")

async def async_api_call(url: str, text: str):
    async with httpx.AsyncClient() as async_client:
        try:
            response = await async_client.post(url,
                            headers={"Content-Type": "application/json"},
                            json={"text": text},
                            timeout=120.0)

            # raise an exception for statuses 40x - 50x
            await response.raise_for_status()
            async def stream_byres():
                async for chunk in await response.aiter_bytes():
                    yield chunk
                    
            return stream_byres()
        
        except httpx.HTTPStatusError as status_error:
            print(f"HTTP error occurred: {status_error.response.status_code} - {status_error.response.text}")
            raise HTTPException(status_code=status_error.response.status_code, detail="Image generation failed")
        
        except httpx.RequestError as request_error:
            print(f"Request error occurred: {request_error}")
            raise HTTPException(status_code=500, detail="Image server unavailable")

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
@client.post("/txt2image")
async def prompt(prompt: Prompt):
    resp = await async_api_call(URLS.text2image, prompt.text)
    return StreamingResponse(resp, media_type="image/png")