import cv2
import numpy as np

def apply_dramatic_shadows(image, shadow_intensity=1.5):
    """Enhances shadows for a dramatic effect."""
    
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply adaptive thresholding to detect shadows
    shadow_mask = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                        cv2.THRESH_BINARY_INV, 21, 10)
    
    # Convert mask to 3 channels (same as original image)
    shadow_mask = cv2.cvtColor(shadow_mask, cv2.COLOR_GRAY2BGR)
    
    # Darken shadows by blending with the original
    result = cv2.addWeighted(image, 1, shadow_mask, -shadow_intensity, 0)
    
    return result
