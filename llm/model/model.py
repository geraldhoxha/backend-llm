from diffusers import StableDiffusionPipeline
import torch
from typing import Annotated
from fastapi import Depends
from pydantic import BaseModel
import transformers
transformers.utils.move_cache()

MODEL = "CompVis/stable-diffusion-v1-4"
MODEL2 = "mm00/anything-v3.0-light"

# Default: 50
# Lower decrease image quality but increase generation speed 
NUM_STEPS = 15
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Initialise the Stable DIffusion Pipeline
pipe = StableDiffusionPipeline.from_pretrained(MODEL2).to(DEVICE)


# Dependency to retreive the pre-initialized model
def get_model():
    return pipe
    
# Dependency for FastAPI endpoints using Annotated for dependency injection.
model_dep = Annotated[StableDiffusionPipeline, Depends(get_model)]


# Expected structure from the client
class Prompt(BaseModel):
    text: str