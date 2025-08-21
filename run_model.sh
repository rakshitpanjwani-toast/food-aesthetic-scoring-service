#!/bin/bash

# Activate the Python 3.10 virtual environment and run the food aesthetics model
export PATH="$HOME/.pyenv/bin:$PATH"
source venv/bin/activate

# Run the model on the images folder
python run.py ./images

echo "Model execution completed!"
