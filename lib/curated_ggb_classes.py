from lib import *
from math import pi

ggb_classes = {}
element_classes = {}

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
			ggb_class = element_classes[node.attrib['type']]
			#print('found element of type', node.attrib['type'])
		except KeyError:
			#print("let's try the tag instead:", node.tag)
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

	@staticmethod
	def attr_repr_of(xml_attrs):
		for key, value in xml_attrs.items():
			if type(value) == str:
				xml_attrs[key] = GGBObject.html_string_repr(value)
		return XMLObject.attr_repr_of(xml_attrs)


	@staticmethod
	def html_string_repr(string):
		replacement_dict = {
			"'" : "&apos;",
			"\n": "&#xa;",
			"<": "&lt;",
			">": "&gt;",
			'"': "&quot;"
		}
		for key, value in replacement_dict.items():
			string = string.replace(key, value)
		return string


def create_ggb_class(name,
	tag=None,
	superclass=GGBObject,
	attrs=None,
	child_classes=None
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
		child_classes=child_classes
	)

	ggb_classes[tag] = ggb_class
	return ggb_class


AbsoluteScreenLocation = create_ggb_class('AbsoluteScreenLocation',
	attrs={
		'x': 0,
		'y': 0
	}
)

AlgebraStyle = create_ggb_class('AlgebraStyle',
	attrs={
		'val': 3,
		'spreadsheet': 0
	}
)

AngleStyle = create_ggb_class('AngleStyle',
	attrs={
		'val': 0
	}
)

AngleUnit = create_ggb_class('AngleUnit',
	attrs={
		'val': 'degree'
	}
)

Animation = create_ggb_class('Animation',
	attrs={
		'speed': 1,
		'type': 1,
		'playing': False,
		'step': None
	}
)

ArcSize = create_ggb_class('ArcSize',
	tag='arcSize',
	attrs={
		'val': 40
	}
)

Auxiliary = create_ggb_class('Auxiliary',
	attrs={
		'val': False
	}
)


Axis = create_ggb_class('Axis',
	attrs={
		'id': 0,
		'show': True,
		'label': '',
		'unitLabel': '1',
		'tickStyle': 1,
		'showNumbers': True,
		'tickDistance': None,
		'tickExpression': None,
		'positiveAxis': None,
		'selectionAllowed': None
	}
)

class Color(create_ggb_class('Color',
	attrs={
		'r': 0,
		'g': 0,
		'b': 0
	})
):
	def __init__(self, *args, **kwargs):
		super().__init__(**kwargs)
		if len(args) == 3:
			rgb_list = args
		elif len(args) == 1 and type(args[0]) == list:
			rgb_list = args[0]
			assert len(rgb_list) == 3, 'list of color values must contain 3 values'
		elif len(args) == 1 and isinstance(args[0], Color):
			color = args[0]
			rgb_list = [color.r, color.g, color.b]
		else:
			rgb_list = 3 * [0]
		self.load_dict(dict(zip(['r', 'g', 'b'], rgb_list)))

	def __repr__(self):
		return self.__class__.__name__ + 3 * ' %i' % (self.r, self.g, self.b)

AxesColor = create_ggb_class('AxesColor',
	superclass=Color
)

BGColor = create_ggb_class('BGColor',
	superclass=Color,
	tag='bgColor'
)
GridColor = create_ggb_class('GridColor',
	superclass=Color
)

ObjColor = create_ggb_class('ObjColor',
	superclass=Color,
	attrs={
		'alpha': None
	}
)

Caption = create_ggb_class('Caption',
	attrs={
		'val': '%n'
	}
)

Checkbox = create_ggb_class('Checkbox',
	attrs={
		'fixed': True
	}
)

Clipping = create_ggb_class('Clipping',
	attrs={
		'use': True,
		'show': False,
		'size': 1
	}
)

Coefficients = create_ggb_class('Coefficients',
	attrs={
		'rep': 'array',
		'data': '[]'
	}
)

Collapsed = create_ggb_class('Collapsed',
	attrs={
		'val': 0
	}
)

