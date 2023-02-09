from diffusers import StableDiffusionPipeline, DEISMultistepScheduler
import torch
import time

# user config
torch.cuda.empty_cache()
model_path = "stabilityai/stable-diffusion-2-1-base"
ckpt_path = "models/2-1-base-test-inference/checkpoint-54000"
prompt = "A cute bunny rabbit"
guidance_scale = 7


# original : 5.24 sec
pipe = StableDiffusionPipeline.from_pretrained(
    model_path,
    revision=None,
    torch_dtype=torch.float16,
)
pipe.unet.load_attn_procs(ckpt_path)
pipe.to("cuda")
start = time.time()
image = pipe(prompt=prompt, guidance_scale=guidance_scale).images[0]
print("time :", time.time() - start)
image.save(f"outputs/{prompt[:20]}_{guidance_scale}-1.png")

# using DEIS schduler : 4.06 sec
pipe = StableDiffusionPipeline.from_pretrained(
    model_path,
    revision=None,
    torch_dtype=torch.float16,
)
pipe.unet.load_attn_procs(ckpt_path)
pipe.scheduler = DEISMultistepScheduler.from_config(pipe.scheduler.config)
pipe.to("cuda")
generator = torch.Generator(device="cuda").manual_seed(0)
start = time.time()
image = pipe(prompt=prompt, guidance_scale=guidance_scale).images[0]
print("time :", time.time() - start)
image.save(f"outputs/{prompt[:20]}_{guidance_scale}-2.png")

# using DEIS schduler + generator : 4.05 sec
pipe = StableDiffusionPipeline.from_pretrained(
    model_path,
    revision=None,
    torch_dtype=torch.float16,
)
pipe.unet.load_attn_procs(ckpt_path)
pipe.scheduler = DEISMultistepScheduler.from_config(pipe.scheduler.config)
pipe.to("cuda")
generator = torch.Generator(device="cuda").manual_seed(0)
start = time.time()
image = pipe(prompt=prompt, generator=generator, guidance_scale=guidance_scale).images[0]
print("time :", time.time() - start)
image.save(f"outputs/{prompt[:20]}_{guidance_scale}-3.png")

