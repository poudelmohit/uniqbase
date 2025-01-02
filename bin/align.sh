#!/bin/bash

# Function to display usage
usage() {
    echo "Usage: $0 <input_pattern> <output_file> <consensus_file>"
    echo "Example: $0 'try1/*_12S.fasta' try1/12S_aligned.fasta try1/12S_consensus.fasta"
    echo "Options:"
    echo "  -h  Show this help message and exit"
    echo
    echo "Description:"
    echo "This script aligns input FASTA sequences using MAFFT, generates a consensus sequence,"
    echo "and reformats the output into two-line FASTA format."
    exit 0
}

# Parse command-line arguments
if [ "$#" -eq 1 ] && [ "$1" == "-h" ]; then
    usage
fi

# Check if correct number of arguments is provided
if [ "$#" -ne 3 ]; then
    echo "Error: Invalid number of arguments."
    usage
fi

# Get input pattern and output file from arguments
input_pattern="$1"
output_file="$2"
consensus_file="$3"

# Create temporary files
temp_input="input_temp.fasta"
temp_output="output_temp.fasta"
temp_consensus="temp_consensus.fasta"

# Gather and concatenate input files
input_files=$(ls $input_pattern 2>/dev/null)
if [ -z "$input_files" ]; then
    echo "Error: No files found matching pattern '$input_pattern'"
    exit 1
fi

cat $input_files > "$temp_input"

# Align sequences using MAFFT
mafft --auto "$temp_input" > "$temp_output"

# Reformat the aligned sequences into two-line FASTA format
seqtk seq "$temp_output" > "$output_file"

# Create a consensus file from aligned FASTA file
cons -sequence "$output_file" -outseq "$temp_consensus"

# Reformat the temp consensus into two-line format
seqtk seq "$temp_consensus" > "$consensus_file"

# Clean up temporary files
rm -f "$temp_input" "$temp_output" "$temp_consensus"
