from diffusers import AltDiffusionPipeline
import torch


torch.cuda.empty_cache()
model_path = "BAAI/AltDiffusion-m9"
ckpt_path = "models/BAAI-AltDiffusion-2/checkpoint-100000"
pipe = AltDiffusionPipeline.from_pretrained(
    model_path,
    revision=None,
    torch_dtype=torch.float16,
)
pipe.unet.load_attn_procs(ckpt_path)
pipe.to("cuda")
prompt = "파란 모자를 착용한 귀여운 토끼"
image = pipe(prompt=prompt, guidance_scale=3.0).images[0]
image.save(f"outputs/altDiffusion/{prompt[:10]}3.png")
