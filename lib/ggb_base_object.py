from lib import *

ggb_classes = {}
element_classes = {}

# code common to all GGB objects (representing XML tags) at any level
class GGBObject(JXObject):

	def __init__(self, node=None, **kwargs):
		super(GGBObject, self).__init__(node=node, **kwargs)
		if node is not None:
			self.tag = node.tag
			self.load_dict(node.attrib, **kwargs)
			self.content = XMLObject.parse_string(node.text)
			self.children = [GGBObject.xml2ggb_object(child) for child in node]
		else:
			self.children = []


	@staticmethod
	def xml2ggb_object(node):
		try:
			ggb_class = element_classes[node.tag]
		except KeyError:
			try:
				ggb_class = ggb_classes[node.tag]
			except KeyError:
				print("Can't create GGBObject: unknown tag", node.tag)
				raise
		ggb_obj = ggb_class.__new__(ggb_class)
		ggb_obj.__init__(node=node)
		ggb_obj.load_dict(node.attrib) # __init__ does not load XML attrs for some reason
		return ggb_obj

	def __repr__(self):
		return self.__class__.__name__




# GGB-specific version of create_xml_class
# that offers to guess an appropriate class name from the tag,
# and keeps a global dict of tag vs. class name correspondences
# (bc of capitalization and namespace issues).
def create_ggb_class(name,
	tag=None,
	superclass=GGBObject,
	attrs=None,
	children=None
):
	global ggb_classes
	def camel_case(string):
		return string[0].lower() + string[1:]
	tag = tag or camel_case(name)

	ggb_class = create_xml_class(
		name,
		superclass=superclass,
		tag=tag,
		attrs=attrs,
		child_classes=children
	)
	ggb_classes[tag] = ggb_class
	return ggb_class
