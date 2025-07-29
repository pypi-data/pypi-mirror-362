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

class AnimatedDataSectionResource(aspose.psd.fileformats.psd.ResourceBlock):
    '''The Animated Data Section Plug-In resource.'''
    
    def save(self, stream : aspose.psd.StreamContainer):
        '''Saves the resource block to the specified stream.
        
        :param stream: The stream to save the resource block to.'''
        ...
    
    def validate_values(self):
        '''Validates the resource values.'''
        ...
    
    @property
    def signature(self) -> int:
        '''Gets the resource signature. Should be always '8BIM'.'''
        ...
    
    @property
    def id(self) -> int:
        '''Gets the unique identifier for the resource.'''
        ...
    
    @id.setter
    def id(self, value : int):
        '''Sets the unique identifier for the resource.'''
        ...
    
    @property
    def name(self) -> str:
        '''Gets the resource name. Pascal string, padded to make the size even (a null name consists of two bytes of 0).'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Sets the resource name. Pascal string, padded to make the size even (a null name consists of two bytes of 0).'''
        ...
    
    @property
    def data_size(self) -> int:
        ...
    
    @property
    def size(self) -> int:
        '''Gets the resource block size in bytes including its data.'''
        ...
    
    @property
    def minimal_version(self) -> int:
        ...
    
    @classmethod
    @property
    def RESOUCE_BLOCK_SIGNATURE(cls) -> int:
        ...
    
    @classmethod
    @property
    def RESOUCE_BLOCK_ME_SA_SIGNATURE(cls) -> int:
        ...
    
    @property
    def key_name(self) -> str:
        ...
    
    @property
    def animated_data_section(self) -> aspose.psd.fileformats.psd.layers.layerresources.AnimatedDataSectionStructure:
        ...
    
    ...

class BackgroundColorResource(aspose.psd.fileformats.psd.ResourceBlock):
    '''The resource with border information of image print settings.'''
    
    def save(self, stream : aspose.psd.StreamContainer):
        '''Saves the resource block to the specified stream.
        
        :param stream: The stream to save the resource block to.'''
        ...
    
    def validate_values(self):
        '''Validates the resource values.'''
        ...
    
    @property
    def signature(self) -> int:
        '''Gets the resource signature. Should be always '8BIM'.'''
        ...
    
    @property
    def id(self) -> int:
        '''Gets the unique identifier for the resource.'''
        ...
    
    @id.setter
    def id(self, value : int):
        '''Sets the unique identifier for the resource.'''
        ...
    
    @property
    def name(self) -> str:
        '''Gets the resource name. Pascal string, padded to make the size even (a null name consists of two bytes of 0).'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Sets the resource name. Pascal string, padded to make the size even (a null name consists of two bytes of 0).'''
        ...
    
    @property
    def data_size(self) -> int:
        ...
    
    @property
    def size(self) -> int:
        '''Gets the resource block size in bytes including its data.'''
        ...
    
    @property
    def minimal_version(self) -> int:
        ...
    
    @classmethod
    @property
    def RESOUCE_BLOCK_SIGNATURE(cls) -> int:
        ...
    
    @classmethod
    @property
    def RESOUCE_BLOCK_ME_SA_SIGNATURE(cls) -> int:
        ...
    
    @property
    def color(self) -> aspose.psd.Color:
        '''Gets the background color.'''
        ...
    
    @color.setter
    def color(self, value : aspose.psd.Color):
        '''Sets the background color.'''
        ...
    
    ...

class BorderInformationResource(aspose.psd.fileformats.psd.ResourceBlock):
    '''The resource with border information of image print settings.'''
    
    def save(self, stream : aspose.psd.StreamContainer):
        '''Saves the resource block to the specified stream.
        
        :param stream: The stream to save the resource block to.'''
        ...
    
    def validate_values(self):
        '''Validates the resource values.'''
        ...
    
    @property
    def signature(self) -> int:
        '''Gets the resource signature. Should be always '8BIM'.'''
        ...
    
    @property
    def id(self) -> int:
        '''Gets the unique identifier for the resource.'''
        ...
    
    @id.setter
    def id(self, value : int):
        '''Sets the unique identifier for the resource.'''
        ...
    
    @property
    def name(self) -> str:
        '''Gets the resource name. Pascal string, padded to make the size even (a null name consists of two bytes of 0).'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Sets the resource name. Pascal string, padded to make the size even (a null name consists of two bytes of 0).'''
        ...
    
    @property
    def data_size(self) -> int:
        ...
    
    @property
    def size(self) -> int:
        '''Gets the resource block size in bytes including its data.'''
        ...
    
    @property
    def minimal_version(self) -> int:
        ...
    
    @classmethod
    @property
    def RESOUCE_BLOCK_SIGNATURE(cls) -> int:
        ...
    
    @classmethod
    @property
    def RESOUCE_BLOCK_ME_SA_SIGNATURE(cls) -> int:
        ...
    
    @property
    def width(self) -> float:
        '''Gets the border width.'''
        ...
    
    @width.setter
    def width(self, value : float):
        '''Sets the border width.'''
        ...
    
    @property
    def unit(self) -> aspose.psd.fileformats.psd.resources.resolutionenums.PhysicalUnit:
        '''Gets the border units.'''
        ...
    
    @unit.setter
    def unit(self, value : aspose.psd.fileformats.psd.resources.resolutionenums.PhysicalUnit):
        '''Sets the border units.'''
        ...
    
    ...

class CaptionDigestResource(aspose.psd.fileformats.psd.ResourceBlock):
    '''CaptionDigest resource'''
    
    def save(self, stream : aspose.psd.StreamContainer):
        '''Saves the resource block to the specified stream.
        
        :param stream: The stream to save the resource block to.'''
        ...
    
    def validate_values(self):
        '''Validates the resource values.'''
        ...
    
    @property
    def signature(self) -> int:
        '''Gets the resource signature. Should be always '8BIM'.'''
        ...
    
    @property
    def id(self) -> int:
        '''Gets the unique identifier for the resource.'''
        ...
    
    @id.setter
    def id(self, value : int):
        '''Sets the unique identifier for the resource.'''
        ...
    
    @property
    def name(self) -> str:
        '''Gets the resource name. Pascal string, padded to make the size even (a null name consists of two bytes of 0).'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Sets the resource name. Pascal string, padded to make the size even (a null name consists of two bytes of 0).'''
        ...
    
    @property
    def data_size(self) -> int:
        ...
    
    @property
    def size(self) -> int:
        '''Gets the resource block size in bytes including its data.'''
        ...
    
    @property
    def minimal_version(self) -> int:
        ...
    
    @classmethod
    @property
    def RESOUCE_BLOCK_SIGNATURE(cls) -> int:
        ...
    
    @classmethod
    @property
    def RESOUCE_BLOCK_ME_SA_SIGNATURE(cls) -> int:
        ...
    
    @property
    def digest(self) -> bytes:
        '''Gets the digest.'''
        ...
    
    @digest.setter
    def digest(self, value : bytes):
        '''Sets the digest.'''
        ...
    
    ...

