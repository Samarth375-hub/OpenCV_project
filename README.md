# 💡 Professional Lighting Effects Editor

A powerful image editing application that allows you to apply professional lighting effects to your photos using OpenCV and Streamlit.

![Lighting Effects Editor](https://github.com/yourusername/lighting-effects-editor/raw/main/screenshot.png)

## ✨ Features

- **Multiple Lighting Effects**:
  - Spotlight: Create a focused light source at a specific point
  - Vignette: Darken the edges while keeping the center bright
  - Light Rays: Simulate beams of light (God Rays)
  - Light Leaks: Add colorful light streaks for a vintage film look
  - Lens Flare: Simulate light scattering within camera lens
  - Color Temperature: Adjust warmth/coolness of the image
  - Dramatic Shadows: Enhance dark areas for a moody look
  - Glowing Highlights: Enhance bright areas for a dreamy look

- **Interactive Controls**:
  - Adjust effect parameters in real-time
  - Position effects with sliders
  - Compare before/after views
  - Save processed images with effect parameters documented

- **Professional Output**:
  - High-quality image processing
  - Side-by-side comparison images
  - Parameter documentation embedded in saved images

## 🚀 Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/lighting-effects-editor.git
   cd lighting-effects-editor
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   streamlit run app.py
   ```

## 📖 Usage

1. Upload an image using the file uploader in the sidebar
2. Select an effect from the dropdown menu
3. Adjust the effect parameters using the sliders
4. Download the processed image using the download button
5. Both the original and processed images will be saved in a single comparison file

## 📸 Example Effects

### Spotlight Effect
Creates a focused light source at a specific point in the image, simulating studio lighting.

### Vignette Effect
Darkens the edges of the image while keeping the center bright, drawing attention to the subject.

### Light Rays Effect
Simulates beams of light coming from a light source, adding a dramatic atmosphere.

### Lens Flare Effect
Simulates the scattering of light within the camera lens, adding a professional cinematic quality.

## 🛠️ Project Structure

- `app.py`: Main Streamlit application
- `effects/`: Directory containing all effect implementations
  - `spotlight.py`: Spotlight effect implementation
  - `vignette.py`: Vignette effect implementation
  - `light_rays.py`: Light rays effect implementation
  - `light_leaks.py`: Light leaks effect implementation
  - `lens_flare.py`: Lens flare effect implementation
  - `color_temperature.py`: Color temperature effect implementation
  - `dramatic_shadows.py`: Dramatic shadows effect implementation
  - `glowing_highlights.py`: Glowing highlights effect implementation
- `results/`: Directory where comparison images are saved

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- OpenCV for image processing capabilities
- Streamlit for the interactive web interface
- All the photographers who provided sample images 