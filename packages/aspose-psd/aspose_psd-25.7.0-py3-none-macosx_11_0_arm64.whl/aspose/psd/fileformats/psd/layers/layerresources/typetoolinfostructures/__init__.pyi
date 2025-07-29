"""The namespace contains PSD file format type tool resource entities."""
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

class AliasStructure(aspose.psd.fileformats.psd.layers.layerresources.OSTypeStructure):
    '''The alias structure.'''
    
    def __init__(self, key_name: aspose.psd.fileformats.psd.layers.layerresources.ClassID):
        '''Initializes a new instance of the  class.
        
        :param key_name: The key name.'''
        ...
    
    def save(self, stream_container: aspose.psd.StreamContainer):
        '''Saves the structure to the specified stream container.
        
        :param stream_container: The stream container.'''
        ...
    
    def save_without_key_name(self, stream_container: aspose.psd.StreamContainer):
        '''Saves the structure to the specified stream container.
        
        :param stream_container: The stream container.'''
        ...
    
    def get_header_length(self) -> int:
        '''Gets the header length.
        
        :returns: The header length'''
        ...
    
    @property
    def key(self) -> int:
        '''Gets the structure key.'''
        ...
    
    @property
    def key_name(self) -> aspose.psd.fileformats.psd.layers.layerresources.ClassID:
        ...
    
    @key_name.setter
    def key_name(self, value : aspose.psd.fileformats.psd.layers.layerresources.ClassID):
        ...
    
    @property
    def length(self) -> int:
        '''Gets the  length in bytes.'''
        ...
    
    @property
    def data_length(self) -> int:
        ...
    
    @property
    def full_path(self) -> str:
        ...
    
    @full_path.setter
    def full_path(self, value : str):
        ...
    
    @classmethod
    @property
    def STRUCTURE_KEY(cls) -> int:
        ...
    
    ...

class BooleanStructure(aspose.psd.fileformats.psd.layers.layerresources.OSTypeStructure):
    '''The boolean structure.'''
    
    def __init__(self, key_name: aspose.psd.fileformats.psd.layers.layerresources.ClassID):
        '''Initializes a new instance of the  class.
        
        :param key_name: The key name.'''
        ...
    
    def save(self, stream_container: aspose.psd.StreamContainer):
        '''Saves the structure to the specified stream container.
        
        :param stream_container: The stream container.'''
        ...
    
    def save_without_key_name(self, stream_container: aspose.psd.StreamContainer):
        '''Saves the structure to the specified stream container.
        
        :param stream_container: The stream container.'''
        ...
    
    def get_header_length(self) -> int:
        '''Gets the header length.
        
        :returns: The header length'''
        ...
    
    @property
    def key(self) -> int:
        '''Gets the structure key.'''
        ...
    
    @property
    def key_name(self) -> aspose.psd.fileformats.psd.layers.layerresources.ClassID:
        ...
    
    @key_name.setter
    def key_name(self, value : aspose.psd.fileformats.psd.layers.layerresources.ClassID):
        ...
    
    @property
    def length(self) -> int:
        '''Gets the  length in bytes.'''
        ...
    
    @property
    def value(self) -> bool:
        '''Gets a boolean value.'''
        ...
    
    @value.setter
    def value(self, value : bool):
        '''Sets a boolean value.'''
        ...
    
    @classmethod
    @property
    def STRUCTURE_KEY(cls) -> int:
        ...
    
    ...

class ClassStructure(aspose.psd.fileformats.psd.layers.layerresources.OSTypeStructure):
    '''The class structure.'''
    
    def __init__(self, key_name: aspose.psd.fileformats.psd.layers.layerresources.ClassID, class_id: aspose.psd.fileformats.psd.layers.layerresources.ClassID, structure_key: int):
        '''Initializes a new instance of the  class.
        
        :param key_name: Name of the key.
        :param class_id: The class ID.
        :param structure_key: The structure key.'''
        ...
    
    def save(self, stream_container: aspose.psd.StreamContainer):
        '''Saves the structure to the specified stream container.
        
        :param stream_container: The stream container.'''
        ...
    
    def save_without_key_name(self, stream_container: aspose.psd.StreamContainer):
        '''Saves the structure to the specified stream container.
        
        :param stream_container: The stream container.'''
        ...
    
    def get_header_length(self) -> int:
        '''Gets the header length.
        
        :returns: The header length'''
        ...
    
    @property
    def key(self) -> int:
        '''Gets the structure key.'''
        ...
    
    @property
    def key_name(self) -> aspose.psd.fileformats.psd.layers.layerresources.ClassID:
        ...
    
    @key_name.setter
    def key_name(self, value : aspose.psd.fileformats.psd.layers.layerresources.ClassID):
        ...
    
    @property
    def length(self) -> int:
        '''Gets the  length in bytes.'''
        ...
    
    @property
    def class_id(self) -> aspose.psd.fileformats.psd.layers.layerresources.ClassID:
        ...
    
    @class_id.setter
    def class_id(self, value : aspose.psd.fileformats.psd.layers.layerresources.ClassID):
        ...
    
    @property
    def class_name(self) -> str:
        ...
    
    @class_name.setter
    def class_name(self, value : str):
        ...
    
    @classmethod
    @property
    def STRUCTURE_KEY_CLSS(cls) -> int:
        ...
    
    @classmethod
    @property
    def STRUCTURE_KEY_TYPE(cls) -> int:
        ...
    
    @classmethod
    @property
    def STRUCTURE_KEY_GLBC(cls) -> int:
        ...
    
    ...

