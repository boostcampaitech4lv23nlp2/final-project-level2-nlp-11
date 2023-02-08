import torch
from torch import autocast
from diffusers import StableDiffusionPipeline

from typing import Dict

import bentoml
from bentoml.io import Image, JSON, Multipart
from pydantic import BaseModel


class StableDiffusionRunnable(bentoml.Runnable):
    """스테이블 디퓨전과 호환되는 Runnable 객체입니다."""

    SUPPORTED_RESOURCES = ("nvidia.com/gpu",)
    SUPPORTS_CPU_MULTI_THREADING = True

    def __init__(self, pretrained_model_path, ckpt_path):
        self.__name__ = "Stable_Diffusion_Runnable"
        self.device = "cuda"
        txt2img_pipe = StableDiffusionPipeline.from_pretrained(pretrained_model_path)
        txt2img_pipe.unet.load_attn_procs(ckpt_path)
        self.txt2img_pipe = txt2img_pipe.to(self.device)

    @bentoml.Runnable.method(batchable=False, batch_dim=0)
    def txt2img(self, input_data: JSON) -> Dict[Image]:
        """유저 텍스트 인풋을 받아서 Image를 Response 합니다.

        Args:
            input_data (JSON): JSON객체 입니다.\n
            prompt, guidance_scale, height, width, num_output, num_inference_steps를 포함할 수 있습니다.


        Returns:
            Image: 모델이 생성한 이미지입니다.
        """
        prompt = input_data["prompt"]
        guidance_scale = input_data.get("guidance_scale", 7.5)
        height = input_data.get("height", 512)
        width = input_data.get("width", 512)
        num_inference_steps = input_data.get("num_inference_steps", 50)
         = input_data.get("num_output", 1)
        with autocast(self.device):
            image_list = []
            image = self.txt2img_pipe(
                prompt=prompt,
                guidance_scale=guidance_scale,
                height=height,
                width=width,
                num_inference_steps=num_inference_steps,
            ).images[0]
            image_list.append(image)
            return image_list


eng_emoji_diffusion_runner = bentoml.Runner(
    StableDiffusionRunnable(
        pretrained_model_path="stabilityai/stable-diffusion-2-1-base",
        ckpt_path="models/eng_model",
    ),
    name="eng_stable_diffusion_runner",
)

kor_emoji_diffusion_runner = bentoml.Runner(
    StableDiffusionRunnable(
        pretrained_model_path="stabilityai/stable-diffusion-2-1-base",
        ckpt_path="models/eng_model",
    ),
    name="kor_stable_diffusion_runner",
)
# make service
svc = bentoml.Service(
    "multilingual_emoji_diffusion",
    runners=[eng_emoji_diffusion_runner, kor_emoji_diffusion_runner],
)


@svc.api(input=JSON(), output=Image(), route="/submit/kor")
def kor2img(input_data):
    return kor_emoji_diffusion_runner.txt2img.run(input_data)


@svc.api(input=JSON(), output=Image(), route="/submit/eng")
def eng2img(input_data):
    return eng_emoji_diffusion_runner.txt2img.run(input_data)
