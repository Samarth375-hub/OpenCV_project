import cv2
import numpy as np

def apply_spotlight_effect(image, center, radius, brightness=1.5, ambient_light=0.2):
    """
    Apply a spotlight effect to an image.
    
    Args:
        image: The input image.
        center: The (x, y) coordinates of the spotlight center.
        radius: The radius of the spotlight.
        brightness: The brightness of the spotlight (default: 1.5).
        ambient_light: The ambient light level outside the spotlight (default: 0.2).
        
    Returns:
        The image with the spotlight effect applied.
    """
    # Create a copy of the image to avoid modifying the original
    result = image.copy()
    
    # Get image dimensions
    height, width = image.shape[:2]
    
    # Create a mask for the spotlight effect using vectorized operations
    # This is faster than using np.ogrid or np.meshgrid
    y, x = np.indices((height, width))
    
    # Calculate squared distance from center (avoid sqrt for performance)
    dist_squared = (x - center[0])**2 + (y - center[1])**2
    
    # Create the main spotlight mask (1.0 inside spotlight, ambient_light outside)
    # Using squared distance comparison for performance
    radius_squared = radius**2
    
    # Create a smooth falloff from center to edge of spotlight
    # Use a faster calculation method with fewer operations
    mask = np.ones_like(dist_squared, dtype=np.float32)
    
    # Calculate the falloff region (between 0.7*radius and radius)
    inner_radius_squared = (0.7 * radius)**2
    
    # Apply different values to different regions
    # 1. Center region (full brightness)
    # 2. Falloff region (gradual transition)
    # 3. Outside region (ambient light)
    
    # Create the mask in one step using numpy's where function
    falloff_region = np.logical_and(dist_squared > inner_radius_squared, dist_squared <= radius_squared)
    outside_region = dist_squared > radius_squared
    
    # Calculate falloff values only where needed
    falloff_values = np.zeros_like(dist_squared, dtype=np.float32)
    if np.any(falloff_region):
        # Normalize distances in falloff region for smooth transition
        normalized_dist = (np.sqrt(dist_squared[falloff_region]) - 0.7 * radius) / (0.3 * radius)
        # Apply smooth falloff using a simple linear function
        falloff_values[falloff_region] = 1.0 - normalized_dist
    
    # Apply the mask values
    mask[falloff_region] = falloff_values[falloff_region]
    mask[outside_region] = ambient_light
    
    # Apply brightness to the spotlight area
    # Vectorized operation for all channels at once
    if image.ndim == 3:  # Color image
        # Reshape mask to apply to all channels
        mask = np.expand_dims(mask, axis=2)
        
        # Apply brightness only to the spotlight area (where mask > ambient_light)
        spotlight_area = mask > ambient_light
        if np.any(spotlight_area):
            # Apply brightness boost only to spotlight area
            result = result.astype(np.float32)
            result[spotlight_area.repeat(3, axis=2)] = np.clip(
                image[spotlight_area.repeat(3, axis=2)].astype(np.float32) * brightness, 
                0, 255
            )
            
        # Apply the mask to the entire image
        result = (result.astype(np.float32) * mask).astype(np.uint8)
    else:  # Grayscale image
        result = (image.astype(np.float32) * mask).astype(np.uint8)
    
    return result
