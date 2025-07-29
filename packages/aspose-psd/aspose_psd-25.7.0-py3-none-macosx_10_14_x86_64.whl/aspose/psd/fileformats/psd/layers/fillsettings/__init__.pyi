"""The namespace contains Fill Layers Settings"""
from typing import List, Optional, Dict, Iterable
import enum
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

class BaseFillSettings(IFillSettings):
    '''Base fill effect settings'''
    
    @property
    def fill_type(self) -> aspose.psd.fileformats.psd.layers.fillsettings.FillType:
        ...
    
    ...

class ColorFillSettings(BaseFillSettings):
    '''Color fill effect settings'''
    
    def __init__(self):
        ...
    
    @property
    def fill_type(self) -> aspose.psd.fileformats.psd.layers.fillsettings.FillType:
        ...
    
    @property
    def color(self) -> aspose.psd.Color:
        '''Gets the color.'''
        ...
    
    @color.setter
    def color(self, value : aspose.psd.Color):
        '''Sets the color.'''
        ...
    
    ...

class GradientColorPoint(aspose.psd.fileformats.psd.layers.IGradientColorPoint):
    '''The Gradient Color Point.'''
    
    @overload
    def __init__(self):
        '''Initializes a new instance of the  class.'''
        ...
    
    @overload
    def __init__(self, color: aspose.psd.Color, location: int, median_point_location: int):
        '''Initializes a new instance of the  class.
        
        :param color: Color point on gradient.
        :param location: The location of the color point on the gradient.
        :param median_point_location: The median gradient point location.'''
        ...
    
    @property
    def color(self) -> aspose.psd.Color:
        '''Gets the color.'''
        ...
    
    @color.setter
    def color(self, value : aspose.psd.Color):
        '''Sets the color.'''
        ...
    
    @property
    def location(self) -> int:
        '''Gets the point location on gradient.'''
        ...
    
    @location.setter
    def location(self, value : int):
        '''Sets the point location on gradient.'''
        ...
    
    @property
    def median_point_location(self) -> int:
        ...
    
    @median_point_location.setter
    def median_point_location(self, value : int):
        ...
    
    @property
    def raw_color(self) -> aspose.psd.fileformats.psd.core.rawcolor.RawColor:
        ...
    
    @raw_color.setter
    def raw_color(self, value : aspose.psd.fileformats.psd.core.rawcolor.RawColor):
        ...
    
    @property
    def color_mode(self) -> int:
        ...
    
    @color_mode.setter
    def color_mode(self, value : int):
        ...
    
    ...

class GradientFillSettings(BaseFillSettings):
    '''Base gradient definition class. It contains common properties for both types of gradient (Solid and Noise).'''
    
    def __init__(self):
        ...
    
    @property
    def fill_type(self) -> aspose.psd.fileformats.psd.layers.fillsettings.FillType:
        ...
    
    @property
    def align_with_layer(self) -> bool:
        ...
    
    @align_with_layer.setter
    def align_with_layer(self, value : bool):
        ...
    
    @property
    def dither(self) -> bool:
        '''Gets a value indicating whether this  is dither.'''
        ...
    
    @dither.setter
    def dither(self, value : bool):
        '''Sets a value indicating whether this  is dither.'''
        ...
    
    @property
    def reverse(self) -> bool:
        '''Gets a value indicating whether this  is reverse.'''
        ...
    
    @reverse.setter
    def reverse(self, value : bool):
        '''Sets a value indicating whether this  is reverse.'''
        ...
    
    @property
    def angle(self) -> float:
        '''Gets the angle.'''
        ...
    
    @angle.setter
    def angle(self, value : float):
        '''Sets the angle.'''
        ...
    
    @property
    def scale(self) -> int:
        '''Gets the scale.'''
        ...
    
    @scale.setter
    def scale(self, value : int):
        '''Sets the scale.'''
        ...
    
    @property
    def horizontal_offset(self) -> float:
        ...
    
    @horizontal_offset.setter
    def horizontal_offset(self, value : float):
        ...
    
    @property
    def vertical_offset(self) -> float:
        ...
    
    @vertical_offset.setter
    def vertical_offset(self, value : float):
        ...
    
    @property
    def gradient_type(self) -> aspose.psd.fileformats.psd.layers.fillsettings.GradientType:
        ...
    
    @gradient_type.setter
    def gradient_type(self, value : aspose.psd.fileformats.psd.layers.fillsettings.GradientType):
        ...
    
    @property
    def gradient(self) -> aspose.psd.fileformats.psd.layers.gradient.BaseGradient:
        '''Gets specific gradient definition instance (Solid/Noise).'''
        ...
    
    @gradient.setter
    def gradient(self, value : aspose.psd.fileformats.psd.layers.gradient.BaseGradient):
        '''Sets specific gradient definition instance (Solid/Noise).'''
        ...
    
    ...

