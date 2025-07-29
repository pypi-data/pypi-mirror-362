"""The namespace contains Tiff file format stream handling classes."""
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

class TiffStreamReader:
    '''The tiff stream for handling little endian tiff file format.'''
    
    @overload
    def __init__(self, data: bytes):
        '''Initializes a new instance of the  class.
        
        :param data: The byte array data.'''
        ...
    
    @overload
    def __init__(self, data: bytes, start_index: int):
        '''Initializes a new instance of the  class.
        
        :param data: The byte array data.
        :param start_index: The start index into ``data``.'''
        ...
    
    @overload
    def __init__(self, data: bytes, start_index: int, data_length: int):
        '''Initializes a new instance of the  class.
        
        :param data: The byte array data.
        :param start_index: The start index into ``data``.
        :param data_length: Length of the data.'''
        ...
    
    @overload
    def __init__(self, stream_container: aspose.psd.StreamContainer):
        '''Initializes a new instance of the  class.
        
        :param stream_container: The stream container.'''
        ...
    
    @overload
    def read_bytes(self, array: bytes, array_index: int, position: int, count: int) -> int:
        '''Reads an array of byte values from the stream.
        
        :param array: The array to fill.
        :param array_index: The array index to start putting values to.
        :param position: The stream position to read from.
        :param count: The elements count to read.
        :returns: The array of byte values.'''
        ...
    
    @overload
    def read_bytes(self, position: int, count: int) -> bytes:
        '''Reads an array of unsigned byte values from the stream.
        
        :param position: The position to read from.
        :param count: The elements count.
        :returns: The array of unsigned byte values.'''
        ...
    
    def read_double(self, position: int) -> float:
        '''Read a single double value from the stream.
        
        :param position: The position to read from.
        :returns: The single double value.'''
        ...
    
    def read_double_array(self, position: int, count: int) -> List[float]:
        '''Reads an array of double values from the stream.
        
        :param position: The position to read from.
        :param count: The elements count.
        :returns: The array of double values.'''
        ...
    
    def read_float(self, position: int) -> float:
        '''Read a single float value from the stream.
        
        :param position: The position to read from.
        :returns: The single float value.'''
        ...
    
    def read_float_array(self, position: int, count: int) -> List[float]:
        '''Reads an array of float values from the stream.
        
        :param position: The position to read from.
        :param count: The elements count.
        :returns: The array of float values.'''
        ...
    
    def read_rational(self, position: int) -> aspose.psd.fileformats.tiff.TiffRational:
        '''Read a single rational number value from the stream.
        
        :param position: The position to read from.
        :returns: The rational number.'''
        ...
    
    def read_s_rational(self, position: int) -> aspose.psd.fileformats.tiff.TiffSRational:
        '''Read a single signed rational number value from the stream.
        
        :param position: The position to read from.
        :returns: The signed rational number.'''
        ...
    
    def read_rational_array(self, position: int, count: int) -> List[aspose.psd.fileformats.tiff.TiffRational]:
        '''Reads an array of rational values from the stream.
        
        :param position: The position to read from.
        :param count: The elements count.
        :returns: The array of rational values.'''
        ...
    
    def read_s_rational_array(self, position: int, count: int) -> List[aspose.psd.fileformats.tiff.TiffSRational]:
        '''Reads an array of signed rational values from the stream.
        
        :param position: The position to read from.
        :param count: The elements count.
        :returns: The array of signed rational values.'''
        ...
    
    def read_s_byte(self, position: int) -> sbyte:
        '''Reads signed byte data from the stream.
        
        :param position: The position to read from.
        :returns: The signed byte value.'''
        ...
    
    def read_s_byte_array(self, position: int, count: int) -> List[sbyte]:
        '''Reads an array of signed byte values from the stream.
        
        :param position: The position to read from.
        :param count: The elements count.
        :returns: The array of signed byte values.'''
        ...
    
    def read_s_long(self, position: int) -> int:
        '''Read signed integer value from the stream.
        
        :param position: The position to read from.
        :returns: A signed integer value.'''
        ...
    
    def read_s_long_array(self, position: int, count: int) -> List[int]:
        '''Reads an array of signed integer values from the stream.
        
        :param position: The position to read from.
        :param count: The elements count.
        :returns: The array of signed integer values.'''
        ...
    
    def read_s_short(self, position: int) -> int:
        '''Read signed short value from the stream.
        
        :param position: The position to read from.
        :returns: A signed short value.'''
        ...
    
    def read_s_short_array(self, position: int, count: int) -> List[int]:
        '''Reads an array of signed short values from the stream.
        
        :param position: The position to read from.
        :param count: The elements count.
        :returns: The array of signed short values.'''
        ...
    
    def read_u_long(self, position: int) -> int:
        '''Read unsigned integer value from the stream.
        
        :param position: The position to read from.
        :returns: An unsigned integer value.'''
        ...
    
    def read_u_long_array(self, position: int, count: int) -> List[int]:
        '''Reads an array of unsigned integer values from the stream.
        
        :param position: The position to read from.
        :param count: The elements count.
        :returns: The array of unsigned integer values.'''
        ...
    
    def read_u_short(self, position: int) -> int:
        '''Read unsigned short value from the stream.
        
        :param position: The position to read from.
        :returns: An unsigned short value.'''
        ...
    
    def read_u_short_array(self, position: int, count: int) -> List[int]:
        '''Reads an array of unsigned integer values from the stream.
        
        :param position: The position to read from.
        :param count: The elements count.
        :returns: The array of unsigned integer values.'''
        ...
    
    def to_stream_container(self, start_position: int) -> aspose.psd.StreamContainer:
        '''Converts the underlying data to the stream container.
        
        :param start_position: The start position to start conversion from.
        :returns: The  with converted data.'''
        ...
    
    @property
    def length(self) -> int:
        '''Gets the reader length.'''
        ...
    
    @property
    def throw_exceptions(self) -> bool:
        ...
    
    @throw_exceptions.setter
    def throw_exceptions(self, value : bool):
        ...
    
    ...

