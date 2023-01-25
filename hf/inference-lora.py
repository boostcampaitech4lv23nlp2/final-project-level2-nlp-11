from diffusers import StableDiffusionPipeline
import torch

model_path = "models/emoji-model-lora"
pipe = StableDiffusionPipeline.from_pretrained(model_path, torch_dtype=torch.float16)
pipe.unet.load_attn_procs(model_path)
pipe.to("cuda")

prompt = "Cute rabbit wearing a blue hat and eating a carrot"
image = pipe(prompt=prompt, guidance_scale=7.5).images[0]
image.save(f"outputs/{prompt[:10]}3.png")