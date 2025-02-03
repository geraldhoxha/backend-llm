import asyncio
import httpx
import pytest
import logging
from main import app
from PIL import Image
from io import BytesIO
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

client = TestClient(app)

def test_health():
    response = client.get("/health")
    
    assert response.status_code == 200
    assert response.json() == {"status": "Healthy"}


# Test image generation prompt
def test_image_generation():
    prompt = "Tree in the forest"
    response = client.post("/model/generate",
                           headers={"Content-Type": "application/json"},
                           json={"text": prompt})
    
    # Verify responses and image content
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"
    
    # Verify generated image
    image = Image.open(BytesIO(response.content))
    assert image.format == "PNG"
    assert image.mode == "RGB"
    

# Test multiple concurrent image generation requests
@pytest.mark.anyio
async def test_concurrent_requests(caplog):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as async_client:
        with caplog.at_level(logging.INFO):
            logger.info("Sending 4 requests")
            
            # Create a list of tasks for conturent requests
            task = [async_client.post("/model/generate",
                           headers={"Content-Type": "application/json"},
                           json={"text": "Red bee"}) for _ in range(4)]
            
            # Run all concurently
            responses = await asyncio.gather(*task)
            
            # Process responses
            for i, response in enumerate(responses):
                logger.info(f"Process {i+1}")
                
                # Verify responses and image content
                assert response.status_code == 200
                assert response.headers["content-type"] == "image/png"
                
                image = Image.open(BytesIO(response.content))
                assert image.format == "PNG"
                assert image.mode == "RGB"
            logger.info("Done with the task")
    
    # Print captured logs
    for record in caplog.records:
        print(record.levelname, record.message)