Condition = create_ggb_class('Condition',
	attrs={
		'showObject': 'true'
	}
)

Construction = create_ggb_class('Construction',
	attrs={
		'title': '',
		'author': '',
		'date': ''
	}
)

Continuous = create_ggb_class('Continuous',
	attrs={
		'val': False
	}
)

Coords = create_ggb_class('Coords',
	attrs={
		'x': 0,
		'y': 0,
		'z': 0,
		'w': None,
		'ox': None,
		'oy': None,
		'oz': None,
		'ow': None,
		'vx': None,
		'vy': None,
		'vz': None,
		'vw': None
	}
)

CoordStyle = create_ggb_class('CoordStyle',
	attrs={
		'style': None,
		'val': None
	}
)

CoordSystem = create_ggb_class('CoordSystem',
	attrs={
		'xZero': 640,
		'yZero': 380,
		'scale': 50,
		'yscale': None,
		'zZero': None,
		'xAngle': None,
		'zAngle': None
	}
)

CurveParam = create_ggb_class('CurveParam',
	attrs={
		't': 0
	}
)

Decimals = create_ggb_class('Decimals',
	attrs={
		'val': 2
	}
)


Decoration = create_ggb_class('Decoration',
	attrs={
		'type': 4
	})

DockBar = create_ggb_class('DockBar',
	attrs={
		'show': False,
		'east': False
	}
)

EigenVectors = create_ggb_class('EigenVectors',
	tag='eigenvectors',
	attrs={
		'x0': 1,
		'y0': 0,
		'z0': 0,
		'x1': 0,
		'y1': 1,
		'z1': 0,
		'x2': 0,
		'y2': 0,
		'z2': 1
	}
)

Entry = create_ggb_class('Entry',
	attrs={
		'key': '',
		'val': ''
	}
)

CASMap = create_ggb_class('CASMap',
	child_classes={
		'entry': Entry
	}
)

EqnStyle = create_ggb_class('EqnStyle',
	attrs={
		'style': 'user',
		'parameter': 't'
	}
)

EVSettings = create_ggb_class('EVSettings',
	tag='evSettings',
	attrs={
		'axes': True,
		'grid': False,
		'gridIsBold': False,
		'pointCapturing': 3,
		'rightAngleStyle': 1,
		'checkboxSize': 26,
		'gridType': 3
	}
)

Expression = create_ggb_class('Expression',
	attrs={
		'label': '',
		'exp': '',
		'type': None,
		'value': None,
		'eval': None,
		'evalCmd': None,
		'native': None
	}
)

Fading = create_ggb_class('Fading',
	attrs={
		'val': 0.1
	}
)

Fixed = create_ggb_class('Fixed',
	attrs={
		'val': True
	}
)

Font = create_ggb_class('Font',
	attrs={
		'size': 16,
		'serif': None,
		'sizeM': None,
		'style': None
	}
)

GGBScript = create_ggb_class('GGBScript',
	tag='ggbscript',
	attrs={
		'val': None,
		'onUpdate': None
	}
)

Grid = create_ggb_class('Grid',
	attrs={
		'distX': 2,
		'distY': 2,
		'distTheta': pi/6
	}
)

Input = create_ggb_class('Input',
	attrs={
		'a0': None,
		'show': None,
		'cmd': None,
		'top': None
	}
)

InputCell = create_ggb_class('InputCell',
	child_classes={
		'expression': Expression
	}
)

IsLatex = create_ggb_class('IsLatex',
	tag='isLaTeX',
	attrs={
		'val': False
	}
)

JavaScript = create_ggb_class('JavaScript',
	tag='javascript',
	attrs={
		'val': None,
		'onUpdate': None
	}
)

KeepTypeOnTransform = create_ggb_class('KeepTypeOnTransform',
	attrs={
		'val': True
	}
)

LabelingStyle = create_ggb_class('LabelingStyle',
	attrs={
		'val': 0
	}
)

LabelMode = create_ggb_class('LabelMode',
	attrs={
		'val': 0
	}
)

LabelOffset = create_ggb_class('LabelOffset',
	attrs={
		'x': -15,
		'y': 15
	}
)

