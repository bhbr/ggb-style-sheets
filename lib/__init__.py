import json
import xml.etree.cElementTree as ET
import sys
sys.setrecursionlimit(100)

# Python object that is described by a JSON file
class JSONObject:

	def __init__(self, filename='', attr_dict=None):
		super(JSONObject, self).__init__()
		self.attr_dict = attr_dict or None
		if filename != '':
			self.load_json(filename)
		self.load_dict(attr_dict)

	@staticmethod
	def convert_to_object(v):
		if type(v) in [str, int, float, bool] or v is None:
			return v
		elif type(v) == dict:
			return JSONObject(attr_dict=v)
		elif type(v) == list:
			return [JSONObject.convert_to_object(w) for w in v]
		else:
			return None

	def load_dict(self, attr_dict):
		if attr_dict is None:
			return
		for (key, value) in attr_dict.items():
			self.__dict__[key] = JSONObject.convert_to_object(value)

	def load_json(self, filename):
		with open(filename, 'r') as file:
			attr_dict = json.load(file)
		self.load_dict(attr_dict)

	def save(self, filename):
		with open(filename, 'w') as f:
			f.write(repr(self))

	def __repr__(self):
		return JSONObject.indented_repr(self)

	@staticmethod
	def indented_repr(v, indent=0):

		def static_short_repr(v):
			if type(v) == str:
				return repr(v).replace("'", '"')
			elif type(v) == list:
				return '[' + ', '.join([static_short_repr(w) for w in v]) + ']'
			elif type(v) == bool:
				if v:
					return 'true'
				else:
					return 'false'
			else:
				return '"' + repr(v) + '"'


		def static_long_repr(v, indent=0):

			def long_repr_of_dict(d):
				string = '{\n'
				for key, value in d.items():
					prefix = '    ' * (indent + 1) + '"' + key + '" : '
					string += prefix + JSONObject.indented_repr(value, indent=indent + 1) + ',\n'
				# remove trailing comma
				string = string[:-2] + '\n'
				string += '    ' * indent + '}'
				return string

			def long_repr_of_list(l):
				string = '[\n'
				for w in v:
					string += '    ' * (indent + 1) + JSONObject.indented_repr(w, indent=indent + 1) + ',\n'
				# remove trailing comma
				string = string[:-2] + '\n'
				string += '    ' * indent + ']'
				return string

			if type(v) == dict:
				return long_repr_of_dict(v)
			if isinstance(v, JSONObject):
				return long_repr_of_dict(v.__dict__)
			elif type(v) == list:
				return long_repr_of_list(v)
			else:
				return repr(v)

		if type(v) is not dict and not isinstance(v, JSONObject):
			short_repr = static_short_repr(v)
			if len(short_repr) <= 80:
				return short_repr
		else:
			return static_long_repr(v, indent=indent)











# Python object that is described by an XML tag
class XMLObject:

	def __init__(self, *args, filename='', node=None, tag='', xml_attrs=None, content=None, children=None, **kwargs):
		super(XMLObject, self).__init__(*args)
		self.xml_attrs = xml_attrs or {}
		self.children = children or []
		self.content = content
		if filename != '':
			self.load_xml(filename)
		elif node is not None:
			self.tag = node.tag
			self.load_dict(node.attrib, **kwargs)
			self.content = XMLObject.parse_string(node.text)
			self.children = [XMLObject(node=child) for child in node]
		else:
			if tag == '':
				tag = type(self).__name__
				tag = tag[0].lower() + tag[1:]
				# TODO: strip colons in XML tags
			self.tag = tag
			self.load_dict(self.xml_attrs, **kwargs)
			self.content = content

	def load_dict(self, xml_attrs, **kwargs):
		xml_attrs = xml_attrs or {}
		self.__dict__.update({key: XMLObject.parse_string(str(value)) for key, value in xml_attrs.items()})
		self.__dict__.update(kwargs)
		self.register_xml_attrs(*(tuple(xml_attrs.keys()) + tuple(kwargs.keys())))

	def load_xml(self, filename):
		et = ET.parse(filename)
		root = et.getroot()
		parsed_object = XMLObject(node=root)
		self.tag = parsed_object.tag
		self.load_dict(parsed_object.xml_attrs)
		self.content = None
		self.children = parsed_object.children

	def add_child(self, new_child):
		self.children.append(new_child)
		
	@staticmethod
	def parse_string(s):
		try:
			x = float(s)
			if int(x) == x:
				return int(x)
			else:
				return x
		except:
			if s == 'true' or s == 'True':
				return True
			elif s == 'false' or s == 'False':
				return False
			elif type(s) == str:
				return s.strip()
			else:
				return s

	def save(self, filename):
		with open(filename, 'w') as f:
			f.write(self.xml_repr())

	def __iter__(self):
		return iter(self.children)

	def __len__(self):
		return len(self.children)

	def __getitem__(self, i):
		return self.children[i]

	def __setitem__(self, i, child):
		self.children[i] = child

	def __missing__(self, i):
		self.children.__missing__(i)

	def __delitem__(self, i):
		del self.children[i]

	def __reversed__(self, i):
		return reversed(self.children)

	def __contains__(self, child):
		return (child in self.children)

	def xml_repr(self):
		if self.__class__.__name__ == 'GeoGebra':
			prefix = '<?xml version="1.0" encoding="utf-8"?>\n'
		else:
			prefix = ''
		return prefix + self.indented_xml_repr()

	def indented_xml_repr(self, indent=0):
		if len(self.children) == 0 and self.content is None:
			string = indent * '    ' + '<{}{}/>\n'.format(self.tag, self.attr_repr())
		else:
			string = indent * '    ' + '<{}{}>'.format(self.tag, self.attr_repr())
			if len(self.children) == 0:
				string += str(self.content) + '</{}>\n'.format(self.tag)
				return string
			string += '\n'
			if self.content is not None and self.content != '':
				string += indent * '    ' + repr(self.content) + '\n'
			for child in self:
				string += child.indented_xml_repr(indent=indent + 1)
			string += indent * '    ' + '</{}>\n'.format(self.tag)
		return string
		
	@staticmethod
	def attr_repr_of(xml_attrs):
		if len(xml_attrs) == 0:
			return ''
		else:
			string = ''
			for (key, value) in xml_attrs.items():
				if value is None:
					continue
				elif type(value) == str:
					value_repr = value
				elif type(value) == bool:
					value_repr = str(value).lower()
				else:
					value_repr = repr(value)
				string += ' {}="{}"'.format(key.replace('_', ':'), value_repr)
			return string

	def attr_repr(self):
		return self.__class__.attr_repr_of(self.xml_attrs)

	def register_xml_attrs(self, *attrs):
		for attr in attrs:
			self.xml_attrs[attr] = self.__dict__[attr]

	def update_xml_attrs(self, *attrs):
		self.register_xml_attrs(*attrs)

	def __str__(self):
		return self.__class__.__name__