class DescriptorStructure(aspose.psd.fileformats.psd.layers.layerresources.OSTypeStructure):
    '''The descriptor structure'''
    
    def __init__(self, key_name: aspose.psd.fileformats.psd.layers.layerresources.ClassID, class_id: aspose.psd.fileformats.psd.layers.layerresources.ClassID, class_name: str, structures: List[aspose.psd.fileformats.psd.layers.layerresources.OSTypeStructure]):
        '''Initializes a new instance of the  class.
        
        :param key_name: The key name.
        :param class_id: The class identifier.
        :param class_name: Name of the class.
        :param structures: The structures.'''
        ...
    
    def save(self, stream_container: aspose.psd.StreamContainer):
        '''Saves the structure to the specified stream container.
        
        :param stream_container: The stream container.'''
        ...
    
    def save_without_key_name(self, stream_container: aspose.psd.StreamContainer):
        '''Saves the structure to the specified stream container.
        
        :param stream_container: The stream container.'''
        ...
    
    def get_header_length(self) -> int:
        '''Gets the header length.
        
        :returns: The header length'''
        ...
    
    @property
    def key(self) -> int:
        '''Gets the structure key.'''
        ...
    
    @property
    def key_name(self) -> aspose.psd.fileformats.psd.layers.layerresources.ClassID:
        ...
    
    @key_name.setter
    def key_name(self, value : aspose.psd.fileformats.psd.layers.layerresources.ClassID):
        ...
    
    @property
    def length(self) -> int:
        '''Gets the  length in bytes.'''
        ...
    
    @property
    def class_name(self) -> str:
        ...
    
    @class_name.setter
    def class_name(self, value : str):
        ...
    
    @property
    def class_id(self) -> aspose.psd.fileformats.psd.layers.layerresources.ClassID:
        ...
    
    @class_id.setter
    def class_id(self, value : aspose.psd.fileformats.psd.layers.layerresources.ClassID):
        ...
    
    @property
    def structures(self) -> List[aspose.psd.fileformats.psd.layers.layerresources.OSTypeStructure]:
        '''Gets a copy of an array of structures.'''
        ...
    
    @structures.setter
    def structures(self, value : List[aspose.psd.fileformats.psd.layers.layerresources.OSTypeStructure]):
        '''Sets a copy of an array of structures.'''
        ...
    
    @classmethod
    @property
    def STRUCTURE_KEY(cls) -> int:
        ...
    
    ...

class DoubleStructure(aspose.psd.fileformats.psd.layers.layerresources.OSTypeStructure):
    '''The double structure.'''
    
    def __init__(self, key_name: aspose.psd.fileformats.psd.layers.layerresources.ClassID):
        '''Initializes a new instance of the  class.
        
        :param key_name: The key name.'''
        ...
    
    def save(self, stream_container: aspose.psd.StreamContainer):
        '''Saves the structure to the specified stream container.
        
        :param stream_container: The stream container.'''
        ...
    
    def save_without_key_name(self, stream_container: aspose.psd.StreamContainer):
        '''Saves the structure to the specified stream container.
        
        :param stream_container: The stream container.'''
        ...
    
    def get_header_length(self) -> int:
        '''Gets the header length.
        
        :returns: The header length'''
        ...
    
    @property
    def key(self) -> int:
        '''Gets the structure key.'''
        ...
    
    @property
    def key_name(self) -> aspose.psd.fileformats.psd.layers.layerresources.ClassID:
        ...
    
    @key_name.setter
    def key_name(self, value : aspose.psd.fileformats.psd.layers.layerresources.ClassID):
        ...
    
    @property
    def length(self) -> int:
        '''Gets the  length in bytes.'''
        ...
    
    @property
    def value(self) -> float:
        '''Gets the double value.'''
        ...
    
    @value.setter
    def value(self, value : float):
        '''Sets the double value.'''
        ...
    
    @classmethod
    @property
    def STRUCTURE_KEY(cls) -> int:
        ...
    
    ...