class GradientMapSettings:
    '''Gradient settings class for gradient map layer. It contains common properties for both types of gradient (Solid and Noise).'''
    
    def __init__(self):
        ...
    
    @property
    def dither(self) -> bool:
        '''Gets a value indicating whether this  is dither.'''
        ...
    
    @dither.setter
    def dither(self, value : bool):
        '''Sets a value indicating whether this  is dither.'''
        ...
    
    @property
    def reverse(self) -> bool:
        '''Gets a value indicating whether this  is reverse.'''
        ...
    
    @reverse.setter
    def reverse(self, value : bool):
        '''Sets a value indicating whether this  is reverse.'''
        ...
    
    @property
    def gradient(self) -> aspose.psd.fileformats.psd.layers.gradient.BaseGradient:
        '''Gets specific gradient definition instance (Solid/Noise).'''
        ...
    
    @gradient.setter
    def gradient(self, value : aspose.psd.fileformats.psd.layers.gradient.BaseGradient):
        '''Sets specific gradient definition instance (Solid/Noise).'''
        ...
    
    ...

class GradientTransparencyPoint(IGradientTransparencyPoint):
    '''Gradient Transparency Point'''
    
    def __init__(self):
        '''Initializes a new instance of the  class.'''
        ...
    
    @property
    def opacity(self) -> float:
        '''Gets the color.'''
        ...
    
    @opacity.setter
    def opacity(self, value : float):
        '''Sets the color.'''
        ...
    
    @property
    def location(self) -> int:
        '''Gets the location.'''
        ...
    
    @location.setter
    def location(self, value : int):
        '''Sets the location.'''
        ...
    
    @property
    def median_point_location(self) -> int:
        ...
    
    @median_point_location.setter
    def median_point_location(self, value : int):
        ...
    
    ...

class IColorFillSettings(IFillSettings):
    '''Base interface for fill settings'''
    
    @property
    def color(self) -> aspose.psd.Color:
        '''Gets the color.'''
        ...
    
    @color.setter
    def color(self, value : aspose.psd.Color):
        '''Sets the color.'''
        ...
    
    @property
    def fill_type(self) -> aspose.psd.fileformats.psd.layers.fillsettings.FillType:
        ...
    
    ...

class IFillSettings:
    '''Base interface for fill settings'''
    
    @property
    def fill_type(self) -> aspose.psd.fileformats.psd.layers.fillsettings.FillType:
        ...
    
    ...

