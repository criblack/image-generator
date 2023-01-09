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
def generate_file(image: UploadFile):
    image_bytes = io.BytesIO()
    new_image = Image.open(image.file)
    if new_image.size[0] != new_image.size[1]:
        new_image = new_image.resize((new_image.size[0], new_image.size[0]))

    new_image.save(image_bytes, format="PNG")

    response = openai.Image.create_variation(image=image_bytes.getvalue())

    return [image["url"] for image in response["data"]]
