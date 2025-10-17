#!/bin/bash

# StudyLeague API Startup Script

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "WARNING: .env file not found. Please create one with your configuration."
    echo "Copy .env.example to .env and update the values."
    exit 1
fi

# Start the Flask application
echo "Starting StudyLeague API..."
python app.py
