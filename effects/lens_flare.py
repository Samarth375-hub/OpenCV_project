import cv2
import numpy as np

def apply_lens_flare(image, position=None, intensity=0.5, flare_size=1.0):
    """
    Applies a realistic lens flare effect with multiple flare elements.
    
    Parameters:
    - position: (x, y) coordinates for the main flare. If None, auto-positioned.
    - intensity: Strength of the flare effect (0.0 to 1.0)
    - flare_size: Size multiplier for the flare elements
    """
    height, width = image.shape[:2]
    
    # If no position is given, set it in the upper right quadrant
    if position is None:
        position = (int(width * 0.7), int(height * 0.3))
    
    # Create a copy of the image to work with
    result = image.copy().astype(np.float32) / 255.0
    
    # Load a flare image with transparency
    try:
        flare = cv2.imread("effects/flare.png", cv2.IMREAD_UNCHANGED)
        if flare is None:
            raise FileNotFoundError
    except:
        print("Warning: Missing 'effects/flare.png' for lens flare effect. Creating a synthetic flare.")
        # Create a synthetic flare if the image is missing
        flare_size_px = int(min(width, height) * 0.3)
        flare = np.zeros((flare_size_px, flare_size_px, 4), dtype=np.uint8)
        center = (flare_size_px // 2, flare_size_px // 2)
        radius = flare_size_px // 2
        
        # Create a radial gradient for the flare
        for y in range(flare_size_px):
            for x in range(flare_size_px):
                distance = np.sqrt((x - center[0])**2 + (y - center[1])**2)
                alpha = max(0, 255 * (1 - distance / radius))
                flare[y, x] = [255, 255, 255, alpha]
    
    # Calculate the center of the image (for positioning secondary flares)
    center_x, center_y = width // 2, height // 2
    
    # Main flare at the specified position
    add_flare_element(result, flare, position, flare_size * 1.0, intensity)
    
    # Create a line from the center to the flare position
    dx = position[0] - center_x
    dy = position[1] - center_y
    
    # Add secondary flares along the line from center to main flare
    # These create the "anamorphic" lens flare look
    for i in range(1, 6):
        # Position secondary flares along the line from center to main flare
        # and also on the opposite side of the center
        pos_factor = np.random.uniform(-0.8, 1.5)  # Randomize positions
        sec_x = int(center_x + dx * pos_factor)
        sec_y = int(center_y + dy * pos_factor)
        
        # Skip if outside the image
        if not (0 <= sec_x < width and 0 <= sec_y < height):
            continue
            
        # Randomize size and intensity for secondary flares
        sec_size = flare_size * np.random.uniform(0.2, 0.6)
        sec_intensity = intensity * np.random.uniform(0.3, 0.7)
        
        # Add the secondary flare
        add_flare_element(result, flare, (sec_x, sec_y), sec_size, sec_intensity)
    
    # Add a horizontal streak (anamorphic lens effect)
    streak = create_anamorphic_streak(width, height, position, intensity * 0.7)
    result = screen_blend(result, streak)
    
    # Add a subtle halo around the main light source
    halo = create_halo(width, height, position, min(width, height) * 0.4 * flare_size, intensity * 0.5)
    result = screen_blend(result, halo)
    
    # Convert back to 8-bit image
    return (np.clip(result, 0, 1) * 255).astype(np.uint8)

def add_flare_element(image, flare_template, position, size=1.0, intensity=1.0):
    """Add a flare element to the image at the specified position."""
    h, w = image.shape[:2]
    flare_h, flare_w = flare_template.shape[:2]
    
    # Calculate new size
    new_size = (int(flare_w * size), int(flare_h * size))
    if new_size[0] == 0 or new_size[1] == 0:
        return
        
    # Resize flare
    flare_resized = cv2.resize(flare_template, new_size)
    
    # Calculate position to center the flare at the specified position
    x1 = max(0, position[0] - new_size[0] // 2)
    y1 = max(0, position[1] - new_size[1] // 2)
    x2 = min(w, x1 + new_size[0])
    y2 = min(h, y1 + new_size[1])
    
    # Adjust flare crop region if needed
    flare_x1 = 0 if x1 >= 0 else -x1
    flare_y1 = 0 if y1 >= 0 else -y1
    flare_x2 = new_size[0] if x2 <= w else new_size[0] - (x2 - w)
    flare_y2 = new_size[1] if y2 <= h else new_size[1] - (y2 - h)
    
    # Check if the crop region is valid
    if flare_x1 >= flare_x2 or flare_y1 >= flare_y2 or x1 >= x2 or y1 >= y2:
        return
    
    # Get the region of the image where the flare will be placed
    roi = image[y1:y2, x1:x2]
    
    # Get the corresponding region of the flare
    flare_roi = flare_resized[flare_y1:flare_y2, flare_x1:flare_x2]
    
    # Check if shapes match
    if roi.shape[:2] != flare_roi.shape[:2]:
        return
    
    # Extract alpha channel and normalize
    if flare_roi.shape[2] == 4:  # With alpha channel
        alpha = flare_roi[:, :, 3] / 255.0 * intensity
        flare_rgb = flare_roi[:, :, :3] / 255.0
    else:  # Without alpha channel
        alpha = np.ones(flare_roi.shape[:2]) * intensity
        flare_rgb = flare_roi / 255.0
    
    # Apply screen blending mode for the flare
    for c in range(3):
        roi[:, :, c] = roi[:, :, c] * (1 - alpha) + (1 - (1 - roi[:, :, c]) * (1 - flare_rgb[:, :, c])) * alpha

def create_anamorphic_streak(width, height, position, intensity=0.5):
    """Create a horizontal streak effect (anamorphic lens flare)."""
    streak = np.zeros((height, width, 3), dtype=np.float32)
    
    # Create a horizontal line with Gaussian falloff in vertical direction
    y_center = position[1]
    for y in range(height):
        # Gaussian falloff in vertical direction
        y_intensity = np.exp(-((y - y_center) ** 2) / (2 * (height * 0.01) ** 2)) * intensity
        streak[y, :] = [y_intensity, y_intensity, y_intensity]
    
    # Apply horizontal gradient to fade the streak
    x_gradient = np.linspace(0, 1, width)
    x_gradient = 1 - np.abs(2 * x_gradient - 1)  # Create a peak at the light source
    x_gradient = x_gradient.reshape(1, width, 1)
    
    streak = streak * x_gradient * 0.7  # Reduce intensity for subtlety
    
    return streak

def create_halo(width, height, position, radius, intensity=0.5):
    """Create a circular halo effect around the light source."""
    halo = np.zeros((height, width, 3), dtype=np.float32)
    
    # Create a mask for the halo
    y, x = np.ogrid[:height, :width]
    dist_squared = (x - position[0])**2 + (y - position[1])**2
    
    # Create a radial gradient
    mask = np.exp(-dist_squared / (2 * (radius/3)**2))
    
    # Apply the mask to create the halo
    for c in range(3):
        halo[:, :, c] = mask * intensity
    
    return halo

def screen_blend(base, overlay):
    """Apply screen blending mode: 1 - (1-a) * (1-b)"""
    return 1.0 - (1.0 - base) * (1.0 - overlay)
