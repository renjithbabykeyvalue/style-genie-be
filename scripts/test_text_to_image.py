from src.services.generation.text_to_image import text_to_image
import uuid

file = text_to_image("Generate an image featuring a (single mannequin wearing a royal blue gown) adorned with exquisite beadings and floral lace. The mannequin should be (standing straight, facing the camera), and presenting the gown in a captivating floor-length design. Ensure meticulous attention to detail for a visually striking portrayal.", f"text_to_image/{str(uuid.uuid4())}.png")
print(file)

