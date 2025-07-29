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

class BigRectangularFilterOptions(FilterOptionsBase):
    '''Big Rectangular Filter Options'''
    
    ...

class BilateralSmoothingFilterOptions(FilterOptionsBase):
    '''The Bilateral Smoothing Filter Options.'''
    
    @property
    def size(self) -> int:
        '''Gets the size of the kernel.'''
        ...
    
    @size.setter
    def size(self, value : int):
        '''Sets the size of the kernel.'''
        ...
    
    @property
    def spatial_factor(self) -> float:
        ...
    
    @spatial_factor.setter
    def spatial_factor(self, value : float):
        ...
    
    @property
    def spatial_power(self) -> float:
        ...
    
    @spatial_power.setter
    def spatial_power(self, value : float):
        ...
    
    @property
    def color_factor(self) -> float:
        ...
    
    @color_factor.setter
    def color_factor(self, value : float):
        ...
    
    @property
    def color_power(self) -> float:
        ...
    
    @color_power.setter
    def color_power(self, value : float):
        ...
    
    ...

class ConvolutionFilterOptions(FilterOptionsBase):
    '''The convolution filter.'''
    
    @property
    def factor(self) -> float:
        '''Gets the factor.'''
        ...
    
    @factor.setter
    def factor(self, value : float):
        '''Sets the factor.'''
        ...
    
    @property
    def bias(self) -> int:
        '''Gets the bias.'''
        ...
    
    @bias.setter
    def bias(self, value : int):
        '''Sets the bias.'''
        ...
    
    ...

class DeconvolutionFilterOptions(FilterOptionsBase):
    '''Deconvolution Filter Options, abstract class'''
    
    @property
    def snr(self) -> float:
        '''Gets the SNR(signal-to-noise ratio)
        recommended range 0.002 - 0.009, default value = 0.007'''
        ...
    
    @snr.setter
    def snr(self, value : float):
        '''Sets the SNR(signal-to-noise ratio)
        recommended range 0.002 - 0.009, default value = 0.007'''
        ...
    
    @property
    def brightness(self) -> float:
        '''Gets the brightness.
        recommended range 1 - 1.5
        default value = 1.15'''
        ...
    
    @brightness.setter
    def brightness(self, value : float):
        '''Sets the brightness.
        recommended range 1 - 1.5
        default value = 1.15'''
        ...
    
    @property
    def grayscale(self) -> bool:
        '''Gets a value indicating whether this :py:class:`aspose.psd.imagefilters.filteroptions.DeconvolutionFilterOptions` is grayscale.
        Return grayscale mode or RGB mode.'''
        ...
    
    @grayscale.setter
    def grayscale(self, value : bool):
        '''Sets a value indicating whether this :py:class:`aspose.psd.imagefilters.filteroptions.DeconvolutionFilterOptions` is grayscale.
        Return grayscale mode or RGB mode.'''
        ...
    
    @property
    def is_partial_loaded(self) -> bool:
        ...
    
    ...

class FilterOptionsBase:
    '''Filter Options Base, abstract class'''
    
    ...

class GaussWienerFilterOptions(DeconvolutionFilterOptions):
    '''Gauss Wiener Filter Options
    Deblur gauss'''
    
    @property
    def snr(self) -> float:
        '''Gets the SNR(signal-to-noise ratio)
        recommended range 0.002 - 0.009, default value = 0.007'''
        ...
    
    @snr.setter
    def snr(self, value : float):
        '''Sets the SNR(signal-to-noise ratio)
        recommended range 0.002 - 0.009, default value = 0.007'''
        ...
    
    @property
    def brightness(self) -> float:
        '''Gets the brightness.
        recommended range 1 - 1.5
        default value = 1.15'''
        ...
    
    @brightness.setter
    def brightness(self, value : float):
        '''Sets the brightness.
        recommended range 1 - 1.5
        default value = 1.15'''
        ...
    
    @property
    def grayscale(self) -> bool:
        '''Gets a value indicating whether this :py:class:`aspose.psd.imagefilters.filteroptions.DeconvolutionFilterOptions` is grayscale.
        Return grayscale mode or RGB mode.'''
        ...
    
    @grayscale.setter
    def grayscale(self, value : bool):
        '''Sets a value indicating whether this :py:class:`aspose.psd.imagefilters.filteroptions.DeconvolutionFilterOptions` is grayscale.
        Return grayscale mode or RGB mode.'''
        ...
    
    @property
    def is_partial_loaded(self) -> bool:
        ...
    
    @property
    def radius(self) -> int:
        '''Gets the radius.'''
        ...
    
    @radius.setter
    def radius(self, value : int):
        '''Sets the radius.'''
        ...
    
    @property
    def smooth(self) -> float:
        '''Gets the smooth.'''
        ...
    
    @smooth.setter
    def smooth(self, value : float):
        '''Sets the smooth.'''
        ...
    
    ...