LabelStyle = create_ggb_class('LabelStyle',
	attrs={
		'axes': 1,
		'serif': False
	}
)

Layer = create_ggb_class('Layer',
	attrs={
		'val': 0
	}
)

Length = create_ggb_class('Length',
	attrs={
		'val': 0
	}
)

EVLineStyle = create_ggb_class('EVLineStyle',
	tag='lineStyle',
	attrs={
		'axes': 1,
		'grid': 0,
	}
)

ElementLineStyle = create_ggb_class('ElementLineStyle',
	tag='lineStyle',
	attrs={
		'thickness': None,
		'type': None,
		'typeHidden': None,
		'opacity': None
	}
)

class LineStyle(ElementLineStyle, EVLineStyle):
	def __init__(self, node=None, **kwargs):
		if node is None:
			super(LineStyle, self).__init__(node=node, **kwargs)
		elif 'thickness' in node.attrib.keys() or 'type' in node.attrib.keys() or 'typeHidden' in node.attrib.keys():
			ElementLineStyle.__init__(self, node=node, **kwargs)
		elif 'axes' in node.attrib.keys() or 'grid' in node.attrib.keys():
			EVLineStyle.__init__(self, node=node, **kwargs)
		else:
			super(LineStyle, self).__init__(node=node, **kwargs)

ggb_classes['linestyle'] = LineStyle

LinkedGeo = create_ggb_class('LinkedGeo',
	attrs={
		'exp': ''
	}
)

Matrix = create_ggb_class('Matrix',
	attrs={
		'A0': 1,
		'A1': 1,
		'A2': 0,
		'A3': 0,
		'A4': 0,
		'A5': 0
	}
)

Mode = create_ggb_class('Mode',
	attrs={
		'val': 1
	}
)

AlgebraView = create_ggb_class('AlgebraView',
	child_classes={
		'mode': Mode,
		'collapsed': Collapsed
	}
)

OutlyingIntersections = create_ggb_class('OutlyingIntersections',
	attrs={
		'val': False
	}
)

Output = create_ggb_class('Output',
	attrs={
		'a0': ''
	}
)

Command = create_ggb_class('Command',
	attrs={
		'name': '',
		'var': None
	},
	child_classes={
		'input': Input,
		'output': Output
	}
)

OutputCell = create_ggb_class('OutputCell',
	child_classes={
		'expression': Expression
	}
)

CellPair = create_ggb_class('CellPair',
	child_classes={
		'inputCell': InputCell,
		'outputCell': OutputCell
	}
)

CASCell = create_ggb_class('CASCell',
	attrs={
		'casLabel': ''
	},
	child_classes={
		'cellPair': CellPair
	}
)

Pane = create_ggb_class('Pane',
	attrs={
		'location': '',
		'divider': 0.5,
		'orientation': 0
	}
)

Panes = create_ggb_class('Panes')

Perspectives = create_ggb_class('Perspectives')

Plate = create_ggb_class('Plate',
	attrs={
		'show': False
	}
)

PointSize = create_ggb_class('PointSize',
	attrs={
		'val': 5
	}
)

PointStyle = create_ggb_class('PointStyle',
	attrs={
		'val': 0
	}
)

PrefCellSize = create_ggb_class('PrefCellSize',
	attrs={
		'width': 70,
		'height': 35
	}
)

Projection = create_ggb_class('Projection',
	attrs={
		'type': 0
	}
)

class EuclidianView3D(create_ggb_class('EuclidianView3D',
	child_classes={
		'plate': Plate,
		'clipping': Clipping,
		'projection': Projection,
		'settings': EVSettings,
		'bgColor': BGColor,
		'coordSystem': CoordSystem
	}
)):
	
	@property
	def axes(self):
		return [c for c in self in isinstance(c, Axis)]

	@property
	def x_axis(self):
		return [a for a in self.axes if a.id == 0][0]
		
	@property
	def y_axis(self):
		return [a for a in self.axes if a.id == 1][0]

	@property
	def z_axis(self):
		return [a for a in self.axes if a.id == 2][0]




