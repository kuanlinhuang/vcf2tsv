import csv
import argparse
import os
import gzip

# create the parser
parser = argparse.ArgumentParser(description='Convert VCF file to TSV and retain the specified INFO fields')
# add the argument
parser.add_argument('--info', nargs='*', help='The INFO fields to be retained')
parser.add_argument('--all', action='store_true', help='Retain all the INFO fields')
parser.add_argument('--gz', action='store_true', help='Output the file as .tsv.gz')
parser.add_argument('input_file', help='The input VCF file')
args = parser.parse_args()

#validate the input file
if not args.input_file.endswith('.vcf') and not args.input_file.endswith('.vcf.gz'):
    raise ValueError("Invalid input file. Please provide a valid .vcf or .vcf.gz file")

if not os.path.isfile(args.input_file):
    raise FileNotFoundError("Input file not found")

# Open the input .vcf file
if args.input_file.endswith('.gz'):
    try:
        vcf_file = gzip.open(args.input_file, 'rt')
    except OSError as e:
        raise ValueError("Invalid input file. Please provide a valid .vcf.gz file") from e
else:
    try:
        vcf_file = open(args.input_file, "r")
    except OSError as e:
        raise ValueError("Invalid input file. Please provide a valid .vcf file") from e

lines = vcf_file.readlines()
vcf_file.close()

# get the file name without the extension
file_name, file_extension = os.path.splitext(args.input_file)
if file_extension == '.gz':
    file_name, file_extension = os.path.splitext(file_name)

# Open the output .tsv file
if args.gz:
    try:
        tsv_file = gzip.open(file_name + '.tsv.gz', "wt")
    except OSError as e:
        raise ValueError("Error creating output file. Please check the output directory and its permissions") from e
else:
    try:
        tsv_file = open(file_name + '.tsv', "w")
    except OSError as e:
        raise ValueError("Error creating output file. Please check the output directory and its permissions") from e

# Create a CSV writer
tsv_writer = csv.writer(tsv_file, delimiter='\t')
header = ["#CHROM","POS","ID","REF","ALT","QUAL","FILTER","INFO"]
if args.info or args.all:
    all_info_fields = set()
    for line in lines:
        # Skip lines that start
        if line.startswith("##"):
            continue
        fields = line.strip().split("\t")
        if line.startswith("#CHROM"):
            info_fields = fields[7].split(":")
            if args.all:
                header.extend(info_fields)
            else:
                for info in args.info:
                    if info in info_fields:
                        header.append(info)
            tsv_writer.writerow(header)
        else:
            if args.all:
                for i,info in enumerate(info_fields):
                    fields.append(fields[7].split(":")[i])
            else:
                for info in args.info:
                    if info in info_fields:
                        fields.append(fields[7].split(":")[info_fields.index(info)])
            tsv_writer.writerow(fields)

# close the output file
tsv_file.close()