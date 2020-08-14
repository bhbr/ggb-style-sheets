# GGB Style Sheets - reusable style sheets for GeoGeba applets

Create separate style sheets (as JSON files) and apply them to your GeoGebra applets for a consistent look.

## Installation

GGB Style Sheets run on Python 3.7 and GeoGebra Classic 6.


## Usage

Create a style sheet as a JSON file (`sample_layout.json`):

```
{
	"window_height": 800,
	"window_width": 1300,

	"color_palette": {
		"orange" : [255, 127, 0],
		"black" : [0, 0, 0],
		"white" : [255, 255, 255],
		"red" : [255, 0, 0],
		"green" : [0, 255, 0],
		"blue" : [0, 0, 255]
	},

	"default_caption_style": {
		"tex": true,
		"bold": true
	},

	"background_color": "black",

	"axes": {
		"color": "white",
		"show": true,
		"show_ticks": true,
		"show_numbers": true,
		"positive_axis_only": false
	},

	"x_axis": {
		"color": "white",
		"show": true,
		"show_numbers": true
	},

	"font_size": 24,

	"line_style": {
		"width": 5,
		"hidden_style": "dotted"
	}
}
```

Then run inside the repo:

```sh
./layouting.py sample_layout.json <GeoGebra file>
```

This will create a copy of the GeoGebra file (adding `_layouted` to the file name) and apply the style rules specified in `sample_layout.json`.

## Optional arguments

- `-x, --keep_xml`: Keep the unzipped GGB file (which is in XML), before and after layouting, for inspection
- `-e, --extract_classes`: Reverse-engineer the GGB file to create native Python classes for all the elements. Otherwise, use a list of curated GGB classes
- `-c, --keep_classes`: Keep the generated Python code for the extracted classes

## Inner workings

GeoGebra files (`.ggb`) are just zipped XML, much like e. g. `.docx`. The file is unzipped and its XML content read into native Python objects.

A selection of classes for the GeoGebra elements (Axes, BGColor, GGBScript etc.) are provided in `curated_ggb_classes.py`. The list is by no means complete As is and as of now, it will most likely fail on your on GGB files. Alternatively, appropriate classes can be created via a Python code generator that inspects the XML tags (flag `--extract_classes`).

The style sheet (JSON) is read in similarly as a native Python object. Then the style rules are applied, where conditionals and other computations can be expressed in Python (root GeoGebra object in `curated_ggb_classes.py`). The result is saved back to XML and zipped up again.





