class EnumeratedDescriptorStructure(aspose.psd.fileformats.psd.layers.layerresources.OSTypeStructure):
    '''The enumerated descriptor structure.'''
    
    def __init__(self, key_name: aspose.psd.fileformats.psd.layers.layerresources.ClassID, type_id: aspose.psd.fileformats.psd.layers.layerresources.ClassID, enum_name: aspose.psd.fileformats.psd.layers.layerresources.ClassID):
        '''Initializes a new instance of the  class.
        
        :param key_name: The key name.
        :param type_id: The type ID.
        :param enum_name: The enum name.'''
        ...
    
    def save(self, stream_container: aspose.psd.StreamContainer):
        '''Saves the structure to the specified stream container.
        
        :param stream_container: The stream container.'''
        ...
    
    def save_without_key_name(self, stream_container: aspose.psd.StreamContainer):
        '''Saves the structure to the specified stream container.
        
        :param stream_container: The stream container.'''
        ...
    
    def get_header_length(self) -> int:
        '''Gets the header length.
        
        :returns: The header length'''
        ...
    
    @property
    def key(self) -> int:
        '''Gets the key.'''
        ...
    
    @property
    def key_name(self) -> aspose.psd.fileformats.psd.layers.layerresources.ClassID:
        ...
    
    @key_name.setter
    def key_name(self, value : aspose.psd.fileformats.psd.layers.layerresources.ClassID):
        ...
    
    @property
    def length(self) -> int:
        '''Gets the  length in bytes.'''
        ...
    
    @property
    def type_id(self) -> aspose.psd.fileformats.psd.layers.layerresources.ClassID:
        ...
    
    @type_id.setter
    def type_id(self, value : aspose.psd.fileformats.psd.layers.layerresources.ClassID):
        ...
    
    @property
    def enum_name(self) -> aspose.psd.fileformats.psd.layers.layerresources.ClassID:
        ...
    
    @enum_name.setter
    def enum_name(self, value : aspose.psd.fileformats.psd.layers.layerresources.ClassID):
        ...
    
    @classmethod
    @property
    def STRUCTURE_KEY(cls) -> int:
        ...
    
    ...

class EnumeratedReferenceStructure(EnumeratedDescriptorStructure):
    '''Enumerated reference structure.'''
    
    def __init__(self, key_name: aspose.psd.fileformats.psd.layers.layerresources.ClassID, class_id: aspose.psd.fileformats.psd.layers.layerresources.ClassID, type_id: aspose.psd.fileformats.psd.layers.layerresources.ClassID, enum_name: aspose.psd.fileformats.psd.layers.layerresources.ClassID):
        '''Initializes a new instance of the  class.
        
        :param key_name: The key name.
        :param class_id: The class ID.
        :param type_id: The type ID.
        :param enum_name: The enum name.'''
        ...
    
    def save(self, stream_container: aspose.psd.StreamContainer):
        '''Saves the structure to the specified stream container.
        
        :param stream_container: The stream container.'''
        ...
    
    def save_without_key_name(self, stream_container: aspose.psd.StreamContainer):
        '''Saves the structure to the specified stream container.
        
        :param stream_container: The stream container.'''
        ...
    
    def get_header_length(self) -> int:
        '''Gets the header length.
        
        :returns: The header length'''
        ...
    
    @property
    def key(self) -> int:
        '''Gets the key.'''
        ...
    
    @property
    def key_name(self) -> aspose.psd.fileformats.psd.layers.layerresources.ClassID:
        ...
    
    @key_name.setter
    def key_name(self, value : aspose.psd.fileformats.psd.layers.layerresources.ClassID):
        ...
    
    @property
    def length(self) -> int:
        '''Gets the  length in bytes.'''
        ...
    
    @property
    def type_id(self) -> aspose.psd.fileformats.psd.layers.layerresources.ClassID:
        ...
    
    @type_id.setter
    def type_id(self, value : aspose.psd.fileformats.psd.layers.layerresources.ClassID):
        ...
    
    @property
    def enum_name(self) -> aspose.psd.fileformats.psd.layers.layerresources.ClassID:
        ...
    
    @enum_name.setter
    def enum_name(self, value : aspose.psd.fileformats.psd.layers.layerresources.ClassID):
        ...
    
    @classmethod
    @property
    def STRUCTURE_KEY(cls) -> int:
        ...
    
    @property
    def class_name(self) -> str:
        ...
    
    @class_name.setter
    def class_name(self, value : str):
        ...
    
    @property
    def class_id(self) -> aspose.psd.fileformats.psd.layers.layerresources.ClassID:
        ...
    
    @class_id.setter
    def class_id(self, value : aspose.psd.fileformats.psd.layers.layerresources.ClassID):
        ...
    
    @classmethod
    @property
    def ENUMERATED_STRUCTURE_KEY(cls) -> int:
        ...
    
    ...

