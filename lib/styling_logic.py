from .curated_ggb_classes import *

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