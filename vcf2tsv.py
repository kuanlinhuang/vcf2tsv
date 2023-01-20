import csv
import argparse
import os
import gzip
import json

# function
def get_info_field_value(info_field, id):
    fields = info_field.split(";")
    for field in fields:
        # check if the ID is in this line's info field
        if id in field:
            split_field = field.split(id+"=")
            if len(split_field) > 1:
                return split_field[1]
    # put NA when the line don't have the info field names
    return "NA"

# create the parser
parser = argparse.ArgumentParser(description='Convert VCF file to TSV, JSON and retain the specified INFO fields')
# add the argument
parser.add_argument('--info', nargs='*', help='The INFO fields to be retained')
parser.add_argument('--all', action='store_true', help='Retain all the INFO fields')
parser.add_argument('--gz', action='store_true', help='Output the file as .tsv.gz')
parser.add_argument('--json', action='store_true', help='Output the file as json')
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

# Open the output
    file_name, file_extension = os.path.splitext(file_name)

# Open the output file
if args.json:
    json_file_name = file_name + '.json'
    try:
        output_file = open(json_file_name, 'w')
    except OSError as e:
        raise ValueError("Error creating output file. Please check the output directory and its permissions") from e
    json_data = []
else:
    if args.gz:
        try:
            output_file = gzip.open(file_name + '.tsv.gz', "wt")
        except OSError as e:
            raise ValueError("Error creating output file. Please check the output directory and its permissions") from e
    else:
        try:
            output_file = open(file_name + '.tsv', "w")
        except OSError as e:
            raise ValueError("Error creating output file. Please check the output directory and its permissions") from e
    # Create a CSV writer
    tsv_writer = csv.writer(output_file, delimiter='\t')
    
header = ["CHROM","POS","ID","REF","ALT","QUAL","FILTER","INFO"]
if args.info or args.all:
    info_field_names = []
    insert_position = 8 # default insert position for info field items: after the entire info field
    for line in lines:
        # Get all the info field names
        if line.startswith("##INFO"):
            info_name = line.strip().split("<ID=")[1].split(",")[0]
            info_field_names.append(info_name)
        # Skip lines that start with '##'
        if line.startswith("##"):
            continue
        
        fields = line.strip().split("\t")
        # Header line
        if line.startswith("#CHROM"):
            info_fields = fields[7]
            if args.all:
                header.extend(info_field_names)
            else:
                for info in args.info:
                    if info in info_field_names:
                        header.append(info)
            additional_fields = fields[8:]
            header.extend(additional_fields)
            
            if args.json:
                json_data.append(header)
            else:
                tsv_writer.writerow(header)
                
        # All other lines in the vcf
        else:
            info_fields = fields[7]
            if args.all:
                for i,info in enumerate(info_field_names):
                    info_field_value = get_info_field_value(info_fields, info)
                    fields.insert(insert_position,info_field_value)
                    insert_position = insert_position + 1
                    
            else:
                for info in args.info:
                    if info in info_field_names:
                        fields.insert(insert_position,info_field_value)
                        
            if args.json:
                json_data.append(dict(zip(header, fields)))
            else:
                tsv_writer.writerow(fields)
if args.json:
    json.dump(json_data, output_file, indent=4)
    output_file.close()
else:
    output_file.close()