Scripting = create_ggb_class('Scripting',
	attrs={
		'blocked': False,
		'disabled': False
	}
)

Selection = create_ggb_class('Selection',
	attrs={
		'hScroll': 0,
		'vScroll': 0,
		'column': -1,
		'row': -1
	}
)

SelectionAllowed = create_ggb_class('SelectionAllowed',
	attrs={
		'val': False
	}
)

Show = create_ggb_class('Show',
	attrs={
		'object': False,
		'label': True,
		'ev': 4,
		'axes': None,
		'grid': None
	}
)

Element = create_ggb_class('Element',
	attrs={
		'label': '',
		'type': 'element'
	},
	child_classes={
		'color': ObjColor,
		'show': Show,
		'layer': Layer,
		'labelMode': LabelMode,
		'animation': Animation,
		'lineStyle': ElementLineStyle
	}
)

Size = create_ggb_class('Size',
	attrs={
		'width': 1310,
		'height': 513
	}
)

Slider = create_ggb_class('Slider',
	attrs={
		'min': 0,
		'max': 100,
		'absoluteScreenLocation': True,
		'width': 200,
		'fixed': False,
		'horizontal': True,
		'showAlgebra': True,
		'x': None,
		'y': None
	}
)

SpreadsheetView = create_ggb_class('SpreadsheetView',
	child_classes={
		'size': Size,
		'prefCellSize': PrefCellSize,
		'selection': Selection
	}
)

StartPoint = create_ggb_class('StartPoint',
	attrs={
		'exp': '',
		'x': None,
		'y': None,
		'z': None,
		'w': None
	}
)

Symbolic = create_ggb_class('Symbolic',
	attrs={
		'val': True
	}
)

TableView = create_ggb_class('TableView',
	tag='tableview',
	attrs={
		'min': -2,
		'max': 2,
		'step': 1
	}
)

ToolBar = create_ggb_class('ToolBar',
	tag='toolbar',
	attrs={
		'show': True,
		'items': '0 73 62 | 1 501 67 , 5 19 , 72 75 76 | 2 15 45 , 18 65 , 7 37 | 4 3 8 9 , 13 44 , 58 , 47 | 16 51 64 , 70 | 10 34 53 11 , 24  20 22 , 21 23 | 55 56 57 , 12 | 36 46 , 38 49  50 , 71  14  68 | 30 29 54 32 31 33 | 25 17 26 60 52 61 | 40 41 42 , 27 28 35 , 6',
		'position': 1,
		'help': False
	}
)

Trace = create_ggb_class('Trace',
	attrs={
		'val': True
	}
)

UsePathAndRegionParameters = create_ggb_class('UsePathAndRegionParameters',
	attrs={
		'val': True
	}
)

UserInput = create_ggb_class('UserInput',
	attrs={
		'show': False
	}
)

Uses3D = create_ggb_class('Uses3D',
	attrs={
		'val': True
	}
)

Kernel = create_ggb_class('Kernel',
	child_classes={
		'uses3D': Uses3D,
		'usePathAndRegionParameters': UsePathAndRegionParameters,
		'coordStyle': CoordStyle,
		'angleUnit': AngleUnit,
		'continuous': Continuous,
		'algebraStyle': AlgebraStyle,
		'decimals': Decimals
	}
)

Value = create_ggb_class('Value',
	attrs={
		'val': 0
	}
)

VectorStartPoint = create_ggb_class('VectorStartPoint',
	tag='startPoint',
	attrs={
		'exp': '',
		'x': None,
		'y': None,
		'z': None,
		'w': None
	}
)

View = create_ggb_class('View',
	attrs={
		'id': 1,
		'visible': False,
		'inframe': False,
		'stylebar': False,
		'location': '1,1,1',
		'size': 500,
		'window': '100,100,600,400',
		'toolbar': None
	}
)

ViewNumber = create_ggb_class('ViewNumber',
	attrs={
		'viewNo': 1
	}
)

