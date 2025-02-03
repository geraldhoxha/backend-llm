# API Documentation
API endpoints provided by the FastAPI-based backend for Backend and Large Language Models (LLM) services

## Base URLs
- Client Service ```/prompts```
- LLM Model Service ```/model```


## Endpoints
### 1. Health check

GET /health
- **Description**: Checks if the API service is healthy
- **Request**: No parameter required
- **Response**:
    ```json
    {
        "status": "Healthy"
    }
    ```

### 2. Text-To-Image generation (Client API)

POST /prompts/text2image
- **Description**: Sends a text prompt to the LLM service to generate an image
- **Request Body**:
    ```json
    {
        "text": "A description of the desired image"
    }
    ```
- **Response**: Streams an image in ```image/png``` format
- Errors:
  - **400**: Bad request if the request format is incorrect.
  - **500**: Server error if the image generation fails or the image server is unavailable

### 3. Text-to-image Generation (Model API)

POST /model/generate
- **Description**: Processes the text prompt using the Stable Diffusion model to generate an image
- **Request Body**:
    ```json
    {
        "text": "A description of the desired image"
    }
    ```
- **Response**: Streams an image in ```image/png``` format.
- Errors:
  - **500**: Server error if the image generation fails or the image server is unavailable