class JXObject(XMLObject, JSONObject):
	pass


# Subclass XMLObject to represent a specific tag
# NB: child_classes refers to nodes, not further subclasses
def create_xml_class(name, superclass=XMLObject, tag=None, attrs=None, child_classes=None):
	attrs = attrs or {}
	child_classes = child_classes or {}
	def camel_case(string):
		return string[0].lower() + string[1:]
	if tag is None:
		if superclass == XMLObject:
			tag = camel_case(name)
		else:
			tag = camel_case(superclass.__name__)
	A = type(name, (superclass,), {'children': [], 'content': None, 'tag': tag})
	class B(A):
		def __init__(self, *args, node=None, additional_child_classes=None, **kwargs):

			super().__init__(*args, node=node, **kwargs)
			additional_child_classes = additional_child_classes or {}
			self.__dict__['xml_attrs'] = self.__dict__['xml_attrs'] or {}
			if attrs is not None:
				for key, value in attrs.items():
					if key not in self.__dict__['xml_attrs'].keys():
						self.__dict__['xml_attrs'][key] = value
			self.__dict__['children'] = self.__dict__['children'] or []
			if 'child_classes' not in self.__dict__.keys():
				self.__dict__['child_classes'] = {}
			self.__dict__['child_classes'].update(dict(child_classes, **additional_child_classes))
			for (child_name, child_class) in self.__dict__['child_classes'].items():
				if child_class in [c.__class__ for c in self.__dict__['children']]:
					child = [c for c in self.__dict__['children'] if c.__class__ == child_class][0]
				else:
					child = child_class.__new__(child_class)
					child.__init__()
					self.__dict__['children'].append(child)

			if node is not None:
				self.load_dict(node.attrib)
			if 'xml_attrs' in kwargs.keys():
				del kwargs['xml_attrs'] # might be part of kwargs
			self.xml_attrs.update(kwargs)
			self.tag = tag
			
		def __getattribute__(self, name):
			if name.startswith('__'):
				return A.__getattribute__(self, name)
			elif name == 'xml_attrs':
				try:
					return self.__dict__['xml_attrs']
				except KeyError:
					return {}
			elif name in self.xml_attrs.keys():
				return self.xml_attrs[name]
			elif 'child_classes' in self.__dict__.keys() and name in self.__dict__['child_classes'].keys():
				child_class = self.child_classes[name]
				children_of_that_class = [c for c in self.children if isinstance(c, child_class)]
				if len(children_of_that_class) == 0:
					return None
				elif len(children_of_that_class) == 1:
					return children_of_that_class[0]
				else:
					raise "More than one child of that class, must be unique"
			else:
				return A.__getattribute__(self, name)

		def __setattr__(self, name, value):
			if name.startswith('__'):
				A.__setattr__(self, name, value)
			elif name == 'xml_attrs':
				self.__dict__['xml_attrs'] = value
			elif name in self.xml_attrs.keys():
				self.xml_attrs[name] = value
			elif 'child_classes' in self.__dict__.keys() and name in self.__dict__['child_classes'].keys():
				child_class = self.child_classes[name]
				for (i, c) in enumerate(self.children):
					if c.__class__ == child_class:
						self.children[i] = value
						break
			else:
				A.__setattr__(self, name, value)
			
	B.__name__ = name

	return B


