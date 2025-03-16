#!/bin/bash

echo "Setting up the Professional Lighting Effects Editor..."
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed or not in the PATH."
    echo "Please install Python 3 from https://www.python.org/downloads/"
    exit 1
fi

# Run the setup script
python3 setup.py

echo
echo "To run the application:"
echo "1. Run the following command:"
echo "   bash start_app.sh"
echo

# Create the start_app.sh file
cat > start_app.sh << 'EOF'
#!/bin/bash
echo "Starting the Professional Lighting Effects Editor..."
echo

source lighting_effects_env/bin/activate
streamlit run app.py

echo
EOF

# Make the start_app.sh file executable
chmod +x start_app.sh

echo "Setup completed successfully!" 