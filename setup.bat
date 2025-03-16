@echo off
echo Setting up the Professional Lighting Effects Editor...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in the PATH.
    echo Please install Python from https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Run the setup script
python setup.py

echo.
echo To run the application:
echo 1. Run the following command:
echo    start_app.bat
echo.

REM Create the start_app.bat file
echo @echo off > start_app.bat
echo echo Starting the Professional Lighting Effects Editor... >> start_app.bat
echo. >> start_app.bat
echo call lighting_effects_env\Scripts\activate.bat >> start_app.bat
echo streamlit run app.py >> start_app.bat
echo. >> start_app.bat
echo pause >> start_app.bat

echo Setup completed successfully!
pause 