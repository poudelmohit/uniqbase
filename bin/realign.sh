#!/bin/bash

# Function to display usage instructions
usage() {
    echo "Usage: $0 -d <input_directory> -c <consensus_file> [-t <threads>] [-h]"
    echo "Options:"
    echo "  -d <input_directory>   Directory containing FASTA files to process."
    echo "  -c <consensus_file>    Consensus FASTA file for alignment."
    echo "  -t <threads>           Number of threads to use for MAFFT (default: 1)."
    echo "  -h                     Show this help message and exit."
    echo
    echo "Example:"
    echo "  $0 -d try1/raw_reads/set1/ -c try1/12S_consensus.fasta -t 8"
    exit 0
}

# Default values
threads=1  # Default to 1 thread if not provided

# Parse command-line arguments
while getopts ":d:c:t:h" opt; do
    case $opt in
        d) input_directory="$OPTARG" ;;
        c) consensus_file="$OPTARG" ;;
        t) threads="$OPTARG" ;;
        h) usage ;;  # Display help and exit
        \?)  # Handle invalid options
            echo "Error: Invalid option -$OPTARG"
            usage ;;
        :)  # Handle missing arguments for options
            echo "Error: Option -$OPTARG requires an argument."
            usage ;;
    esac
done

# Validate required arguments
if [ -z "$input_directory" ] || [ -z "$consensus_file" ]; then
    echo "Error: Missing required arguments."
    usage
fi

# Ensure input directory exists
if [ ! -d "$input_directory" ]; then
    echo "Error: Input directory '$input_directory' does not exist."
    exit 1
fi

# Ensure consensus file exists
if [ ! -f "$consensus_file" ]; then
    echo "Error: Consensus file '$consensus_file' does not exist."
    exit 1
fi

# Process each FASTA file in the directory
for file in "$input_directory"/*.fasta; do
    if [ -f "$file" ]; then
        # Generate output file name
        output_filename="${file%.fasta}_aligned.fasta"

        # Align the sequences
        echo "Aligning $file..."
        mafft --6merpair --keeplength --thread "$threads" --addfragments "$file" "$consensus_file" > temp.fasta

        # Convert to two-line FASTA format
        seqtk seq temp.fasta > "$output_filename"

        # Clean up temporary file
        rm -f temp.fasta

        echo "Aligned file saved to $output_filename"
    else
        echo "No FASTA files found in the directory."
    fi
done

echo "Alignment completed."