class TiffStreamWriter:
    '''Tiff stream writer.'''
    
    def __init__(self, writer: aspose.psd.StreamContainer):
        '''Initializes a new instance of the  class.
        
        :param writer: The stream writer.'''
        ...
    
    @overload
    def write(self, data: bytes, offset: int, data_length: int):
        '''Writes the specified data.
        
        :param data: The data to write.
        :param offset: The data offset.
        :param data_length: Length of the data to writer.'''
        ...
    
    @overload
    def write(self, data: bytes):
        '''Writes the specified data.
        
        :param data: The data to write.'''
        ...
    
    def write_double(self, data: float):
        '''Writes a single double value to the stream.
        
        :param data: The value to write.'''
        ...
    
    def write_double_array(self, data: List[float]):
        '''Writes an array of double values to the stream.
        
        :param data: The array to write.'''
        ...
    
    def write_float(self, data: float):
        '''Writes a single float value to the stream.
        
        :param data: The value to write.'''
        ...
    
    def write_float_array(self, data: List[float]):
        '''Writes an array of float values to the stream.
        
        :param data: The array to write.'''
        ...
    
    def write_rational(self, data: aspose.psd.fileformats.tiff.TiffRational):
        '''Writes a single rational number value to the stream.
        
        :param data: The value to write.'''
        ...
    
    def write_s_rational(self, data: aspose.psd.fileformats.tiff.TiffSRational):
        '''Writes a single signed rational number value to the stream.
        
        :param data: The value to write.'''
        ...
    
    def write_rational_array(self, data: List[aspose.psd.fileformats.tiff.TiffRational]):
        '''Writes an array of unsigned rational values to the stream.
        
        :param data: The array to write.'''
        ...
    
    def write_s_rational_array(self, data: List[aspose.psd.fileformats.tiff.TiffSRational]):
        '''Writes an array of signed rational values to the stream.
        
        :param data: The array to write.'''
        ...
    
    def write_s_byte(self, data: sbyte):
        '''Writes a single signed byte value to the stream.
        
        :param data: The value to write.'''
        ...
    
    def write_s_byte_array(self, data: List[sbyte]):
        '''Writes an array of signed byte values to the stream.
        
        :param data: The array to write.'''
        ...
    
    def write_s_long_array(self, data: List[int]):
        '''Writes an array of integer values to the stream.
        
        :param data: The array to write.'''
        ...
    
    def write_s_short(self, data: int):
        '''Writes a single short value to the stream.
        
        :param data: The value to write.'''
        ...
    
    def write_s_short_array(self, data: List[int]):
        '''Writes an array of short values to the stream.
        
        :param data: The array to write.'''
        ...
    
    def write_slong(self, data: int):
        '''Writes a single integer value to the stream.
        
        :param data: The value to write.'''
        ...
    
    def write_u_byte(self, data: byte):
        '''Writes a single byte value to the stream.
        
        :param data: The value to write.'''
        ...
    
    def write_u_long(self, data: int):
        '''Writes a single unsigned integer value to the stream.
        
        :param data: The value to write.'''
        ...
    
    def write_u_long_array(self, data: List[int]):
        '''Writes an array of unsigned integer values to the stream.
        
        :param data: The array to write.'''
        ...
    
    def write_u_short(self, data: int):
        '''Writes a single unsigned short value to the stream.
        
        :param data: The value to write.'''
        ...
    
    def write_u_short_array(self, data: List[int]):
        '''Writes an array of unsigned short values to the stream.
        
        :param data: The array to write.'''
        ...
    
    @property
    def sync_root(self) -> any:
        ...
    
    @property
    def position(self) -> int:
        '''Gets the stream position.'''
        ...
    
    @position.setter
    def position(self, value : int):
        '''Sets the stream position.'''
        ...
    
    ...

