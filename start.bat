@echo off

REM StudyLeague API Startup Script for Windows

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Check if .env file exists
if not exist ".env" (
    echo WARNING: .env file not found. Please create one with your configuration.
    echo Copy .env.example to .env and update the values.
    pause
    exit /b 1
)

REM Start the Flask application
echo Starting StudyLeague API...
python app.py

pause
