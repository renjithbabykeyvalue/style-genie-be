import base64
import requests
import os
from src.config import STABILITY_API_KEY
from src.services.aws import AWSClient
from PIL import Image


STABLE_DIFFUSION_XL_1_URL = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/image-to-image"

def image_to_image(prompt: str, input_image_path: str, s3_key: str):            
    
    
    init_image = Image.open(input_image_path)
    init_image = init_image.resize((1024, 1024))
    init_image.save(input_image_path)
    
    
    response = requests.post(STABLE_DIFFUSION_XL_1_URL,
        headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {STABILITY_API_KEY}"
        },
        files={
            "init_image": open(input_image_path, "rb")
        },
        data={
            "init_image_mode": "IMAGE_STRENGTH",
            "image_strength": 0.35,
            "steps": 40,
            "seed": 0,
            "cfg_scale": 5,
            "samples": 1,
            "text_prompts[0][text]": prompt,
            "text_prompts[0][weight]": 1,
            "text_prompts[1][text]": 'blurry, bad',
            "text_prompts[1][weight]": -1,
        }
    )

    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))

    data = response.json()

    # make sure the out directory exists
    if not os.path.exists("./out"):
        os.makedirs("./out")

    aws_client = AWSClient()
    for i, image in enumerate(data["artifacts"]):
        out_file = f'./out/txt2img_{image["seed"]}.png'
        with open(out_file, "wb") as f:
            f.write(base64.b64decode(image["base64"]))
            aws_client.upload_to_s3(out_file, s3_key)
            
    return aws_client.get_s3_public_url(s3_key)
