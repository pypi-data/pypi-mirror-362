"""The namespace contains classes that represent the structures containing the characteristics of a colorant (swatch) used in a document."""
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

class ColorantBase(aspose.psd.xmp.types.complex.ComplexTypeBase):
    '''Represents XMP Colorant type.'''
    
    def get_xmp_representation(self) -> str:
        '''Gets the string contained value in XMP format.
        
        :returns: Returns the string contained value in XMP format.'''
        ...
    
    @property
    def prefix(self) -> str:
        '''Gets the prefix.'''
        ...
    
    @property
    def namespace_uri(self) -> str:
        ...
    
    @property
    def mode(self) -> aspose.psd.xmp.schemas.photoshop.ColorMode:
        '''Gets .'''
        ...
    
    @property
    def swatch_name(self) -> str:
        ...
    
    @swatch_name.setter
    def swatch_name(self, value : str):
        ...
    
    @property
    def color_type(self) -> aspose.psd.xmp.types.complex.colorant.ColorType:
        ...
    
    @color_type.setter
    def color_type(self, value : aspose.psd.xmp.types.complex.colorant.ColorType):
        ...
    
    ...

class ColorantCmyk(ColorantBase):
    '''Represents CMYK Colorant.'''
    
    @overload
    def __init__(self):
        '''Initializes a new instance of the  class.'''
        ...
    
    @overload
    def __init__(self, black: float, cyan: float, magenta: float, yellow: float):
        '''Initializes a new instance of the  class.
        
        :param black: The black component value.
        :param cyan: The cyan color component value.
        :param magenta: The magenta component value.
        :param yellow: The yellow component value.'''
        ...
    
    def get_xmp_representation(self) -> str:
        '''Gets the string contained value in XMP format.
        
        :returns: Returns the string contained value in XMP format.'''
        ...
    
    @property
    def prefix(self) -> str:
        '''Gets the prefix.'''
        ...
    
    @property
    def namespace_uri(self) -> str:
        ...
    
    @property
    def mode(self) -> aspose.psd.xmp.schemas.photoshop.ColorMode:
        '''Gets .'''
        ...
    
    @property
    def swatch_name(self) -> str:
        ...
    
    @swatch_name.setter
    def swatch_name(self, value : str):
        ...
    
    @property
    def color_type(self) -> aspose.psd.xmp.types.complex.colorant.ColorType:
        ...
    
    @color_type.setter
    def color_type(self, value : aspose.psd.xmp.types.complex.colorant.ColorType):
        ...
    
    @property
    def black(self) -> float:
        '''Gets the black component value.'''
        ...
    
    @black.setter
    def black(self, value : float):
        '''Sets the black component value.'''
        ...
    
    @property
    def cyan(self) -> float:
        '''Gets the cyan component value.'''
        ...
    
    @cyan.setter
    def cyan(self, value : float):
        '''Sets the cyan component value.'''
        ...
    
    @property
    def magenta(self) -> float:
        '''Gets the magenta component value.'''
        ...
    
    @magenta.setter
    def magenta(self, value : float):
        '''Sets the magenta component value.'''
        ...
    
    @property
    def yellow(self) -> float:
        '''Gets the yellow component value.'''
        ...
    
    @yellow.setter
    def yellow(self, value : float):
        '''Sets the yellow component value.'''
        ...
    
    @classmethod
    @property
    def COLOR_VALUE_MAX(cls) -> float:
        ...
    
    @classmethod
    @property
    def COLOR_VALUE_MIN(cls) -> float:
        ...
    
    ...

