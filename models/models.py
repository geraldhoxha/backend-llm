from pydantic import BaseModel, ConfigDict

# API endpoints for text-to-image (and others)
class URLS(ConfigDict):
    text2image="http://192.168.49.2:30081/model/generate"
    text2image_local="http://localhost:8081/model/generate"


# Expected structure from the client
class Prompt(BaseModel):
    text: str