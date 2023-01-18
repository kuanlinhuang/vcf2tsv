# vcf2tsv
## VCF to TSV Converter (Genomics)

This script converts a VCF file to a TSV file, and allows the user to retain specified or all the INFO fields as separate columns in the output TSV file.

## Usage
The script can be run from the command line, and accepts the following arguments:  
`--info   The INFO fields to be retained`  
`--all    Retain all the INFO fields`

## Examples

To retain specified INFO fields DP and AD in the output TSV file, run the script as follows:  
`python script.py --info DP AD`

To retain all the INFO fields in the output TSV file, run the script as follows:  
`python script.py --all`

## Note
This script assumes that the input VCF file is well-formed and contains the specified INFO fields, it does not handle missing fields or different versions of VCF files.

## Dependencies
* Python 3
* argparse library
* csv library
Please make sure you have these libraries installed before running the script.

## Output
The script will create an output TSV file with the same file name in the same folder as the input VCF file, it will have the same columns as the input VCF file, with the specified or all the INFO fields as additional columns, if any.
