from PIL import Image
import numpy as np

def rgb_to_ansi(r, g, b):
    return 16 + 36 * round(r / 255 * 5) + 6 * round(g / 255 * 5) + round(b / 255 * 5)

def nearest_ansi_color(rgb):
    return min(range(256), key=lambda i: sum((a-b)**2 for a, b in zip(rgb, ansi_to_rgb(i))))

def ansi_to_rgb(ansi):
    if ansi < 16:
        return [(0,0,0),(128,0,0),(0,128,0),(128,128,0),(0,0,128),(128,0,128),(0,128,128),(192,192,192),
                (128,128,128),(255,0,0),(0,255,0),(255,255,0),(0,0,255),(255,0,255),(0,255,255),(255,255,255)][ansi]
    elif ansi < 232:
        ansi -= 16
        return ((ansi // 36) * 51, ((ansi % 36) // 6) * 51, (ansi % 6) * 51)
    else:
        gray = (ansi - 232) * 10 + 8
        return (gray, gray, gray)

def dither(image):
    img = np.array(image, dtype=float)
    h, w = img.shape[:2]
    for y in range(h):
        for x in range(w):
            old = img[y, x].copy()
            new = [nearest_ansi_color(old)]
            img[y, x] = new
            err = old - ansi_to_rgb(new[0])
            if x + 1 < w:
                img[y, x + 1] += err * 7/16
            if y + 1 < h:
                if x > 0:
                    img[y + 1, x - 1] += err * 3/16
                img[y + 1, x] += err * 5/16
                if x + 1 < w:
                    img[y + 1, x + 1] += err * 1/16
    return img.astype(np.uint8)

def print_image(image_path, width=120):
    image = Image.open(image_path).convert('RGB')
    image = image.resize((width, int((image.height / image.width) * width / 2)))
    image = Image.fromarray(dither(np.array(image)))
    
    for y in range(0, image.height - 1, 2):
        for x in range(image.width):
            upper_color = rgb_to_ansi(*image.getpixel((x, y)))
            lower_color = rgb_to_ansi(*image.getpixel((x, y + 1)))
            print(f"\033[38;5;{upper_color}m\033[48;5;{lower_color}m▀\033[0m", end='')
        print()

# Example usage
print_image('assets/image.png')
