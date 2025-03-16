import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io
import time
import os
from datetime import datetime

# Import effects
from effects.spotlight import apply_spotlight_effect
from effects.vignette import apply_vignette_effect
from effects.light_rays import apply_light_rays_effect
from effects.color_temperature import apply_color_temperature
from effects.dramatic_shadows import apply_dramatic_shadows
from effects.glowing_highlights import apply_glowing_highlights
from effects.light_leaks import apply_light_leaks
from effects.lens_flare import apply_lens_flare

# Streamlit UI setup
st.set_page_config(page_title="Lighting Effects Editor", layout="wide")
st.title("💡 Professional Lighting Effects Editor")

# Sidebar
st.sidebar.header("🔧 Adjust Effect Parameters")
st.sidebar.write("Upload an image and choose an effect to apply.")

# Image upload
uploaded_file = st.sidebar.file_uploader("📂 Upload an image", type=["jpg", "jpeg", "png", "webp"])
if uploaded_file:
    image = Image.open(uploaded_file)
    image = np.array(image)  # Convert to OpenCV format

    # List all available effects in a single dropdown
    all_effects = ["Spotlight", "Vignette", "Light Rays", "Light Leaks", "Flare", 
                  "Color Temperature", "Dramatic Shadows", "Glowing Highlights"]
    
    # Create a selectbox for effects
    effect_option = st.sidebar.selectbox("🎛 Choose Effect:", all_effects)

    # Initialize session state variables **only if not set**
    if "brightness" not in st.session_state:
        st.session_state["brightness"] = 1.5
    # Always ensure radius is at least 600
    st.session_state["radius"] = max(600, st.session_state.get("radius", 600))
    if "shadow_intensity" not in st.session_state:
        st.session_state["shadow_intensity"] = 1.5
    if "ambient_light" not in st.session_state:
        st.session_state["ambient_light"] = 0.2
    if "images_saved" not in st.session_state:
        st.session_state["images_saved"] = False
        st.session_state["save_message"] = ""

    # Sidebar effect parameters (No direct session state modification)
    if effect_option == "Spotlight":
        max_radius = min(image.shape[0], image.shape[1]) // 2
        
        # Set a fixed default radius of 600 pixels
        default_radius = 600
        
        # Ensure the session state radius is at least 600
        if st.session_state["radius"] < 600:
            st.session_state["radius"] = 600

        brightness = st.sidebar.slider("🔆 Brightness", 0.5, 3.0, st.session_state["brightness"])
        radius = st.sidebar.slider("⭕ Spotlight Radius", 600, max_radius, st.session_state["radius"])

        center_x = st.sidebar.slider("🎯 Spotlight X", 0, image.shape[1], image.shape[1] // 2)
        center_y = st.sidebar.slider("🎯 Spotlight Y", 0, image.shape[0], image.shape[0] // 2)

        # Add ambient light control
        ambient_light = st.sidebar.slider("🌑 Ambient Light", 0.0, 0.5, st.session_state["ambient_light"], 0.05)
        
        # Show a loading indicator while processing
        with st.spinner("Applying spotlight effect..."):
            # Pass the ambient light parameter to the spotlight effect
            output = apply_spotlight_effect(image, (center_x, center_y), radius, brightness, ambient_light)

        # Update session state to keep user adjustments
        st.session_state["brightness"] = brightness
        st.session_state["radius"] = radius
        st.session_state["ambient_light"] = ambient_light
    elif effect_option == "Vignette":
        intensity = st.sidebar.slider("🌗 Intensity", 0.5, 3.0, 1.5)
        output = apply_vignette_effect(image, intensity)

    elif effect_option == "Light Rays":
        intensity = st.sidebar.slider("☀️ Light Rays Intensity", 0.1, 2.0, 1.0)
        angle = st.sidebar.slider("🌅 Light Rays Angle", 0, 360, 45)
        num_rays = st.sidebar.slider("🔢 Number of Rays", 5, 50, 20)
        ray_width = st.sidebar.slider("📏 Ray Width", 1, 10, 2)
        ray_length = st.sidebar.slider("📏 Ray Length", 0.1, 1.0, 0.8)
        output = apply_light_rays_effect(image, intensity, angle, num_rays, ray_width, ray_length)

    elif effect_option == "Color Temperature":
        warmth = st.sidebar.slider("🌡 Warmth (-100 to 100)", -100, 100, 0)
        output = apply_color_temperature(image, warmth/100)

    elif effect_option == "Dramatic Shadows":
        intensity = st.sidebar.slider("🌑 Shadow Intensity", 0.5, 3.0, st.session_state["shadow_intensity"])
        output = apply_dramatic_shadows(image, intensity)
        st.session_state["shadow_intensity"] = intensity

    elif effect_option == "Glowing Highlights":
        intensity = st.sidebar.slider("✨ Highlight Intensity", 0.5, 3.0, 1.5)
        output = apply_glowing_highlights(image, intensity)
        
    elif effect_option == "Light Leaks":
        intensity = st.sidebar.slider("🌈 Light Leak Intensity", 0.1, 1.0, 0.5)
        output = apply_light_leaks(image, intensity)
        
    elif effect_option == "Flare":
        intensity = st.sidebar.slider("💫 Flare Intensity", 0.1, 1.0, 0.5)
        flare_size = st.sidebar.slider("📐 Flare Size", 0.5, 2.0, 1.0)
        
        # Initialize flare position in session state if not already set
        if "flare_position" not in st.session_state:
            st.session_state["flare_position"] = (image.shape[1] // 2, image.shape[0] // 2)  # Default center
        
        # Display instructions
        st.write("👆 Click on the image to position the flare")
        
        # Display the image for clicking
        col1, col2 = st.columns([3, 1])
        with col1:
            # Convert image to PIL for display
            preview_img = Image.fromarray(image)
            
            # Create a placeholder for the image
            img_placeholder = st.empty()
            img_placeholder.image(preview_img, width=None)
            
            # Get the dimensions of the displayed image container
            # This is a workaround since Streamlit doesn't provide exact dimensions
            container_width = st.container().width
            
            # Handle click event
            if st.button("Reset Flare Position"):
                st.session_state["flare_position"] = (image.shape[1] // 2, image.shape[0] // 2)
                st.rerun()
        
        # Create columns for manual position adjustment
        col_x, col_y = st.columns(2)
        with col_x:
            # Add a slider for X position
            new_x = st.slider("Flare X Position", 0, image.shape[1], st.session_state["flare_position"][0])
            if new_x != st.session_state["flare_position"][0]:
                st.session_state["flare_position"] = (new_x, st.session_state["flare_position"][1])
        
        with col_y:
            # Add a slider for Y position
            new_y = st.slider("Flare Y Position", 0, image.shape[0], st.session_state["flare_position"][1])
            if new_y != st.session_state["flare_position"][1]:
                st.session_state["flare_position"] = (st.session_state["flare_position"][0], new_y)
        
        # Apply the lens flare effect with the current position
        output = apply_lens_flare(image, st.session_state["flare_position"], intensity, flare_size)
        
        # Show the current flare position
        st.write(f"Current flare position: X={st.session_state['flare_position'][0]}, Y={st.session_state['flare_position'][1]}")

    # Display the original and processed images side by side
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Original Image")
        st.image(image, width=None)
    with col2:
        st.subheader(f"With {effect_option} Effect")
        st.image(output, width=None)
        
    # Add download button for the processed image
    # Create a unique filename based on effect and timestamp
    timestamp = int(time.time())
    effect_name = effect_option.lower().replace(' ', '_')
    filename_base = f"{effect_name}_{timestamp}"
    
    # Create the results directory if it doesn't exist
    os.makedirs("results", exist_ok=True)
    
    # Function to save both images when download button is clicked
    def save_images():
        # Create a side-by-side comparison image
        # Get dimensions
        h, w = image.shape[:2]
        
        # Define font at the beginning of the function
        font = cv2.FONT_HERSHEY_SIMPLEX
        
        # Create a new canvas with both images side by side
        # If images have an alpha channel (RGBA), convert to RGB for JPG compatibility
        if image.shape[2] == 4:
            img_left = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)
        else:
            img_left = image.copy()
            
        if output.shape[2] == 4:
            img_right = cv2.cvtColor(output, cv2.COLOR_RGBA2RGB)
        else:
            img_right = output.copy()
        
        # Create the combined image
        combined_img = np.zeros((h, w*2, 3), dtype=np.uint8)
        combined_img[:, :w] = img_left
        combined_img[:, w:] = img_right
        
        # Add a vertical dividing line between the images
        combined_img[:, w-1:w+1] = [255, 255, 255]  # White line
        
        # Add date and time stamp at the top right corner
        timestamp_str = datetime.now().strftime("%Y-%m-%d %H:%M")
        timestamp_font_size = 0.7
        timestamp_text_size = cv2.getTextSize(timestamp_str, font, timestamp_font_size, 1)[0]
        timestamp_x = w*2 - timestamp_text_size[0] - 10
        cv2.rectangle(combined_img, (timestamp_x-5, 10), (timestamp_x + timestamp_text_size[0] + 5, 10 + timestamp_text_size[1] + 5), (0, 0, 0), -1)
        cv2.putText(combined_img, timestamp_str, (timestamp_x, 30), font, timestamp_font_size, (255, 255, 255), 1, cv2.LINE_AA)
        
        # Add labels to the images
        # Increase font size for main labels (Original and Effect)
        title_font_size = 1.5
        title_thickness = 3
        # Add background for the title text
        for title, x_pos in [("Original", 10), (f"{effect_option} Effect", w+10)]:
            text_size = cv2.getTextSize(title, font, title_font_size, title_thickness)[0]
            cv2.rectangle(combined_img, (x_pos-5, 10), (x_pos + text_size[0] + 5, 10 + text_size[1] + 10), (0, 0, 0), -1)
        
        # Draw the title text
        cv2.putText(combined_img, "Original", (10, 50), font, title_font_size, (255, 255, 255), title_thickness, cv2.LINE_AA)
        cv2.putText(combined_img, f"{effect_option} Effect", (w+10, 50), font, title_font_size, (255, 255, 255), title_thickness, cv2.LINE_AA)
        
        # Add effect parameters at the bottom of the image
        if effect_option == "Spotlight":
            param_text = f"Brightness: {brightness:.1f}   Radius: {radius}   Ambient: {ambient_light:.2f}"
        elif effect_option == "Vignette":
            param_text = f"Intensity: {intensity:.1f}"
        elif effect_option == "Light Rays":
            param_text = f"Intensity: {intensity:.1f}   Angle: {angle}°   Rays: {num_rays}"
            param_text2 = f"Ray Width: {ray_width}   Ray Length: {ray_length:.1f}"
        elif effect_option == "Color Temperature":
            param_text = f"Warmth: {warmth}"
        elif effect_option == "Dramatic Shadows":
            param_text = f"Shadow Intensity: {intensity:.1f}"
        elif effect_option == "Glowing Highlights":
            param_text = f"Highlight Intensity: {intensity:.1f}"
        elif effect_option == "Light Leaks":
            param_text = f"Leak Intensity: {intensity:.1f}"
        elif effect_option == "Flare":
            param_text = f"Intensity: {intensity:.1f}   Size: {flare_size:.1f}"
            param_text2 = f"Position: X={st.session_state['flare_position'][0]}, Y={st.session_state['flare_position'][1]}"
        
        # Increase font size for parameters text
        param_font_size = 1.2
        param_thickness = 2
        
        # Add a solid black background for the parameter text
        # Make it taller if we have two lines of parameters
        if effect_option in ["Light Rays", "Flare"]:
            cv2.rectangle(combined_img, (0, h-100), (w*2, h), (0, 0, 0), -1)
            # Draw the parameter text in two lines
            cv2.putText(combined_img, "Parameters:", (20, h-70), font, param_font_size, (255, 255, 255), param_thickness, cv2.LINE_AA)
            cv2.putText(combined_img, param_text, (20, h-40), font, param_font_size, (255, 255, 255), param_thickness, cv2.LINE_AA)
            cv2.putText(combined_img, param_text2, (20, h-15), font, param_font_size, (255, 255, 255), param_thickness, cv2.LINE_AA)
        else:
            cv2.rectangle(combined_img, (0, h-70), (w*2, h), (0, 0, 0), -1)
            # Draw the parameter text in one line
            cv2.putText(combined_img, "Parameters:", (20, h-40), font, param_font_size, (255, 255, 255), param_thickness, cv2.LINE_AA)
            cv2.putText(combined_img, param_text, (20, h-15), font, param_font_size, (255, 255, 255), param_thickness, cv2.LINE_AA)
        
        # Save the combined image
        combined_path = os.path.join("results", f"comparison_{filename_base}.jpg")
        cv2.imwrite(combined_path, cv2.cvtColor(combined_img, cv2.COLOR_RGB2BGR))
        
        # Set session state to show success message
        st.session_state["images_saved"] = True
        st.session_state["save_message"] = f"✅ Comparison image saved to results directory as comparison_{filename_base}.jpg"
    
    # Add download button with callback
    buf = io.BytesIO()
    Image.fromarray(output).save(buf, format="PNG")
    btn = st.download_button(
        label="💾 Download Processed Image",
        data=buf.getvalue(),
        file_name=f"processed_{filename_base}.png",
        mime="image/png",
        on_click=save_images
    )
    
    # Display success message if images were saved
    if st.session_state["images_saved"]:
        st.success(st.session_state["save_message"])
        
        # Add a button to view the saved comparison image
        if "last_saved_image" not in st.session_state:
            st.session_state["last_saved_image"] = ""
        
        st.session_state["last_saved_image"] = f"comparison_{filename_base}.jpg"
        
        # Create columns for the success message area
        col1, col2 = st.columns([3, 1])
        with col2:
            # Add a button to view the saved image
            if st.button("👁️ View Saved Image"):
                # Read the saved image
                saved_img_path = os.path.join("results", st.session_state["last_saved_image"])
                if os.path.exists(saved_img_path):
                    saved_img = cv2.imread(saved_img_path)
                    saved_img = cv2.cvtColor(saved_img, cv2.COLOR_BGR2RGB)
                    # Display the image in a new section
                    st.subheader("Saved Comparison Image")
                    st.image(saved_img, width=None)
                else:
                    st.error("Image file not found.")
        
        # Reset the flag after displaying the message
        st.session_state["images_saved"] = False
    
    # Add a section for effect description
    with st.expander("ℹ️ About this effect"):
        if effect_option == "Spotlight":
            st.write("The Spotlight effect creates a focused light source at a specific point in the image, simulating studio lighting.")
        elif effect_option == "Vignette":
            st.write("The Vignette effect darkens the edges of the image while keeping the center bright, drawing attention to the subject.")
        elif effect_option == "Light Rays":
            st.write("The Light Rays effect (also known as God Rays) simulates beams of light coming from a light source, adding a dramatic atmosphere.")
        elif effect_option == "Color Temperature":
            st.write("The Color Temperature effect adjusts the warmth or coolness of the image, simulating different lighting conditions.")
        elif effect_option == "Dramatic Shadows":
            st.write("The Dramatic Shadows effect enhances the dark areas of the image for a more moody, cinematic look.")
        elif effect_option == "Glowing Highlights":
            st.write("The Glowing Highlights effect enhances the bright areas of the image, creating a dreamy, ethereal look.")
        elif effect_option == "Light Leaks":
            st.write("The Light Leaks effect simulates light leaking into the camera, adding random colorful light streaks for a vintage film photography feel.")
        elif effect_option == "Flare":
            st.write("The Lens Flare effect simulates the scattering of light within the camera lens, adding a professional cinematic quality.")
            
else:
    # Display sample images when no file is uploaded
    st.info("👈 Please upload an image to get started.")
    st.write("### Sample Images")
    
    # Display sample images in a grid
    sample_images = ["image1.jpg", "image2.jpg", "image3.jpg", "image4.jpg", "image5.jpg", "image6.webp"]
    cols = st.columns(3)
    
    for i, img_path in enumerate(sample_images):
        try:
            with cols[i % 3]:
                st.image(img_path, width=None, caption=f"Sample {i+1}")
        except:
            pass
    
    st.write("### About This App")
    st.write("""
    This professional lighting effects editor allows you to apply various lighting and color effects to your images.
    Upload an image and experiment with different effects to enhance your photos.
    
    Features:
    - Multiple lighting effects (spotlight, vignette, light rays, etc.)
    - Color grading and temperature adjustments
    - Dramatic shadows and glowing highlights
    - Download your processed images
    """)

# Add a footer
st.markdown("---")
st.markdown("Made with ❤️ using OpenCV and Streamlit")

# The desktop OpenCV application code is commented out below
# import cv2
# from effects.spotlight import apply_spotlight_effect
# from effects.vignette import apply_vignette_effect
# from effects.light_rays import apply_light_rays_effect
# from effects.color_temperature import apply_color_temperature
# from effects.dramatic_shadows import apply_dramatic_shadows
# from effects.glowing_highlights import apply_glowing_highlights
# from effects.light_leaks import apply_light_leaks
# from effects.lens_flare import apply_lens_flare  # New Effect
# 
# # Load an image
# image_path = "image6.webp"  # Change this to your image path
# image = cv2.imread(image_path)
# 
# if image is None:
#     print("Error: Could not load image. Check the file path.")
#     exit()
# 
# # Get image dimensions dynamically
# height, width = image.shape[:2]
# 
# # Default values
# center = (width // 2, height // 2)  
# radius = min(width, height) // 5    
# brightness = 1.5                    
# intensity = 1.5                     
# effect_mode = "spotlight"           
# light_rays_intensity = 0.5          
# light_rays_angle = 45               
# warmth = 0                          
# shadow_intensity = 1.5              
# glow_intensity = 0.5                
# leak_intensity = 0.5                
# flare_intensity = 0.5  # Lens Flare intensity
# flare_position = (width // 3, height // 3)  # Default flare position
# 
# def update_effect():
#     """Applies the selected effect and displays the image."""
#     if effect_mode == "spotlight":
#         processed_image = apply_spotlight_effect(image, center, radius, brightness)
#     elif effect_mode == "vignette":
#         processed_image = apply_vignette_effect(image, intensity)
#     elif effect_mode == "light_rays":
#         processed_image = apply_light_rays_effect(image, light_rays_intensity, light_rays_angle)
#     elif effect_mode == "color_temp":
#         processed_image = apply_color_temperature(image, warmth)
#     elif effect_mode == "shadows":
#         processed_image = apply_dramatic_shadows(image, shadow_intensity)
#     elif effect_mode == "glow":
#         processed_image = apply_glowing_highlights(image, glow_intensity)
#     elif effect_mode == "light_leaks":
#         processed_image = apply_light_leaks(image, leak_intensity)
#     elif effect_mode == "lens_flare":
#         processed_image = apply_lens_flare(image, flare_position, flare_intensity)
#     
#     cv2.imshow("Lighting Effects", processed_image)
# 
# # Mouse click event to change spotlight center or flare position
# def mouse_callback(event, x, y, flags, param):
#     global center, flare_position
#     if effect_mode == "spotlight" and event == cv2.EVENT_LBUTTONDOWN:
#         center = (x, y)
#     elif effect_mode == "lens_flare" and event == cv2.EVENT_LBUTTONDOWN:
#         flare_position = (x, y)
#     update_effect()
# 
# cv2.namedWindow("Lighting Effects", cv2.WINDOW_NORMAL)
# cv2.setMouseCallback("Lighting Effects", mouse_callback)
# 
# # Show initial effect
# update_effect()
# 
# while True:
#     key = cv2.waitKey(0) & 0xFF
# 
#     if key == ord("1"):  # Spotlight effect
#         effect_mode = "spotlight"
#     elif key == ord("2"):  # Vignette effect
#         effect_mode = "vignette"
#     elif key == ord("3"):  # Light Rays effect
#         effect_mode = "light_rays"
#     elif key == ord("4"):  # Color Temperature effect
#         effect_mode = "color_temp"
#     elif key == ord("5"):  # Dramatic Shadows effect
#         effect_mode = "shadows"
#     elif key == ord("6"):  # Glowing Highlights effect
#         effect_mode = "glow"
#     elif key == ord("7"):  # Light Leaks effect
#         effect_mode = "light_leaks"
#     elif key == ord("8"):  # Lens Flare effect
#         effect_mode = "lens_flare"
#     elif key == ord("+"):  
#         if effect_mode == "lens_flare":
#             flare_intensity = min(1.0, flare_intensity + 0.1)
#     elif key == ord("-"):  
#         if effect_mode == "lens_flare":
#             flare_intensity = max(0.1, flare_intensity - 0.1)
#     elif key == ord("b") and effect_mode == "spotlight":  
#         brightness = min(3.0, brightness + 0.1)
#     elif key == ord("d") and effect_mode == "spotlight":
#         brightness = max(0.5, brightness - 0.1)
#     elif key == 27:  # ESC key to exit
#         break
# 
#     update_effect()
# 
# cv2.destroyAllWindows()
