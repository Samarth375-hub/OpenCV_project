# 💡 Professional Lighting Effects Editor

A powerful image editing application that allows you to apply professional lighting effects to your photos using OpenCV and Streamlit.

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

### Automatic Setup (Recommended)

#### Windows Users
1. Clone this repository:
   ```
   git clone https://github.com/Samarth375-hub/OpenCV_project.git
   cd OpenCV_project
   ```

2. Run the setup script:
   ```
   setup.bat
   ```

3. Start the application:
   ```
   start_app.bat
   ```

#### macOS/Linux Users
1. Clone this repository:
   ```
   git clone https://github.com/Samarth375-hub/OpenCV_project.git
   cd OpenCV_project
   ```

2. Run the setup script:
   ```
   bash setup.sh
   ```

3. Start the application:
   ```
   bash start_app.sh
   ```

### Manual Setup

1. Clone this repository:
   ```
   git clone https://github.com/Samarth375-hub/OpenCV_project.git
   cd OpenCV_project
   ```

2. Create and activate a virtual environment (recommended):
   ```
   # Windows
   python -m venv lighting_effects_env
   lighting_effects_env\Scripts\activate

   # macOS/Linux
   python -m venv lighting_effects_env
   source lighting_effects_env/bin/activate
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Create a Streamlit configuration file (optional but recommended):
   ```
   # Create the .streamlit directory if it doesn't exist
   mkdir -p .streamlit

   # Create the config.toml file with the following content
   echo "[server]
   headless = false
   port = 8502
   enableCORS = false
   enableXsrfProtection = false
   address = \"localhost\"

   [browser]
   serverAddress = \"localhost\"
   serverPort = 8502" > .streamlit/config.toml
   ```

5. Run the application:
   ```
   streamlit run app.py
   ```

6. Access the application in your browser:
   ```
   http://localhost:8502
   ```

## 🔧 Troubleshooting

### Port Already in Use
If you see an error message saying "Port 8501 is already in use", you can:
- Use a different port by modifying the `.streamlit/config.toml` file
- Kill the existing Streamlit process:
  ```
  # Windows
  taskkill /f /im python.exe
  
  # macOS/Linux
  pkill -f streamlit
  ```

### Streamlit Version Compatibility
This application is compatible with Streamlit version 1.32.0. If you encounter any issues with different versions:
- Check your Streamlit version: `pip show streamlit`
- Update to the recommended version: `pip install streamlit==1.32.0`

### Image Display Issues
If images are not displaying correctly, ensure you're using the correct parameter for your Streamlit version:
- For newer versions of Streamlit: `use_container_width=True`
- For older versions of Streamlit: `width=None`

The current code uses `width=None` which is compatible with most Streamlit versions.

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