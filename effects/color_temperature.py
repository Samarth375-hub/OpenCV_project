import cv2
import numpy as np

def apply_color_temperature(image, warmth=0):
    """Adjusts the color temperature of an image.
       warmth > 0 → Warmer (adds red/yellow)
       warmth < 0 → Cooler (adds blue)"""
    
    # Split into BGR channels
    b, g, r = cv2.split(image.astype(np.float32))

    if warmth > 0:  # Warm effect (increase red, decrease blue slightly)
        r += warmth * 50
        b -= warmth * 25
    elif warmth < 0:  # Cool effect (increase blue, decrease red slightly)
        b += abs(warmth) * 50
        r -= abs(warmth) * 25

    # Clip values to valid range
    b = np.clip(b, 0, 255)
    g = np.clip(g, 0, 255)
    r = np.clip(r, 0, 255)

    # Merge back and convert to 8-bit
    adjusted_image = cv2.merge([b, g, r]).astype(np.uint8)
    return adjusted_image
