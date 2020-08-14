# Extract classes from the XSD description of the GGB file format
# (instead of reverse-engineering from a GGB file as is being done currently)
# This is not yet working.

import xml.etree.cElementTree as ET
from lib import XMLObject

et = ET.parse('ggb.xsd')
root = et.getroot()

xs = '{http://www.w3.org/2001/XMLSchema}:'

def class_from_element(element):
	if element.tag != xs + 'element':
		print('Cannot create class from this tag (not an element)')
		return

	class A(XMLObject):
		pass

	A.__name__ = element.attribs['name']
	return A