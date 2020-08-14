#!/usr/bin/python3
from lib.ggb_class_extractor import extract_classes_from_ggb_file
import xml.etree.cElementTree as ET
from lib.curated_ggb_classes import *
from lib.styling_logic import GeoGebra
import os, sys, shutil
from zipfile import ZipFile
import argparse


# required arguments:
#   GGB file
#   layouting file (a JSON file, see sample_layout.json)
#
# optional flags:
# -x, --keep_xml: Keep the unzipped GGB file (which is in XML),
#                 before and after layouting, for inspection
# -e, --extract_classes: Reverse-engineer the GGB file to create
#                 native Python classes for all the elements.
#                 Otherwise, use a list of curated GGB classes
# -c, --keep_classes: Keep the generated Python code for the extracted classes

#sysarg parsing
try:
	parser = argparse.ArgumentParser()
	parser.add_argument(
	    "layout_file", help="path to layout file (JSON)"
	)
	parser.add_argument(
	    "ggb_file", help="path to GGB file"
	)
	optional_args = [
		('-x', '--keep_xml'),
		('-e', '--extract_classes'),
		('-c', '--keep_classes')
	]
	for short_arg, long_arg in optional_args:
		parser.add_argument(short_arg, long_arg, action="store_true")
	parser.add_argument("-o", "--output_name")
	args = parser.parse_args()
	input_name = '.'.join(args.ggb_file.split('.')[:-1]) # remove file ending
	output_name =  input_name + '_layouted'
	layout_file = args.layout_file
	keep_xml = args.keep_xml
	extract_classes = args.extract_classes
	keep_classes = args.keep_classes

except argparse.ArgumentError as err:
	print(str(err))
	sys.exit(2)

# GGB class extraction
if extract_classes:
	print("extracting GGB classes...")
	code = extract_classes_from_ggb_file(input_name)
	ggb_dir = os.path.dirname(input_name)
	if keep_classes:
		with open(ggb_dir + '/extracted_ggb_classes.py', 'w') as f:
			f.write('from lib.ggb_base_object import create_ggb_class\n')
			for line in sorted(code):
				f.write(line)
	else:
		try:
			os.remove(ggb_dir + '/extracted_ggb_classes.py')
		except:
			pass

	for line in code:
		exec(line)
# or use the curated ones
else:
	from lib.curated_ggb_classes import *

 # remove remnant outputs from previous run
if os.path.isdir(input_name):
	shutil.rmtree(input_name)
if os.path.isfile(output_name + '.ggb'):
	os.remove(output_name + '.ggb')
if os.path.isdir(output_name):
	shutil.rmtree(output_name)

# unzip GGB file into a folder and make a copy
os.rename(input_name + '.ggb', input_name + '.zip')
ZipFile(input_name + '.zip', 'r').extractall(input_name)
os.rename(input_name + '.zip', input_name + '.ggb')
os.mkdir(output_name)
for file in os.listdir(input_name):
	shutil.copy(input_name + '/' + file, output_name)

# read XML
et = ET.parse(input_name + '/geogebra.xml')
root = et.getroot()
ggb_root = GeoGebra(node=root)

# apply the layout and save
ggb_root.apply_layout(filename=layout_file)
ggb_root.save(output_name + '/geogebra.xml')
shutil.make_archive(output_name, 'zip', output_name)
os.rename(output_name + '.zip', output_name + '.ggb')

if not keep_xml:
	shutil.rmtree(input_name)
	shutil.rmtree(output_name)






