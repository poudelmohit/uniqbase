cd UniqBase
ls

## Setting up directories:

    m
### Main package directory
    mkdir -p uniqbase
    touch uniqbase/__init__.py
    touch uniqbase/main.py
    touch uniqbase/aligner.py
    touch uniqbase/marker_finder.py
    touch uniqbase/sequence_checker.py
    touch uniqbase/utils.py

# Tests directory
    mkdir -p tests
    touch tests/__init__.py
    touch tests/test_aligner.py
    touch tests/test_marker_finder.py
    touch tests/test_sequence_checker.py
    touch tests/test_utils.py

# Data directory
    mkdir -p data
    touch data/example.fasta
    touch data/species_sequences.fasta
    touch data/README.md

# Scripts directory
mkdir -p scripts
touch scripts/run_uniqbase.py

# Documentation directory
mkdir -p docs
touch docs/index.md
touch docs/usage.md

# Project root files
touch setup.py
touch requirements.txt
touch environment.yml
touch README.md
touch LICENSE
touch .gitignore