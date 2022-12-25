import os
import io

from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from PIL import Image
import openai

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.post("/")
def generate_file(image: UploadFile, description: str = Form()):
    image_bytes = io.BytesIO()
    new_image = Image.open(image.file)
    new_image.save(image_bytes, format="PNG")

    mask = Image.new("L", new_image.size, 0)
    mask_bytes = io.BytesIO()
    mask.save(mask_bytes, format="PNG")

    response = openai.Image.create_edit(
        image=image_bytes.getvalue(),
        mask=mask_bytes.getvalue(),
        prompt=description
    )

    return response["data"][0]["url"]
