#!/usr/bin/env python3

import pandas as pd
import argparse

def parse_fasta(fasta_file):
    """Parse a FASTA file to extract headers and sequences."""
    headers = []
    sequences = []

    with open(fasta_file, "r") as file:
        lines = file.readlines()
        for i in range(len(lines)):
            if lines[i].startswith(">"):  # Identify header lines
                headers.append(lines[i].strip())
                if i + 1 < len(lines):
                    sequences.append(lines[i + 1].strip())  # Next line as sequence
    return headers, sequences

def process_fasta(headers, sequences):
    """Process headers and sequences into a DataFrame."""
    df = pd.DataFrame({"header": headers, "sequence": sequences})

    # Split headers into 'identifier' and 'name'
    df[['identifier', 'name']] = df['header'].str.split(';', expand=True)
    df = df.drop(columns=['header'])
    df['name'] = df['name'].str.split("=", expand=False).str[1]
    df = df[['identifier', 'name', 'sequence']]

    # Expand sequence into individual columns based on position
    for i in range(len(df['sequence'][0])):
        df[f'{i+1}'] = df['sequence'].apply(lambda x: x[i])

    # Reorder columns
    columns_order = ['identifier', 'name'] + [col for col in df.columns if col not in ['identifier', 'name', 'sequence']]
    return df[columns_order]

def filter_identical_columns(df):
    """Filter columns with identical values across all rows."""
    df1 = (df.groupby('name').nunique() == 1)
    columns_to_keep = ['name'] + df1.columns[df1.all()].tolist()
    df_filtered = df[columns_to_keep].drop_duplicates().reset_index(drop=True)
    return df_filtered.loc[:, df_filtered.nunique() > 1]

def main():
    parser = argparse.ArgumentParser(description="Process a FASTA file into a DataFrame.")
    parser.add_argument("input_fasta", help="Input FASTA file")
    parser.add_argument("output_file", help="Output filename for the processed DataFrame (CSV format)")
    args = parser.parse_args()

    # Parse the FASTA file
    headers, sequences = parse_fasta(args.input_fasta)

    # Process the headers and sequences into a DataFrame
    df = process_fasta(headers, sequences)

    # Filter the DataFrame to retain only unique columns
    df_filtered = filter_identical_columns(df)

    # Save the final DataFrame to a CSV file
    df_filtered.to_csv(args.output_file, index=False)
    print(f"Processed DataFrame saved to {args.output_file}")

if __name__ == "__main__":
    main()
