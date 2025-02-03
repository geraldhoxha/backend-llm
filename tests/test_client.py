import pytest
import httpx
from main import app
from fastapi import HTTPException
from unittest.mock import AsyncMock
from fastapi.testclient import TestClient
from routers.client import async_api_call

# FastAPI test instance
client = TestClient(app)

# Utility function to create async iterators from an iterable.
# This is used to simulate asynchronous streaming of data.
async def async_iter(iterable):
    for item in iterable:
        yield item

def test_health():
    response = client.get("/health")
    
    assert response.status_code == 200
    assert response.json() == {"status": "Healthy"}


# Test for a successful asynchronous API call.
@pytest.mark.asyncio
async def test_async_api_call_success(mocker):
    mock_response = AsyncMock()
    # Mock the aiter_bytes method to return an async iterator (using async_iter)
    mock_response.aiter_bytes = AsyncMock(return_value=async_iter([b"chunk1", b"chunk2"]))
    mock_response.raise_for_status = AsyncMock()
    
    # Patch the post method of httpx.AsyncClient to return the mock_response.
    mock_post = mocker.patch("httpx.AsyncClient.post", return_value=mock_response)
    
    url = "https://example.com/api"
    text = "test input"
    
    # Call the async_api_call function which uses the patched httpx.AsyncClient.post.
    response = await async_api_call(url, text)
    
    # Convert the async iterator response to a list
    chunks = [chunk async for chunk in response]
    assert chunks == [b"chunk1", b"chunk2"]
    
    # Assert that the patched post method was called once with the correct parameters.
    mock_post.assert_called_once_with(url,
                                      headers={"Content-Type": "application/json"},
                                      json={"text": text},
                                      timeout=120.0
                                      )

# Test for handling a request error during the asynchronous API call.
@pytest.mark.asyncio
async def test_async_api_call_request_error(mocker):
    # Patch the post method of httpx.AsyncClient to raise a RequestError.
    mocker.patch("httpx.AsyncClient.post", side_effect=httpx.RequestError("Request failed"))
    
    url = "https://example.com/api"
    text = "test input"
    
    # Assert the HTTPExeption is raised when calling asynv_api_call
    with pytest.raises(HTTPException) as exc_info:
        await async_api_call(url, text)
    
    # Assert status and message
    assert exc_info.value.status_code == 500
    assert exc_info.value.detail == "Image server unavailable"