class ColorHalftoneInformationResource(aspose.psd.fileformats.psd.ResourceBlock):
    '''Halftoning resource'''
    
    def save(self, stream : aspose.psd.StreamContainer):
        '''Saves the resource block to the specified stream.
        
        :param stream: The stream to save the resource block to.'''
        ...
    
    def validate_values(self):
        '''Validates the resource values.'''
        ...
    
    @property
    def signature(self) -> int:
        '''Gets the resource signature. Should be always '8BIM'.'''
        ...
    
    @property
    def id(self) -> int:
        '''Gets the unique identifier for the resource.'''
        ...
    
    @id.setter
    def id(self, value : int):
        '''Sets the unique identifier for the resource.'''
        ...
    
    @property
    def name(self) -> str:
        '''Gets the resource name. Pascal string, padded to make the size even (a null name consists of two bytes of 0).'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Sets the resource name. Pascal string, padded to make the size even (a null name consists of two bytes of 0).'''
        ...
    
    @property
    def data_size(self) -> int:
        ...
    
    @property
    def size(self) -> int:
        '''Gets the resource block size in bytes including its data.'''
        ...
    
    @property
    def minimal_version(self) -> int:
        ...
    
    @classmethod
    @property
    def RESOUCE_BLOCK_SIGNATURE(cls) -> int:
        ...
    
    @classmethod
    @property
    def RESOUCE_BLOCK_ME_SA_SIGNATURE(cls) -> int:
        ...
    
    @property
    def halftone_data(self) -> bytes:
        ...
    
    @halftone_data.setter
    def halftone_data(self, value : bytes):
        ...
    
    ...

class ColorTransferFunctionsResource(aspose.psd.fileformats.psd.ResourceBlock):
    '''Color transfer resource'''
    
    def save(self, stream : aspose.psd.StreamContainer):
        '''Saves the resource block to the specified stream.
        
        :param stream: The stream to save the resource block to.'''
        ...
    
    def validate_values(self):
        '''Validates the resource values.'''
        ...
    
    @property
    def signature(self) -> int:
        '''Gets the resource signature. Should be always '8BIM'.'''
        ...
    
    @property
    def id(self) -> int:
        '''Gets the unique identifier for the resource.'''
        ...
    
    @id.setter
    def id(self, value : int):
        '''Sets the unique identifier for the resource.'''
        ...
    
    @property
    def name(self) -> str:
        '''Gets the resource name. Pascal string, padded to make the size even (a null name consists of two bytes of 0).'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Sets the resource name. Pascal string, padded to make the size even (a null name consists of two bytes of 0).'''
        ...
    
    @property
    def data_size(self) -> int:
        ...
    
    @property
    def size(self) -> int:
        '''Gets the resource block size in bytes including its data.'''
        ...
    
    @property
    def minimal_version(self) -> int:
        ...
    
    @classmethod
    @property
    def RESOUCE_BLOCK_SIGNATURE(cls) -> int:
        ...
    
    @classmethod
    @property
    def RESOUCE_BLOCK_ME_SA_SIGNATURE(cls) -> int:
        ...
    
    @property
    def color_transfer_data(self) -> bytes:
        ...
    
    @color_transfer_data.setter
    def color_transfer_data(self, value : bytes):
        ...
    
    ...

class DocumentSpecificIdsResource(aspose.psd.fileformats.psd.ResourceBlock):
    '''Document Specific Ids resource'''
    
    def save(self, stream : aspose.psd.StreamContainer):
        '''Saves the resource block to the specified stream.
        
        :param stream: The stream to save the resource block to.'''
        ...
    
    def validate_values(self):
        '''Validates the resource values.'''
        ...
    
    @property
    def signature(self) -> int:
        '''Gets the resource signature. Should be always '8BIM'.'''
        ...
    
    @property
    def id(self) -> int:
        '''Gets the identifier.'''
        ...
    
    @id.setter
    def id(self, value : int):
        '''Sets the identifier.'''
        ...
    
    @property
    def name(self) -> str:
        '''Gets the resource name. Pascal string, padded to make the size even (a null name consists of two bytes of 0).'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Sets the resource name. Pascal string, padded to make the size even (a null name consists of two bytes of 0).'''
        ...
    
    @property
    def data_size(self) -> int:
        ...
    
    @property
    def size(self) -> int:
        '''Gets the resource block size in bytes including its data.'''
        ...
    
    @property
    def minimal_version(self) -> int:
        ...
    
    @classmethod
    @property
    def RESOUCE_BLOCK_SIGNATURE(cls) -> int:
        ...
    
    @classmethod
    @property
    def RESOUCE_BLOCK_ME_SA_SIGNATURE(cls) -> int:
        ...
    
    ...

class FixedPointDecimal:
    '''Fixed-point decimal, with 16-bit integer and 16-bit fraction.'''
    
    def to_double(self) -> float:
        '''Converts current fixed point decimal to double.
        
        :returns: The converted value.'''
        ...
    
    @property
    def integer(self) -> int:
        '''Gets the integer.'''
        ...
    
    @integer.setter
    def integer(self, value : int):
        '''Sets the integer.'''
        ...
    
    @property
    def fraction(self) -> int:
        '''Gets the fraction.'''
        ...
    
    @fraction.setter
    def fraction(self, value : int):
        '''Sets the fraction.'''
        ...
    
    ...

class GlobalAltitudeResource(aspose.psd.fileformats.psd.ResourceBlock):
    '''Global altitude resource'''
    
    def save(self, stream : aspose.psd.StreamContainer):
        '''Saves the resource block to the specified stream.
        
        :param stream: The stream to save the resource block to.'''
        ...
    
    def validate_values(self):
        '''Validates the resource values.'''
        ...
    
    @property
    def signature(self) -> int:
        '''Gets the resource signature. Should be always '8BIM'.'''
        ...
    
    @property
    def id(self) -> int:
        '''Gets the unique identifier for the resource.'''
        ...
    
    @id.setter
    def id(self, value : int):
        '''Sets the unique identifier for the resource.'''
        ...
    
    @property
    def name(self) -> str:
        '''Gets the resource name. Pascal string, padded to make the size even (a null name consists of two bytes of 0).'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Sets the resource name. Pascal string, padded to make the size even (a null name consists of two bytes of 0).'''
        ...
    
    @property
    def data_size(self) -> int:
        ...
    
    @property
    def size(self) -> int:
        '''Gets the resource block size in bytes including its data.'''
        ...
    
    @property
    def minimal_version(self) -> int:
        ...
    
    @classmethod
    @property
    def RESOUCE_BLOCK_SIGNATURE(cls) -> int:
        ...
    
    @classmethod
    @property
    def RESOUCE_BLOCK_ME_SA_SIGNATURE(cls) -> int:
        ...
    
    @property
    def altitude(self) -> int:
        '''Gets the altitude.'''
        ...
    
    @altitude.setter
    def altitude(self, value : int):
        '''Sets the altitude.'''
        ...
    
    ...

class GlobalAngleResource(aspose.psd.fileformats.psd.ResourceBlock):
    '''Global angle resource'''
    
    def save(self, stream : aspose.psd.StreamContainer):
        '''Saves the resource block to the specified stream.
        
        :param stream: The stream to save the resource block to.'''
        ...
    
    def validate_values(self):
        '''Validates the resource values.'''
        ...
    
    @property
    def signature(self) -> int:
        '''Gets the resource signature. Should be always '8BIM'.'''
        ...
    
    @property
    def id(self) -> int:
        '''Gets the unique identifier for the resource.'''
        ...
    
    @id.setter
    def id(self, value : int):
        '''Sets the unique identifier for the resource.'''
        ...
    
    @property
    def name(self) -> str:
        '''Gets the resource name. Pascal string, padded to make the size even (a null name consists of two bytes of 0).'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Sets the resource name. Pascal string, padded to make the size even (a null name consists of two bytes of 0).'''
        ...
    
    @property
    def data_size(self) -> int:
        ...
    
    @property
    def size(self) -> int:
        '''Gets the resource block size in bytes including its data.'''
        ...
    
    @property
    def minimal_version(self) -> int:
        ...
    
    @classmethod
    @property
    def RESOUCE_BLOCK_SIGNATURE(cls) -> int:
        ...
    
    @classmethod
    @property
    def RESOUCE_BLOCK_ME_SA_SIGNATURE(cls) -> int:
        ...
    
    @property
    def global_angle(self) -> int:
        ...
    
    @global_angle.setter
    def global_angle(self, value : int):
        ...
    
    ...

