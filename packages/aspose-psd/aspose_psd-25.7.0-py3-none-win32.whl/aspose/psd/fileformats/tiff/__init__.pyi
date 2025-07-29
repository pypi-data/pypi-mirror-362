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

class TiffDataType:
    '''The tiff data type.'''
    
    @staticmethod
    def read_tag(data_stream : aspose.psd.fileformats.tiff.filemanagement.TiffStreamReaderposition : int) -> aspose.psd.fileformats.tiff.TiffDataType:
        '''Reads the tag data.
        
        :param data_stream: The data stream.
        :param position: The tag position.
        :returns: The read tag.'''
        ...
    
    def compare_to(self, obj : any) -> int:
        '''Compares the current instance with another object of the same type and returns an integer that indicates whether the current instance precedes, follows, or occurs in the same position in the sort order as the other object.
        
        :param obj: An object to compare with this instance.
        :returns: A 32-bit signed integer that indicates the relative order of the objects being compared. The return value has these meanings:
        Value
        Meaning
        Less than zero
        This instance is less than ``obj``.
        Zero
        This instance is equal to ``obj``.
        Greater than zero
        This instance is greater than ``obj``.'''
        ...
    
    def deep_clone(self) -> aspose.psd.fileformats.tiff.TiffDataType:
        '''Performs a deep clone of this instance.
        
        :returns: A deep clone of the current instance.'''
        ...
    
    def write_tag(self, data_stream : aspose.psd.fileformats.tiff.filemanagement.TiffStreamWriter, additional_data_offset : int):
        '''Writes the tag data.
        
        :param data_stream: The data stream.
        :param additional_data_offset: The offset to write additional data to.'''
        ...
    
    def write_additional_data(self, data_stream : aspose.psd.fileformats.tiff.filemanagement.TiffStreamWriter) -> int:
        '''Writes the additional tag data.
        
        :param data_stream: The data stream.
        :returns: The actual bytes written.'''
        ...
    
    @property
    def count(self) -> int:
        '''Gets the count of elements.'''
        ...
    
    @property
    def id(self) -> int:
        '''Gets tag id integer representation.'''
        ...
    
    @property
    def tag_id(self) -> aspose.psd.fileformats.tiff.enums.TiffTags:
        ...
    
    @property
    def tag_type(self) -> aspose.psd.fileformats.tiff.enums.TiffDataTypes:
        ...
    
    @property
    def aligned_data_size(self) -> int:
        ...
    
    @property
    def data_size(self) -> int:
        ...
    
    @property
    def value(self) -> any:
        '''Gets the value this data type contains.'''
        ...
    
    @value.setter
    def value(self, value : any):
        '''Sets the value this data type contains.'''
        ...
    
    @property
    def is_valid(self) -> bool:
        ...
    
    ...

class TiffExifIfd:
    '''The TIFF Exif image file directory class.'''
    
    @property
    def has_value(self) -> bool:
        ...
    
    @property
    def offset(self) -> int:
        '''Gets the pointer to EXIF IFD.'''
        ...
    
    @offset.setter
    def offset(self, value : int):
        '''Sets the pointer to EXIF IFD.'''
        ...
    
    ...

class TiffRational:
    '''The tiff rational type.'''
    
    @overload
    @staticmethod
    def approximate_fraction(value : floatepsilon : float) -> aspose.psd.fileformats.tiff.TiffRational:
        '''Approximates the provided value to a fraction.
        
        :param value: The value.
        :param epsilon: The error allowed.
        :returns: A rational number having error less than ``epsilon``.'''
        ...
    
    @overload
    @staticmethod
    def approximate_fraction(value : float) -> aspose.psd.fileformats.tiff.TiffRational:
        '''Approximates the provided value to a fraction.
        
        :param value: The value.
        :returns: A rational number having error less than :py:attr:`aspose.psd.fileformats.tiff.TiffRational.EPSILON`.'''
        ...
    
    @overload
    @staticmethod
    def approximate_fraction(value : floatepsilon : float) -> aspose.psd.fileformats.tiff.TiffRational:
        '''Approximates the provided value to a fraction.
        
        :param value: The value.
        :param epsilon: The error allowed.
        :returns: A rational number having error less than ``epsilon``.'''
        ...
    
    @overload
    @staticmethod
    def approximate_fraction(value : float) -> aspose.psd.fileformats.tiff.TiffRational:
        '''Approximates the provided value to a fraction.
        
        :param value: The value.
        :returns: A rational number having error less than :py:attr:`aspose.psd.fileformats.tiff.TiffRational.EPSILON`.'''
        ...
    
    @property
    def denominator(self) -> int:
        '''Gets the denominator.'''
        ...
    
    @property
    def nominator(self) -> int:
        '''Gets the nominator.'''
        ...
    
    @property
    def value(self) -> float:
        '''Gets the float value.'''
        ...
    
    @property
    def value_d(self) -> float:
        ...
    
    @classmethod
    @property
    def EPSILON(cls) -> float:
        '''The epsilon for fraction calculation'''
        ...
    
    ...

class TiffSRational:
    '''The tiff rational type.'''
    
    @overload
    @staticmethod
    def approximate_fraction(value : floatepsilon : float) -> aspose.psd.fileformats.tiff.TiffSRational:
        '''Approximates the provided value to a fraction.
        
        :param value: The value.
        :param epsilon: The error allowed.
        :returns: A rational number having error less than ``epsilon``.'''
        ...
    
    @overload
    @staticmethod
    def approximate_fraction(value : float) -> aspose.psd.fileformats.tiff.TiffSRational:
        '''Approximates the provided value to a fraction.
        
        :param value: The value.
        :returns: A rational number having error less than :py:attr:`aspose.psd.fileformats.tiff.TiffSRational.EPSILON`.'''
        ...
    
    @overload
    @staticmethod
    def approximate_fraction(value : floatepsilon : float) -> aspose.psd.fileformats.tiff.TiffSRational:
        '''Approximates the provided value to a fraction.
        
        :param value: The value.
        :param epsilon: The error allowed.
        :returns: A rational number having error less than ``epsilon``.'''
        ...
    
    @overload
    @staticmethod
    def approximate_fraction(value : float) -> aspose.psd.fileformats.tiff.TiffSRational:
        '''Approximates the provided value to a fraction.
        
        :param value: The value.
        :returns: A rational number having error less than :py:attr:`aspose.psd.fileformats.tiff.TiffSRational.EPSILON`.'''
        ...
    
    @property
    def denominator(self) -> int:
        '''Gets the denominator.'''
        ...
    
    @property
    def nominator(self) -> int:
        '''Gets the nominator.'''
        ...
    
    @property
    def value(self) -> float:
        '''Gets the float value.'''
        ...
    
    @property
    def value_d(self) -> float:
        ...
    
    @classmethod
    @property
    def EPSILON(cls) -> float:
        '''The epsilon for fraction calculation'''
        ...
    
    ...

