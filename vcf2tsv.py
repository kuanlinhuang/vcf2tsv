import csv
import argparse
import os

# create the parser
parser = argparse.ArgumentParser(description='Convert VCF file to TSV and retain the specified INFO fields')
# add the argument
parser.add_argument('--info', nargs='*', help='The INFO fields to be retained')
parser.add_argument('--all', action='store_true', help='Retain all the INFO fields')
parser.add_argument('input_file', help='The input VCF file')
args = parser.parse_args()

# Open the input .vcf file
with open(args.input_file, "r") as vcf_file:
    # Read the file as a list of lines
    lines = vcf_file.readlines()

# get the file name without the extension
file_name, file_extension = os.path.splitext(args.input_file)
# Open the output .tsv file
with open(file_name + '.tsv', "w") as tsv_file:
    # Create a CSV writer
    tsv_writer = csv.writer(tsv_file, delimiter='\t')
    header = ["#CHROM","POS","ID","REF","ALT","QUAL","FILTER","INFO"]
    if args.info or args.all:
        all_info_fields = set()
        for line in lines:
            # Skip lines that start with '##'
            if line.startswith("##"):
                continue
            fields = line.strip().split("\t")
            info_fields = fields[7].split(";")
            for field in info_fields:
                try:
                    key,value = field.split("=")
                    all_info_fields.add(key)
                except ValueError:
                    all_info_fields.add(field)
        if args.all:
            header.extend(all_info_fields)
        else:
            header.extend(args.info)
    tsv_writer.writerow(header)
    # Iterate over the lines in the input file
    for line in lines:
        # Skip lines that start with '##'
        if line.startswith("##"):
            continue

        # Split the line on tabs
        fields = line.strip().split("\t")
        if args.info or args.all:
            info_fields = fields[7].split(";")
            info_dict = {}
            for field in info_fields:
                try:
                    key,value = field.split("=")
                    info_dict[key] = value
                except ValueError:
                    info_dict[field] = None
            if args.all:
                for info in all_info_fields:
                    fields.append(info_dict.get(info))
            else:
                for info in args.info:
                    fields.append(info_dict.get(info))
        # Write the fields to the output file
        tsv_writer.writerow(fields)
