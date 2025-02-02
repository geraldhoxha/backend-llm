import pytest
import httpx
from main import app
from fastapi import HTTPException
from unittest.mock import AsyncMock
from fastapi.testclient import TestClient
from routers.client import async_api_call

# Utility function to create async iterators
async def async_iter(iterable):
    for item in iterable:
        yield item
        
        
client = TestClient(app)

def test_health():
    response = client.get("/health")
    
    assert response.status_code == 200
    assert response.json() == {"status": "Healthy"}

@pytest.mark.asyncio
async def test_async_api_call_success(mocker):
    mock_response = AsyncMock()
    # Mock the aiter_bytes method to return an async iterator (using async_iter)
    mock_response.aiter_bytes = AsyncMock(return_value=async_iter([b"chunk1", b"chunk2"]))
    mock_response.raise_for_status = AsyncMock()
    mock_post = mocker.patch("httpx.AsyncClient.post", return_value=mock_response)
    
    url = "https://example.com/api"
    text = "test input"
    response = await async_api_call(url, text)
    
    # Convert the async iterator response to a list
    chunks = [chunk async for chunk in response]
    
    assert chunks == [b"chunk1", b"chunk2"]
    mock_post.assert_called_once_with(url, headers={"Content-Type": "application/json"}, json={"text": text}, timeout=120.0)


@pytest.mark.asyncio
async def test_async_api_call_request_error(mocker):
    mocker.patch("httpx.AsyncClient.post", side_effect=httpx.RequestError("Request failed"))
    
    url = "https://example.com/api"
    text = "test input"
    
    with pytest.raises(HTTPException) as exc_info:
        await async_api_call(url, text)
    
    assert exc_info.value.status_code == 500
    assert exc_info.value.detail == "Image server unavailable"

