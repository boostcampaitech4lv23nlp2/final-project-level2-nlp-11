import torch
from torch import autocast
from diffusers import StableDiffusionPipeline

# from diffusers import StableDiffusionImg2ImgPipeline

import bentoml
from bentoml.io import Image, JSON, Multipart
from pydantic import BaseModel


class StableDiffusionRunnable(bentoml.Runnable):
    SUPPORTED_RESOURCES = ("nvidia.com/gpu",)
    SUPPORTS_CPU_MULTI_THREADING = True

    def __init__(self):
        model_id = "stabilityai/stable-diffusion-2-1-base"
        ckpt_path = "./models/2-1-base-test-inference/checkpoint-15000"
        self.device = "cuda"

        txt2img_pipe = StableDiffusionPipeline.from_pretrained(
            model_id
        )
        txt2img_pipe.unet.load_attn_procs(ckpt_path)
        self.txt2img_pipe = txt2img_pipe.to(self.device)


    @bentoml.Runnable.method(batchable=False, batch_dim=0)
    def txt2img(self, input_data):
        prompt = input_data["prompt"]
        guidance_scale = input_data.get("guidance_scale", 7.5)
        height = input_data.get("height", 512)
        width = input_data.get("width", 512)
        num_inference_steps = input_data.get("num_inference_steps", 50)
        with autocast(self.device):
            images = self.txt2img_pipe(
                prompt=prompt,
                guidance_scale=guidance_scale,
                height=height,
                width=width,
                num_inference_steps=num_inference_steps,
            ).images
            image = images[0]
            return image


stable_diffusion_runner = bentoml.Runner(
    StableDiffusionRunnable, name="stable_diffusion_runner", max_batch_size=10
)

svc = bentoml.Service("stable_diffusion_fp16", runners=[stable_diffusion_runner])


@svc.api(input=JSON(), output=Image())
def txt2img(input_data):
    return stable_diffusion_runner.txt2img.run(input_data)


# img2img_input_spec = Multipart(img=Image(), data=JSON())
# @svc.api(input=img2img_input_spec, output=Image())
# def img2img(img, data):
#     return stable_diffusion_runner.img2img.run(img, data)
