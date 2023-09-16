import base64
import requests
import os
from src.config import STABILITY_API_KEY
from src.services.aws import AWSClient

STABLE_DIFFUSION_XL_1_URL = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"


def text_to_image(prompt: str, s3_key: str):
    body = {
        "steps": 10,
        "width": 1024,
        "height": 1024,
        "seed": 0,
        "cfg_scale": 8,
        "samples": 1,
        "style_preset": "photographic",
        "text_prompts": [
            {
                "text": prompt,
                "weight": 1
            },
            {
                "text": "blurry, bad",
                "weight": -1
            }
        ],
    }

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {STABILITY_API_KEY}",
    }

    response = requests.post(
        url=STABLE_DIFFUSION_XL_1_URL,
        headers=headers,
        json=body,
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
