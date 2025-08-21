#!/bin/bash

# Start the Food Aesthetics API server
export PATH="$HOME/.pyenv/bin:$PATH"
source venv/bin/activate

echo "🚀 Starting Food Aesthetics API server..."
echo "📱 API will be available at: http://localhost:8000"
echo "📚 Interactive docs at: http://localhost:8000/docs"
echo "🔍 Health check at: http://localhost:8000/health"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python api.py