class GridAndGuidesResouce(aspose.psd.fileformats.psd.ResourceBlock):
    '''Represents the grid and guides resource.'''
    
    def save(self, stream : aspose.psd.StreamContainer):
        '''Saves the resource block to the specified stream.
        
        :param stream: The stream to save the resource block to.'''
        ...
    
    def validate_values(self):
        '''Validates the resource values.'''
        ...
    
    @property
    def signature(self) -> int:
        '''Gets the resource signature. Should be always '8BIM'.'''
        ...
    
    @property
    def id(self) -> int:
        '''Gets the unique identifier for the resource.'''
        ...
    
    @id.setter
    def id(self, value : int):
        '''Sets the unique identifier for the resource.'''
        ...
    
    @property
    def name(self) -> str:
        '''Gets the resource name. Pascal string, padded to make the size even (a null name consists of two bytes of 0).'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Sets the resource name. Pascal string, padded to make the size even (a null name consists of two bytes of 0).'''
        ...
    
    @property
    def data_size(self) -> int:
        ...
    
    @property
    def size(self) -> int:
        '''Gets the resource block size in bytes including its data.'''
        ...
    
    @property
    def minimal_version(self) -> int:
        ...
    
    @classmethod
    @property
    def RESOUCE_BLOCK_SIGNATURE(cls) -> int:
        ...
    
    @classmethod
    @property
    def RESOUCE_BLOCK_ME_SA_SIGNATURE(cls) -> int:
        ...
    
    @property
    def guides(self) -> List[aspose.psd.fileformats.psd.resources.GuideResource]:
        '''Gets the guides.'''
        ...
    
    @guides.setter
    def guides(self, value : List[aspose.psd.fileformats.psd.resources.GuideResource]):
        '''Sets the guides.'''
        ...
    
    @property
    def guide_count(self) -> int:
        ...
    
    @property
    def header_version(self) -> int:
        ...
    
    @header_version.setter
    def header_version(self, value : int):
        ...
    
    @property
    def grid_cycle_x(self) -> int:
        ...
    
    @grid_cycle_x.setter
    def grid_cycle_x(self, value : int):
        ...
    
    @property
    def grid_cycle_y(self) -> int:
        ...
    
    @grid_cycle_y.setter
    def grid_cycle_y(self, value : int):
        ...
    
    ...

class GuideResource:
    '''The guide resource block.'''
    
    @property
    def location(self) -> int:
        '''Gets the location of guide in document coordinates.'''
        ...
    
    @location.setter
    def location(self, value : int):
        '''Sets the location of guide in document coordinates.'''
        ...
    
    @property
    def direction(self) -> aspose.psd.fileformats.psd.resources.GuideDirection:
        '''Gets the direction of guide.'''
        ...
    
    @direction.setter
    def direction(self, value : aspose.psd.fileformats.psd.resources.GuideDirection):
        '''Sets the direction of guide.'''
        ...
    
    @classmethod
    @property
    def GUIDE_RESOURCE_SIZE(cls) -> int:
        ...
    
    ...

class IccProfileResource(aspose.psd.fileformats.psd.ResourceBlock):
    '''Represents the ICC profile resource.'''
    
    def save(self, stream : aspose.psd.StreamContainer):
        '''Saves the resource block to the specified stream.
        
        :param stream: The stream to save the resource block to.'''
        ...
    
    def validate_values(self):
        '''Validates the resource values.'''
        ...
    
    @property
    def signature(self) -> int:
        '''Gets the resource signature. Should be always '8BIM'.'''
        ...
    
    @property
    def id(self) -> int:
        '''Gets the unique identifier for the resource.'''
        ...
    
    @id.setter
    def id(self, value : int):
        '''Sets the unique identifier for the resource.'''
        ...
    
    @property
    def name(self) -> str:
        '''Gets the resource name. Pascal string, padded to make the size even (a null name consists of two bytes of 0).'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Sets the resource name. Pascal string, padded to make the size even (a null name consists of two bytes of 0).'''
        ...
    
    @property
    def data_size(self) -> int:
        ...
    
    @property
    def size(self) -> int:
        '''Gets the resource block size in bytes including its data.'''
        ...
    
    @property
    def minimal_version(self) -> int:
        ...
    
    @classmethod
    @property
    def RESOUCE_BLOCK_SIGNATURE(cls) -> int:
        ...
    
    @classmethod
    @property
    def RESOUCE_BLOCK_ME_SA_SIGNATURE(cls) -> int:
        ...
    
    ...

class IccUntaggedResource(aspose.psd.fileformats.psd.ResourceBlock):
    '''Icc untagged resource'''
    
    def save(self, stream : aspose.psd.StreamContainer):
        '''Saves the resource block to the specified stream.
        
        :param stream: The stream to save the resource block to.'''
        ...
    
    def validate_values(self):
        '''Validates the resource values.'''
        ...
    
    @property
    def signature(self) -> int:
        '''Gets the resource signature. Should be always '8BIM'.'''
        ...
    
    @property
    def id(self) -> int:
        '''Gets the unique identifier for the resource.'''
        ...
    
    @id.setter
    def id(self, value : int):
        '''Sets the unique identifier for the resource.'''
        ...
    
    @property
    def name(self) -> str:
        '''Gets the resource name. Pascal string, padded to make the size even (a null name consists of two bytes of 0).'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Sets the resource name. Pascal string, padded to make the size even (a null name consists of two bytes of 0).'''
        ...
    
    @property
    def data_size(self) -> int:
        ...
    
    @property
    def size(self) -> int:
        '''Gets the resource block size in bytes including its data.'''
        ...
    
    @property
    def minimal_version(self) -> int:
        ...
    
    @classmethod
    @property
    def RESOUCE_BLOCK_SIGNATURE(cls) -> int:
        ...
    
    @classmethod
    @property
    def RESOUCE_BLOCK_ME_SA_SIGNATURE(cls) -> int:
        ...
    
    @property
    def profile(self) -> byte:
        '''Gets the profile.'''
        ...
    
    @profile.setter
    def profile(self, value : byte):
        '''Sets the profile.'''
        ...
    
    ...

class LayerGroupInformationResource(aspose.psd.fileformats.psd.ResourceBlock):
    '''Layer group information resource'''
    
    def save(self, stream : aspose.psd.StreamContainer):
        '''Saves the resource block to the specified stream.
        
        :param stream: The stream to save the resource block to.'''
        ...
    
    def validate_values(self):
        '''Validates the resource values.'''
        ...
    
    @property
    def signature(self) -> int:
        '''Gets the resource signature. Should be always '8BIM'.'''
        ...
    
    @property
    def id(self) -> int:
        '''Gets the unique identifier for the resource.'''
        ...
    
    @id.setter
    def id(self, value : int):
        '''Sets the unique identifier for the resource.'''
        ...
    
    @property
    def name(self) -> str:
        '''Gets the resource name. Pascal string, padded to make the size even (a null name consists of two bytes of 0).'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Sets the resource name. Pascal string, padded to make the size even (a null name consists of two bytes of 0).'''
        ...
    
    @property
    def data_size(self) -> int:
        ...
    
    @property
    def size(self) -> int:
        '''Gets the resource block size in bytes including its data.'''
        ...
    
    @property
    def minimal_version(self) -> int:
        ...
    
    @classmethod
    @property
    def RESOUCE_BLOCK_SIGNATURE(cls) -> int:
        ...
    
    @classmethod
    @property
    def RESOUCE_BLOCK_ME_SA_SIGNATURE(cls) -> int:
        ...
    
    @property
    def groups(self) -> List[int]:
        '''Gets the groups.'''
        ...
    
    @groups.setter
    def groups(self, value : List[int]):
        '''Sets the groups.'''
        ...
    
    ...

