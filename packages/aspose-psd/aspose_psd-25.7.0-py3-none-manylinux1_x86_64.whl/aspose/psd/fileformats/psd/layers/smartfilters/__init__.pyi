"""The namespace contains PSD file format entities contained in layers."""
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

class AddNoiseSmartFilter(SmartFilter):
    '''The AddNoise smart filter.'''
    
    def __init__(self):
        '''Initializes a new instance of the  class.'''
        ...
    
    def apply(self, raster_image: aspose.psd.RasterImage):
        '''Applies the current filter to input  image.
        
        :param raster_image: The raster image.'''
        ...
    
    def apply_to_mask(self, layer_with_mask: aspose.psd.fileformats.psd.layers.Layer):
        '''Applies the current filter to input  mask data.
        
        :param layer_with_mask: The layer with mask data.'''
        ...
    
    def clone(self) -> aspose.psd.fileformats.psd.layers.smartfilters.SmartFilter:
        '''Makes the memberwise clone of the current instance of the type.
        
        :returns: Returns the memberwise clone of the current instance of the type.'''
        ...
    
    @property
    def source_descriptor(self) -> aspose.psd.fileformats.psd.layers.layerresources.typetoolinfostructures.DescriptorStructure:
        ...
    
    @property
    def name(self) -> str:
        '''Gets the smart filter name.'''
        ...
    
    @property
    def filter_id(self) -> int:
        ...
    
    @property
    def is_enabled(self) -> bool:
        ...
    
    @is_enabled.setter
    def is_enabled(self, value : bool):
        ...
    
    @property
    def opacity(self) -> float:
        '''Gets the opacity value of smart filter.'''
        ...
    
    @opacity.setter
    def opacity(self, value : float):
        '''Sets the opacity value of smart filter.'''
        ...
    
    @property
    def blend_mode(self) -> aspose.psd.fileformats.core.blending.BlendMode:
        ...
    
    @blend_mode.setter
    def blend_mode(self, value : aspose.psd.fileformats.core.blending.BlendMode):
        ...
    
    @property
    def distribution(self) -> aspose.psd.fileformats.psd.layers.smartfilters.NoiseDistribution:
        '''Gets the distribution of noise filter.'''
        ...
    
    @distribution.setter
    def distribution(self, value : aspose.psd.fileformats.psd.layers.smartfilters.NoiseDistribution):
        '''Sets the distribution of noise filter.'''
        ...
    
    @property
    def amount_noise(self) -> float:
        ...
    
    @amount_noise.setter
    def amount_noise(self, value : float):
        ...
    
    @property
    def is_monochromatic(self) -> bool:
        ...
    
    @is_monochromatic.setter
    def is_monochromatic(self, value : bool):
        ...
    
    @classmethod
    @property
    def FILTER_TYPE(cls) -> int:
        ...
    
    ...

