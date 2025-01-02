#!/usr/bin/env python3

import pandas as pd
import os
import argparse

def extract_positions_from_even_lines(filename, positions):
    """
    Extracts specified bases from sequence lines (escaping headers) in a FASTA file.
    """
    positions = [int(pos) for pos in positions]
    results = []
    with open(filename, 'r') as file:
        lines = file.readlines()
        for i, line in enumerate(lines):
            # Process only odd-numbered lines (0-based, i.e., actual sequence lines)
            if i % 2 != 0:
                result = [line[pos - 1] for pos in positions if pos <= len(line.strip())]
                results.append(result)

    # Create a DataFrame from results
    df = pd.DataFrame(results, columns=positions)
    df.replace('-', 'X', inplace=True)
    df = df.loc[:, (df != 'X').any(axis=0)]  # Keep columns with at least one valid entry
    return df


def calculate_composition_percentage(df, sample_id):
    """
    Calculates the composition percentage for each position and prepares output.
    """
    composition = {}
    for column in df.columns:
        counts = df[column].value_counts(normalize=True) * 100
        composition[column] = counts.round(2)
    composition_df = pd.DataFrame(composition)

    # Prepare output for the sample
    highest_composition_df = pd.DataFrame(index=[sample_id, sample_id + '_perc'])
    for column in composition_df.columns:
        if not composition_df[column].empty:
            max_value = composition_df[column].idxmax()
            max_percentage = composition_df[column].max()
            highest_composition_df[column] = [max_value, max_percentage]

    return highest_composition_df


def process_all_files(directory, positions, diagnostic_df, output_file):
    """
    Processes all `_aligned.fasta` files in the directory and generates the final output CSV.
    """
    all_dfs = []
    for filename in os.listdir(directory):
        if filename.endswith('_aligned.fasta'):
            full_path = os.path.join(directory, filename)
            sample_id = os.path.splitext(filename)[0]  # Strip the extension for sample ID
            print(f"Processing {filename}...")
            
            # Extract positions and calculate composition percentages
            position_df = extract_positions_from_even_lines(full_path, positions)
            result_df = calculate_composition_percentage(position_df, sample_id)
            all_dfs.append(result_df)

    # Concatenate all DataFrames and save to CSV
    if all_dfs:
        combined_sample_df = pd.concat(all_dfs, axis=0)

        # also, add the diagnostic df:
        final_df = pd.concat([diagnostic_df, combined_sample_df], axis=0)
        final_df.to_csv(output_file)
        print(f"Successfully saved results to {output_file}")
    else:
        print("No `_aligned.fasta` files found in the directory.")


if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Process aligned FASTA files and calculate specific position compositions.")
    parser.add_argument("directory", help="Path to the directory containing `_aligned.fasta` files.")
    parser.add_argument("positions_csv", help="Path to the CSV file with unique positions.")
    parser.add_argument("--output", default="final_output.csv", help="Path for the output CSV file (default: final_output.csv).")

    args = parser.parse_args()

    # Load diagnostic positions
    try:
        diagnostic_df_main = pd.read_csv(args.positions_csv, index_col=0)
        diagnostic_df_main.columns = [int(col) for col in diagnostic_df_main.columns]
    except Exception as e:
        print(f"Error reading positions CSV: {e}")
        exit(1)

    # Process all files and save results
    process_all_files(args.directory, list(diagnostic_df_main.columns), diagnostic_df_main, args.output)
