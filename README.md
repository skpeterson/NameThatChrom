# NameThatChrom

Welcome to NameThatChrom Jeopardy!

What is NameThatChrom?
This script converts chromosome names in a BAM file from RefSeq to UCSC style, sorts the converted BAM file, and indexes it.


**Command-Line Arguments**
| Argument         | Description                                                                                     | Required | Default |
|------------------|-------------------------------------------------------------------------------------------------|----------|---------|
| `input_bam`      | Input BAM file path.                                                                            | Yes      | N/A     |
| `output_bam`     | Output BAM file path.                                                                           | Yes      | N/A     |
| `mapping_file`   | Space-delimited file mapping RefSeq to UCSC chromosome names (no header).                       | Yes      | N/A     |
| `--threads`      | Number of threads for sorting.								     | No       | 8

Note: this does not overwrite the provided BAM file, instead it will make a new one, so be sure to provide a unique name for the new output BAM

## How to play
1. Insert your bam file
2. Choos your category: 'RefSeq to UCSC'
3. Get your UCSC-style output and claim your points!


## Okay, but really, how to use this tool
1. Locate BAM filed intended for conversion
2. Ensure the 'data/chr_mapping.txt' file contains the desired mappings
3. Run the script


## Example Bash Script

If you're working on a Linux based HPC system, here's how you would run the script

```bash
#!/bin/bash

#SBATCH -N 1
#SBATCH --mem 200g
#SBATCH -n 1
#SBATCH --cpus-per-task=12
#SBATCH -t 1-00:00:00
#SBATCH --mail-type=end
#SBATCH --mail-user=user@email

# load python
module load python/3.11.9

INPUT_BAM="/path/to/bam/to/convert/sample.bam"
OUTPUT_BAM="path/to/where/new/bam/should/go/sample_converted.bam"
MAPPING_FILE="/data/chr_mapping.txt"


# run script
python /scripts/convert_refseq_to_ucsc_chroms.py \
       --input_bam $INPUT_BAM \
       --output_bam $OUTPUT_BAM \
       --mapping_file $MAPPING_FILE \
       --threads 12
```

