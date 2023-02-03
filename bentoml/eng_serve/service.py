import torch
from torch import autocast
from diffusers import StableDiffusionPipeline, DEISMultistepScheduler

# from diffusers import StableDiffusionImg2ImgPipeline

import bentoml
from PIL import Image
from bentoml.io import Image, JSON
from pydantic import BaseModel

import base64
from io import BytesIO
from typing import Optional


class UserInput(BaseModel):
    prompt: str = "a cute bunny rabbit"
    guidance_scale: float = 15
    size: int = 512
    num_inference_steps: int = 30
    num_images_per_prompt: int = 1


class StableDiffusionRunnable(bentoml.Runnable):
    SUPPORTED_RESOURCES = ("nvidia.com/gpu",)
    SUPPORTS_CPU_MULTI_THREADING = True

    def __init__(self):
        pretrained_model_path = "stabilityai/stable-diffusion-2-1-base"
        ckpt_path = "models/eng_model"
        self.device = "cuda"
        txt2img_pipe = StableDiffusionPipeline.from_pretrained(
            pretrained_model_path,
            torch_dtype=torch.float16,
        )
        txt2img_pipe.unet.load_attn_procs(ckpt_path)
        txt2img_pipe.scheduler = DEISMultistepScheduler.from_config(
            txt2img_pipe.scheduler.config
        )
        self.txt2img_pipe = txt2img_pipe.to(self.device)
        self.__name__ = "Stable_Diffusion_Runnable"

    @bentoml.Runnable.method(batchable=False, batch_dim=0)
    def txt2img(self, input_data):
        prompt = input_data.prompt
        guidance_scale = input_data.guidance_scale
        size = input_data.size
        num_inference_steps = input_data.num_inference_steps
        num_images_per_prompt = input_data.num_images_per_prompt
        with autocast(self.device):
            images = self.txt2img_pipe(
                prompt=prompt,
                guidance_scale=guidance_scale,
                height=size,
                width=size,
                num_inference_steps=num_inference_steps,
                num_images_per_prompt=num_images_per_prompt,
            ).images

            def to_base64(image: Image):
                with BytesIO() as output:
                    image.save(output, format="PNG")
                    return base64.b64encode(output.getvalue()).decode("utf-8")

        return {i: to_base64(image) for i, image in enumerate(images)}


eng_emoji_diffusion_runner = bentoml.Runner(
    StableDiffusionRunnable,
    name="eng_stable_diffusion_runner",
)
# make service
svc_eng = bentoml.Service("eng_emoji_diffusion", runners=[eng_emoji_diffusion_runner])


@svc_eng.api(input=JSON(pydantic_model=UserInput), output=JSON(), route="/eng_submit")
def eng2img(input_data):
    return eng_emoji_diffusion_runner.txt2img.run(input_data)