class IntegerStructure(aspose.psd.fileformats.psd.layers.layerresources.OSTypeStructure):
    '''The integer structure.'''
    
    def __init__(self, key_name: aspose.psd.fileformats.psd.layers.layerresources.ClassID):
        '''Initializes a new instance of the  class.
        
        :param key_name: The key name.'''
        ...
    
    def save(self, stream_container: aspose.psd.StreamContainer):
        '''Saves the structure to the specified stream container.
        
        :param stream_container: The stream container.'''
        ...
    
    def save_without_key_name(self, stream_container: aspose.psd.StreamContainer):
        '''Saves the structure to the specified stream container.
        
        :param stream_container: The stream container.'''
        ...
    
    def get_header_length(self) -> int:
        '''Gets the header length.
        
        :returns: The header length'''
        ...
    
    @property
    def key(self) -> int:
        '''Gets the key.'''
        ...
    
    @property
    def key_name(self) -> aspose.psd.fileformats.psd.layers.layerresources.ClassID:
        ...
    
    @key_name.setter
    def key_name(self, value : aspose.psd.fileformats.psd.layers.layerresources.ClassID):
        ...
    
    @property
    def length(self) -> int:
        '''Gets the  length in bytes.'''
        ...
    
    @property
    def value(self) -> int:
        '''Gets an integer value.'''
        ...
    
    @value.setter
    def value(self, value : int):
        '''Sets an integer value.'''
        ...
    
    @classmethod
    @property
    def STRUCTURE_KEY(cls) -> int:
        ...
    
    ...

class ListStructure(aspose.psd.fileformats.psd.layers.layerresources.OSTypeStructure):
    '''The list structure.'''
    
    def __init__(self, key_name: aspose.psd.fileformats.psd.layers.layerresources.ClassID):
        '''Initializes a new instance of the  class.
        
        :param key_name: The key name.'''
        ...
    
    def save(self, stream_container: aspose.psd.StreamContainer):
        '''Saves the structure to the specified stream container.
        
        :param stream_container: The stream container.'''
        ...
    
    def save_without_key_name(self, stream_container: aspose.psd.StreamContainer):
        '''Saves the structure to the specified stream container.
        
        :param stream_container: The stream container.'''
        ...
    
    def get_header_length(self) -> int:
        '''Gets the header length.
        
        :returns: The header length'''
        ...
    
    @property
    def key(self) -> int:
        '''Gets the structure key.'''
        ...
    
    @property
    def key_name(self) -> aspose.psd.fileformats.psd.layers.layerresources.ClassID:
        ...
    
    @key_name.setter
    def key_name(self, value : aspose.psd.fileformats.psd.layers.layerresources.ClassID):
        ...
    
    @property
    def length(self) -> int:
        '''Gets the  length in bytes.'''
        ...
    
    @property
    def items_count(self) -> int:
        ...
    
    @property
    def types(self) -> List[aspose.psd.fileformats.psd.layers.layerresources.OSTypeStructure]:
        '''Gets a copy of an array of structures.'''
        ...
    
    @types.setter
    def types(self, value : List[aspose.psd.fileformats.psd.layers.layerresources.OSTypeStructure]):
        '''Sets a copy of an array of structures.'''
        ...
    
    @classmethod
    @property
    def STRUCTURE_KEY(cls) -> int:
        ...
    
    ...

