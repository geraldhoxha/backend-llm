from diffusers import StableDiffusionPipeline
import torch
from typing import Annotated
from fastapi import Depends
from pydantic import BaseModel
import transformers
transformers.utils.move_cache()

MODEL = "CompVis/stable-diffusion-v1-4"
MODEL2 = "mm00/anything-v3.0-light"

# default: 50
# lower decrease image quality but increase generation speed 
NUM_STEPS = 15
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Initialise the model
pipe = StableDiffusionPipeline.from_pretrained(MODEL2).to(DEVICE)

def get_model():
    return pipe
    
model_dep = Annotated[StableDiffusionPipeline, Depends(get_model)]


class Prompt(BaseModel):
    text: str