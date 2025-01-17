import pysam
import argparse
import os
import tempfile

def load_chr_mapping(mapping_file):
    """
    Load chromosome mapping from file.
    Expected format: refseq_chr<tab>ucsc_chr
    Example: NC_000001.11    chr1
    """
    chr_map = {}
    with open(mapping_file, 'r') as f:
        for line in f:
            refseq, ucsc = line.strip().split(' ')
            chr_map[refseq] = ucsc
    return chr_map

def convert_sort_and_index_bam(input_bam, output_bam, chr_map, threads=12):
    """
    Convert chromosome names in BAM file using provided mapping,
    sort by coordinate, and create index.
    """
    # Open input BAM file
    try:
        input_bam = pysam.AlignmentFile(input_bam, "rb")
    except ValueError as e:
        print(f"Error reading BAM file: {e}")
        return
    
    # Create new header with updated chromosome names
    new_header = input_bam.header.to_dict()
    
    # Update sequence dictionary in header
    for seq in new_header['SQ']:
        if seq['SN'] in chr_map:
            seq['SN'] = chr_map[seq['SN']]
    
    # Create temporary BAM file for initial conversion
    temp_prefix = "temp_converted"
    with tempfile.NamedTemporaryFile(prefix=temp_prefix, suffix='.bam', delete=False) as temp:
        temp_bam_path = temp.name
    
    # Create temporary output BAM file with new header
    temp_out = pysam.AlignmentFile(temp_bam_path, "wb", header=new_header)
    
    # Process reads and update chromosome names
    for read in input_bam:
        if read.reference_name and read.reference_name in chr_map:
            read.reference_id = temp_out.get_tid(chr_map[read.reference_name])
        temp_out.write(read)
    
    # Close files
    input_bam.close()
    temp_out.close()
    
    # Sort the BAM file
    print("Sorting BAM file...")
    pysam.sort("-@", str(threads), "-o", output_bam, temp_bam_path)
    
    # Remove temporary file
    os.unlink(temp_bam_path)
    
    # Index the final sorted BAM file
    print("Creating BAM index...")
    pysam.index(output_bam)

def main():
    parser = argparse.ArgumentParser(description='Convert chromosome names in BAM file from RefSeq to UCSC style, then sort, and index the converted bam file')
    parser.add_argument('-i','--input_bam', required=True, help='Input BAM file')
    parser.add_argument('-o','--output_bam', required=True, help='Output BAM file')
    parser.add_argument('-m', '--mapping_file', required=True, help='Space-delimited file mapping RefSeq to UCSC chromosome names (no header)')
    parser.add_argument('--threads', type=int, default=8, help='Number of threads for sorting (default: 8)')
    
    args = parser.parse_args()
    
    # Load chromosome mapping
    chr_map = load_chr_mapping(args.mapping_file)
    
    # Print chromosome mappings for verification
    print("Using the following chromosome mappings:")
    for refseq, ucsc in chr_map.items():
        print(f"{refseq} -> {ucsc}")
    
    # Convert, sort, and index BAM file
    convert_sort_and_index_bam(args.input_bam, args.output_bam, chr_map, args.threads)
    
    print(f"Converted, sorted BAM file saved to: {args.output_bam}")
    print(f"BAM index created: {args.output_bam}.bai")

if __name__ == "__main__":
    main()