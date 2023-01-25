from PIL import Image
import os
from tqdm import tqdm

path = 'datasets/noto_sans'
files = [file_name for file_name in os.listdir(path) if file_name.endswith('.png')]

for file_name in tqdm(files, unit="file"):
    # Open the image
    img = Image.open(os.path.join(path, file_name)).convert("RGBA")
        
    # Create a new image with a white background
    img_bg = Image.new('RGBA', img.size, "WHITE")
        
    # Paste the original image on top of the new image
    img_bg.paste(img, mask=img)

    # Save the new image with the same file name
    img_bg.convert("RGB").save(os.path.join(path, file_name), "PNG")