class IGradientFillSettings(IFillSettings):
    '''Base interface for Gradient fill settings.'''
    
    @property
    def align_with_layer(self) -> bool:
        ...
    
    @align_with_layer.setter
    def align_with_layer(self, value : bool):
        ...
    
    @property
    def dither(self) -> bool:
        '''Gets a value indicating whether this  is dither.'''
        ...
    
    @dither.setter
    def dither(self, value : bool):
        '''Sets a value indicating whether this  is dither.'''
        ...
    
    @property
    def reverse(self) -> bool:
        '''Gets a value indicating whether this  is reverse.'''
        ...
    
    @reverse.setter
    def reverse(self, value : bool):
        '''Sets a value indicating whether this  is reverse.'''
        ...
    
    @property
    def angle(self) -> float:
        '''Gets the angle.'''
        ...
    
    @angle.setter
    def angle(self, value : float):
        '''Sets the angle.'''
        ...
    
    @property
    def scale(self) -> int:
        '''Gets the scale.'''
        ...
    
    @scale.setter
    def scale(self, value : int):
        '''Sets the scale.'''
        ...
    
    @property
    def horizontal_offset(self) -> float:
        ...
    
    @horizontal_offset.setter
    def horizontal_offset(self, value : float):
        ...
    
    @property
    def vertical_offset(self) -> float:
        ...
    
    @vertical_offset.setter
    def vertical_offset(self, value : float):
        ...
    
    @property
    def gradient_type(self) -> aspose.psd.fileformats.psd.layers.fillsettings.GradientType:
        ...
    
    @gradient_type.setter
    def gradient_type(self, value : aspose.psd.fileformats.psd.layers.fillsettings.GradientType):
        ...
    
    @property
    def gradient(self) -> aspose.psd.fileformats.psd.layers.gradient.BaseGradient:
        '''Gets specific gradient definition instance (Solid/Noise).'''
        ...
    
    @gradient.setter
    def gradient(self, value : aspose.psd.fileformats.psd.layers.gradient.BaseGradient):
        '''Sets specific gradient definition instance (Solid/Noise).'''
        ...
    
    @property
    def fill_type(self) -> aspose.psd.fileformats.psd.layers.fillsettings.FillType:
        ...
    
    ...

class IGradientTransparencyPoint:
    '''Base interface for fill settings'''
    
    @property
    def opacity(self) -> float:
        '''Gets the opacity.'''
        ...
    
    @opacity.setter
    def opacity(self, value : float):
        '''Sets the opacity.'''
        ...
    
    @property
    def location(self) -> int:
        '''Gets the location. Value range 0-4096.'''
        ...
    
    @location.setter
    def location(self, value : int):
        '''Sets the location. Value range 0-4096.'''
        ...
    
    @property
    def median_point_location(self) -> int:
        ...
    
    @median_point_location.setter
    def median_point_location(self, value : int):
        ...
    
    ...

class IPatternFillSettings(IFillSettings):
    '''Interface for Pattern fill settings'''
    
    @property
    def angle(self) -> float:
        '''Gets the angle.'''
        ...
    
    @angle.setter
    def angle(self, value : float):
        '''Sets the angle.'''
        ...
    
    @property
    def linked(self) -> bool:
        '''Gets a value indicating whether this  is linked.'''
        ...
    
    @linked.setter
    def linked(self, value : bool):
        '''Sets a value indicating whether this  is linked.'''
        ...
    
    @property
    def scale(self) -> float:
        '''Gets the scale.'''
        ...
    
    @scale.setter
    def scale(self, value : float):
        '''Sets the scale.'''
        ...
    
    @property
    def point_type(self) -> str:
        ...
    
    @point_type.setter
    def point_type(self, value : str):
        ...
    
    @property
    def pattern_name(self) -> str:
        ...
    
    @pattern_name.setter
    def pattern_name(self, value : str):
        ...
    
    @property
    def pattern_id(self) -> str:
        ...
    
    @pattern_id.setter
    def pattern_id(self, value : str):
        ...
    
    @property
    def horizontal_offset(self) -> int:
        ...
    
    @horizontal_offset.setter
    def horizontal_offset(self, value : int):
        ...
    
    @property
    def vertical_offset(self) -> int:
        ...
    
    @vertical_offset.setter
    def vertical_offset(self, value : int):
        ...
    
    @property
    def pattern_data(self) -> List[int]:
        ...
    
    @pattern_data.setter
    def pattern_data(self, value : List[int]):
        ...
    
    @property
    def pattern_width(self) -> int:
        ...
    
    @pattern_width.setter
    def pattern_width(self, value : int):
        ...
    
    @property
    def pattern_height(self) -> int:
        ...
    
    @pattern_height.setter
    def pattern_height(self, value : int):
        ...
    
    @property
    def fill_type(self) -> aspose.psd.fileformats.psd.layers.fillsettings.FillType:
        ...
    
    ...

