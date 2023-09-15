from diffusers import DiffusionPipeline
import torch

device = "mps" if torch.backends.mps.is_available() else "cpu"

# device = "cpu"



# load both base & refiner
# base = DiffusionPipeline.from_pretrained(
#     "stabilityai/stable-diffusion-xl-base-1.0", torch_dtype=torch.float16, variant="fp16", use_safetensors=True
# )

base = DiffusionPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0", variant="fp16", use_safetensors=True
)
base.enable_attention_slicing()
base.to(device)

refiner = DiffusionPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-refiner-1.0",
    text_encoder_2=base.text_encoder_2,
    vae=base.vae,
    # torch_dtype=torch.float16,
    # torch_dtype=torch.float16,
    use_safetensors=True,
    variant="fp16",
)
base.enable_attention_slicing()
refiner.to(device)

# Define how many steps and what % of steps to be run on each experts (80/20) here
n_steps = 20
high_noise_frac = 0.8

# prompt = '''Generate an image featuring a (single mannequin wearing a royal blue gown) adorned with exquisite beadings and floral lace. The mannequin should be (standing straight, facing the camera), and presenting the gown in a captivating floor-length design. Ensure meticulous attention to detail for a visually striking portrayal.'''
# prompt = '''Produce an image featuring a (full-length mannequin wearing a dark blue gown). The (scene should be well-lit, with a dark gray background). The (mannequin should be at the center, standing upright with both arms relaxed) by its side. (Emphasize the dress's details, floral embellishments). (Exclude facial features from the mannequin, focusing solely on the clothing's presentation)'''
# prompt = '''Produce an image showcasing a (mannequin wearing a striking dark blue half length dress). The (scene should be well-lit, with a dark gray background). The (mannequin should be at the center, standing upright facing forward with both arms relaxed) by its side. Pay special attention to (emphasizing the dress's details, including floral embellishments). (Exclude facial features from the mannequin), focusing intently on presenting the (gorgeous half-length dress)'''
turtleneck_prompt = '''A (mannequin wearing) striking dark blue dress, Dress style - ( Turtle-neck design, Half sleeve, Calf Length, Floral Embellishments, Silk material), Scene Details - (Dark grey background, Mannequin at center, Standing upright with both arms relaxed, Upfront, Exclude facial features)'''
prompt = '''A (mannequin wearing) striking dark blue dress, Dress style - ( Round neck design, Half sleeve, Calf Length, Floral Embellishments, Silk material), Scene Details - (Dark grey background, Mannequin at center, Standing upright with both arms relaxed, Upfront, Exclude facial features)'''

# run both experts
image = base(
    prompt=prompt,
    num_inference_steps=n_steps,
    denoising_end=high_noise_frac,
    output_type="latent",
).images
image = refiner(
    prompt=prompt,
    num_inference_steps=n_steps,
    denoising_start=high_noise_frac,
    image=image,
).images[0]

image.save(f"astronaut_rides_horse_refined.png")
