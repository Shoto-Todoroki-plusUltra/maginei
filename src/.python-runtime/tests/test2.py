from PIL import Image
import math, os, sys

def rgb_to_ansi(r, g, b):
    return f"\033[38;2;{r};{g};{b}m"

def get_color_escape(r, g, b, background=False):
    return '\033[{};2;{};{};{}m'.format(48 if background else 38, r, g, b)

def print_image(image_path, width=250):
    image = Image.open(image_path).convert('RGB')
    
    aspect_ratio = image.height / image.width
    height = math.ceil(width * aspect_ratio * 0.55)

    if height % 2 != 0:
        height += 1
    
    image = image.resize((width, height))
    
    true_color = os.getenv('COLORTERM') in ('truecolor', '24bit')
    
    for y in range(0, height, 2):
        for x in range(width):
            upper_pixel = image.getpixel((x, y))
            lower_pixel = image.getpixel((x, y + 1)) if y + 1 < height else (0, 0, 0)
            
            if true_color:
                upper_color = get_color_escape(*upper_pixel)
                lower_color = get_color_escape(*lower_pixel, background=True)
            else:
                upper_color = rgb_to_ansi_256(*upper_pixel)
                lower_color = f"\033[48;5;{rgb_to_ansi_256(*lower_pixel)}m"
            
            print(f"{upper_color}{lower_color}▀\033[0m", end='')
        print()

def rgb_to_ansi_256(r, g, b):
    if r == g == b:
        if r < 8:
            return 16
        if r > 248:
            return 231
        return round(((r - 8) / 247) * 24) + 232
    return 16 + (36 * round(r / 255 * 5)) + (6 * round(g / 255 * 5)) + round(b / 255 * 5)

print_image('assets/image.png')
