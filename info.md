# just to create idea of what this tool does and step by step approach:


## Introduction:

    With rise in modern sequencing techniques, understanding and manipulating short read sequencing data is more important than ever. Just like all other fields of  biology, ecology has also recently seen rise in genomics techniques for myriad research purposes. Several tools have been already published that helps in identifying species from their sequence. For example, BLAST is undobudtedly the most popular tool (algorithm) for species identification based on alignment. However, for species identification from scat samples, where each sample might contain multiple species (predator, prey, contamination, etc) it is crucial to measure the relative proportion of all species that is possibly present in the sample.
    
    For example, lets say a researcher sequenced a scat sample of Coyote, which had recently preyed on bobcat (a hypothetical example). Visually, scat sample of both coyote and bobcat looks indistinguishable. While doing blast, some reads should align well with coyote sequences in Genbank, while some other reads will align with bobcat sequences. But the blast result in this case might not be super helpful because bobcats and coyotes share huge similarity in their genome, both being carnivores. 


    Here we have created a tool UniqBase that serves the purpose of species identification based on diagnostic nucleotide of the species, which helps the user in decision making about the species identified from BLAST as predator. The modular functions in the script allows users 
    
    1. to fetch the reference sequences of the potential species (bobcat and coyote in this example) from the genbank (fetch_seq.sh),
    
    2. align the fetched sequences (align.sh),
    
    3. identify the positions which are unique to the potential species (uniq_base_pos.py) [ for eg: this script looks through all the input sequences and results only those positions where all bobcat bases is different than all coyote bases], and also outputs a consensus fasta file

    4. relalign the consensus with input fasta files 

    5. Caluclates composition of bases in the aligned file at the unique position, and returns a final csv file that helps the user to see if the most abundant base in the unique positons is similar to the diagnostic base of the potential species or not.

## Example usage:

### 1. fetch_seq.sh

    mkdir try1

    scripts/fetch_seq.sh -q "Lynx rufus[Organism] AND 12S[All Fields] AND mitochondrion[filter] NOT predicted[All Fields]" -f bobcat_12S -o try1

    grep -n "^>" try1/bobcat_12S.fasta | wc -l # only 9 seqs here

    scripts/fetch_seq.sh -q "Canis latrans[Organism] AND 12S[All Fields] AND mitochondrion[filter] NOT predicted[All Fields]" -f coyote_12S -o try1

    grep -n "^>" try1/coyote_12S.fasta | wc -l # 48 seqs here

### 2. align.sh

#### Align 12S of bobcat and coyote:
    
    scripts/align.sh "try1/*_12S.fasta" try1/12S2_aligned.fasta try1/12S_consensus.fasta

### 3. Uniq Base Position:

    scripts/uniq_base_pos.py try1/12S_aligned.fasta try1/12S_uniq_pos.csv

### 4. Compare the input sequence files by aligning with the consensus fasta file:

    # raw fasta files with known species from qPCR are saved into:
    ls try1/raw_reads/set1/
    # samples starting with 102 and 118 are bobcat 12S, 
    # samples starting with 130 and 135 are coyote 12S.

### 5. Realignment with the consensus file:

    scripts/realign.sh -d try1/raw_reads/set1/ -c try1/12S_consensus.fasta -t 10

### 6. Final Position Check:

    scripts/calculate_composition.py try1/raw_reads/set1/ try1/12S_uniq_pos.csv --output try1/final_12S_output.csv