class GaussianBlurSmartFilter(SmartFilter):
    '''The GaussianBlur smart filter.'''
    
    def __init__(self):
        '''Initializes a new instance of the  class.'''
        ...
    
    def apply(self, raster_image: aspose.psd.RasterImage):
        '''Applies the current filter to input  image.
        
        :param raster_image: The raster image.'''
        ...
    
    def apply_to_mask(self, layer_with_mask: aspose.psd.fileformats.psd.layers.Layer):
        '''Applies the current filter to input  mask data.
        
        :param layer_with_mask: The layer with mask data.'''
        ...
    
    def clone(self) -> aspose.psd.fileformats.psd.layers.smartfilters.SmartFilter:
        '''Makes the memberwise clone of the current instance of the type.
        
        :returns: Returns the memberwise clone of the current instance of the type.'''
        ...
    
    @property
    def source_descriptor(self) -> aspose.psd.fileformats.psd.layers.layerresources.typetoolinfostructures.DescriptorStructure:
        ...
    
    @property
    def name(self) -> str:
        '''Gets the smart filter name.'''
        ...
    
    @property
    def filter_id(self) -> int:
        ...
    
    @property
    def is_enabled(self) -> bool:
        ...
    
    @is_enabled.setter
    def is_enabled(self, value : bool):
        ...
    
    @property
    def opacity(self) -> float:
        '''Gets the opacity value of smart filter.'''
        ...
    
    @opacity.setter
    def opacity(self, value : float):
        '''Sets the opacity value of smart filter.'''
        ...
    
    @property
    def blend_mode(self) -> aspose.psd.fileformats.core.blending.BlendMode:
        ...
    
    @blend_mode.setter
    def blend_mode(self, value : aspose.psd.fileformats.core.blending.BlendMode):
        ...
    
    @property
    def radius(self) -> float:
        '''Gets the radius of gaussian smart filter.'''
        ...
    
    @radius.setter
    def radius(self, value : float):
        '''Sets the radius of gaussian smart filter.'''
        ...
    
    @classmethod
    @property
    def FILTER_TYPE(cls) -> int:
        ...
    
    ...

class SharpenSmartFilter(SmartFilter):
    '''The Sharpen smart filter.'''
    
    @overload
    def __init__(self):
        '''Initializes a new instance of the  class.'''
        ...
    
    @overload
    def __init__(self, source_descriptor: aspose.psd.fileformats.psd.layers.layerresources.typetoolinfostructures.DescriptorStructure):
        '''Initializes a new instance of the  class.
        
        :param source_descriptor: The descriptor structure with smart filter info.'''
        ...
    
    def apply(self, raster_image: aspose.psd.RasterImage):
        '''Applies the current filter to input  image.
        
        :param raster_image: The raster image.'''
        ...
    
    def apply_to_mask(self, layer_with_mask: aspose.psd.fileformats.psd.layers.Layer):
        '''Applies the current filter to input  mask data.
        
        :param layer_with_mask: The layer with mask data.'''
        ...
    
    def clone(self) -> aspose.psd.fileformats.psd.layers.smartfilters.SmartFilter:
        '''Makes the memberwise clone of the current instance of the type.
        
        :returns: Returns the memberwise clone of the current instance of the type.'''
        ...
    
    @property
    def source_descriptor(self) -> aspose.psd.fileformats.psd.layers.layerresources.typetoolinfostructures.DescriptorStructure:
        ...
    
    @property
    def name(self) -> str:
        '''Gets the smart filter name.'''
        ...
    
    @property
    def filter_id(self) -> int:
        ...
    
    @property
    def is_enabled(self) -> bool:
        ...
    
    @is_enabled.setter
    def is_enabled(self, value : bool):
        ...
    
    @property
    def opacity(self) -> float:
        '''Gets the opacity value of smart filter.'''
        ...
    
    @opacity.setter
    def opacity(self, value : float):
        '''Sets the opacity value of smart filter.'''
        ...
    
    @property
    def blend_mode(self) -> aspose.psd.fileformats.core.blending.BlendMode:
        ...
    
    @blend_mode.setter
    def blend_mode(self, value : aspose.psd.fileformats.core.blending.BlendMode):
        ...
    
    @classmethod
    @property
    def FILTER_TYPE(cls) -> int:
        ...
    
    ...

