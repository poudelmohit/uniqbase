# UniqBase

### Introduction

**UniqBase** is a bioinformatics tool designed for accurate species identification by analyzing unique nucleotide positions in fasta files. The tool is particularly useful for species identification in complex samples, such as predator scat, where multiple species' DNA may be present.

With a modular design, **UniqBase** provides a step-by-step workflow that includes sequence fetching, alignment, unique position identification, realignment, and composition analysis.

### Features

- Fetch reference sequences from GenBank based on user-defined queries.
- Align multiple sequences and generate consensus sequences.
- Identify unique nucleotide positions diagnostic of specific species.
- Realign input sequences against consensus sequences.
- Analyze nucleotide composition at unique positions to infer species identity.

### Installation

Clone the repository:

    git clone https://github.com/poudelmohit/uniqbase.git
    cd uniqbase
    chmod +x bin/*
    pip install -r requirements.txt

### Usage

1. Fetch Reference Sequences

Retrieve reference sequences for species of interest from GenBank using [fetch_seq.sh](bin/fetch_seq.sh)

    bin/fetch_seq.sh -q "<query>" -f <filename> -o <output_directory>

Example:

    bin/fetch_seq.sh -q "Lynx rufus[Organism] AND 12S[All Fields] AND mitochondrion[filter]" -f bobcat_12S -o data/

2. Align Fetched Sequences

Align sequences and generate a consensus file using [align.sh](bin/align.sh):

    bin/align.sh "<input_pattern>" <output_file> <consensus_file>

Example:

    bin/align.sh "data/*_12S.fasta" data/12S_aligned.fasta data/12S_consensus.fasta

3. Identify Unique Positions

Identify nucleotide positions unique to each species using [uniq_base_pos.py](bin/uniq_base_pos.py):

    bin/uniq_base_pos.py <aligned_fasta> <output_csv>

Example

    bin/uniq_base_pos.py data/12S_aligned.fasta data/12S_uniq_pos.csv

4. Align Input Sequences with Consensus

Realign input sequences to the consensus sequence using [realign.sh](bin/realign.sh):

    bin/realign.sh -d <input_directory> -c <consensus_file> -t <threads>

Example:

    bin/realign.sh -d data/raw_reads/ -c data/12S_consensus.fasta -t 4

5. Analyze Composition

Analyze nucleotide composition at unique positions using [calculate_composition.py](bin/calculate_composition.py):

    bin/calculate_composition.py <input_directory> <positions_csv> --output <output_file>

Example:

    bin/calculate_composition.py data/raw_reads/ data/12S_uniq_pos.csv --output data/final_output.csv


### Contributing

*Contributions are welcome! To contribute:*

1. Fork this repository.
2. Create a feature branch (git checkout -b feature-name).
3. Commit your changes (git commit -m "Add feature").
4. Push to the branch (git push origin feature-name).
5. Create a pull request.

### Acknowledgments

[**Alavarado-Serrano LAB, Ohio Univesity**](https://alvarado-s.weebly.com)
![Logo](https://github.com/poudelmohit/portfolio/blob/main/assets/lablogo-small.png)

### Developed By

[**Mohit Poudel**](https://poudelmohit.github.io)





