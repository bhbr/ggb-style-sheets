import xml.etree.cElementTree as ET
import os, sys, shutil
from zipfile import ZipFile
from collections import OrderedDict
from functools import cmp_to_key


# The GGB class extractor parses a GGB file (as XML) and generates
# Python code for declaring appropriate classes that are internal
# native representations of the XML tags. These classes may serve
# as an API-of-sorts for GeoGebra, beyond mere layouting.
# Currently, only layouting is performed at this level (in the GeoGebra
# class, see curated_ggb_classes.py) and the Python objects then
# saved to XML again.

def attr_dict_from_xml_element(el):
	return {el.tag: el.attrib}

def attr_dict_from_node(node):
	found_tag_attribs = attr_dict_from_xml_element(node)
	for child in node:
		for tag, attribs in attr_dict_from_node(child).items():
			if tag in found_tag_attribs.keys():
				for (attr, value) in attribs.items():
					if attr not in found_tag_attribs[tag]:
						found_tag_attribs[tag][attr] = value
			else:
				found_tag_attribs[tag] = attribs
	return found_tag_attribs

def child_tags_from_xml_element(el):
	child_tags = [c.tag for c in el]
	unique_child_tags = [t for t in child_tags if child_tags.count(t) == 1]
	return {el.tag: unique_child_tags}

def child_tags_from_node(node):
	found_child_tags = child_tags_from_xml_element(node)
	for child in node:
		for tag, child_tags in child_tags_from_node(child).items():
			if tag in found_child_tags.keys():
				for child_tag in child_tags:
					if child_tag not in found_child_tags[tag]:
						found_child_tags[tag].append(child_tag)
			else:
				found_child_tags[tag] = child_tags
	return found_child_tags




def extract_classes_from_ggb_file(input_name):

	tag_attr_dict = {}
	tag_children_dict = {}

	os.rename(input_name + '.ggb', input_name + '.zip')
	ZipFile(input_name + '.zip', 'r').extractall(input_name)
	os.rename(input_name + '.zip', input_name + '.ggb')

	with open(input_name + '/geogebra.xml', 'r') as file:
		full_text = file.read()
	full_text = full_text.replace('&#x8;', r'\b')
	with open(input_name + '/geogebra.xml', 'w') as file:
		file.write(full_text)

	et = ET.parse(input_name + '/geogebra.xml')
	root = et.getroot()

	tag_attribs = attr_dict_from_node(root)
	tag_children = child_tags_from_node(root)

	for tag, attribs in tag_attribs.items():
		if tag == 'element':
			continue
		if tag not in tag_attr_dict.keys():
			tag_attr_dict[tag] = attribs
		else:
			tag_attr_dict[tag].update(attribs)

	for tag, child_tags in tag_children.items():
		if tag not in tag_children_dict.keys():
			tag_children_dict[tag] = child_tags
		else:
			tag_children_dict[tag] = list(set(tag_children_dict[tag] + child_tags))

	shutil.rmtree(input_name)



	code = []
	element_code = []

	def get_child_tags(tag):
		try:
			return tag_children_dict[tag2]
		except:
			return []

	# comparator to sort the classes according to dependencies
	def compare(tag_attr_pair1, tag_attr_pair2):
		tag1, attr1 = tag_attr_pair1
		tag2, attr2 = tag_attr_pair2
		child_tags1 = get_child_tags(tag1)
		child_tags2 = get_child_tags(tag2)
		if tag1 in child_tags2:
			return 1
		elif tag2 in child_tags1:
			return -1
		else:
			return 0

	tag_attrs = tag_attr_dict.items()
	sorted_tag_attrs = sorted(tag_attrs, key=cmp_to_key(compare))
	tag_attr_dict = OrderedDict(sorted_tag_attrs)


	for (tag, attribs) in tag_attr_dict.items():

		if tag == 'geogebra':
			continue

		child_tags = get_child_tags(tag)
		attr_dict = attribs

		# replacements for code generation
		for (key, value) in attr_dict.items():
			value = value.replace('\n', '&#xa;')
			attr_dict[key] = '"' + value + '"'

		attr_dict_string = '{\n\t\t' + ',\n\t\t'.join(["'%s': %s" % item for item in attr_dict.items()]) + '\n\t}'
		child_tag_dict = {child_tag : child_tag.capitalize() for child_tag in child_tags}
		child_tag_dict_string = '{\n\t\t' + ',\n\t\t'.join(["'%s': %s" % item for item in child_tag_dict.items()]) + '\n\t}'

		tag_cap = tag.capitalize()
		if len(attribs) != 0:
			if len(child_tags) > 0:
				code.append("{} = create_ggb_class('{}',\n\ttag='{}',\n\tattrs={},\n\tchildren={}\n)\n".format(tag_cap, tag_cap, tag, attr_dict_string, child_tag_dict_string))
			else:
				code.append("{} = create_ggb_class('{}',\n\ttag='{}',\n\tattrs={})\n".format(tag_cap, tag_cap, tag, attr_dict_string))
		else:
			if len(child_tags) > 0:
				code.append("{} = create_ggb_class('{}',\n\ttag='{}',\n\tchildren={}\n)\n".format(tag_cap, tag, tag_cap, child_tag_dict_string))
			else:
				code.append("{} = create_ggb_class('{}',\n\ttag='{}')\n".format(tag_cap, tag_cap, tag, attr_dict_string))

	return code