class SmartFilter:
    '''The class to process a base logic of smart filters.'''
    
    def apply(self, raster_image: aspose.psd.RasterImage):
        '''Applies the current filter to input  image.
        
        :param raster_image: The raster image.'''
        ...
    
    def apply_to_mask(self, layer_with_mask: aspose.psd.fileformats.psd.layers.Layer):
        '''Applies the current filter to input  mask data.
        
        :param layer_with_mask: The layer with mask data.'''
        ...
    
    def clone(self) -> aspose.psd.fileformats.psd.layers.smartfilters.SmartFilter:
        '''Makes the memberwise clone of the current instance of the type.
        
        :returns: Returns the memberwise clone of the current instance of the type.'''
        ...
    
    @property
    def source_descriptor(self) -> aspose.psd.fileformats.psd.layers.layerresources.typetoolinfostructures.DescriptorStructure:
        ...
    
    @property
    def name(self) -> str:
        '''Gets the smart filter name.'''
        ...
    
    @property
    def filter_id(self) -> int:
        ...
    
    @property
    def is_enabled(self) -> bool:
        ...
    
    @is_enabled.setter
    def is_enabled(self, value : bool):
        ...
    
    @property
    def opacity(self) -> float:
        '''Gets the opacity value of smart filter.'''
        ...
    
    @opacity.setter
    def opacity(self, value : float):
        '''Sets the opacity value of smart filter.'''
        ...
    
    @property
    def blend_mode(self) -> aspose.psd.fileformats.core.blending.BlendMode:
        ...
    
    @blend_mode.setter
    def blend_mode(self, value : aspose.psd.fileformats.core.blending.BlendMode):
        ...
    
    ...

class SmartFilters:
    '''The smart filters of .'''
    
    def update_resource_values(self):
        '''Updates the smart filter data into the .'''
        ...
    
    @property
    def is_enabled(self) -> bool:
        ...
    
    @property
    def is_valid_at_position(self) -> bool:
        ...
    
    @property
    def is_mask_enabled(self) -> bool:
        ...
    
    @property
    def is_mask_linked(self) -> bool:
        ...
    
    @property
    def is_mask_extend_with_white(self) -> bool:
        ...
    
    @property
    def filters(self) -> List[aspose.psd.fileformats.psd.layers.smartfilters.SmartFilter]:
        '''Gets the smart filters.'''
        ...
    
    @filters.setter
    def filters(self, value : List[aspose.psd.fileformats.psd.layers.smartfilters.SmartFilter]):
        '''Sets the smart filters.'''
        ...
    
    ...

class UnknownSmartFilter(SmartFilter):
    '''The class to hold unknown smart filter data.'''
    
    def apply(self, raster_image: aspose.psd.RasterImage):
        '''Applies the current filter to input  image.
        
        :param raster_image: The raster image.'''
        ...
    
    def apply_to_mask(self, layer_with_mask: aspose.psd.fileformats.psd.layers.Layer):
        '''Applies the current filter to input  mask data.
        
        :param layer_with_mask: The layer with mask data.'''
        ...
    
    def clone(self) -> aspose.psd.fileformats.psd.layers.smartfilters.SmartFilter:
        '''Makes the memberwise clone of the current instance of the type.
        
        :returns: Returns the memberwise clone of the current instance of the type.'''
        ...
    
    @property
    def source_descriptor(self) -> aspose.psd.fileformats.psd.layers.layerresources.typetoolinfostructures.DescriptorStructure:
        ...
    
    @property
    def name(self) -> str:
        '''Gets the smart filter name.'''
        ...
    
    @property
    def filter_id(self) -> int:
        ...
    
    @property
    def is_enabled(self) -> bool:
        ...
    
    @is_enabled.setter
    def is_enabled(self, value : bool):
        ...
    
    @property
    def opacity(self) -> float:
        '''Gets the opacity value of smart filter.'''
        ...
    
    @opacity.setter
    def opacity(self, value : float):
        '''Sets the opacity value of smart filter.'''
        ...
    
    @property
    def blend_mode(self) -> aspose.psd.fileformats.core.blending.BlendMode:
        ...
    
    @blend_mode.setter
    def blend_mode(self, value : aspose.psd.fileformats.core.blending.BlendMode):
        ...
    
    ...

class NoiseDistribution(enum.Enum):
    UNIFORM = enum.auto()
    '''The uniform noise distribution.'''
    GAUSSIAN = enum.auto()
    '''The gaussian noise distribution.'''