class ColorantLab(ColorantBase):
    '''Represents LAB Colorant.'''
    
    @overload
    def __init__(self):
        '''Initializes a new instance of the  class.'''
        ...
    
    @overload
    def __init__(self, a: int, b: int, l: float):
        '''Initializes a new instance of the  class.
        
        :param a: A component.
        :param b: B component.
        :param l: L component.'''
        ...
    
    def get_xmp_representation(self) -> str:
        '''Gets the string contained value in XMP format.
        
        :returns: Returns the string contained value in XMP format.'''
        ...
    
    @property
    def prefix(self) -> str:
        '''Gets the prefix.'''
        ...
    
    @property
    def namespace_uri(self) -> str:
        ...
    
    @property
    def mode(self) -> aspose.psd.xmp.schemas.photoshop.ColorMode:
        '''Gets .'''
        ...
    
    @property
    def swatch_name(self) -> str:
        ...
    
    @swatch_name.setter
    def swatch_name(self, value : str):
        ...
    
    @property
    def color_type(self) -> aspose.psd.xmp.types.complex.colorant.ColorType:
        ...
    
    @color_type.setter
    def color_type(self, value : aspose.psd.xmp.types.complex.colorant.ColorType):
        ...
    
    @property
    def a(self) -> int:
        '''Gets the A component.'''
        ...
    
    @a.setter
    def a(self, value : int):
        '''Sets the A component.'''
        ...
    
    @property
    def b(self) -> int:
        '''Gets the B component.'''
        ...
    
    @b.setter
    def b(self, value : int):
        '''Sets the B component.'''
        ...
    
    @property
    def l(self) -> float:
        '''Gets the L component.'''
        ...
    
    @l.setter
    def l(self, value : float):
        '''Sets the L component.'''
        ...
    
    @classmethod
    @property
    def MIN_A(cls) -> int:
        ...
    
    @classmethod
    @property
    def MAX_A(cls) -> int:
        ...
    
    @classmethod
    @property
    def MIN_B(cls) -> int:
        ...
    
    @classmethod
    @property
    def MAX_B(cls) -> int:
        ...
    
    @classmethod
    @property
    def MIN_L(cls) -> float:
        ...
    
    @classmethod
    @property
    def MAX_L(cls) -> float:
        ...
    
    ...

class ColorantRgb(ColorantBase):
    '''Represents RGB Colorant.'''
    
    @overload
    def __init__(self):
        '''Initializes a new instance of the  class.'''
        ...
    
    @overload
    def __init__(self, red: byte, green: byte, blue: byte):
        '''Initializes a new instance of the  class.
        
        :param red: The red component value.
        :param green: The green component value.
        :param blue: The blue component value.'''
        ...
    
    def get_xmp_representation(self) -> str:
        '''Gets the string contained value in XMP format.
        
        :returns: Returns the string contained value in XMP format.'''
        ...
    
    @property
    def prefix(self) -> str:
        '''Gets the prefix.'''
        ...
    
    @property
    def namespace_uri(self) -> str:
        ...
    
    @property
    def mode(self) -> aspose.psd.xmp.schemas.photoshop.ColorMode:
        '''Gets .'''
        ...
    
    @property
    def swatch_name(self) -> str:
        ...
    
    @swatch_name.setter
    def swatch_name(self, value : str):
        ...
    
    @property
    def color_type(self) -> aspose.psd.xmp.types.complex.colorant.ColorType:
        ...
    
    @color_type.setter
    def color_type(self, value : aspose.psd.xmp.types.complex.colorant.ColorType):
        ...
    
    @property
    def red(self) -> byte:
        '''Gets the red component value.'''
        ...
    
    @red.setter
    def red(self, value : byte):
        '''Sets the red component value.'''
        ...
    
    @property
    def green(self) -> byte:
        '''Gets the green component value.'''
        ...
    
    @green.setter
    def green(self, value : byte):
        '''Sets the green component value.'''
        ...
    
    @property
    def blue(self) -> byte:
        '''Gets the blue component value.'''
        ...
    
    @blue.setter
    def blue(self, value : byte):
        '''Sets the blue component value.'''
        ...
    
    ...

class ColorMode(enum.Enum):
    CMYK = enum.auto()
    '''CMYK color mode.'''
    RGB = enum.auto()
    '''RGB color mode.'''
    LAB = enum.auto()
    '''LAB color mode.'''

class ColorType(enum.Enum):
    PROCESS = enum.auto()
    '''Process color type.'''
    SPOT = enum.auto()
    '''Spot color type.'''