class EuclidianView(create_ggb_class('EuclidianView',
	child_classes={
		'size': Size,
		'settings': EVSettings,
		'axesColor': AxesColor,
		'lineStyle': LineStyle,
		'gridColor': GridColor,
		'grid': Grid,
		'labelStyle': LabelStyle,
		'bgColor': BGColor,
		'viewNumber': ViewNumber,
		'coordSystem': CoordSystem
	}
)):

	@property
	def axes(self):
		return [c for c in self in isinstance(c, Axis)]

	@property
	def x_axis(self):
		return [a for a in self.axes if a.id == 0][0]

	@property
	def y_axis(self):
		return [a for a in self.axes if a.id == 1][0]


Views = create_ggb_class('Views')

Perspective = create_ggb_class('Perspective',
	attrs={
		'id': 'tmp'
	},
	child_classes={
		'views': Views,
		'toolBar': ToolBar,
		'input': Input,
		'dockBar': DockBar,
		'panes': Panes
	}
)

Window = create_ggb_class('Window',
	attrs={
		'width': 1310,
		'height': 1103
	}
)

GUI = create_ggb_class('GUI',
	tag='gui',
	child_classes={
		'labelingStyle': LabelingStyle,
		'window': Window,
		'font': Font,
		'perspectives': Perspectives
	}
)

# # # # # # # # # # # #
#  ELEMENT SUBCLASSES #
# # # # # # # # # # # #


def create_element_class(name, type=None, attrs=None, child_classes=None):
	global element_classes, ggb_classes
	attrs = attrs or {}
	type = type or name.lower()
	attrs['type'] = type
	child_classes = child_classes or {}

	A = create_ggb_class(
		name,
		tag='element',
		superclass=Element,
		attrs=attrs,
		child_classes=child_classes
	)

	A.__name__ = name
	element_classes[type] = A
	ggb_classes[type] = A
	return A




Boolean = create_element_class('Boolean',
	child_classes={
		'value': Value,
		'checkbox': Checkbox

		}
)

FunctionNVar = create_element_class('FunctionNVar',
	type='functionNVar'
)

List = create_element_class('List',
	child_classes={
		'pointSize': PointSize,
		'pointStyle': PointStyle
	}
)

Numeric = create_element_class('Numeric',
	child_classes={
		'value': Value,
		'symbolic': Symbolic,
		'slider': Slider
	}
)

Point = create_element_class('Point',
	child_classes={
		'auxiliary': Auxiliary,
		'coords': Coords,
		'label_offset': LabelOffset,
		'size': PointSize,
		'style': PointStyle,
		'caption': Caption,
		'javascript': JavaScript
	}
)

Polygon = create_element_class('Polygon')

Segment = create_element_class('Segment',
	child_classes={
		'auxiliary': Auxiliary,
		'coords': Coords,
		'outlying_intersections': OutlyingIntersections,
		'keep_type_on_transform': KeepTypeOnTransform
	}
)

TextField = create_element_class('TextField',
	child_classes={
		'fixed': Fixed,
		'lined_geo': LinkedGeo
	}
)

Vector = create_element_class('Vector',
	child_classes={
		'start_point': VectorStartPoint
	}
)

Vector3D = create_element_class('Vector3D')


# # # # # # # # # # # #
# ROOT CLASS GEOGEBRA #
# # # # # # # # # # # #