class LayerGroupsEnabledResource(aspose.psd.fileformats.psd.ResourceBlock):
    '''Layer groups enabled resource'''
    
    def save(self, stream : aspose.psd.StreamContainer):
        '''Saves the resource block to the specified stream.
        
        :param stream: The stream to save the resource block to.'''
        ...
    
    def validate_values(self):
        '''Validates the resource values.'''
        ...
    
    @property
    def signature(self) -> int:
        '''Gets the resource signature. Should be always '8BIM'.'''
        ...
    
    @property
    def id(self) -> int:
        '''Gets the unique identifier for the resource.'''
        ...
    
    @id.setter
    def id(self, value : int):
        '''Sets the unique identifier for the resource.'''
        ...
    
    @property
    def name(self) -> str:
        '''Gets the resource name. Pascal string, padded to make the size even (a null name consists of two bytes of 0).'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Sets the resource name. Pascal string, padded to make the size even (a null name consists of two bytes of 0).'''
        ...
    
    @property
    def data_size(self) -> int:
        ...
    
    @property
    def size(self) -> int:
        '''Gets the resource block size in bytes including its data.'''
        ...
    
    @property
    def minimal_version(self) -> int:
        ...
    
    @classmethod
    @property
    def RESOUCE_BLOCK_SIGNATURE(cls) -> int:
        ...
    
    @classmethod
    @property
    def RESOUCE_BLOCK_ME_SA_SIGNATURE(cls) -> int:
        ...
    
    @property
    def ds(self) -> bytes:
        ...
    
    @ds.setter
    def ds(self, value : bytes):
        ...
    
    ...

class LayerSelectionIdsResource(aspose.psd.fileformats.psd.ResourceBlock):
    '''Layer selection ids resource'''
    
    def save(self, stream : aspose.psd.StreamContainer):
        '''Saves the resource block to the specified stream.
        
        :param stream: The stream to save the resource block to.'''
        ...
    
    def validate_values(self):
        '''Validates the resource values.'''
        ...
    
    @property
    def signature(self) -> int:
        '''Gets the resource signature. Should be always '8BIM'.'''
        ...
    
    @property
    def id(self) -> int:
        '''Gets the unique identifier for the resource.'''
        ...
    
    @id.setter
    def id(self, value : int):
        '''Sets the unique identifier for the resource.'''
        ...
    
    @property
    def name(self) -> str:
        '''Gets the resource name. Pascal string, padded to make the size even (a null name consists of two bytes of 0).'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Sets the resource name. Pascal string, padded to make the size even (a null name consists of two bytes of 0).'''
        ...
    
    @property
    def data_size(self) -> int:
        ...
    
    @property
    def size(self) -> int:
        '''Gets the resource block size in bytes including its data.'''
        ...
    
    @property
    def minimal_version(self) -> int:
        ...
    
    @classmethod
    @property
    def RESOUCE_BLOCK_SIGNATURE(cls) -> int:
        ...
    
    @classmethod
    @property
    def RESOUCE_BLOCK_ME_SA_SIGNATURE(cls) -> int:
        ...
    
    @property
    def count(self) -> int:
        '''Gets the count.'''
        ...
    
    @count.setter
    def count(self, value : int):
        '''Sets the count.'''
        ...
    
    @property
    def layer_ids(self) -> List[int]:
        ...
    
    @layer_ids.setter
    def layer_ids(self, value : List[int]):
        ...
    
    ...

class LayerStateInformationResource(aspose.psd.fileformats.psd.ResourceBlock):
    '''Layer state information resource'''
    
    def save(self, stream : aspose.psd.StreamContainer):
        '''Saves the resource block to the specified stream.
        
        :param stream: The stream to save the resource block to.'''
        ...
    
    def validate_values(self):
        '''Validates the resource values.'''
        ...
    
    @property
    def signature(self) -> int:
        '''Gets the resource signature. Should be always '8BIM'.'''
        ...
    
    @property
    def id(self) -> int:
        '''Gets the unique identifier for the resource.'''
        ...
    
    @id.setter
    def id(self, value : int):
        '''Sets the unique identifier for the resource.'''
        ...
    
    @property
    def name(self) -> str:
        '''Gets the resource name. Pascal string, padded to make the size even (a null name consists of two bytes of 0).'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Sets the resource name. Pascal string, padded to make the size even (a null name consists of two bytes of 0).'''
        ...
    
    @property
    def data_size(self) -> int:
        ...
    
    @property
    def size(self) -> int:
        '''Gets the resource block size in bytes including its data.'''
        ...
    
    @property
    def minimal_version(self) -> int:
        ...
    
    @classmethod
    @property
    def RESOUCE_BLOCK_SIGNATURE(cls) -> int:
        ...
    
    @classmethod
    @property
    def RESOUCE_BLOCK_ME_SA_SIGNATURE(cls) -> int:
        ...
    
    @property
    def layer_index(self) -> int:
        ...
    
    @layer_index.setter
    def layer_index(self, value : int):
        ...
    
    ...

class PixelAspectRatioResource(aspose.psd.fileformats.psd.ResourceBlock):
    '''Pixel aspect ration resource'''
    
    def save(self, stream : aspose.psd.StreamContainer):
        '''Saves the resource block to the specified stream.
        
        :param stream: The stream to save the resource block to.'''
        ...
    
    def validate_values(self):
        '''Validates the resource values.'''
        ...
    
    @property
    def signature(self) -> int:
        '''Gets the resource signature. Should be always '8BIM'.'''
        ...
    
    @property
    def id(self) -> int:
        '''Gets the unique identifier for the resource.'''
        ...
    
    @id.setter
    def id(self, value : int):
        '''Sets the unique identifier for the resource.'''
        ...
    
    @property
    def name(self) -> str:
        '''Gets the resource name. Pascal string, padded to make the size even (a null name consists of two bytes of 0).'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Sets the resource name. Pascal string, padded to make the size even (a null name consists of two bytes of 0).'''
        ...
    
    @property
    def data_size(self) -> int:
        ...
    
    @property
    def size(self) -> int:
        '''Gets the resource block size in bytes including its data.'''
        ...
    
    @property
    def minimal_version(self) -> int:
        ...
    
    @classmethod
    @property
    def RESOUCE_BLOCK_SIGNATURE(cls) -> int:
        ...
    
    @classmethod
    @property
    def RESOUCE_BLOCK_ME_SA_SIGNATURE(cls) -> int:
        ...
    
    @property
    def version(self) -> int:
        '''Gets the version.'''
        ...
    
    @version.setter
    def version(self, value : int):
        '''Sets the version.'''
        ...
    
    @property
    def aspect_ratio(self) -> float:
        ...
    
    @aspect_ratio.setter
    def aspect_ratio(self, value : float):
        ...
    
    ...

