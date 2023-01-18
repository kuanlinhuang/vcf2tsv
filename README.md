# vcf2tsv
## VCF to TSV Converter (Genomics)

This script converts a VCF file to a TSV file, and allows the user to retain specified or all the INFO fields as separate columns in the output TSV file. It also handle .vcf.gz and .tsv.gz formats.

## Usage
The script can be run from the command line, and accepts the following arguments:  
`--info   The INFO fields to be retained`  
`--all    Retain all the INFO fields`  
`--gz     Output the file as .tsv.gz`

## Examples

To retain specified INFO fields DP and AD in the output TSV file, run the script as follows:  
`python script.py --info DP AD`

To retain all the INFO fields in the output TSV file, run the script as follows:  
`python script.py --all`

To retain all the INFO fields in the output .tsv.gz file, run the script as follows:  
`python script.py --all --gz input.vcf.gz`

## Note
This script assumes that the input VCF file is well-formed and contains the specified INFO fields, it does not handle missing fields or different versions of VCF files.

## Dependencies
* Python 3
* argparse library
* csv library
* gzip library
Please make sure you have these libraries installed before running the script.

## Demo files
The demo files are downloaded from ClinVar ftp site (https://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh38/)

## Output
The script will create an output TSV file with the same file name in the same folder as the input VCF file, it will have the same columns as the input VCF file, with the specified or all the INFO fields as additional columns.  It will also handle the case if the input is .vcf.gz, it will create the output file with the same name but with .tsv extension and if --gz flag is set it will create the output file with gzip compression.
