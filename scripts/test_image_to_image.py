from src.services.generation.image_to_image import image_to_image
import uuid

s3_key = f"image_to_image/{str(uuid.uuid4())}.png"
prompt = "A beautiful model wearing the dress from the input image, natural background."

file = image_to_image(prompt=prompt,input_image_path="samples/dress-input.png", s3_key=s3_key)
print(file)