class PrintFlagsResource(aspose.psd.fileformats.psd.ResourceBlock):
    '''Print flags resource'''
    
    def save(self, stream : aspose.psd.StreamContainer):
        '''Saves the resource block to the specified stream.
        
        :param stream: The stream to save the resource block to.'''
        ...
    
    def validate_values(self):
        '''Validates the resource values.'''
        ...
    
    @property
    def signature(self) -> int:
        '''Gets the resource signature. Should be always '8BIM'.'''
        ...
    
    @property
    def id(self) -> int:
        '''Gets the unique identifier for the resource.'''
        ...
    
    @id.setter
    def id(self, value : int):
        '''Sets the unique identifier for the resource.'''
        ...
    
    @property
    def name(self) -> str:
        '''Gets the resource name. Pascal string, padded to make the size even (a null name consists of two bytes of 0).'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Sets the resource name. Pascal string, padded to make the size even (a null name consists of two bytes of 0).'''
        ...
    
    @property
    def data_size(self) -> int:
        ...
    
    @property
    def size(self) -> int:
        '''Gets the resource block size in bytes including its data.'''
        ...
    
    @property
    def minimal_version(self) -> int:
        ...
    
    @classmethod
    @property
    def RESOUCE_BLOCK_SIGNATURE(cls) -> int:
        ...
    
    @classmethod
    @property
    def RESOUCE_BLOCK_ME_SA_SIGNATURE(cls) -> int:
        ...
    
    @property
    def version(self) -> int:
        '''Gets the version.'''
        ...
    
    @version.setter
    def version(self, value : int):
        '''Sets the version.'''
        ...
    
    @property
    def center_crop_mark(self) -> byte:
        ...
    
    @center_crop_mark.setter
    def center_crop_mark(self, value : byte):
        ...
    
    @property
    def bleed_width(self) -> int:
        ...
    
    @bleed_width.setter
    def bleed_width(self, value : int):
        ...
    
    @property
    def bleed_scale(self) -> int:
        ...
    
    @bleed_scale.setter
    def bleed_scale(self, value : int):
        ...
    
    ...

class PrintScaleResource(aspose.psd.fileformats.psd.ResourceBlock):
    '''Print Scale resource'''
    
    def save(self, stream : aspose.psd.StreamContainer):
        '''Saves the resource block to the specified stream.
        
        :param stream: The stream to save the resource block to.'''
        ...
    
    def validate_values(self):
        '''Validates the resource values.'''
        ...
    
    @property
    def signature(self) -> int:
        '''Gets the resource signature. Should be always '8BIM'.'''
        ...
    
    @property
    def id(self) -> int:
        '''Gets the unique identifier for the resource.'''
        ...
    
    @id.setter
    def id(self, value : int):
        '''Sets the unique identifier for the resource.'''
        ...
    
    @property
    def name(self) -> str:
        '''Gets the resource name. Pascal string, padded to make the size even (a null name consists of two bytes of 0).'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Sets the resource name. Pascal string, padded to make the size even (a null name consists of two bytes of 0).'''
        ...
    
    @property
    def data_size(self) -> int:
        ...
    
    @property
    def size(self) -> int:
        '''Gets the resource block size in bytes including its data.'''
        ...
    
    @property
    def minimal_version(self) -> int:
        ...
    
    @classmethod
    @property
    def RESOUCE_BLOCK_SIGNATURE(cls) -> int:
        ...
    
    @classmethod
    @property
    def RESOUCE_BLOCK_ME_SA_SIGNATURE(cls) -> int:
        ...
    
    @property
    def style(self) -> int:
        '''Gets the style.'''
        ...
    
    @style.setter
    def style(self, value : int):
        '''Sets the style.'''
        ...
    
    @property
    def x_location(self) -> float:
        ...
    
    @x_location.setter
    def x_location(self, value : float):
        ...
    
    @property
    def y_location(self) -> float:
        ...
    
    @y_location.setter
    def y_location(self, value : float):
        ...
    
    @property
    def scale(self) -> float:
        '''Gets the scale.'''
        ...
    
    @scale.setter
    def scale(self, value : float):
        '''Sets the scale.'''
        ...
    
    ...

class QuickMaskInformationResource(aspose.psd.fileformats.psd.ResourceBlock):
    '''Quick mask information resource'''
    
    def save(self, stream : aspose.psd.StreamContainer):
        '''Saves the resource block to the specified stream.
        
        :param stream: The stream to save the resource block to.'''
        ...
    
    def validate_values(self):
        '''Validates the resource values.'''
        ...
    
    @property
    def signature(self) -> int:
        '''Gets the resource signature. Should be always '8BIM'.'''
        ...
    
    @property
    def id(self) -> int:
        '''Gets the unique identifier for the resource.'''
        ...
    
    @id.setter
    def id(self, value : int):
        '''Sets the unique identifier for the resource.'''
        ...
    
    @property
    def name(self) -> str:
        '''Gets the resource name. Pascal string, padded to make the size even (a null name consists of two bytes of 0).'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Sets the resource name. Pascal string, padded to make the size even (a null name consists of two bytes of 0).'''
        ...
    
    @property
    def data_size(self) -> int:
        ...
    
    @property
    def size(self) -> int:
        '''Gets the resource block size in bytes including its data.'''
        ...
    
    @property
    def minimal_version(self) -> int:
        ...
    
    @classmethod
    @property
    def RESOUCE_BLOCK_SIGNATURE(cls) -> int:
        ...
    
    @classmethod
    @property
    def RESOUCE_BLOCK_ME_SA_SIGNATURE(cls) -> int:
        ...
    
    @property
    def channel_id(self) -> int:
        ...
    
    @channel_id.setter
    def channel_id(self, value : int):
        ...
    
    @property
    def is_mask_empty(self) -> bool:
        ...
    
    @is_mask_empty.setter
    def is_mask_empty(self, value : bool):
        ...
    
    ...

class ResolutionInfoResource(aspose.psd.fileformats.psd.ResourceBlock):
    '''The resolution info resource'''
    
    def save(self, stream : aspose.psd.StreamContainer):
        '''Saves the resource block to the specified stream.
        
        :param stream: The stream to save the resource block to.'''
        ...
    
    def validate_values(self):
        '''Validates the resource values.'''
        ...
    
    @property
    def signature(self) -> int:
        '''Gets the resource signature. Should be always '8BIM'.'''
        ...
    
    @property
    def id(self) -> int:
        '''Gets the unique identifier for the resource.'''
        ...
    
    @id.setter
    def id(self, value : int):
        '''Sets the unique identifier for the resource.'''
        ...
    
    @property
    def name(self) -> str:
        '''Gets the resource name. Pascal string, padded to make the size even (a null name consists of two bytes of 0).'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Sets the resource name. Pascal string, padded to make the size even (a null name consists of two bytes of 0).'''
        ...
    
    @property
    def data_size(self) -> int:
        ...
    
    @property
    def size(self) -> int:
        '''Gets the resource block size in bytes including its data.'''
        ...
    
    @property
    def minimal_version(self) -> int:
        ...
    
    @classmethod
    @property
    def RESOUCE_BLOCK_SIGNATURE(cls) -> int:
        ...
    
    @classmethod
    @property
    def RESOUCE_BLOCK_ME_SA_SIGNATURE(cls) -> int:
        ...
    
    @property
    def h_dpi(self) -> aspose.psd.fileformats.psd.resources.FixedPointDecimal:
        ...
    
    @h_dpi.setter
    def h_dpi(self, value : aspose.psd.fileformats.psd.resources.FixedPointDecimal):
        ...
    
    @property
    def v_dpi(self) -> aspose.psd.fileformats.psd.resources.FixedPointDecimal:
        ...
    
    @v_dpi.setter
    def v_dpi(self, value : aspose.psd.fileformats.psd.resources.FixedPointDecimal):
        ...
    
    @property
    def h_res_display_unit(self) -> aspose.psd.fileformats.psd.resources.resolutionenums.ResolutionUnit:
        ...
    
    @h_res_display_unit.setter
    def h_res_display_unit(self, value : aspose.psd.fileformats.psd.resources.resolutionenums.ResolutionUnit):
        ...
    
    @property
    def v_res_display_unit(self) -> aspose.psd.fileformats.psd.resources.resolutionenums.ResolutionUnit:
        ...
    
    @v_res_display_unit.setter
    def v_res_display_unit(self, value : aspose.psd.fileformats.psd.resources.resolutionenums.ResolutionUnit):
        ...
    
    @property
    def width_display_unit(self) -> aspose.psd.fileformats.psd.resources.resolutionenums.PhysicalUnit:
        ...
    
    @width_display_unit.setter
    def width_display_unit(self, value : aspose.psd.fileformats.psd.resources.resolutionenums.PhysicalUnit):
        ...
    
    @property
    def height_display_unit(self) -> aspose.psd.fileformats.psd.resources.resolutionenums.PhysicalUnit:
        ...
    
    @height_display_unit.setter
    def height_display_unit(self, value : aspose.psd.fileformats.psd.resources.resolutionenums.PhysicalUnit):
        ...
    
    ...

