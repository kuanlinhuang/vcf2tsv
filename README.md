## VCF to TSV/JSON Converter (Genomics)

This script converts a VCF file to a TSV or a JSON file, and allows the user to retain specified or all the INFO fields as separate columns in the output TSV or JSON file. It also handle .gz formats.

## Usage
The script can be run from the command line, and accepts the following arguments:  
`-h, --help - Show the help message and exit`  
`--info   Select specific info field to be retained as separate columns`  
`--all    Retain all the INFO fields as separate columns`  
`--gz     Output the file as gzip`
`--json - Output file format as json`

## Examples

To retain specified INFO fields DP and AD in the output TSV file, run the script as follows:  
`python vcf2tsv.py --info DP AD`

To retain all the INFO fields as separate columns in the output TSV file, run the script as follows:  
`python vcf2tsv.py --all`

To retain all the INFO fields as separate columns in the output .tsv.gz file, run the script as follows:  
`python vcf2tsv.py --all --gz input.vcf.gz`

To retain all the INFO fields as separate columns in the output .json file, run the script as follows:  
`python vcf2tsv.py --all --json input.vcf`

## Note
This script assumes that the input VCF file is well-formed and contains the specified INFO fields that are specified in the header.

## Dependencies
* Python 3
* argparse library
* csv library
* gzip library
Please make sure you have these libraries installed before running the script.

## Demo files
The demo files are downloaded from ClinVar ftp site (https://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh38/) or 1000 genome ftp site (http://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/). 

## Output
The script will create an output TSV or JSON file with the corresponding file name in the same folder as the input VCF file, it will have the same columns as the input VCF file, with the specified or all the INFO fields as additional columns.  It will also handle the case if the input is .vcf.gz, it will create the output file with the same name but with .tsv extension and if --gz flag is set it will create the output file with gzip compression.