class GeoGebra(create_ggb_class('GeoGebra',
	tag='geogebra',
	attrs={
		'app': 'classic',
		'platform': 'w',
		'format': '5.0',
		'version': '5.0.528.0',
		'id': '',
		'{http://www.w3.org/2001/XMLSchema-instance}noNamespaceSchemaLocation': 'http://www.geogebra.org/ggb.xsd'
	},
	child_classes={
		'algebraView': AlgebraView,
		'construction': Construction,
		'scripting': Scripting,
		'euclidianView3D': EuclidianView3D,
		'gui': GUI,
		'kernel': Kernel,
		'tableView': TableView,
		'spreadsheetView': SpreadsheetView
	}
)):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		if type(self.format) == int:
		# correct misparsed version number ('5.0' not 5)
			self.format = str(float(self.format))
		self.elements = [c for c in self.construction if c.tag == 'element']
		self.layout = JSONObject()
		self.colors = {}

	def attr_repr(self):
		attrs_with_ns = self.xml_attrs.copy()
		attrs_with_ns['xmlns:xsi'] = 'http://www.w3.org/2001/XMLSchema-instance'
		attrs_with_ns['xsi:noNamespaceSchemaLocation'] = attrs_with_ns['{http://www.w3.org/2001/XMLSchema-instance}noNamespaceSchemaLocation']
		del attrs_with_ns['{http://www.w3.org/2001/XMLSchema-instance}noNamespaceSchemaLocation']
		return GeoGebra.attr_repr_of(attrs_with_ns)

	@property
	def euclidianViews(self):
		return [c for c in self if c.__class__.__name__.startswith('EuclidianView')]

	def apply_layout(self, filename):
		self.layout = JSONObject(filename=filename)
		self.colors = self.layout.color_palette.__dict__
		self.set_bg_color(self.parse_color(self.layout.background_color))
		self.set_caption_style()
		self.set_hidden_line_style()
		self.set_axes_style()

	def parse_color(self, rgb_or_name):
		if type(rgb_or_name) == str:
			return Color(self.colors[rgb_or_name])
		else:
			return Color(rgb_or_name)

	def set_bg_color(self, views=None):
		views = views or self.euclidianViews # if no views specified, iterate over all EVs
		bg_color = BGColor(self.parse_color(self.layout.background_color))
		for child in views:
			child.bgColor = bg_color
		self.euclidianView3D.bgColor = bg_color

	def set_caption_style(self):
		use_tex = self.layout.default_caption_style.tex
		use_bold = self.layout.default_caption_style.bold
		for el in self.elements:
			try:
				caption = el.caption
			except AttributeError:
				caption = Caption(xml_attrs={'val': '%n'})
				el.caption = caption
			caption_text = GeoGebra.strip_tex(caption.val)
			if use_tex:
				if use_bold:
					caption_text = r'\boldsymbol{%s}' % caption_text
				caption_text = '$%s$' % caption_text
			el.caption.val = caption_text

	def set_hidden_line_style(self):
		style_string = self.layout.line_style.hidden_style
		if style_string == 'invisible':
			style_int = 0
		elif style_string == 'dotted':
			style_int = 1
		elif style_string == 'unchanged':
			style_int = 2
		else:
			style_int = 2
		# invisible, dotted or unchanged
		for el in self.construction:
			try:
				el.lineStyle.typeHidden = style_int
			except:
				continue

	def set_axes_style(self):
		# show toggle does not work properly bc of GeoGebra
		for ev in self.euclidianViews:
			ev.settings.axes = self.layout.axes.show
			if ev is not self.euclidianView3D:
				ev.axesColor = AxesColor(self.parse_color(self.layout.axes.color))
			axes = [c for c in ev if isinstance(c, Axis)]
			for axis in axes:
				axis.show = self.layout.axes.show
				if not self.layout.axes.show_ticks:
					axis.tickStyle = 0
				axis.showNumbers = self.layout.axes.show_numbers
				axis.positiveAxisOnly = self.layout.axes.positive_axis_only



	@staticmethod
	def strip_tex_cmd(string, tag):
		if tag not in string:
			return string
		start_index = string.find('\\' + tag + '{')
		index_behind_tag = start_index + len(tag) + 2
		string = string[index_behind_tag:]
		brace_count = 0
		close_brace_index = 0
		for (i, char) in enumerate(string):
			if char == '{':
				brace_count += 1
			elif char == '}':
				brace_count -= 1
			if brace_count == -1:
				close_brace_index = i
				break
		string = string[:close_brace_index] + string[close_brace_index + 1:]
		return GeoGebra.strip_tex_cmd(string, tag)

	@staticmethod
	def strip_tex(string):
		if string.startswith('$') and string.endswith('$'):
			string = string[1:-1]
			return GeoGebra.strip_tex_cmd(string, 'boldsymbol')
		else:
			return string
