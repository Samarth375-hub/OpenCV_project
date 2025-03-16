import os
import subprocess
import sys
import platform

def create_virtual_env():
    """Create a virtual environment for the project."""
    print("Creating virtual environment...")
    
    # Check if virtual environment already exists
    if os.path.exists("lighting_effects_env"):
        print("Virtual environment already exists.")
        return
    
    try:
        subprocess.check_call([sys.executable, "-m", "venv", "lighting_effects_env"])
        print("Virtual environment created successfully.")
    except subprocess.CalledProcessError:
        print("Failed to create virtual environment. Please create it manually.")
        print("Run: python -m venv lighting_effects_env")

def install_requirements():
    """Install the required packages."""
    print("Installing required packages...")
    
    # Determine the path to the Python executable in the virtual environment
    if platform.system() == "Windows":
        python_path = os.path.join("lighting_effects_env", "Scripts", "python.exe")
    else:
        python_path = os.path.join("lighting_effects_env", "bin", "python")
    
    # Check if the Python executable exists
    if not os.path.exists(python_path):
        print(f"Python executable not found at {python_path}")
        print("Please activate the virtual environment manually and run:")
        print("pip install -r requirements.txt")
        return
    
    try:
        subprocess.check_call([python_path, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Required packages installed successfully.")
    except subprocess.CalledProcessError:
        print("Failed to install required packages. Please install them manually.")
        print("Run: pip install -r requirements.txt")

def create_streamlit_config():
    """Create the Streamlit configuration file."""
    print("Creating Streamlit configuration...")
    
    # Create the .streamlit directory if it doesn't exist
    os.makedirs(".streamlit", exist_ok=True)
    
    # Create the config.toml file
    config_content = """[server]
headless = false
port = 8502
enableCORS = false
enableXsrfProtection = false
address = "localhost"

[browser]
serverAddress = "localhost"
serverPort = 8502
"""
    
    with open(os.path.join(".streamlit", "config.toml"), "w") as f:
        f.write(config_content)
    
    print("Streamlit configuration created successfully.")

def main():
    """Main function to set up the project."""
    print("Setting up the Professional Lighting Effects Editor...")
    
    create_virtual_env()
    install_requirements()
    create_streamlit_config()
    
    print("\nSetup completed successfully!")
    print("\nTo run the application:")
    
    if platform.system() == "Windows":
        print("1. Activate the virtual environment: lighting_effects_env\\Scripts\\activate")
    else:
        print("1. Activate the virtual environment: source lighting_effects_env/bin/activate")
    
    print("2. Run the application: streamlit run app.py")
    print("3. Access the application in your browser: http://localhost:8502")

if __name__ == "__main__":
    main() 