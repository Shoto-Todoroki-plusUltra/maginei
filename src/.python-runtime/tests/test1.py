from PIL import Image
import math

def rgb_to_ansi_256(r, g, b):
    if r == g == b:
        if r < 8:
            return 16
        if r > 248:
            return 231
        return round(((r - 8) / 247) * 24) + 232
    return 16 + (36 * round(r / 255 * 5)) + (6 * round(g / 255 * 5)) + round(b / 255 * 5)

def print_image(image_path, width=1000):
    image = Image.open(image_path).convert('RGB')
    
    aspect_ratio = image.height / image.width
    height = math.ceil(width * aspect_ratio * 0.8) 
    
    if height % 2 != 0:
        height += 1
    
    image = image.resize((width, height))
    
    for y in range(0, height, 2):
        for x in range(width):
            upper_pixel = image.getpixel((x, y))
            lower_pixel = image.getpixel((x, y + 1)) if y + 1 < height else (0, 0, 0)
            
            upper_color = rgb_to_ansi_256(*upper_pixel)
            lower_color = rgb_to_ansi_256(*lower_pixel)
            
            print(f"\033[38;5;{upper_color}m\033[48;5;{lower_color}m▀\033[0m", end='')
        print()

# Example usage
print_image('assets/image.png')
