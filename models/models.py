from pydantic import BaseModel, ConfigDict


class URLS(ConfigDict):
    text2image="http://192.168.49.2:30081/model/generate"
    text2image_local="http://localhost:8081/model/generate"

class Prompt(BaseModel):
    text: str