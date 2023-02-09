#pip install rembg
from rembg import remove
from PIL import Image

input_path = 'outputs/Cute rabbi3.png'
output_path = 'outputs/remove_bg.png'

input = Image.open(input_path)
output = remove(input)
output.save(output_path)