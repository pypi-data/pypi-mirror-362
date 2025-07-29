from typing import List, Optional, Dict, Iterable
import aspose.pycore
import aspose.pydrawing
import aspose.psd
import aspose.psd.asynctask
import aspose.psd.brushes
import aspose.psd.coreexceptions
import aspose.psd.coreexceptions.compressors
import aspose.psd.coreexceptions.imageformats
import aspose.psd.customfonthandler
import aspose.psd.dithering
import aspose.psd.evalute
import aspose.psd.exif
import aspose.psd.exif.enums
import aspose.psd.extensions
import aspose.psd.fileformats
import aspose.psd.fileformats.ai
import aspose.psd.fileformats.bmp
import aspose.psd.fileformats.core
import aspose.psd.fileformats.core.blending
import aspose.psd.fileformats.core.vectorpaths
import aspose.psd.fileformats.jpeg
import aspose.psd.fileformats.jpeg2000
import aspose.psd.fileformats.pdf
import aspose.psd.fileformats.png
import aspose.psd.fileformats.psd
import aspose.psd.fileformats.psd.core
import aspose.psd.fileformats.psd.core.rawcolor
import aspose.psd.fileformats.psd.layers
import aspose.psd.fileformats.psd.layers.adjustmentlayers
import aspose.psd.fileformats.psd.layers.animation
import aspose.psd.fileformats.psd.layers.filllayers
import aspose.psd.fileformats.psd.layers.fillsettings
import aspose.psd.fileformats.psd.layers.gradient
import aspose.psd.fileformats.psd.layers.layereffects
import aspose.psd.fileformats.psd.layers.layerresources
import aspose.psd.fileformats.psd.layers.layerresources.strokeresources
import aspose.psd.fileformats.psd.layers.layerresources.typetoolinfostructures
import aspose.psd.fileformats.psd.layers.smartfilters
import aspose.psd.fileformats.psd.layers.smartfilters.rendering
import aspose.psd.fileformats.psd.layers.smartobjects
import aspose.psd.fileformats.psd.layers.text
import aspose.psd.fileformats.psd.layers.warp
import aspose.psd.fileformats.psd.resources
import aspose.psd.fileformats.psd.resources.enums
import aspose.psd.fileformats.psd.resources.resolutionenums
import aspose.psd.fileformats.tiff
import aspose.psd.fileformats.tiff.enums
import aspose.psd.fileformats.tiff.filemanagement
import aspose.psd.flatarray
import aspose.psd.flatarray.exceptions
import aspose.psd.imagefilters
import aspose.psd.imagefilters.filteroptions
import aspose.psd.imageloadoptions
import aspose.psd.imageoptions
import aspose.psd.interfaces
import aspose.psd.memorymanagement
import aspose.psd.multithreading
import aspose.psd.palettehelper
import aspose.psd.progressmanagement
import aspose.psd.shapes
import aspose.psd.shapesegments
import aspose.psd.sources
import aspose.psd.xmp
import aspose.psd.xmp.schemas
import aspose.psd.xmp.schemas.dublincore
import aspose.psd.xmp.schemas.pdf
import aspose.psd.xmp.schemas.photoshop
import aspose.psd.xmp.schemas.xmpbaseschema
import aspose.psd.xmp.schemas.xmpdm
import aspose.psd.xmp.schemas.xmpmm
import aspose.psd.xmp.schemas.xmprm
import aspose.psd.xmp.types
import aspose.psd.xmp.types.basic
import aspose.psd.xmp.types.complex
import aspose.psd.xmp.types.complex.colorant
import aspose.psd.xmp.types.complex.dimensions
import aspose.psd.xmp.types.complex.font
import aspose.psd.xmp.types.complex.resourceevent
import aspose.psd.xmp.types.complex.resourceref
import aspose.psd.xmp.types.complex.thumbnail
import aspose.psd.xmp.types.complex.version
import aspose.psd.xmp.types.derived

