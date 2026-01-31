#!/usr/bin/env bash
# Simple script to run the Statistics Iceland web application

echo "Starting Statistics Iceland Data Viewer..."
echo "=========================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies if needed
if ! python -c "import flask" 2>/dev/null; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
fi

# Run the application
echo ""
echo "Starting Flask application..."
echo "Open your browser at: http://localhost:5000"
echo ""
python app.py
