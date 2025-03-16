import cv2
import numpy as np

def apply_vignette_effect(image, intensity=1.5):
    """Applies a vignette effect by darkening the edges while keeping the center bright."""
    height, width = image.shape[:2]

    # Create Gaussian kernel for X and Y
    X = cv2.getGaussianKernel(width, width / intensity)
    Y = cv2.getGaussianKernel(height, height / intensity)
    
    # Outer product to create 2D mask
    mask = Y @ X.T

    # Normalize to range [0,1]
    mask = mask / np.max(mask)

    # Convert mask to 3-channel for color images
    mask = cv2.merge([mask, mask, mask])

    # Convert image to float and apply vignette
    image = image.astype(np.float32) / 255.0
    vignette_image = image * mask

    # Convert back to 8-bit image
    vignette_image = (vignette_image * 255).astype(np.uint8)
    
    return vignette_image
