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

class WarpSettings:
    '''Parameters of layer with warp'''
    
    @property
    def style(self) -> aspose.psd.fileformats.psd.layers.warp.WarpStyles:
        '''Gets style of warp'''
        ...
    
    @style.setter
    def style(self, value : aspose.psd.fileformats.psd.layers.warp.WarpStyles):
        '''Sets style of warp'''
        ...
    
    @property
    def rotate(self) -> aspose.psd.fileformats.psd.layers.warp.WarpRotates:
        '''Gets rotate value'''
        ...
    
    @rotate.setter
    def rotate(self, value : aspose.psd.fileformats.psd.layers.warp.WarpRotates):
        '''Sets rotate value'''
        ...
    
    @property
    def value(self) -> float:
        '''Gets value of warp'''
        ...
    
    @value.setter
    def value(self, value : float):
        '''Sets value of warp'''
        ...
    
    @property
    def processing_area(self) -> int:
        ...
    
    @processing_area.setter
    def processing_area(self, value : int):
        ...
    
    @property
    def bounds(self) -> aspose.psd.Rectangle:
        '''Gets bounds of warp image'''
        ...
    
    @property
    def mesh_points(self) -> List[aspose.psd.Point]:
        ...
    
    @mesh_points.setter
    def mesh_points(self, value : List[aspose.psd.Point]):
        ...
    
    ...

class WarpRotates:
    '''Types of warp rotation'''
    
    @classmethod
    @property
    def HORIZONTAL(cls) -> WarpRotates:
        '''Horizontal warp direction'''
        ...
    
    @classmethod
    @property
    def VERTICAL(cls) -> WarpRotates:
        '''Vertical warp direction'''
        ...
    
    ...

class WarpStyles:
    '''Types of support warp styles supported'''
    
    @classmethod
    @property
    def NONE(cls) -> WarpStyles:
        '''It style is set when the layer without deformation'''
        ...
    
    @classmethod
    @property
    def CUSTOM(cls) -> WarpStyles:
        '''Style with arbitrary movement of points'''
        ...
    
    @classmethod
    @property
    def ARC(cls) -> WarpStyles:
        '''Arc style of warp'''
        ...
    
    @classmethod
    @property
    def ARC_UPPER(cls) -> WarpStyles:
        '''Upper Arc style of warp'''
        ...
    
    @classmethod
    @property
    def ARC_LOWER(cls) -> WarpStyles:
        '''Lower Arc style of warp'''
        ...
    
    @classmethod
    @property
    def ARCH(cls) -> WarpStyles:
        '''Arch style of warp'''
        ...
    
    @classmethod
    @property
    def BULGE(cls) -> WarpStyles:
        '''Bulge style of warp'''
        ...
    
    @classmethod
    @property
    def FLAG(cls) -> WarpStyles:
        '''Flag style of warp'''
        ...
    
    @classmethod
    @property
    def FISH(cls) -> WarpStyles:
        '''Fish style of warp'''
        ...
    
    @classmethod
    @property
    def RISE(cls) -> WarpStyles:
        '''Rise style of warp'''
        ...
    
    @classmethod
    @property
    def WAVE(cls) -> WarpStyles:
        '''Wave style of warp'''
        ...
    
    @classmethod
    @property
    def TWIST(cls) -> WarpStyles:
        '''Twist type of warp'''
        ...
    
    @classmethod
    @property
    def SQUEEZE(cls) -> WarpStyles:
        '''Squeeze type of warp'''
        ...
    
    @classmethod
    @property
    def INFLATE(cls) -> WarpStyles:
        '''Inflate type of warp'''
        ...
    
    ...

