import asyncio
from random import randint
from PIL import Image
import requests
import os
from time import sleep
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
HF_API_KEY = os.getenv("HuggingFaceAPIKey")

# Setup API and headers
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": f"Bearer {HF_API_KEY}"}

# Ensure required folders exist
os.makedirs("Data", exist_ok=True)
os.makedirs(os.path.join("Frontend", "Files"), exist_ok=True)

def open_images(prompt):
    folder_path = "Data"
    safe_prompt = prompt.replace(" ", "_")
    files = [f"{safe_prompt}{i}.jpg" for i in range(1, 5)]

    for jpg_file in files:
        image_path = os.path.join(folder_path, jpg_file)
        try:
            img = Image.open(image_path)
            print(f"Opening image: {image_path}")
            img.show()
            sleep(1)
        except IOError:
            print(f"Unable to open {image_path}")

async def query(payload):
    try:
        response = await asyncio.to_thread(requests.post, API_URL, headers=headers, json=payload)
        return response.content
    except Exception as e:
        print(f"[ERROR] Image query failed: {e}")
        return b""

async def generate_images(prompt: str):
    tasks = []
    for _ in range(4):
        payload = {
            "inputs": f"{prompt}, quality=4K, sharpness=maximum, Ultra High details, high resolution, seed = {randint(0, 1000000)}",
        }
        tasks.append(asyncio.create_task(query(payload)))

    image_bytes_list = await asyncio.gather(*tasks)
    safe_prompt = prompt.replace(" ", "_")
    for i, image_bytes in enumerate(image_bytes_list):
        file_path = os.path.join("Data", f"{safe_prompt}{i + 1}.jpg")
        with open(file_path, "wb") as f:
            f.write(image_bytes)

def GenerateImages(prompt: str):
    asyncio.run(generate_images(prompt))
    open_images(prompt)

# Main loop: watches for trigger from frontend
while True:
    try:
        data_file = os.path.join("Frontend", "Files", "ImageGeneration.data")
        with open(data_file, "r") as f:
            data = f.read().strip()

        parts = data.split(",")
        if len(parts) != 2:
            raise ValueError("[ERROR] ImageGeneration.data must contain exactly two comma-separated values like: prompt,True")

        Prompt, Status = parts
        if Status.strip() == "True":
            print("Generating Images ...")
            GenerateImages(prompt=Prompt.strip())

            with open(data_file, "w") as f:
                f.write("False,False")
            break
        else:
            sleep(1)

    except Exception as e:
        print(f"[ERROR] Main loop failed: {e}")
        sleep(1)