class ObjectArrayStructure(aspose.psd.fileformats.psd.layers.layerresources.OSTypeStructure):
    '''Defines the ObjectArrayStructure class that usually holds  array.
    It is used in the PSD file resources, such as PlLd Resource and SoLd Resource.'''
    
    @overload
    def __init__(self, key_name: str, class_id_name: str, structures: List[aspose.psd.fileformats.psd.layers.layerresources.OSTypeStructure]):
        '''Initializes a new instance of the  class.
        
        :param key_name: Name of the key.
        :param class_id_name: Name of the class identifier.
        :param structures: The structures.'''
        ...
    
    @overload
    def __init__(self, key: int, key_name: aspose.psd.fileformats.psd.layers.layerresources.ClassID, class_id: aspose.psd.fileformats.psd.layers.layerresources.ClassID, class_name: str, structures: List[aspose.psd.fileformats.psd.layers.layerresources.OSTypeStructure]):
        '''Initializes a new instance of the  class.
        
        :param key: The integer key.
        :param key_name: The key name.
        :param class_id: The class identifier.
        :param class_name: Name of the class.
        :param structures: The structures.'''
        ...
    
    def save(self, stream_container: aspose.psd.StreamContainer):
        '''Saves the structure to the specified stream container.
        
        :param stream_container: The stream container.'''
        ...
    
    def save_without_key_name(self, stream_container: aspose.psd.StreamContainer):
        '''Saves the structure to the specified stream container.
        
        :param stream_container: The stream container.'''
        ...
    
    def get_header_length(self) -> int:
        '''Gets the header length.
        
        :returns: The header length'''
        ...
    
    @property
    def key(self) -> int:
        '''Gets the object array structure key.'''
        ...
    
    @property
    def key_name(self) -> aspose.psd.fileformats.psd.layers.layerresources.ClassID:
        ...
    
    @key_name.setter
    def key_name(self, value : aspose.psd.fileformats.psd.layers.layerresources.ClassID):
        ...
    
    @property
    def length(self) -> int:
        '''Gets the  length in bytes.'''
        ...
    
    @property
    def structure_count(self) -> int:
        ...
    
    @property
    def class_name(self) -> str:
        ...
    
    @class_name.setter
    def class_name(self, value : str):
        ...
    
    @property
    def class_id(self) -> aspose.psd.fileformats.psd.layers.layerresources.ClassID:
        ...
    
    @class_id.setter
    def class_id(self, value : aspose.psd.fileformats.psd.layers.layerresources.ClassID):
        ...
    
    @property
    def structures(self) -> List[aspose.psd.fileformats.psd.layers.layerresources.OSTypeStructure]:
        '''Gets a copy of an array of structures.'''
        ...
    
    @structures.setter
    def structures(self, value : List[aspose.psd.fileformats.psd.layers.layerresources.OSTypeStructure]):
        '''Sets a copy of an array of structures.'''
        ...
    
    @classmethod
    @property
    def STRUCTURE_KEY(cls) -> int:
        ...
    
    ...

class OffsetStructure(aspose.psd.fileformats.psd.layers.layerresources.OSTypeStructure):
    '''The offset structure.'''
    
    def __init__(self, key_name: aspose.psd.fileformats.psd.layers.layerresources.ClassID, class_id: aspose.psd.fileformats.psd.layers.layerresources.ClassID):
        '''Initializes a new instance of the  class.
        
        :param key_name: The key name.
        :param class_id: The class ID.'''
        ...
    
    def save(self, stream_container: aspose.psd.StreamContainer):
        '''Saves the structure to the specified stream container.
        
        :param stream_container: The stream container.'''
        ...
    
    def save_without_key_name(self, stream_container: aspose.psd.StreamContainer):
        '''Saves the structure to the specified stream container.
        
        :param stream_container: The stream container.'''
        ...
    
    def get_header_length(self) -> int:
        '''Gets the header length.
        
        :returns: The header length'''
        ...
    
    @property
    def key(self) -> int:
        '''Gets the structure key.'''
        ...
    
    @property
    def key_name(self) -> aspose.psd.fileformats.psd.layers.layerresources.ClassID:
        ...
    
    @key_name.setter
    def key_name(self, value : aspose.psd.fileformats.psd.layers.layerresources.ClassID):
        ...
    
    @property
    def length(self) -> int:
        '''Gets the  length in bytes.'''
        ...
    
    @property
    def class_name(self) -> str:
        ...
    
    @class_name.setter
    def class_name(self, value : str):
        ...
    
    @property
    def class_id(self) -> aspose.psd.fileformats.psd.layers.layerresources.ClassID:
        ...
    
    @class_id.setter
    def class_id(self, value : aspose.psd.fileformats.psd.layers.layerresources.ClassID):
        ...
    
    @property
    def value(self) -> int:
        '''Gets the integer value.'''
        ...
    
    @value.setter
    def value(self, value : int):
        '''Sets the integer value.'''
        ...
    
    @classmethod
    @property
    def STRUCTURE_KEY(cls) -> int:
        ...
    
    ...

class PathStructure(aspose.psd.fileformats.psd.layers.layerresources.OSTypeStructure):
    '''The path structure.'''
    
    def __init__(self, key_name: aspose.psd.fileformats.psd.layers.layerresources.ClassID):
        '''Initializes a new instance of the  class.
        
        :param key_name: The key name.'''
        ...
    
    def save(self, stream_container: aspose.psd.StreamContainer):
        '''Saves the structure to the specified stream container.
        
        :param stream_container: The stream container.'''
        ...
    
    def save_without_key_name(self, stream_container: aspose.psd.StreamContainer):
        '''Saves the structure to the specified stream container.
        
        :param stream_container: The stream container.'''
        ...
    
    def get_header_length(self) -> int:
        '''Gets the header length.
        
        :returns: The header length'''
        ...
    
    @property
    def key(self) -> int:
        '''Gets the structure key.'''
        ...
    
    @property
    def key_name(self) -> aspose.psd.fileformats.psd.layers.layerresources.ClassID:
        ...
    
    @key_name.setter
    def key_name(self, value : aspose.psd.fileformats.psd.layers.layerresources.ClassID):
        ...
    
    @property
    def length(self) -> int:
        '''Gets the  length in bytes.'''
        ...
    
    @property
    def prefix(self) -> str:
        '''Gets the path prefix.'''
        ...
    
    @prefix.setter
    def prefix(self, value : str):
        '''Sets the path prefix.'''
        ...
    
    @property
    def path(self) -> str:
        '''Gets the path.'''
        ...
    
    @path.setter
    def path(self, value : str):
        '''Sets the path.'''
        ...
    
    @classmethod
    @property
    def STRUCTURE_KEY(cls) -> int:
        ...
    
    ...

