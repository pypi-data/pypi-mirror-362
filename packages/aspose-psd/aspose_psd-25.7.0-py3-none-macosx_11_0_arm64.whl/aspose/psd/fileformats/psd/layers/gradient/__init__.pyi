"""The namespace handles Psd file format processing."""
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

class BaseGradient:
    '''Base gradient definition class. It contains common properties for both types of gradient (Solid and Noise).'''
    
    @property
    def gradient_name(self) -> str:
        ...
    
    @gradient_name.setter
    def gradient_name(self, value : str):
        ...
    
    @property
    def gradient_mode(self) -> aspose.psd.fileformats.psd.layers.gradient.GradientKind:
        ...
    
    ...

class NoiseGradient(BaseGradient):
    '''Noise gradient definition class.'''
    
    def __init__(self):
        ...
    
    @property
    def gradient_name(self) -> str:
        ...
    
    @gradient_name.setter
    def gradient_name(self, value : str):
        ...
    
    @property
    def gradient_mode(self) -> aspose.psd.fileformats.psd.layers.gradient.GradientKind:
        ...
    
    @property
    def rnd_number_seed(self) -> int:
        ...
    
    @rnd_number_seed.setter
    def rnd_number_seed(self, value : int):
        ...
    
    @property
    def show_transparency(self) -> bool:
        ...
    
    @show_transparency.setter
    def show_transparency(self, value : bool):
        ...
    
    @property
    def use_vector_color(self) -> bool:
        ...
    
    @use_vector_color.setter
    def use_vector_color(self, value : bool):
        ...
    
    @property
    def roughness(self) -> int:
        '''Gets the Roughness factor.'''
        ...
    
    @roughness.setter
    def roughness(self, value : int):
        '''Sets the Roughness factor.'''
        ...
    
    @property
    def color_model(self) -> aspose.psd.fileformats.psd.layers.gradient.NoiseColorModel:
        ...
    
    @color_model.setter
    def color_model(self, value : aspose.psd.fileformats.psd.layers.gradient.NoiseColorModel):
        ...
    
    @property
    def minimum_color(self) -> aspose.psd.fileformats.psd.core.rawcolor.RawColor:
        ...
    
    @minimum_color.setter
    def minimum_color(self, value : aspose.psd.fileformats.psd.core.rawcolor.RawColor):
        ...
    
    @property
    def maximum_color(self) -> aspose.psd.fileformats.psd.core.rawcolor.RawColor:
        ...
    
    @maximum_color.setter
    def maximum_color(self, value : aspose.psd.fileformats.psd.core.rawcolor.RawColor):
        ...
    
    @property
    def expansion_count(self) -> int:
        ...
    
    @expansion_count.setter
    def expansion_count(self, value : int):
        ...
    
    ...

class SolidGradient(BaseGradient):
    '''Gradient fill effect settings.'''
    
    def __init__(self):
        ...
    
    @staticmethod
    def generate_lfx_2_resource_nodes() -> List[aspose.psd.fileformats.psd.layers.layerresources.OSTypeStructure]:
        '''Generates the LFX2 resource nodes.
        
        :returns: Generated List of'''
        ...
    
    def add_color_point(self) -> aspose.psd.fileformats.psd.layers.fillsettings.GradientColorPoint:
        '''Adds the color point.
        
        :returns: Created color point'''
        ...
    
    def add_transparency_point(self) -> aspose.psd.fileformats.psd.layers.fillsettings.GradientTransparencyPoint:
        '''Adds the color point.
        
        :returns: Created transparency point'''
        ...
    
    def remove_transparency_point(self, point: aspose.psd.fileformats.psd.layers.fillsettings.IGradientTransparencyPoint):
        '''Removes the transparency point.
        
        :param point: The point.'''
        ...
    
    def remove_color_point(self, point: aspose.psd.fileformats.psd.layers.IGradientColorPoint):
        '''Removes the color point.
        
        :param point: The point.'''
        ...
    
    @property
    def gradient_name(self) -> str:
        ...
    
    @gradient_name.setter
    def gradient_name(self, value : str):
        ...
    
    @property
    def gradient_mode(self) -> aspose.psd.fileformats.psd.layers.gradient.GradientKind:
        ...
    
    @property
    def color_points(self) -> List[aspose.psd.fileformats.psd.layers.IGradientColorPoint]:
        ...
    
    @color_points.setter
    def color_points(self, value : List[aspose.psd.fileformats.psd.layers.IGradientColorPoint]):
        ...
    
    @property
    def transparency_points(self) -> List[aspose.psd.fileformats.psd.layers.fillsettings.IGradientTransparencyPoint]:
        ...
    
    @transparency_points.setter
    def transparency_points(self, value : List[aspose.psd.fileformats.psd.layers.fillsettings.IGradientTransparencyPoint]):
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
    def interpolation(self) -> int:
        '''Gets ot sets Interpolation. Determines Smoothness, when 'Gradient Type' = 'Solid'. Value range: 0-4096.'''
        ...
    
    @interpolation.setter
    def interpolation(self, value : int):
        '''Gets ot sets Interpolation. Determines Smoothness, when 'Gradient Type' = 'Solid'. Value range: 0-4096.'''
        ...
    
    ...

class GradientKind(enum.Enum):
    SOLID = enum.auto()
    '''Solid Gradient kind'''
    NOISE = enum.auto()
    '''Noise Gradient kind'''

class NoiseColorModel(enum.Enum):
    RGB = enum.auto()
    '''RGB color model.'''
    HSB = enum.auto()
    '''HSB color model.'''
    LAB = enum.auto()
    '''LAB color mdoel.'''

