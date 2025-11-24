#!/bin/bash

# Exit on error
set -e

# Check if OUTPUT_FOLDER is set
if [ -z "${OUTPUT_FOLDER}" ]; then
    echo "ERROR: OUTPUT_FOLDER environment variable is not set"
    exit 1
fi

# Activate virtual environment and check if successful
if ! source .venv/bin/activate; then
    echo "ERROR: Failed to activate virtual environment"
    exit 1
fi

# Run Python script for each output directory
echo "Running main.py ..."
if ! python3 /docker/main.py; then
    echo "ERROR: Python script execution failed"
    exit 1
fi

echo "Script completed successfully"