class Thumbnail4Resource(ThumbnailResource):
    '''Represents the thumbnail resource for psd 4.0.'''
    
    def save(self, stream : aspose.psd.StreamContainer):
        '''Saves the resource block to the specified stream.
        
        :param stream: The stream to save the resource block to.'''
        ...
    
    def validate_values(self):
        '''Validates the resource values.'''
        ...
    
    @property
    def signature(self) -> int:
        '''Gets the resource signature. Should be always '8BIM'.'''
        ...
    
    @property
    def id(self) -> int:
        '''Gets the unique identifier for the resource.'''
        ...
    
    @id.setter
    def id(self, value : int):
        '''Sets the unique identifier for the resource.'''
        ...
    
    @property
    def name(self) -> str:
        '''Gets the resource name. Pascal string, padded to make the size even (a null name consists of two bytes of 0).'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Sets the resource name. Pascal string, padded to make the size even (a null name consists of two bytes of 0).'''
        ...
    
    @property
    def data_size(self) -> int:
        ...
    
    @property
    def size(self) -> int:
        '''Gets the resource block size in bytes including its data.'''
        ...
    
    @property
    def minimal_version(self) -> int:
        ...
    
    @classmethod
    @property
    def RESOUCE_BLOCK_SIGNATURE(cls) -> int:
        ...
    
    @classmethod
    @property
    def RESOUCE_BLOCK_ME_SA_SIGNATURE(cls) -> int:
        ...
    
    @property
    def jpeg_options(self) -> aspose.psd.imageoptions.JpegOptions:
        ...
    
    @jpeg_options.setter
    def jpeg_options(self, value : aspose.psd.imageoptions.JpegOptions):
        ...
    
    @property
    def format(self) -> aspose.psd.fileformats.psd.resources.ThumbnailFormat:
        '''Gets the thumbnail data format.'''
        ...
    
    @format.setter
    def format(self, value : aspose.psd.fileformats.psd.resources.ThumbnailFormat):
        '''Sets the thumbnail data format.'''
        ...
    
    @property
    def width(self) -> int:
        '''Gets the width of thumbnail in pixels.'''
        ...
    
    @width.setter
    def width(self, value : int):
        '''Sets the width of thumbnail in pixels.'''
        ...
    
    @property
    def height(self) -> int:
        '''Gets the height of thumbnail in pixels.'''
        ...
    
    @height.setter
    def height(self, value : int):
        '''Sets the height of thumbnail in pixels.'''
        ...
    
    @property
    def width_bytes(self) -> int:
        ...
    
    @property
    def total_size(self) -> int:
        ...
    
    @property
    def size_after_compression(self) -> int:
        ...
    
    @property
    def bits_pixel(self) -> int:
        ...
    
    @bits_pixel.setter
    def bits_pixel(self, value : int):
        ...
    
    @property
    def planes_count(self) -> int:
        ...
    
    @planes_count.setter
    def planes_count(self, value : int):
        ...
    
    @property
    def thumbnail_argb_32_data(self) -> List[int]:
        ...
    
    @thumbnail_argb_32_data.setter
    def thumbnail_argb_32_data(self, value : List[int]):
        ...
    
    @property
    def thumbnail_data(self) -> List[aspose.psd.Color]:
        ...
    
    @thumbnail_data.setter
    def thumbnail_data(self, value : List[aspose.psd.Color]):
        ...
    
    ...

class ThumbnailResource(aspose.psd.fileformats.psd.ResourceBlock):
    '''The thumbnail resource block.'''
    
    def save(self, stream : aspose.psd.StreamContainer):
        '''Saves the resource block to the specified stream.
        
        :param stream: The stream to save the resource block to.'''
        ...
    
    def validate_values(self):
        '''Validates the resource values.'''
        ...
    
    @property
    def signature(self) -> int:
        '''Gets the resource signature. Should be always '8BIM'.'''
        ...
    
    @property
    def id(self) -> int:
        '''Gets the unique identifier for the resource.'''
        ...
    
    @id.setter
    def id(self, value : int):
        '''Sets the unique identifier for the resource.'''
        ...
    
    @property
    def name(self) -> str:
        '''Gets the resource name. Pascal string, padded to make the size even (a null name consists of two bytes of 0).'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Sets the resource name. Pascal string, padded to make the size even (a null name consists of two bytes of 0).'''
        ...
    
    @property
    def data_size(self) -> int:
        ...
    
    @property
    def size(self) -> int:
        '''Gets the resource block size in bytes including its data.'''
        ...
    
    @property
    def minimal_version(self) -> int:
        ...
    
    @classmethod
    @property
    def RESOUCE_BLOCK_SIGNATURE(cls) -> int:
        ...
    
    @classmethod
    @property
    def RESOUCE_BLOCK_ME_SA_SIGNATURE(cls) -> int:
        ...
    
    @property
    def jpeg_options(self) -> aspose.psd.imageoptions.JpegOptions:
        ...
    
    @jpeg_options.setter
    def jpeg_options(self, value : aspose.psd.imageoptions.JpegOptions):
        ...
    
    @property
    def format(self) -> aspose.psd.fileformats.psd.resources.ThumbnailFormat:
        '''Gets the thumbnail data format.'''
        ...
    
    @format.setter
    def format(self, value : aspose.psd.fileformats.psd.resources.ThumbnailFormat):
        '''Sets the thumbnail data format.'''
        ...
    
    @property
    def width(self) -> int:
        '''Gets the width of thumbnail in pixels.'''
        ...
    
    @width.setter
    def width(self, value : int):
        '''Sets the width of thumbnail in pixels.'''
        ...
    
    @property
    def height(self) -> int:
        '''Gets the height of thumbnail in pixels.'''
        ...
    
    @height.setter
    def height(self, value : int):
        '''Sets the height of thumbnail in pixels.'''
        ...
    
    @property
    def width_bytes(self) -> int:
        ...
    
    @property
    def total_size(self) -> int:
        ...
    
    @property
    def size_after_compression(self) -> int:
        ...
    
    @property
    def bits_pixel(self) -> int:
        ...
    
    @bits_pixel.setter
    def bits_pixel(self, value : int):
        ...
    
    @property
    def planes_count(self) -> int:
        ...
    
    @planes_count.setter
    def planes_count(self, value : int):
        ...
    
    @property
    def thumbnail_argb_32_data(self) -> List[int]:
        ...
    
    @thumbnail_argb_32_data.setter
    def thumbnail_argb_32_data(self, value : List[int]):
        ...
    
    @property
    def thumbnail_data(self) -> List[aspose.psd.Color]:
        ...
    
    @thumbnail_data.setter
    def thumbnail_data(self, value : List[aspose.psd.Color]):
        ...
    
    ...

