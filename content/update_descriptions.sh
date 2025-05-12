#!/bin/bash

# Convenience script to run the description generator

# Change to the script directory
cd "$(dirname "$0")"

# Activate the virtual environment
source venv/bin/activate

# Run the Python script with all arguments passed through
./generate_description.py "$@"