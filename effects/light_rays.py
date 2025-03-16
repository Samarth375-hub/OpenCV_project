import cv2
import numpy as np

def apply_light_rays_effect(image, intensity=0.5, angle=45, num_rays=20, ray_width=2, ray_length=0.8):
    """
    Applies a light rays (God Rays) effect with customizable parameters.
    
    Parameters:
    - intensity: Strength of the light rays effect (0.0 to 1.0)
    - angle: Direction of light rays in degrees (0-360)
    - num_rays: Number of light rays to generate
    - ray_width: Width/thickness of each ray
    - ray_length: Length of rays as a proportion of image diagonal (0.0 to 1.0)
    """
    height, width = image.shape[:2]
    diagonal = np.sqrt(height**2 + width**2)
    
    # Convert angle to radians
    angle_rad = np.radians(angle)
    
    # Calculate the light source position based on angle
    # Light source will be positioned outside the image
    distance = diagonal * 0.5
    center_x = width // 2
    center_y = height // 2
    
    # Calculate light source position (outside the image)
    source_x = int(center_x - np.cos(angle_rad) * distance)
    source_y = int(center_y - np.sin(angle_rad) * distance)
    
    # Create an empty mask for light rays
    light_rays = np.zeros((height, width), dtype=np.float32)
    
    # Generate multiple light rays
    for i in range(num_rays):
        # Randomize ray angle slightly for natural look
        ray_angle = angle_rad + np.radians(np.random.uniform(-15, 15))
        
        # Calculate ray end point
        ray_length_px = diagonal * ray_length
        end_x = int(source_x + np.cos(ray_angle) * ray_length_px)
        end_y = int(source_y + np.sin(ray_angle) * ray_length_px)
        
        # Draw the ray
        cv2.line(light_rays, (source_x, source_y), (end_x, end_y), 
                 np.random.uniform(0.7, 1.0), thickness=ray_width)
    
    # Apply Gaussian blur to soften the rays
    light_rays = cv2.GaussianBlur(light_rays, (0, 0), diagonal * 0.01)
    
    # Apply additional blur for glow effect
    glow = cv2.GaussianBlur(light_rays, (0, 0), diagonal * 0.03)
    light_rays = cv2.addWeighted(light_rays, 0.6, glow, 0.4, 0)
    
    # Convert to 3-channel image
    light_rays = cv2.merge([light_rays] * 3)
    
    # Apply screen blending mode for more realistic light
    image_float = image.astype(np.float32) / 255.0
    light_rays = light_rays * intensity
    
    # Screen blend mode: 1 - (1-a) * (1-b)
    blended = 1.0 - (1.0 - image_float) * (1.0 - light_rays)
    blended = np.clip(blended, 0.0, 1.0)
    
    # Convert back to 8-bit image
    result = (blended * 255).astype(np.uint8)
    return result
