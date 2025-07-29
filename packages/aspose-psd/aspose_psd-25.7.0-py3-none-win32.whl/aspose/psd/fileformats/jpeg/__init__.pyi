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

class JFIFData:
    '''The jfif segment.'''
    
    @property
    def density_units(self) -> aspose.psd.fileformats.jpeg.JfifDensityUnits:
        ...
    
    @density_units.setter
    def density_units(self, value : aspose.psd.fileformats.jpeg.JfifDensityUnits):
        ...
    
    @property
    def thumbnail(self) -> aspose.psd.RasterImage:
        '''Gets the thumbnail.'''
        ...
    
    @thumbnail.setter
    def thumbnail(self, value : aspose.psd.RasterImage):
        '''Sets the thumbnail.'''
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
    def x_density(self) -> int:
        ...
    
    @x_density.setter
    def x_density(self, value : int):
        ...
    
    @property
    def y_density(self) -> int:
        ...
    
    @y_density.setter
    def y_density(self, value : int):
        ...
    
    ...

class JpegLsPresetCodingParameters:
    '''Defines the JPEG-LS preset coding parameters as defined in ISO/IEC 14495-1, C.2.4.1.1.
    JPEG-LS defines a default set of parameters, but custom parameters can be used.
    When used these parameters are written into the encoded bit stream as they are needed for the decoding process.'''
    
    @property
    def maximum_sample_value(self) -> int:
        ...
    
    @maximum_sample_value.setter
    def maximum_sample_value(self, value : int):
        ...
    
    @property
    def threshold1(self) -> int:
        '''Gets the first quantization threshold value for the local gradients.'''
        ...
    
    @threshold1.setter
    def threshold1(self, value : int):
        '''Sets the first quantization threshold value for the local gradients.'''
        ...
    
    @property
    def threshold2(self) -> int:
        '''Gets the second quantization threshold value for the local gradients.'''
        ...
    
    @threshold2.setter
    def threshold2(self, value : int):
        '''Sets the second quantization threshold value for the local gradients.'''
        ...
    
    @property
    def threshold3(self) -> int:
        '''Gets the third quantization threshold value for the local gradients.'''
        ...
    
    @threshold3.setter
    def threshold3(self, value : int):
        '''Sets the third quantization threshold value for the local gradients.'''
        ...
    
    @property
    def reset_value(self) -> int:
        ...
    
    @reset_value.setter
    def reset_value(self, value : int):
        ...
    
    ...

class JfifDensityUnits:
    '''The jfif density units.'''
    
    @classmethod
    @property
    def NO_UNITS(cls) -> JfifDensityUnits:
        '''The no units.'''
        ...
    
    @classmethod
    @property
    def PIXELS_PER_INCH(cls) -> JfifDensityUnits:
        '''The pixels per inch.'''
        ...
    
    @classmethod
    @property
    def PIXELS_PER_CM(cls) -> JfifDensityUnits:
        '''The pixels per cm.'''
        ...
    
    ...

class JpegCompressionColorMode:
    '''Сolor mode for jpeg images.'''
    
    @classmethod
    @property
    def GRAYSCALE(cls) -> JpegCompressionColorMode:
        '''The Grayscale image.'''
        ...
    
    @classmethod
    @property
    def Y_CB_CR(cls) -> JpegCompressionColorMode:
        '''YCbCr image, standard option for jpeg images.'''
        ...
    
    @classmethod
    @property
    def CMYK(cls) -> JpegCompressionColorMode:
        '''4-component CMYK image.'''
        ...
    
    @classmethod
    @property
    def YCCK(cls) -> JpegCompressionColorMode:
        '''The ycck color jpeg image. Needs icc profile for saving.'''
        ...
    
    @classmethod
    @property
    def RGB(cls) -> JpegCompressionColorMode:
        '''The RGB Color mode.'''
        ...
    
    ...

class JpegCompressionMode:
    '''Compression mode for jpeg images.'''
    
    @classmethod
    @property
    def BASELINE(cls) -> JpegCompressionMode:
        '''The baseline compression.'''
        ...
    
    @classmethod
    @property
    def PROGRESSIVE(cls) -> JpegCompressionMode:
        '''The progressive compression.'''
        ...
    
    @classmethod
    @property
    def LOSSLESS(cls) -> JpegCompressionMode:
        '''The lossless compression.'''
        ...
    
    @classmethod
    @property
    def JPEG_LS(cls) -> JpegCompressionMode:
        '''The JPEG-LS compression.'''
        ...
    
    ...

class JpegLsInterleaveMode:
    '''Defines the interleave mode for multi-component (color) pixel data.'''
    
    @classmethod
    @property
    def NONE(cls) -> JpegLsInterleaveMode:
        '''The data is encoded and stored as component for component: RRRGGGBBB.'''
        ...
    
    @classmethod
    @property
    def LINE(cls) -> JpegLsInterleaveMode:
        '''The interleave mode is by line. A full line of each component is encoded before moving to the next line.'''
        ...
    
    @classmethod
    @property
    def SAMPLE(cls) -> JpegLsInterleaveMode:
        '''The data is encoded and stored by sample. For color images this is the format like RGBRGBRGB.'''
        ...
    
    ...

class SampleRoundingMode:
    '''Defines a way in which an n-bit value is converted to an 8-bit value.'''
    
    @classmethod
    @property
    def EXTRAPOLATE(cls) -> SampleRoundingMode:
        '''Extrapolate an 8-bit value to fit it into n bits, where 1 < n < 8.
        The number of all possible 8-bit values is 1 << 8 = 256, from 0 to 255.
        The number of all possible n-bit values is 1 << n, from 0 to (1 << n) - 1.
        The most reasonable n-bit value Vn corresponding to some 8-bit value V8 is equal to Vn = V8 >> (8 - n).'''
        ...
    
    @classmethod
    @property
    def TRUNCATE(cls) -> SampleRoundingMode:
        '''Truncate an 8-bit value to fit it into n bits, where 1 < n < 8.
        The number of all possible n-bit values is 1 << n, from 0 to (1 << n) - 1.
        The most reasonable n-bit value Vn corresponding to some 8-bit value V8 is equal to Vn = V8 & ((1 << n) - 1).'''
        ...
    
    ...