class IText:
    '''Interface for Text Editing for Text Layers'''
    
    def produce_portion(self) -> aspose.psd.fileformats.psd.layers.text.ITextPortion:
        '''Produces the new portion with default parameters
        
        :returns: Reference to newly created :py:class:`aspose.psd.fileformats.psd.layers.text.ITextPortion`.'''
        ...
    
    def produce_portions(self, portions_of_text : List[str], style_prototype : aspose.psd.fileformats.psd.layers.text.ITextStyle, paragraph_prototype : aspose.psd.fileformats.psd.layers.text.ITextParagraph) -> List[aspose.psd.fileformats.psd.layers.text.ITextPortion]:
        '''Produces the new portions with input or default parameters.
        
        :param portions_of_text: The portions of text to create new :py:class:`aspose.psd.fileformats.psd.layers.text.ITextPortion`.
        :param style_prototype: A style that, if not null, will be applied in the new :py:class:`aspose.psd.fileformats.psd.layers.text.ITextPortion`, otherwise will be default.
        :param paragraph_prototype: A paragraph that, if not null, will be applied in the new :py:class:`aspose.psd.fileformats.psd.layers.text.ITextPortion`, otherwise will be default.
        :returns: Returns the new portions :py:class:`aspose.psd.fileformats.psd.layers.text.ITextPortion` based on input parameters.'''
        ...
    
    def add_portion(self, portion : aspose.psd.fileformats.psd.layers.text.ITextPortion):
        '''Adds the portion of text to the end
        
        :param portion: The portion.'''
        ...
    
    def insert_portion(self, portion : aspose.psd.fileformats.psd.layers.text.ITextPortion, index : int):
        '''Inserts the :py:class:`aspose.psd.fileformats.psd.layers.text.ITextPortion` to specified position
        
        :param portion: The portion.
        :param index: The index.'''
        ...
    
    def remove_portion(self, index : int):
        '''Removes the portion in specified index
        
        :param index: The index.'''
        ...
    
    def update_layer_data(self):
        '''Updates the layer data.'''
        ...
    
    @property
    def items(self) -> List[aspose.psd.fileformats.psd.layers.text.ITextPortion]:
        '''Gets the items.'''
        ...
    
    @property
    def text(self) -> str:
        '''Gets the text.'''
        ...
    
    @property
    def text_orientation(self) -> aspose.psd.fileformats.psd.TextOrientation:
        ...
    
    @text_orientation.setter
    def text_orientation(self, value : aspose.psd.fileformats.psd.TextOrientation):
        ...
    
    ...

class ITextParagraph:
    '''The interface to work with paragraph'''
    
    def apply(self, paragraph : aspose.psd.fileformats.psd.layers.text.ITextParagraph):
        '''Applies the specified paragraph.
        
        :param paragraph: The paragraph.'''
        ...
    
    def is_equal(self, paragraph : aspose.psd.fileformats.psd.layers.text.ITextParagraph) -> bool:
        '''Determines whether the specified paragraph is equal.
        
        :param paragraph: The paragraph.
        :returns: ``true`` if the specified paragraph is equal; otherwise, ``false``.'''
        ...
    
    @property
    def justification(self) -> aspose.psd.fileformats.psd.JustificationMode:
        '''Gets the justification.'''
        ...
    
    @justification.setter
    def justification(self, value : aspose.psd.fileformats.psd.JustificationMode):
        '''Sets the justification.'''
        ...
    
    @property
    def first_line_indent(self) -> float:
        ...
    
    @first_line_indent.setter
    def first_line_indent(self, value : float):
        ...
    
    @property
    def start_indent(self) -> float:
        ...
    
    @start_indent.setter
    def start_indent(self, value : float):
        ...
    
    @property
    def end_indent(self) -> float:
        ...
    
    @end_indent.setter
    def end_indent(self, value : float):
        ...
    
    @property
    def space_before(self) -> float:
        ...
    
    @space_before.setter
    def space_before(self, value : float):
        ...
    
    @property
    def space_after(self) -> float:
        ...
    
    @space_after.setter
    def space_after(self, value : float):
        ...
    
    @property
    def auto_hyphenate(self) -> bool:
        ...
    
    @auto_hyphenate.setter
    def auto_hyphenate(self, value : bool):
        ...
    
    @property
    def hyphenated_word_size(self) -> int:
        ...
    
    @hyphenated_word_size.setter
    def hyphenated_word_size(self, value : int):
        ...
    
    @property
    def pre_hyphen(self) -> int:
        ...
    
    @pre_hyphen.setter
    def pre_hyphen(self, value : int):
        ...
    
    @property
    def post_hyphen(self) -> int:
        ...
    
    @post_hyphen.setter
    def post_hyphen(self, value : int):
        ...
    
    @property
    def consecutive_hyphens(self) -> int:
        ...
    
    @consecutive_hyphens.setter
    def consecutive_hyphens(self, value : int):
        ...
    
    @property
    def zone(self) -> float:
        '''Gets the zone.'''
        ...
    
    @zone.setter
    def zone(self, value : float):
        '''Sets the zone.'''
        ...
    
    @property
    def word_spacing(self) -> List[float]:
        ...
    
    @word_spacing.setter
    def word_spacing(self, value : List[float]):
        ...
    
    @property
    def letter_spacing(self) -> List[float]:
        ...
    
    @letter_spacing.setter
    def letter_spacing(self, value : List[float]):
        ...
    
    @property
    def glyph_spacing(self) -> List[float]:
        ...
    
    @glyph_spacing.setter
    def glyph_spacing(self, value : List[float]):
        ...
    
    @property
    def auto_leading(self) -> float:
        ...
    
    @auto_leading.setter
    def auto_leading(self, value : float):
        ...
    
    @property
    def leading_type(self) -> aspose.psd.fileformats.psd.LeadingType:
        ...
    
    @leading_type.setter
    def leading_type(self, value : aspose.psd.fileformats.psd.LeadingType):
        ...
    
    @property
    def hanging(self) -> bool:
        '''Gets a value indicating whether this :py:class:`aspose.psd.fileformats.psd.layers.text.ITextParagraph` is hanging.'''
        ...
    
    @hanging.setter
    def hanging(self, value : bool):
        '''Sets a value indicating whether this :py:class:`aspose.psd.fileformats.psd.layers.text.ITextParagraph` is hanging.'''
        ...
    
    @property
    def burasagari(self) -> bool:
        '''Gets a value indicating whether this :py:class:`aspose.psd.fileformats.psd.layers.text.ITextParagraph` is burasagiri.'''
        ...
    
    @burasagari.setter
    def burasagari(self, value : bool):
        '''Sets a value indicating whether this :py:class:`aspose.psd.fileformats.psd.layers.text.ITextParagraph` is burasagiri.'''
        ...
    
    @property
    def kinsoku_order(self) -> int:
        ...
    
    @kinsoku_order.setter
    def kinsoku_order(self, value : int):
        ...
    
    @property
    def every_line_composer(self) -> bool:
        ...
    
    @every_line_composer.setter
    def every_line_composer(self, value : bool):
        ...
    
    ...

