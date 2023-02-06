import torch

from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse

from uuid import UUID, uuid4
from pydantic import BaseModel, Field

from typing import List, Union , Dict, Any, Optional
from fastapi.param_functions import Depends
from app.utils import generation_image, image_to_byte
from datetime import datetime
from diffusers import StableDiffusionPipeline

app = FastAPI()
pretrained_model = 'runwayml/stable-diffusion-v1-5'
model_path = "models/emoji-model-lora"

pipe = StableDiffusionPipeline.from_pretrained(pretrained_model, torch_dtype=torch.float16)
pipe.unet.load_attn_procs(model_path)

pipe.to("cuda")

@app.get("/")
def hello_world() :
    return {"hello" : "world"}

#json data 
#inference_data 
#prompt , cfg , num_inference, inference_step
class Product(BaseModel) :
    id : UUID = Field(default_factory= uuid4)
    prompt : str
    guidance_scale : float
    num_inference : int
    inference_step : int
    resize : int

class Order(BaseModel) :
    id : UUID = Field(default_factory=uuid4)
    products : Product = Field(default_factory=Product)
    # 최초에 빈 list를 만들어서 저장한다
    created_at : datetime = Field(default_factory=datetime.now)
    updated_at : datetime = Field(default_factory=datetime.now)

class InferenceImageProduct(Product) :
    image_list : list

@app.post("/submit")
async def make_image(data: Product = Body(...)) :
    # Depends : 의존성 주입
    # 반복적이고 공통적인 로직이 중요할 때 사용 할 수 있음
    # 모델을 Load, Config Load
    # async , Depends 검색해서 또 학습해보기!
    prompt = data.dict()['prompt']
    guidance_scale = data.dict()['guidance_scale']
    num_inference = data.dict()['num_inference']
    inference_step = data.dict()['inference_step']
    resize = data.dict()['resize']

    # TODO: pipe load와 inference를 분리해서 함수로 만들기
    image_list = generation_image(
        pipe= pipe,
        prompt=prompt,
        guidance_scale = guidance_scale,
        num_inference = num_inference,
        inference_step = inference_step,
        resize= resize,
        )

    decode_image_list = image_to_byte(image_list)
    image_proudct = InferenceImageProduct(
        prompt=prompt,
        guidance_scale = guidance_scale,
        num_inference = num_inference,
        inference_step = inference_step,
        image_list = decode_image_list,
        resize=resize
        )

    new_order = Order(products = image_proudct)
    return new_order