class PropertyStructure(aspose.psd.fileformats.psd.layers.layerresources.OSTypeStructure):
    '''The property structure.'''
    
    def __init__(self, key_name: aspose.psd.fileformats.psd.layers.layerresources.ClassID, class_id: aspose.psd.fileformats.psd.layers.layerresources.ClassID, key_id: aspose.psd.fileformats.psd.layers.layerresources.ClassID):
        '''Initializes a new instance of the  class.
        
        :param key_name: Name of the key.
        :param class_id: The class ID.
        :param key_id: The key ID.'''
        ...
    
    def save(self, stream_container: aspose.psd.StreamContainer):
        '''Saves the structure to the specified stream container.
        
        :param stream_container: The stream container.'''
        ...
    
    def save_without_key_name(self, stream_container: aspose.psd.StreamContainer):
        '''Saves the structure to the specified stream container.
        
        :param stream_container: The stream container.'''
        ...
    
    def get_header_length(self) -> int:
        '''Gets the header length.
        
        :returns: The header length'''
        ...
    
    @property
    def key(self) -> int:
        '''Gets the structure key.'''
        ...
    
    @property
    def key_name(self) -> aspose.psd.fileformats.psd.layers.layerresources.ClassID:
        ...
    
    @key_name.setter
    def key_name(self, value : aspose.psd.fileformats.psd.layers.layerresources.ClassID):
        ...
    
    @property
    def length(self) -> int:
        '''Gets the  length in bytes.'''
        ...
    
    @property
    def class_name(self) -> str:
        ...
    
    @class_name.setter
    def class_name(self, value : str):
        ...
    
    @property
    def class_id(self) -> aspose.psd.fileformats.psd.layers.layerresources.ClassID:
        ...
    
    @class_id.setter
    def class_id(self, value : aspose.psd.fileformats.psd.layers.layerresources.ClassID):
        ...
    
    @property
    def key_id(self) -> aspose.psd.fileformats.psd.layers.layerresources.ClassID:
        ...
    
    @key_id.setter
    def key_id(self, value : aspose.psd.fileformats.psd.layers.layerresources.ClassID):
        ...
    
    @classmethod
    @property
    def STRUCTURE_KEY(cls) -> int:
        ...
    
    ...

class RawDataStructure(aspose.psd.fileformats.psd.layers.layerresources.OSTypeStructure):
    '''The raw data structure.'''
    
    def __init__(self, key_name: aspose.psd.fileformats.psd.layers.layerresources.ClassID):
        '''Initializes a new instance of the  class.
        
        :param key_name: The key name.'''
        ...
    
    def save(self, stream_container: aspose.psd.StreamContainer):
        '''Saves the structure to the specified stream container.
        
        :param stream_container: The stream container.'''
        ...
    
    def save_without_key_name(self, stream_container: aspose.psd.StreamContainer):
        '''Saves the structure to the specified stream container.
        
        :param stream_container: The stream container.'''
        ...
    
    def get_header_length(self) -> int:
        '''Gets the header length.
        
        :returns: The header length'''
        ...
    
    @property
    def key(self) -> int:
        '''Gets the key.'''
        ...
    
    @property
    def key_name(self) -> aspose.psd.fileformats.psd.layers.layerresources.ClassID:
        ...
    
    @key_name.setter
    def key_name(self, value : aspose.psd.fileformats.psd.layers.layerresources.ClassID):
        ...
    
    @property
    def length(self) -> int:
        '''Gets the  length in bytes.'''
        ...
    
    @property
    def data(self) -> bytes:
        '''Gets the data.'''
        ...
    
    @data.setter
    def data(self, value : bytes):
        '''Sets the data.'''
        ...
    
    @classmethod
    @property
    def STRUCTURE_KEY(cls) -> int:
        ...
    
    ...

