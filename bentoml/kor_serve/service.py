import torch
from torch import autocast
from diffusers import StableDiffusionPipeline, DEISMultistepScheduler

# from diffusers import StableDiffusionImg2ImgPipeline

import bentoml
from PIL import Image
from bentoml.io import Image, JSON
from pydantic import BaseModel
from fastapi import FastAPI, Response

import base64
from io import BytesIO
from typing import Optional
from rembg import remove

server_check = 0
fastapi_app = FastAPI()


class UserInput(BaseModel):
    """**유저가 보낸 Response입니다.**

    Args:
        다음과 같은 attribute를 사용할 수 있습니다.
        prompt: str = "a cute bunny rabbit"
        guidance_scale: Optional[float] = 15
        size: Optional[int] = 512
        num_inference_steps: Optional[int] = 30
        num_images_per_prompt: Optional[int] = 1

    """

    prompt: str = "a cute bunny rabbit"
    guidance_scale: Optional[float] = 15
    size: Optional[int] = 512
    num_inference_steps: Optional[int] = 30
    num_images_per_prompt: Optional[int] = 1


class StableDiffusionRunnable(bentoml.Runnable):
    SUPPORTED_RESOURCES = ("nvidia.com/gpu",)
    SUPPORTS_CPU_MULTI_THREADING = True

    def __init__(self):
        pretrained_model_path = "BAAI/AltDiffusion-m9"
        ckpt_path = "models/kor_model"
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
    def txt2img(self, input_data: JSON) -> JSON:
        """**유저 인풋을 입력받아 txt2img_pipe에 inference하는 함수입니다.**

        Args:
            input_data (JSON): 유저의 인풋입니다.

        Returns:
            JSON: base64형태로 인코딩된 이미지정보가 담긴 JSON을 리턴합니다.
        """
        global server_check
        server_check = 1
        prompt = input_data.prompt
        guidance_scale = input_data.guidance_scale
        size = input_data.size
        num_inference_steps = input_data.num_inference_steps
        num_images_per_prompt = input_data.num_images_per_prompt
        with autocast(self.device):
            images = self.txt2img_pipe(
                prompt=prompt,
                guidance_scale=guidance_scale,
                num_inference_steps=num_inference_steps,
                num_images_per_prompt=num_images_per_prompt,
            ).images
        # TODO: 배경제거 기능 추가하기.
        def to_base64(image: Image) -> str:
            """**Image 리스트를 Json형태로 보내기 위해 Base64포맷으로 전환합니다.**

            Args:
                image (Image): Json형태로 전환할 이미지.

            Returns:
                str: Base64형태로 전환된 문자열.
            """
            with BytesIO() as output:
                image.save(output, format="PNG")
                return base64.b64encode(output.getvalue()).decode("utf-8")

        server_check = 0  # <- this is code(서버가 사용가능함으로 전환.)
        #
        return {
            i: to_base64(remove(image.resize((size, size))))
            for i, image in enumerate(images)
        }


# runner를 할당합니다.
kor_emoji_diffusion_runner = bentoml.Runner(
    StableDiffusionRunnable,
    name="kor_stable_diffusion_runner",
)
# make service
svc_kor = bentoml.Service("eng_emoji_diffusion", runners=[kor_emoji_diffusion_runner])
# fastapi와 포트를 연결할 수 있도록 마운트해주는 함수
svc_kor.mount_asgi_app(fastapi_app)

# 영어 텍스트인풋을 제공받는 path
@svc_kor.api(input=JSON(pydantic_model=UserInput), output=JSON(), route="/kor_submit")
def kor2img(input_data: JSON) -> JSON:
    """**클라이언트의 Request(prompt:kor)를 입력받아 생성된 이미지를 JSON형태로 리턴합니다.**\n
    Args:
        input_data (JSON): 사용자의 Request입니다. 다음과 같은 attribute가 존재합니다.
        다음과 같은 attribute를 사용할 수 있습니다.
        prompt: str = "귀여운 새끼 토끼"
        guidance_scale: Optional[float] = 15
        size: Optional[int] = 512
        num_inference_steps: Optional[int] = 30
        num_images_per_prompt: Optional[int] = 1
    \n
    Returns:
        JSON: Base64형태로 포매팅된 이미지를 JSON형태로 리턴합니다.
        attribute는 유저의 이미지 출력 개수 요청에 따라 0~3의 값을 가집니다.
        value는 Base64형태로 포매팅된 문자열입니다.
    """
    return kor_emoji_diffusion_runner.txt2img.run(input_data)


@fastapi_app.get("/health")
async def check() -> Response:
    """**서버가 지금 응답을 받을 수 있는 상태인지 체크하는 함수입니다.**
    \n
    Returns:
        (Response): 현재 서버의 상태입니다.
        서버가 현재 추론중이라면 status_code 503을,
        서버가 사용 가능하다면 200을 리턴합니다.
    """
    return (
        Response(content="inference is available", status_code=200)
        if not server_check
        else Response(status_code=503)
    )
