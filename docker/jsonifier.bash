#!/bin/bash

# Exit on error
set -e

# Check if OUTPUT_FOLDER is set
if [ -z "${OUTPUT_FOLDER}" ]; then
    echo "ERROR: OUTPUT_FOLDER environment variable is not set"
    exit 1
fi

outputs_json_dir='outputs_json'
echo "Creating directory outputs_json..."
mkdir -p "${OUTPUT_FOLDER}/${outputs_json_dir}"

# Loop over output directories
for i in {1..5}; do
    output_dir="output_${i}"

    # Create output directory
    echo "Creating directory ${output_dir}..."
    mkdir -p "${OUTPUT_FOLDER}/${output_dir}"
done

# Activate virtual environment and check if successful
if ! source .venv/bin/activate; then
    echo "ERROR: Failed to activate virtual environment"
    exit 1
fi

echo "INPUT_FOLDER:"
ls -al ${INPUT_FOLDER}

echo "INPUT_FOLDER/inputs.json:"
cat ${INPUT_FOLDER}/inputs.json

# Run Python script for each output directory
echo "Running main.py for ${output_dir}..."
if ! python3 /docker/main.py; then
    echo "ERROR: Python script execution failed for ${output_dir}"
    exit 1
fi

# Change to output directory
cd "${OUTPUT_FOLDER}" || exit 1

# Create zip archives for each output directory
echo "Creating zip archives..."
for i in {1..5}; do
    output_dir="output_${i}"
    echo "Zipping ${output_dir}..."
    if ! zip -r "${output_dir}.zip" "${output_dir}"; then
        echo "ERROR: Failed to create zip archive for ${output_dir}"
        exit 1
    fi
done
echo "Zipping ${outputs_json_dir}..."
if ! zip -r "${outputs_json_dir}.zip" "${outputs_json_dir}"; then
    echo "ERROR: Failed to create zip archive for ${outputs_json_dir}"
    exit 1
fi

echo "Script completed successfully"
