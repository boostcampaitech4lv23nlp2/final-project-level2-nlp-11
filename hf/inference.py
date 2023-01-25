from diffusers import StableDiffusionPipeline
import torch
from PIL import Image

# TODO: Integrate all inference files in one.
# TODO: Implement parseargument, config etc
model_path = "models/emoji-model"
test_model_path = "Norod78/sd15-fluentui-emoji"
pipe = StableDiffusionPipeline.from_pretrained(test_model_path, torch_dtype=torch.float16)
pipe.to("cuda")
prompt = "Miner with Head Lantern"
outputs = pipe(prompt=prompt, guidance_scale=5, num_images_per_prompt=4)
# outputs.images[0].save(f"outputs/{prompt[:10]}4.png")

def image_grid(imgs, rows, cols):
    assert len(imgs) == rows*cols

    w, h = imgs[0].size
    grid = Image.new('RGB', size=(cols*w, rows*h))
    grid_w, grid_h = grid.size
    
    for i, img in enumerate(imgs):
        grid.paste(img, box=(i%cols*w, i//cols*h))
    return grid

grid = image_grid(outputs.images, rows=2,cols=2)
# TODO: 파일 저장 형식 좀 더 robust하게. 
grid.save(f"outputs/grids/grid-{prompt[:14] if len(prompt)>15 else prompt}.png")