class PatternFillSettings(BaseFillSettings):
    '''Pattern fill effect settings'''
    
    def __init__(self):
        ...
    
    @staticmethod
    def generate_lfx_2_resource_nodes(point_type: str, color: aspose.psd.Color, pattern_name: str, identifier: str, scale: float, linked: bool, offset: aspose.psd.PointF) -> Iterable[aspose.psd.fileformats.psd.layers.layerresources.OSTypeStructure]:
        '''Generates the LFX2 resource nodes.
        
        :param point_type: Type of the point.
        :param color: The color.
        :param pattern_name: Name of the pattern.
        :param identifier: The identifier.
        :param scale: The scale.
        :param linked: if set to ``true`` [linked].
        :param offset: The offset.
        :returns: List of'''
        ...
    
    @property
    def fill_type(self) -> aspose.psd.fileformats.psd.layers.fillsettings.FillType:
        ...
    
    @property
    def color(self) -> aspose.psd.Color:
        '''Gets the color.'''
        ...
    
    @color.setter
    def color(self, value : aspose.psd.Color):
        '''Sets the color.'''
        ...
    
    @property
    def linked(self) -> bool:
        '''Gets a value indicating whether this  is linked.'''
        ...
    
    @linked.setter
    def linked(self, value : bool):
        '''Sets a value indicating whether this  is linked.'''
        ...
    
    @property
    def scale(self) -> float:
        '''Gets the scale.'''
        ...
    
    @scale.setter
    def scale(self, value : float):
        '''Sets the scale.'''
        ...
    
    @property
    def align_with_layer(self) -> bool:
        ...
    
    @align_with_layer.setter
    def align_with_layer(self, value : bool):
        ...
    
    @property
    def point_type(self) -> str:
        ...
    
    @point_type.setter
    def point_type(self, value : str):
        ...
    
    @property
    def pattern_name(self) -> str:
        ...
    
    @pattern_name.setter
    def pattern_name(self, value : str):
        ...
    
    @property
    def pattern_id(self) -> str:
        ...
    
    @pattern_id.setter
    def pattern_id(self, value : str):
        ...
    
    @property
    def horizontal_offset(self) -> int:
        ...
    
    @horizontal_offset.setter
    def horizontal_offset(self, value : int):
        ...
    
    @property
    def vertical_offset(self) -> int:
        ...
    
    @vertical_offset.setter
    def vertical_offset(self, value : int):
        ...
    
    @property
    def pattern_data(self) -> List[int]:
        ...
    
    @pattern_data.setter
    def pattern_data(self, value : List[int]):
        ...
    
    @property
    def pattern_width(self) -> int:
        ...
    
    @pattern_width.setter
    def pattern_width(self, value : int):
        ...
    
    @property
    def pattern_height(self) -> int:
        ...
    
    @pattern_height.setter
    def pattern_height(self, value : int):
        ...
    
    @property
    def angle(self) -> float:
        '''Gets the angle.'''
        ...
    
    @angle.setter
    def angle(self, value : float):
        '''Sets the angle.'''
        ...
    
    ...

class FillType(enum.Enum):
    COLOR = enum.auto()
    '''The color fill type'''
    GRADIENT = enum.auto()
    '''The gradient fill type'''
    PATTERN = enum.auto()
    '''The pattern fill type'''

class GradientType(enum.Enum):
    LINEAR = enum.auto()
    '''The linear gradient type'''
    RADIAL = enum.auto()
    '''The radial gradient type'''
    ANGLE = enum.auto()
    '''The angle gradient type'''
    REFLECTED = enum.auto()
    '''The reflected gradient type'''
    DIAMOND = enum.auto()
    '''The diamond gradient type'''
    SHAPE_BURST = enum.auto()
    '''The shape burst gradient type'''