class TransparencyIndexResource(aspose.psd.fileformats.psd.ResourceBlock):
    '''The transparency index resource block.'''
    
    def save(self, stream : aspose.psd.StreamContainer):
        '''Saves the resource block to the specified stream.
        
        :param stream: The stream to save the resource block to.'''
        ...
    
    def validate_values(self):
        '''Validates the resource values.'''
        ...
    
    @property
    def signature(self) -> int:
        '''Gets the resource signature. Should be always '8BIM'.'''
        ...
    
    @property
    def id(self) -> int:
        '''Gets the unique identifier for the resource.'''
        ...
    
    @id.setter
    def id(self, value : int):
        '''Sets the unique identifier for the resource.'''
        ...
    
    @property
    def name(self) -> str:
        '''Gets the resource name. Pascal string, padded to make the size even (a null name consists of two bytes of 0).'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Sets the resource name. Pascal string, padded to make the size even (a null name consists of two bytes of 0).'''
        ...
    
    @property
    def data_size(self) -> int:
        ...
    
    @property
    def size(self) -> int:
        '''Gets the resource block size in bytes including its data.'''
        ...
    
    @property
    def minimal_version(self) -> int:
        ...
    
    @classmethod
    @property
    def RESOUCE_BLOCK_SIGNATURE(cls) -> int:
        ...
    
    @classmethod
    @property
    def RESOUCE_BLOCK_ME_SA_SIGNATURE(cls) -> int:
        ...
    
    @property
    def transparency_index(self) -> int:
        ...
    
    @transparency_index.setter
    def transparency_index(self, value : int):
        ...
    
    ...

class UnicodeAlphaNamesResource(aspose.psd.fileformats.psd.ResourceBlock):
    '''Unicode alpha names resource'''
    
    def save(self, stream : aspose.psd.StreamContainer):
        '''Saves the resource block to the specified stream.
        
        :param stream: The stream to save the resource block to.'''
        ...
    
    def validate_values(self):
        '''Validates the resource values.'''
        ...
    
    @property
    def signature(self) -> int:
        '''Gets the resource signature. Should be always '8BIM'.'''
        ...
    
    @property
    def id(self) -> int:
        '''Gets the unique identifier for the resource.'''
        ...
    
    @id.setter
    def id(self, value : int):
        '''Sets the unique identifier for the resource.'''
        ...
    
    @property
    def name(self) -> str:
        '''Gets the resource name. Pascal string, padded to make the size even (a null name consists of two bytes of 0).'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Sets the resource name. Pascal string, padded to make the size even (a null name consists of two bytes of 0).'''
        ...
    
    @property
    def data_size(self) -> int:
        ...
    
    @property
    def size(self) -> int:
        '''Gets the resource block size in bytes including its data.'''
        ...
    
    @property
    def minimal_version(self) -> int:
        ...
    
    @classmethod
    @property
    def RESOUCE_BLOCK_SIGNATURE(cls) -> int:
        ...
    
    @classmethod
    @property
    def RESOUCE_BLOCK_ME_SA_SIGNATURE(cls) -> int:
        ...
    
    @property
    def alpha_names(self) -> str:
        ...
    
    @alpha_names.setter
    def alpha_names(self, value : str):
        ...
    
    ...

class UnknownResource(aspose.psd.fileformats.psd.ResourceBlock):
    '''The unknown resource. When a resource block is not recognized then this resource block is created.'''
    
    def save(self, stream : aspose.psd.StreamContainer):
        '''Saves the resource block to the specified stream.
        
        :param stream: The stream to save the resource block to.'''
        ...
    
    def validate_values(self):
        '''Validates the resource values.'''
        ...
    
    @property
    def signature(self) -> int:
        '''Gets the resource signature. Should be always '8BIM'.'''
        ...
    
    @property
    def id(self) -> int:
        '''Gets the unique identifier for the resource.'''
        ...
    
    @id.setter
    def id(self, value : int):
        '''Sets the unique identifier for the resource.'''
        ...
    
    @property
    def name(self) -> str:
        '''Gets the resource name. Pascal string, padded to make the size even (a null name consists of two bytes of 0).'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Sets the resource name. Pascal string, padded to make the size even (a null name consists of two bytes of 0).'''
        ...
    
    @property
    def data_size(self) -> int:
        ...
    
    @property
    def size(self) -> int:
        '''Gets the resource block size in bytes including its data.'''
        ...
    
    @property
    def minimal_version(self) -> int:
        ...
    
    @classmethod
    @property
    def RESOUCE_BLOCK_SIGNATURE(cls) -> int:
        ...
    
    @classmethod
    @property
    def RESOUCE_BLOCK_ME_SA_SIGNATURE(cls) -> int:
        ...
    
    @property
    def data(self) -> bytes:
        '''Gets the resource data.'''
        ...
    
    ...

class UrlListResource(aspose.psd.fileformats.psd.ResourceBlock):
    '''Url list resource'''
    
    def save(self, stream : aspose.psd.StreamContainer):
        '''Saves the resource block to the specified stream.
        
        :param stream: The stream to save the resource block to.'''
        ...
    
    def validate_values(self):
        '''Validates the resource values.'''
        ...
    
    @property
    def signature(self) -> int:
        '''Gets the resource signature. Should be always '8BIM'.'''
        ...
    
    @property
    def id(self) -> int:
        '''Gets the unique identifier for the resource.'''
        ...
    
    @id.setter
    def id(self, value : int):
        '''Sets the unique identifier for the resource.'''
        ...
    
    @property
    def name(self) -> str:
        '''Gets the resource name. Pascal string, padded to make the size even (a null name consists of two bytes of 0).'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Sets the resource name. Pascal string, padded to make the size even (a null name consists of two bytes of 0).'''
        ...
    
    @property
    def data_size(self) -> int:
        ...
    
    @property
    def size(self) -> int:
        '''Gets the resource block size in bytes including its data.'''
        ...
    
    @property
    def minimal_version(self) -> int:
        ...
    
    @classmethod
    @property
    def RESOUCE_BLOCK_SIGNATURE(cls) -> int:
        ...
    
    @classmethod
    @property
    def RESOUCE_BLOCK_ME_SA_SIGNATURE(cls) -> int:
        ...
    
    @property
    def count(self) -> int:
        '''Gets the count.'''
        ...
    
    @count.setter
    def count(self, value : int):
        '''Sets the count.'''
        ...
    
    @property
    def longs(self) -> List[int]:
        '''Gets the longs.'''
        ...
    
    @longs.setter
    def longs(self, value : List[int]):
        '''Sets the longs.'''
        ...
    
    @property
    def ids(self) -> List[int]:
        '''Gets the ids.'''
        ...
    
    @ids.setter
    def ids(self, value : List[int]):
        '''Sets the ids.'''
        ...
    
    @property
    def texts(self) -> List[str]:
        '''Gets the texts.'''
        ...
    
    @texts.setter
    def texts(self, value : List[str]):
        '''Sets the texts.'''
        ...
    
    ...

