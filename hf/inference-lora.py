from diffusers import StableDiffusionPipeline
import torch


torch.cuda.empty_cache()
model_path = "stabilityai/stable-diffusion-2-1-base"
ckpt_path = "models/2-1-base-test-inference/checkpoint-15000"
pipe = StableDiffusionPipeline.from_pretrained(
    model_path,
    revision=None,
    torch_dtype=torch.float16,
)
pipe.unet.load_attn_procs(ckpt_path)
pipe.to("cuda")

prompt = "cute green bird"
image = pipe(prompt=prompt, guidance_scale=10, num_inference_steps=25).images[0]
image.save(f"outputs/{prompt[:10]}10.png")
