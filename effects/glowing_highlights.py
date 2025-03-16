import cv2
import numpy as np

def apply_glowing_highlights(image, glow_intensity=0.5):
    """Enhances bright areas in the image to create a glowing effect."""
    
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Threshold to detect bright areas
    _, highlight_mask = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
    
    # Convert mask to 3 channels
    highlight_mask = cv2.cvtColor(highlight_mask, cv2.COLOR_GRAY2BGR)
    
    # Blur the bright areas to create a glow effect
    blurred = cv2.GaussianBlur(image, (15, 15), 10)
    
    # Blend the glowing highlights with the original image
    result = cv2.addWeighted(image, 1, blurred, glow_intensity, 0)
    
    return result