class ITextPortion:
    '''Interface to manipulate text portions'''
    
    @property
    def text(self) -> str:
        '''Gets the text.'''
        ...
    
    @text.setter
    def text(self, value : str):
        '''Sets the text.'''
        ...
    
    @property
    def style(self) -> aspose.psd.fileformats.psd.layers.text.ITextStyle:
        '''Gets the style.'''
        ...
    
    @property
    def paragraph(self) -> aspose.psd.fileformats.psd.layers.text.ITextParagraph:
        '''Sets the style.'''
        ...
    
    ...

class ITextStyle:
    '''Interface to work with Text Style'''
    
    def apply(self, style : aspose.psd.fileformats.psd.layers.text.ITextStyle):
        '''Applies the specified style.
        
        :param style: The style.'''
        ...
    
    def is_equal(self, style : aspose.psd.fileformats.psd.layers.text.ITextStyle) -> bool:
        '''Determines whether the specified style is equal.
        
        :param style: The style.
        :returns: ``true`` if the specified style is equal; otherwise, ``false``.'''
        ...
    
    @property
    def font_size(self) -> float:
        ...
    
    @font_size.setter
    def font_size(self, value : float):
        ...
    
    @property
    def font_index(self) -> int:
        ...
    
    @property
    def font_name(self) -> str:
        ...
    
    @font_name.setter
    def font_name(self, value : str):
        ...
    
    @property
    def auto_leading(self) -> bool:
        ...
    
    @auto_leading.setter
    def auto_leading(self, value : bool):
        ...
    
    @property
    def leading(self) -> float:
        '''Gets the leading.'''
        ...
    
    @leading.setter
    def leading(self, value : float):
        '''Sets the leading.'''
        ...
    
    @property
    def tracking(self) -> int:
        '''Gets the tracking.'''
        ...
    
    @tracking.setter
    def tracking(self, value : int):
        '''Sets the tracking.'''
        ...
    
    @property
    def kerning(self) -> int:
        '''Gets the kerning.'''
        ...
    
    @kerning.setter
    def kerning(self, value : int):
        '''Sets the kerning.'''
        ...
    
    @property
    def auto_kerning(self) -> aspose.psd.fileformats.psd.AutoKerning:
        ...
    
    @auto_kerning.setter
    def auto_kerning(self, value : aspose.psd.fileformats.psd.AutoKerning):
        ...
    
    @property
    def fill_color(self) -> aspose.psd.Color:
        ...
    
    @fill_color.setter
    def fill_color(self, value : aspose.psd.Color):
        ...
    
    @property
    def stroke_color(self) -> aspose.psd.Color:
        ...
    
    @stroke_color.setter
    def stroke_color(self, value : aspose.psd.Color):
        ...
    
    @property
    def hindi_numbers(self) -> bool:
        ...
    
    @hindi_numbers.setter
    def hindi_numbers(self, value : bool):
        ...
    
    @property
    def faux_bold(self) -> bool:
        ...
    
    @faux_bold.setter
    def faux_bold(self, value : bool):
        ...
    
    @property
    def faux_italic(self) -> bool:
        ...
    
    @faux_italic.setter
    def faux_italic(self, value : bool):
        ...
    
    @property
    def underline(self) -> bool:
        '''Gets a value indicating whether [underline].'''
        ...
    
    @underline.setter
    def underline(self, value : bool):
        '''Sets a value indicating whether [underline].'''
        ...
    
    @property
    def strikethrough(self) -> bool:
        '''Gets a value indicating whether [strikethrough].'''
        ...
    
    @strikethrough.setter
    def strikethrough(self, value : bool):
        '''Sets a value indicating whether [strikethrough].'''
        ...
    
    @property
    def font_baseline(self) -> aspose.psd.fileformats.psd.FontBaseline:
        ...
    
    @font_baseline.setter
    def font_baseline(self, value : aspose.psd.fileformats.psd.FontBaseline):
        ...
    
    @property
    def baseline_shift(self) -> float:
        ...
    
    @baseline_shift.setter
    def baseline_shift(self, value : float):
        ...
    
    @property
    def font_caps(self) -> aspose.psd.fileformats.psd.FontCaps:
        ...
    
    @font_caps.setter
    def font_caps(self, value : aspose.psd.fileformats.psd.FontCaps):
        ...
    
    @property
    def standard_ligatures(self) -> bool:
        ...
    
    @standard_ligatures.setter
    def standard_ligatures(self, value : bool):
        ...
    
    @property
    def discretionary_ligatures(self) -> bool:
        ...
    
    @discretionary_ligatures.setter
    def discretionary_ligatures(self, value : bool):
        ...
    
    @property
    def contextual_alternates(self) -> bool:
        ...
    
    @contextual_alternates.setter
    def contextual_alternates(self, value : bool):
        ...
    
    @property
    def language_index(self) -> int:
        ...
    
    @property
    def vertical_scale(self) -> float:
        ...
    
    @vertical_scale.setter
    def vertical_scale(self, value : float):
        ...
    
    @property
    def horizontal_scale(self) -> float:
        ...
    
    @horizontal_scale.setter
    def horizontal_scale(self, value : float):
        ...
    
    @property
    def fractions(self) -> bool:
        '''The fractions symbols can be replaced with special glyph.'''
        ...
    
    @fractions.setter
    def fractions(self, value : bool):
        '''The fractions symbols can be replaced with special glyph.'''
        ...
    
    @property
    def is_standard_vertical_roman_alignment_enabled(self) -> bool:
        ...
    
    @is_standard_vertical_roman_alignment_enabled.setter
    def is_standard_vertical_roman_alignment_enabled(self, value : bool):
        ...
    
    @property
    def no_break(self) -> bool:
        ...
    
    @no_break.setter
    def no_break(self, value : bool):
        ...
    
    ...

class TextFontInfo:
    '''Represents the information about font. This class cannot be inherited.'''
    
    @property
    def font_type(self) -> int:
        ...
    
    @property
    def script(self) -> int:
        '''Gets the script.'''
        ...
    
    @property
    def synthetic(self) -> bool:
        '''Gets a value indicating whether this :py:class:`Aspose.PSD.FileFormats.Psd.Layers.Text.FontInformation` is synthetic.'''
        ...
    
    @property
    def post_script_name(self) -> str:
        ...
    
    @property
    def family_name(self) -> str:
        ...
    
    @property
    def style(self) -> aspose.psd.FontStyle:
        '''Gets font style parsed from subfamily name'''
        ...
    
    ...

