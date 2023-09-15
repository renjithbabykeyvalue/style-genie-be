# !pip install transformers accelerate
from diffusers import StableDiffusionControlNetInpaintPipeline, ControlNetModel,DDIMScheduler
from diffusers.utils import load_image
import numpy as np
import torch
import cv2
from PIL import Image


# device = "mps" if torch.backends.mps.is_available() else "cpu"
device = "cpu"
generator = torch.Generator(device).manual_seed(1)


# init_image = Image.open(
    # "./resources/test_img_dress.png"
# )

init_image = Image.open('./astronaut_rides_horse_refined.png')

init_image.save('./results/img_to_img_sd/opened_img.png')
init_image = init_image.resize((512, 512))
im_np = np.array(init_image)
im_fg = np.array(im_np[:, :, :-1])
im_msk = 255 - np.array(im_np[:, :, -1])


mask_image = Image.fromarray(im_msk)
mask_image = mask_image.resize((512, 512))

# # get canny image
canny_image = cv2.Canny(im_fg, 100, 200)
canny_image = canny_image[:, :, None]
canny_image = np.concatenate([canny_image, canny_image, canny_image], axis=2)
canny_image = Image.fromarray(canny_image)
canny_image.save('./results/img_to_img_sd/canny_img.png')

def make_inpaint_condition(image, image_mask):
    image = np.array(image.convert("RGB")).astype(np.float32) / 255.0
    image_mask = np.array(image_mask.convert("L")).astype(np.float32) / 255.0

    assert image.shape[0:1] == image_mask.shape[0:1], "image and image_mask must have the same image size"
    image[image_mask > 0.5] = -1.0  # set as masked pixel
    image = np.expand_dims(image, 0).transpose(0, 3, 1, 2)
    image = torch.from_numpy(image)
    return image


control_image = make_inpaint_condition(init_image, mask_image)

controlnet = [ControlNetModel.from_pretrained(
    "lllyasviel/control_v11p_sd15_inpaint", torch_dtype=torch.float16
),ControlNetModel.from_pretrained("lllyasviel/sd-controlnet-canny", torch_dtype=torch.float16)]
pipe = StableDiffusionControlNetInpaintPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5", controlnet=controlnet, torch_dtype=torch.float16
)

pipe.scheduler = DDIMScheduler.from_config(pipe.scheduler.config)
pipe.to(device)

# prompt = '''
#     Generate a photo of 
#     a mannequin wearing the dress from the input image.
#     Instructions:
#     1. Front view, centered, long shot photo
#     2. Dark grey background
#     3. Mannequin should in white colour
#     4. Mannequin should be standing. Full body with hands and neck. No face needed.
# '''

# prompt = '''Produce an image featuring a full-length mannequin wearing the dress from the provided input image. The scene should be well-lit, with a dark gray background. The mannequin should be at the center, standing upright with both arms relaxed by its side. Emphasize the dress's details, ensuring it fits the mannequin perfectly. Exclude facial features from the mannequin, focusing solely on the clothing's presentation.'''

# v_neck_prompt = '''Generate a full-length image of a mannequin wearing the provided dress, but with a noticeable alteration: transform the current neckline into an elegant V-neck design. Maintain a well-lit scene with a dark gray background, positioning the mannequin at the center, standing upright with relaxed arms by its side. Pay close attention to the dress's original details, ensuring a perfect fit on the mannequin. Exclude any facial features from the mannequin, focusing exclusively on showcasing the new V-neck design seamlessly integrated with the garment's existing style.'''
turtle_neck_prompt = '''Produce a full-length image of a mannequin wearing the provided dress, but with a distinct alteration: change the existing neckline to a turtleneck design. Maintain a well-lit scene with a dark gray background, position the mannequin at the center, standing upright with relaxed arms by its side. Pay close attention to the dress's original details, ensuring a perfect fit on the mannequin. Exclude any facial features from the mannequin, concentrating solely on showcasing the new turtleneck design, seamlessly integrated with the garment's existing style.'''
# u_neck_prompt = '''Produce a full-length image of a mannequin wearing the provided dress, with a distinct alteration: create an attractive scoop neck design for the dress, giving it a stylish and flattering appearance. Maintain a well-lit scene with a dark gray background, position the mannequin at the center, standing upright with relaxed arms by its side. Pay close attention to the dress's original details, ensuring a perfect fit on the mannequin. Exclude any facial features from the mannequin, focusing solely on showcasing the new scoop neck design, seamlessly integrated with the garment's existing style.'''

prompt =  ''' A beautiful model wearing the dress from the input image, natural background '''

# generate image
images = pipe(
    prompt=prompt,
    num_inference_steps=20,
    generator=generator,
    eta=1.0,
    image=init_image,
    mask_image=mask_image,
    control_image=[control_image,canny_image],
    num_images_per_prompt=4,
    guidance_scale=10
).images
for index,image in enumerate(images):
    image.save(f'./results/img_to_img_sd/final_{index}.png')

