"""The namespace contains classes that represent the basic type values of XMP properties."""
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

class XmpBoolean(aspose.psd.xmp.types.XmpTypeBase):
    '''Represents XMP Boolean basic type.'''
    
    @overload
    def __init__(self, value: bool):
        '''Initializes a new instance of the  class based on boolean value.
        
        :param value: The Boolean value. Allowed values are True or False.'''
        ...
    
    @overload
    def __init__(self):
        '''Initializes a new instance of the  class with default value.'''
        ...
    
    @overload
    def __init__(self, value: str):
        '''Initializes a new instance of the  class.
        
        :param value: The value.'''
        ...
    
    def get_xmp_representation(self) -> str:
        '''Returns string contained value in XMP format.
        
        :returns: Returns string contained value in XMP format.'''
        ...
    
    @property
    def value(self) -> bool:
        '''Gets a value indicating whether this  is value.'''
        ...
    
    @value.setter
    def value(self, value : bool):
        '''Sets a value indicating whether this  is value.'''
        ...
    
    ...

class XmpDate(aspose.psd.xmp.types.XmpTypeBase):
    '''Represents Date in XMP packet.'''
    
    @overload
    def __init__(self, date_time: DateTime):
        '''Initializes a new instance of the  class.
        
        :param date_time: A date-time value which is represented using a subset of ISO RFC 8601 formatting.'''
        ...
    
    @overload
    def __init__(self, date_string: str):
        '''Initializes a new instance of the  class.
        
        :param date_string: The string representation of date.'''
        ...
    
    def get_xmp_representation(self) -> str:
        '''Returns string contained value in XMP format.
        
        :returns: Returns string contained value in XMP format.'''
        ...
    
    @property
    def value(self) -> DateTime:
        '''Gets the date value.'''
        ...
    
    @value.setter
    def value(self, value : DateTime):
        '''Sets the date value.'''
        ...
    
    @property
    def format(self) -> str:
        '''Gets the format string for current value.'''
        ...
    
    @classmethod
    @property
    def ISO_8601_FORMAT(cls) -> str:
        ...
    
    ...

class XmpInteger(aspose.psd.xmp.types.XmpTypeBase):
    '''Represents XMP Integer basic type.'''
    
    @overload
    def __init__(self, value: int):
        '''Initializes a new instance of the  class.
        
        :param value: The value.'''
        ...
    
    @overload
    def __init__(self, value: int):
        '''Initializes a new instance of the  class.
        
        :param value: The value.'''
        ...
    
    @overload
    def __init__(self, value: str):
        '''Initializes a new instance of the  class.
        
        :param value: The value.'''
        ...
    
    def get_xmp_representation(self) -> str:
        '''Gets the string contained value in XMP format.
        
        :returns: Returns the string contained value in XMP format.'''
        ...
    
    @property
    def value(self) -> int:
        '''Gets the value.'''
        ...
    
    @value.setter
    def value(self, value : int):
        '''Sets the value.'''
        ...
    
    ...

class XmpReal(aspose.psd.xmp.types.XmpTypeBase):
    '''Represents XMP Real.'''
    
    @overload
    def __init__(self, value: float):
        '''Initializes a new instance of the  class.
        
        :param value: Float value.'''
        ...
    
    @overload
    def __init__(self, value: str):
        '''Initializes a new instance of the  class.
        
        :param value: The value.'''
        ...
    
    def get_xmp_representation(self) -> str:
        '''Gets the string contained value in XMP format.
        
        :returns: Returns the string contained value in XMP format.'''
        ...
    
    @property
    def value(self) -> float:
        '''Gets float the value.'''
        ...
    
    @value.setter
    def value(self, value : float):
        '''Sets float the value.'''
        ...
    
    ...

class XmpText(aspose.psd.xmp.types.XmpTypeBase):
    '''Represents XMP Text basic type.'''
    
    def __init__(self, value: str):
        '''Initializes a new instance of the  class.
        
        :param value: The value.'''
        ...
    
    def get_xmp_representation(self) -> str:
        '''Gets the string contained value in XMP format.
        
        :returns: Returns the string contained value in XMP format.'''
        ...
    
    @property
    def value(self) -> str:
        '''Gets the text value.'''
        ...
    
    @value.setter
    def value(self, value : str):
        '''Sets the text value.'''
        ...
    
    ...

