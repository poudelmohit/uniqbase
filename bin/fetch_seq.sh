#!/bin/bash

# Function to display usage
usage() {
    echo "Usage: $0 -q <query> -f <output_filename (without .fasta)> -o <output_directory>"
    echo "Options:"
    echo "  -q <query>              Query for NCBI search."
    echo "  -f <output_filename>    Base name of the output FASTA file (without extension)."
    echo "  -o <output_directory>   Directory where the output file will be saved."
    echo "  -h                      Show this help message and exit."
    exit 0
}

# Parse command-line arguments
while getopts ":hq:f:o:" opt; do
    case "$opt" in
        h) usage ;;  # Display usage information and exit
        q) query=$OPTARG ;;
        f) output_filename=$OPTARG ;;
        o) output_directory=$OPTARG ;;
        \?)  # Handle invalid options
            echo "Invalid option: -$OPTARG" >&2
            usage ;;
        :)  # Handle missing arguments for options
            echo "Option -$OPTARG requires an argument." >&2
            usage ;;
    esac
done

# Ensure all required arguments are provided
if [ -z "$query" ] || [ -z "$output_filename" ] || [ -z "$output_directory" ]; then
    echo "Error: Missing required arguments."
    usage
fi

# Ensure the output directory exists
if [ ! -d "$output_directory" ]; then
    echo "Error: Output directory does not exist."
    exit 1
fi

# Run the esearch and efetch commands, saving the output to the specified file in the output directory
esearch -db nuccore -query "$query" | efetch -format fasta | \
sed -E "s/^(>[^ ]*).*/\1;name=${output_filename}/" > "$output_directory/$output_filename.fasta"

# Notify the user
echo "Output saved to $output_directory/$output_filename.fasta; with $(grep "^>" "$output_directory/$output_filename.fasta" | wc -l) sequences"