class ReferenceStructure(aspose.psd.fileformats.psd.layers.layerresources.OSTypeStructure):
    '''The reference structure.'''
    
    def __init__(self, key_name: aspose.psd.fileformats.psd.layers.layerresources.ClassID):
        '''Initializes a new instance of the  class.
        
        :param key_name: The key name.'''
        ...
    
    def save(self, stream_container: aspose.psd.StreamContainer):
        '''Saves the structure to the specified stream container.
        
        :param stream_container: The stream container.'''
        ...
    
    def save_without_key_name(self, stream_container: aspose.psd.StreamContainer):
        '''Saves the structure to the specified stream container.
        
        :param stream_container: The stream container.'''
        ...
    
    def get_header_length(self) -> int:
        '''Gets the header length.
        
        :returns: The header length'''
        ...
    
    @property
    def key(self) -> int:
        '''Gets the structure key.'''
        ...
    
    @property
    def key_name(self) -> aspose.psd.fileformats.psd.layers.layerresources.ClassID:
        ...
    
    @key_name.setter
    def key_name(self, value : aspose.psd.fileformats.psd.layers.layerresources.ClassID):
        ...
    
    @property
    def length(self) -> int:
        '''Gets the  length in bytes.'''
        ...
    
    @property
    def items(self) -> List[aspose.psd.fileformats.psd.layers.layerresources.OSTypeStructure]:
        '''Gets a copy of an array of structures.'''
        ...
    
    @items.setter
    def items(self, value : List[aspose.psd.fileformats.psd.layers.layerresources.OSTypeStructure]):
        '''Sets a copy of an array of structures.'''
        ...
    
    @classmethod
    @property
    def STRUCTURE_KEY(cls) -> int:
        ...
    
    ...

class StringStructure(aspose.psd.fileformats.psd.layers.layerresources.OSTypeStructure):
    '''The string structure.'''
    
    @overload
    def __init__(self, key_name: aspose.psd.fileformats.psd.layers.layerresources.ClassID):
        '''Initializes a new instance of the  class.
        
        :param key_name: The key name.'''
        ...
    
    @overload
    def __init__(self, key_name: aspose.psd.fileformats.psd.layers.layerresources.ClassID, value: str):
        '''Initializes a new instance of the  class with value.
        
        :param key_name: The key name.
        :param value: The value.'''
        ...
    
    def save(self, stream_container: aspose.psd.StreamContainer):
        '''Saves the structure to the specified stream container.
        
        :param stream_container: The stream container.'''
        ...
    
    def save_without_key_name(self, stream_container: aspose.psd.StreamContainer):
        '''Saves the structure to the specified stream container.
        
        :param stream_container: The stream container.'''
        ...
    
    def get_header_length(self) -> int:
        '''Gets the header length.
        
        :returns: The header length'''
        ...
    
    @property
    def key(self) -> int:
        '''Gets the key.'''
        ...
    
    @property
    def key_name(self) -> aspose.psd.fileformats.psd.layers.layerresources.ClassID:
        ...
    
    @key_name.setter
    def key_name(self, value : aspose.psd.fileformats.psd.layers.layerresources.ClassID):
        ...
    
    @property
    def length(self) -> int:
        '''Gets the  length in bytes.'''
        ...
    
    @property
    def value(self) -> str:
        '''Gets the value.'''
        ...
    
    @value.setter
    def value(self, value : str):
        '''Sets the value.'''
        ...
    
    @classmethod
    @property
    def STRUCTURE_KEY(cls) -> int:
        ...
    
    ...

class UnitArrayStructure(aspose.psd.fileformats.psd.layers.layerresources.OSTypeStructure):
    '''Defines the UnitArrayStructure class that holds  values array and their measure unit.
    It is used in the PSD file resources, usually by .'''
    
    def __init__(self, key_name: aspose.psd.fileformats.psd.layers.layerresources.ClassID, unit_type: aspose.psd.fileformats.psd.layers.layerresources.typetoolinfostructures.UnitTypes, values: List[float]):
        '''Initializes a new instance of the  class.
        
        :param key_name: Name of the key.
        :param unit_type: Type of the unit.
        :param values: The values.'''
        ...
    
    def save(self, stream_container: aspose.psd.StreamContainer):
        '''Saves the structure to the specified stream container.
        
        :param stream_container: The stream container.'''
        ...
    
    def save_without_key_name(self, stream_container: aspose.psd.StreamContainer):
        '''Saves the structure to the specified stream container.
        
        :param stream_container: The stream container.'''
        ...
    
    def get_header_length(self) -> int:
        '''Gets the header length.
        
        :returns: The header length'''
        ...
    
    @property
    def key(self) -> int:
        '''Gets this unit array structure key.'''
        ...
    
    @property
    def key_name(self) -> aspose.psd.fileformats.psd.layers.layerresources.ClassID:
        ...
    
    @key_name.setter
    def key_name(self, value : aspose.psd.fileformats.psd.layers.layerresources.ClassID):
        ...
    
    @property
    def length(self) -> int:
        '''Gets the  length in bytes.'''
        ...
    
    @property
    def unit_type(self) -> aspose.psd.fileformats.psd.layers.layerresources.typetoolinfostructures.UnitTypes:
        ...
    
    @unit_type.setter
    def unit_type(self, value : aspose.psd.fileformats.psd.layers.layerresources.typetoolinfostructures.UnitTypes):
        ...
    
    @property
    def value_count(self) -> int:
        ...
    
    @property
    def values(self) -> List[float]:
        '''Gets the unit array structure values.'''
        ...
    
    @values.setter
    def values(self, value : List[float]):
        '''Sets the unit array structure values.'''
        ...
    
    @classmethod
    @property
    def STRUCTURE_KEY(cls) -> int:
        ...
    
    ...

