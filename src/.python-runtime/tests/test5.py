from PIL import Image
import math, os

def rgb_to_ansi(r, g, b, background=False):
    return f"\033[{48 if background else 38};2;{r};{g};{b}m"

def print_image(image_path, width=1000):  # Width is number of characters, not pixels
    image = Image.open(image_path).convert('RGB')
    
    # Calculate height while maintaining aspect ratio
    aspect_ratio = image.height / image.width
    height = math.ceil(width * aspect_ratio * 0.5)  # 0.5 because we're using 2 rows per character
    
    # Ensure height is even
    if height % 2 != 0:
        height += 1
    
    # Actual pixel dimensions (2x2 pixels per character)
    pixel_width = width * 2
    pixel_height = height * 2
    
    image = image.resize((pixel_width, pixel_height), Image.LANCZOS)
    
    # Check if the terminal supports true color
    true_color = os.getenv('COLORTERM') in ('truecolor', '24bit')
    
    for y in range(0, pixel_height, 2):
        for x in range(0, pixel_width, 2):
            pixels = [
                image.getpixel((x, y)),
                image.getpixel((x + 1, y)),
                image.getpixel((x, y + 1)),
                image.getpixel((x + 1, y + 1))
            ]
            
            if true_color:
                colors = [rgb_to_ansi(*p) for p in pixels]
            else:
                colors = [f"\033[38;5;{rgb_to_ansi_256(*p)}m" for p in pixels]
            
            top_left, top_right, bottom_left, bottom_right = colors
            
            if pixels[0] == pixels[1] == pixels[2] == pixels[3]:
                print(f"{rgb_to_ansi(*pixels[0], True)} \033[0m", end='')
            elif pixels[0] == pixels[2] and pixels[1] == pixels[3]:
                print(f"{top_right}{rgb_to_ansi(*pixels[0], True)}▌\033[0m", end='')
            elif pixels[0] == pixels[1] and pixels[2] == pixels[3]:
                print(f"{bottom_left}{rgb_to_ansi(*pixels[0], True)}▀\033[0m", end='')
            else:
                print(f"{bottom_right}{rgb_to_ansi(*pixels[0], True)}▟\033[0m", end='')
        print()

def rgb_to_ansi_256(r, g, b):
    if r == g == b:
        if r < 8:
            return 16
        if r > 248:
            return 231
        return round(((r - 8) / 247) * 24) + 232
    return 16 + (36 * round(r / 255 * 5)) + (6 * round(g / 255 * 5)) + round(b / 255 * 5)

# Example usage
print_image('assets/image.png')