class VersionInfoResource(aspose.psd.fileformats.psd.ResourceBlock):
    '''Version Info resource'''
    
    def save(self, stream : aspose.psd.StreamContainer):
        '''Saves the resource block to the specified stream.
        
        :param stream: The stream to save the resource block to.'''
        ...
    
    def validate_values(self):
        '''Validates the resource values.'''
        ...
    
    @property
    def signature(self) -> int:
        '''Gets the resource signature. Should be always '8BIM'.'''
        ...
    
    @property
    def id(self) -> int:
        '''Gets the unique identifier for the resource.'''
        ...
    
    @id.setter
    def id(self, value : int):
        '''Sets the unique identifier for the resource.'''
        ...
    
    @property
    def name(self) -> str:
        '''Gets the resource name. Pascal string, padded to make the size even (a null name consists of two bytes of 0).'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Sets the resource name. Pascal string, padded to make the size even (a null name consists of two bytes of 0).'''
        ...
    
    @property
    def data_size(self) -> int:
        ...
    
    @property
    def size(self) -> int:
        '''Gets the resource block size in bytes including its data.'''
        ...
    
    @property
    def minimal_version(self) -> int:
        ...
    
    @classmethod
    @property
    def RESOUCE_BLOCK_SIGNATURE(cls) -> int:
        ...
    
    @classmethod
    @property
    def RESOUCE_BLOCK_ME_SA_SIGNATURE(cls) -> int:
        ...
    
    @property
    def version(self) -> int:
        '''Gets the version.'''
        ...
    
    @version.setter
    def version(self, value : int):
        '''Sets the version.'''
        ...
    
    @property
    def has_real_merged_data(self) -> bool:
        ...
    
    @has_real_merged_data.setter
    def has_real_merged_data(self, value : bool):
        ...
    
    @property
    def reader_name(self) -> str:
        ...
    
    @reader_name.setter
    def reader_name(self, value : str):
        ...
    
    @property
    def writer_name(self) -> str:
        ...
    
    @writer_name.setter
    def writer_name(self, value : str):
        ...
    
    @property
    def file_version(self) -> int:
        ...
    
    @file_version.setter
    def file_version(self, value : int):
        ...
    
    ...

class WatermarkResource(aspose.psd.fileformats.psd.ResourceBlock):
    '''Watermark resource'''
    
    def save(self, stream : aspose.psd.StreamContainer):
        '''Saves the resource block to the specified stream.
        
        :param stream: The stream to save the resource block to.'''
        ...
    
    def validate_values(self):
        '''Validates the resource values.'''
        ...
    
    @property
    def signature(self) -> int:
        '''Gets the resource signature. Should be always '8BIM'.'''
        ...
    
    @property
    def id(self) -> int:
        '''Gets the unique identifier for the resource.'''
        ...
    
    @id.setter
    def id(self, value : int):
        '''Sets the unique identifier for the resource.'''
        ...
    
    @property
    def name(self) -> str:
        '''Gets the resource name. Pascal string, padded to make the size even (a null name consists of two bytes of 0).'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Sets the resource name. Pascal string, padded to make the size even (a null name consists of two bytes of 0).'''
        ...
    
    @property
    def data_size(self) -> int:
        ...
    
    @property
    def size(self) -> int:
        '''Gets the resource block size in bytes including its data.'''
        ...
    
    @property
    def minimal_version(self) -> int:
        ...
    
    @classmethod
    @property
    def RESOUCE_BLOCK_SIGNATURE(cls) -> int:
        ...
    
    @classmethod
    @property
    def RESOUCE_BLOCK_ME_SA_SIGNATURE(cls) -> int:
        ...
    
    @property
    def is_watermark(self) -> bool:
        ...
    
    @is_watermark.setter
    def is_watermark(self, value : bool):
        ...
    
    ...

class WorkingPathResource(aspose.psd.fileformats.psd.ResourceBlock):
    '''Working path resource.'''
    
    def save(self, stream : aspose.psd.StreamContainer):
        '''Saves the resource block to the specified stream.
        
        :param stream: The stream to save the resource block to.'''
        ...
    
    def validate_values(self):
        '''Validates the resource values.'''
        ...
    
    @property
    def signature(self) -> int:
        '''Gets the resource signature. Should be always '8BIM'.'''
        ...
    
    @property
    def id(self) -> int:
        '''Gets the unique identifier for the resource.'''
        ...
    
    @id.setter
    def id(self, value : int):
        '''Sets the unique identifier for the resource.'''
        ...
    
    @property
    def name(self) -> str:
        '''Gets the resource name. Pascal string, padded to make the size even (a null name consists of two bytes of 0).'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Sets the resource name. Pascal string, padded to make the size even (a null name consists of two bytes of 0).'''
        ...
    
    @property
    def data_size(self) -> int:
        ...
    
    @property
    def size(self) -> int:
        '''Gets the resource block size in bytes including its data.'''
        ...
    
    @property
    def minimal_version(self) -> int:
        ...
    
    @classmethod
    @property
    def RESOUCE_BLOCK_SIGNATURE(cls) -> int:
        ...
    
    @classmethod
    @property
    def RESOUCE_BLOCK_ME_SA_SIGNATURE(cls) -> int:
        ...
    
    @property
    def paths(self) -> List[aspose.psd.fileformats.core.vectorpaths.VectorPathRecord]:
        '''Gets the path records.'''
        ...
    
    @paths.setter
    def paths(self, value : List[aspose.psd.fileformats.core.vectorpaths.VectorPathRecord]):
        '''Sets the path records.'''
        ...
    
    @property
    def version(self) -> int:
        '''Gets the version.'''
        ...
    
    @version.setter
    def version(self, value : int):
        '''Sets the version.'''
        ...
    
    @property
    def is_disabled(self) -> bool:
        ...
    
    @is_disabled.setter
    def is_disabled(self, value : bool):
        ...
    
    @property
    def is_not_linked(self) -> bool:
        ...
    
    @is_not_linked.setter
    def is_not_linked(self, value : bool):
        ...
    
    @property
    def is_inverted(self) -> bool:
        ...
    
    @is_inverted.setter
    def is_inverted(self, value : bool):
        ...
    
    ...

class XmpResource(aspose.psd.fileformats.psd.ResourceBlock):
    '''Represents the XMP metadata resource.'''
    
    def save(self, stream : aspose.psd.StreamContainer):
        '''Saves the resource block to the specified stream.
        
        :param stream: The stream to save the resource block to.'''
        ...
    
    def validate_values(self):
        '''Validates the resource values.'''
        ...
    
    @property
    def signature(self) -> int:
        '''Gets the resource signature. Should be always '8BIM'.'''
        ...
    
    @property
    def id(self) -> int:
        '''Gets the unique identifier for the resource.'''
        ...
    
    @id.setter
    def id(self, value : int):
        '''Sets the unique identifier for the resource.'''
        ...
    
    @property
    def name(self) -> str:
        '''Gets the resource name. Pascal string, padded to make the size even (a null name consists of two bytes of 0).'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Sets the resource name. Pascal string, padded to make the size even (a null name consists of two bytes of 0).'''
        ...
    
    @property
    def data_size(self) -> int:
        ...
    
    @property
    def size(self) -> int:
        '''Gets the resource block size in bytes including its data.'''
        ...
    
    @property
    def minimal_version(self) -> int:
        ...
    
    @classmethod
    @property
    def RESOUCE_BLOCK_SIGNATURE(cls) -> int:
        ...
    
    @classmethod
    @property
    def RESOUCE_BLOCK_ME_SA_SIGNATURE(cls) -> int:
        ...
    
    @property
    def xmp_data(self) -> aspose.psd.xmp.XmpPacketWrapper:
        ...
    
    @xmp_data.setter
    def xmp_data(self, value : aspose.psd.xmp.XmpPacketWrapper):
        ...
    
    ...

class GuideDirection:
    '''The guide direction.'''
    
    @classmethod
    @property
    def VERTICAL(cls) -> GuideDirection:
        '''Vertical guide direction.'''
        ...
    
    @classmethod
    @property
    def HORIZONTAL(cls) -> GuideDirection:
        '''Horizontal guide direction.'''
        ...
    
    ...

class ThumbnailFormat:
    '''Specifies thumbnail data format.'''
    
    @classmethod
    @property
    def K_RAW_RGB(cls) -> ThumbnailFormat:
        '''Raw RGB format.'''
        ...
    
    @classmethod
    @property
    def K_JPEG_RGB(cls) -> ThumbnailFormat:
        '''Compressed Jpeg format.'''
        ...
    
    ...

