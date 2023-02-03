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

    def __init__(self, pretrained_model_path, ckpt_path):
        self.device = "cuda"
        txt2img_pipe = StableDiffusionPipeline.from_pretrained(pretrained_model_path)
        txt2img_pipe.unet.load_attn_procs(ckpt_path)
        self.txt2img_pipe = txt2img_pipe.to(self.device)
        self.__name__ = "Stable_Diffusion_Runnable"

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


kor_emoji_diffusion_runner = bentoml.Runner(
    StableDiffusionRunnable(
        pretrained_model_path="stabilityai/stable-diffusion-2-1-base",
        ckpt_path="models/eng_model",
    ),
    name="kor_stable_diffusion_runner",
)
# make service
svc_kor = bentoml.Service("kor_emoji_diffusion", runners=[kor_emoji_diffusion_runner])


@svc_kor.api(input=JSON(), output=Image(), route="/kor_submit")
def kor2img(input_data):
    return kor_stable_diffusion_runner.txt2img.run(input_data)
