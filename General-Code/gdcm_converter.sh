#!/bin/bash

# Check if the gdcmconv tool is installed
if ! command -v gdcmconv &> /dev/null; then
    echo "gdcmconv is not installed. Please install GDCM (Grassroots DICOM) first."
    exit 1
fi

# Prompt the user for the input directory containing DICOM files
read -p "Enter the input directory path: " input_directory

# Check if the input directory exists
if [ ! -d "$input_directory" ]; then
    echo "Input directory does not exist. Please provide a valid directory path."
    exit 1
fi

# Prompt the user for the output directory for the converted files
read -p "Enter the output directory path: " output_directory

# Create the output directory if it doesn't exist
mkdir -p "$output_directory"

# Use a loop to process each DICOM file in the input directory
for input_file in "$input_directory"/*.dcm; do
    # Get the filename without the path
    filename=$(basename "$input_file")

    # Specify the output file path
    output_file="$output_directory/$filename"

    # Use gdcmconv with -w to convert the DICOM file
    gdcmconv -w "$input_file" "$output_file"

    # Check if gdcmconv was successful
    if [ $? -eq 0 ]; then
        echo "Converted $filename successfully."
    else
        echo "Failed to convert $filename."
    fi
done

echo "Conversion complete."