class UnitStructure(aspose.psd.fileformats.psd.layers.layerresources.OSTypeStructure):
    '''The unit structure.'''
    
    def __init__(self, key_name: aspose.psd.fileformats.psd.layers.layerresources.ClassID):
        '''Initializes a new instance of the  class.
        
        :param key_name: The key name.'''
        ...
    
    def save(self, stream_container: aspose.psd.StreamContainer):
        '''Saves the structure to the specified stream container.
        
        :param stream_container: The stream container.'''
        ...
    
    def save_without_key_name(self, stream_container: aspose.psd.StreamContainer):
        '''Saves the structure to the specified stream container.
        
        :param stream_container: The stream container.'''
        ...
    
    def get_header_length(self) -> int:
        '''Gets the header length.
        
        :returns: The header length'''
        ...
    
    @property
    def key(self) -> int:
        '''Gets the structure key.'''
        ...
    
    @property
    def key_name(self) -> aspose.psd.fileformats.psd.layers.layerresources.ClassID:
        ...
    
    @key_name.setter
    def key_name(self, value : aspose.psd.fileformats.psd.layers.layerresources.ClassID):
        ...
    
    @property
    def length(self) -> int:
        '''Gets the  length in bytes.'''
        ...
    
    @property
    def unit_type(self) -> aspose.psd.fileformats.psd.layers.layerresources.typetoolinfostructures.UnitTypes:
        ...
    
    @unit_type.setter
    def unit_type(self, value : aspose.psd.fileformats.psd.layers.layerresources.typetoolinfostructures.UnitTypes):
        ...
    
    @property
    def value(self) -> float:
        '''Gets the value.'''
        ...
    
    @value.setter
    def value(self, value : float):
        '''Sets the value.'''
        ...
    
    @classmethod
    @property
    def STRUCTURE_KEY(cls) -> int:
        ...
    
    ...

class UnknownStructure(aspose.psd.fileformats.psd.layers.layerresources.OSTypeStructure):
    '''The unknown structure.'''
    
    def __init__(self, key_name: aspose.psd.fileformats.psd.layers.layerresources.ClassID, key: int):
        '''Initializes a new instance of the  class.
        
        :param key_name: The key name.
        :param key: The structure key.'''
        ...
    
    def save(self, stream_container: aspose.psd.StreamContainer):
        '''Saves the structure to the specified stream container.
        
        :param stream_container: The stream container.'''
        ...
    
    def save_without_key_name(self, stream_container: aspose.psd.StreamContainer):
        '''Saves the structure to the specified stream container.
        
        :param stream_container: The stream container.'''
        ...
    
    def get_header_length(self) -> int:
        '''Gets the header length.
        
        :returns: The header length'''
        ...
    
    @property
    def key(self) -> int:
        '''Gets the structure key.'''
        ...
    
    @property
    def key_name(self) -> aspose.psd.fileformats.psd.layers.layerresources.ClassID:
        ...
    
    @key_name.setter
    def key_name(self, value : aspose.psd.fileformats.psd.layers.layerresources.ClassID):
        ...
    
    @property
    def length(self) -> int:
        '''Gets the  length in bytes.'''
        ...
    
    @property
    def data(self) -> bytes:
        '''Gets the data.'''
        ...
    
    @data.setter
    def data(self, value : bytes):
        '''Sets the data.'''
        ...
    
    ...

class UnitTypes(enum.Enum):
    ANGLE = enum.auto()
    '''Angle unit.'''
    DENSITY = enum.auto()
    '''Density unit.'''
    DISTANCE = enum.auto()
    '''Distance unit.'''
    NONE = enum.auto()
    '''Undefined unit.'''
    PERCENT = enum.auto()
    '''Percent unit.'''
    PIXELS = enum.auto()
    '''Pixels unit.'''
    POINTS = enum.auto()
    '''Points unit.'''
    MILLIMETERS = enum.auto()
    '''Millimeters unit.'''

