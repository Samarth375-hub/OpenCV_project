import cv2
import numpy as np

def apply_light_leaks(image, intensity=0.5):
    """Applies a light leaks effect by overlaying a gradient with random bright patches."""
    height, width = image.shape[:2]

    # Create a blank overlay
    overlay = np.zeros((height, width, 3), dtype=np.uint8)

    # Define random bright colors for the leaks
    colors = [
        (255, 100, 50),  # Warm orange-red
        (255, 200, 100),  # Soft yellow
        (100, 150, 255),  # Cool blue
        (255, 50, 200)    # Magenta-pink
    ]

    # Randomly place light leaks
    for _ in range(4):  
        x = np.random.randint(0, width // 2)
        y = np.random.randint(0, height)
        radius = np.random.randint(width // 6, width // 3)
        color = colors[np.random.randint(0, len(colors))]

        cv2.circle(overlay, (x, y), radius, color, -1)  # Draw the leak

    # Blur the overlay to make leaks soft
    overlay = cv2.GaussianBlur(overlay, (151, 151), 0)

    # Blend the overlay with the original image
    result = cv2.addWeighted(image, 1.0, overlay, intensity, 0)

    return result
