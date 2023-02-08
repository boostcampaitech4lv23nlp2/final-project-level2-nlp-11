from diffusers import StableDiffusionPipeline
from PIL import Image
from typing import List , Dict
import torch
import random
import io
import base64

def generation_image(pipe,
                prompt : str,
                guidance_scale : int,
                num_inference : int,
                inference_step : int,
                resize : int 
                ) -> List :

    output_image = []
    for i in range(num_inference):
        generator = torch.Generator("cuda").manual_seed(random.randint(0,1024))
        image = pipe(prompt=prompt, guidance_scale=guidance_scale, num_inference_steps= inference_step, generator=generator).images[0]
        image = image.resize((resize,resize))
        output_image.append(image)
    return output_image

def image_to_byte(image_list : List ) -> List :
    
    decode_image_list = []
    for idx , image in enumerate(image_list):
        imgByteArr = io.BytesIO()
        image.save(imgByteArr, format = 'png')
        imgByteArr = imgByteArr.getvalue()
        encoded_img = base64.b64encode(imgByteArr)
        decoded_img = encoded_img.decode('ascii')
        decode_image_list.append(decoded_img)
    
    return decode_image_list
