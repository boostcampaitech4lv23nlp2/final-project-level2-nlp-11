import re
import os
from unicodedata import name

path = "datasets/noto_sans"


def get_emoji_name(file_name):
    # Extract the Unicode code point(s) from the file name
    match = re.search(r'emoji_u([\da-f_]+)\.png', file_name, re.IGNORECASE)
    if match:
        code_points = match.group(1).split("_")
        # Convert the code point(s) to a Unicode character(s)
        emoji = "".join([chr(int(code, 16)) for code in code_points])
        # Look up the character name in the Unicode data
        emoji_name = " ".join([name(ch, None) or f"U+{ord(ch):X}" for ch in emoji])
        if emoji_name:
            return emoji_name.lower().capitalize()
    return None

for file_name in os.listdir(path):
    emoji_name = get_emoji_name(file_name)
    if emoji_name:
        os.rename(os.path.join(path, file_name), os.path.join(path, emoji_name +'.png'))