class GaussianBlurFilterOptions(ConvolutionFilterOptions):
    '''The Gaussian blur'''
    
    @property
    def factor(self) -> float:
        '''Gets the factor.'''
        ...
    
    @factor.setter
    def factor(self, value : float):
        '''Sets the factor.'''
        ...
    
    @property
    def bias(self) -> int:
        '''Gets the bias.'''
        ...
    
    @bias.setter
    def bias(self, value : int):
        '''Sets the bias.'''
        ...
    
    @property
    def radius(self) -> int:
        '''Gets the radius.'''
        ...
    
    @radius.setter
    def radius(self, value : int):
        '''Sets the radius.'''
        ...
    
    @property
    def sigma(self) -> float:
        '''Gets the sigma.'''
        ...
    
    @sigma.setter
    def sigma(self, value : float):
        '''Sets the sigma.'''
        ...
    
    ...

class MedianFilterOptions(FilterOptionsBase):
    '''Median filter'''
    
    @property
    def size(self) -> int:
        '''Gets the size.'''
        ...
    
    @size.setter
    def size(self, value : int):
        '''Sets the size.'''
        ...
    
    ...

class MotionWienerFilterOptions(DeconvolutionFilterOptions):
    '''Deconvolution filter options
    deblur motion'''
    
    @property
    def snr(self) -> float:
        '''Gets the SNR(signal-to-noise ratio)
        recommended range 0.002 - 0.009, default value = 0.007'''
        ...
    
    @snr.setter
    def snr(self, value : float):
        '''Sets the SNR(signal-to-noise ratio)
        recommended range 0.002 - 0.009, default value = 0.007'''
        ...
    
    @property
    def brightness(self) -> float:
        '''Gets the brightness.
        recommended range 1 - 1.5
        default value = 1.15'''
        ...
    
    @brightness.setter
    def brightness(self, value : float):
        '''Sets the brightness.
        recommended range 1 - 1.5
        default value = 1.15'''
        ...
    
    @property
    def grayscale(self) -> bool:
        '''Gets a value indicating whether this :py:class:`aspose.psd.imagefilters.filteroptions.DeconvolutionFilterOptions` is grayscale.
        Return grayscale mode or RGB mode.'''
        ...
    
    @grayscale.setter
    def grayscale(self, value : bool):
        '''Sets a value indicating whether this :py:class:`aspose.psd.imagefilters.filteroptions.DeconvolutionFilterOptions` is grayscale.
        Return grayscale mode or RGB mode.'''
        ...
    
    @property
    def is_partial_loaded(self) -> bool:
        ...
    
    @property
    def length(self) -> int:
        '''Gets the length.'''
        ...
    
    @length.setter
    def length(self, value : int):
        '''Sets the length.'''
        ...
    
    @property
    def smooth(self) -> float:
        '''Gets the smooth.'''
        ...
    
    @smooth.setter
    def smooth(self, value : float):
        '''Sets the smooth.'''
        ...
    
    @property
    def angle(self) -> float:
        '''Gets the angle in gradus.'''
        ...
    
    @angle.setter
    def angle(self, value : float):
        '''Sets the angle in gradus.'''
        ...
    
    ...

class SharpenFilterOptions(ConvolutionFilterOptions):
    '''The Sharpen filter options'''
    
    @property
    def factor(self) -> float:
        '''Gets the factor.'''
        ...
    
    @factor.setter
    def factor(self, value : float):
        '''Sets the factor.'''
        ...
    
    @property
    def bias(self) -> int:
        '''Gets the bias.'''
        ...
    
    @bias.setter
    def bias(self, value : int):
        '''Sets the bias.'''
        ...
    
    @property
    def size(self) -> int:
        '''Gets the size.'''
        ...
    
    @size.setter
    def size(self, value : int):
        '''Sets the size.'''
        ...
    
    @property
    def sigma(self) -> float:
        '''Gets the sigma.'''
        ...
    
    @sigma.setter
    def sigma(self, value : float):
        '''Sets the sigma.'''
        ...
    
    ...

class SmallRectangularFilterOptions(FilterOptionsBase):
    '''Small rectangular filter options'''
    
    ...

