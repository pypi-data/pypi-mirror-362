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

class ColorComponent:
    '''Color component is an abstraction over Channel Value and Channel Value.
    Any color is composed from an array of ColorComponent'''
    
    @classmethod
    @property
    def permitted_full_names(cls) -> List[str]:
        ...
    
    @property
    def bit_depth(self) -> byte:
        ...
    
    @property
    def value(self) -> int:
        '''Gets the value.
        Please note, if you try to set value that is more than
        possible stored in current bit depth, you'll get an exception'''
        ...
    
    @value.setter
    def value(self, value : int):
        '''Sets the value.
        Please note, if you try to set value that is more than
        possible stored in current bit depth, you'll get an exception'''
        ...
    
    @property
    def name(self) -> str:
        '''Gets the name of color component.'''
        ...
    
    @property
    def description(self) -> str:
        '''Gets the description of Color Component'''
        ...
    
    @property
    def full_name(self) -> str:
        ...
    
    ...

class RawColor:
    '''Raw Color Class helps to store colors with any channels count, any color mode and any bit depth
    Please note, some internal classes can have issues with converting RawColor to its' native format,
    so if API provides for you CMYK color, it's more reliable to use the provided format.
    Also, there are can be some cases when Raw Color can be converted'''
    
    def get_color_mode_name(self) -> str:
        '''Gets the name of the color mode. Color mode name accumulated from channels/components names
        
        :returns: String with the color mode name'''
        ...
    
    def get_bit_depth(self) -> int:
        '''Gets the bit depth of Raw Color.
        For example for ARGB color with 8 bits per channel/component is 32
        Bit Depth of full ARGB color with 16 bits per channel/component is 64.
        Bit depth is accumulated from the sum of channels' bit depths.
        It's possible if different channels will have different bit depths.
        
        :returns: The sum of all channels bit depths'''
        ...
    
    def get_as_int(self) -> int:
        '''Gets the color as int in case it's possible to get it.
        
        :returns: Channels data stored in Int'''
        ...
    
    def set_as_int(self, value : int):
        '''Sets data to all channels from int argument if it's possible
        
        :param value: The int value that contains component data'''
        ...
    
    def get_as_long(self) -> int:
        '''Gets the color as long in case it's possible to get it.
        
        :returns: Channels data stored in Int'''
        ...
    
    def set_as_long(self, value : int):
        '''Sets data to all channels from int argument if it's possible
        
        :param value: The int value that contains component data'''
        ...
    
    @property
    def components(self) -> List[aspose.psd.fileformats.psd.core.rawcolor.ColorComponent]:
        '''Gets the components of color. Each component is separate channel, and if you use not popular
        color scheme, it's better to work with each channel separately.'''
        ...
    
    @property
    def color_mode(self) -> int:
        ...
    
    @color_mode.setter
    def color_mode(self, value : int):
        ...
    
    ...

