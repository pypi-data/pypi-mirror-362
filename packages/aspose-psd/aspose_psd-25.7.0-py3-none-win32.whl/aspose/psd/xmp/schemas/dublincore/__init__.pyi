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

class DublinCorePackage(aspose.psd.xmp.XmpPackage):
    '''Represents Dublic Core schema.'''
    
    @overload
    def set_title(self, title : str):
        '''Adds Dublin Core title.
        
        :param title: The title.'''
        ...
    
    @overload
    def set_title(self, title : aspose.psd.xmp.LangAlt):
        '''Adds Dublin Core title for different languages.
        
        :param title: Instance of :py:class:`aspose.psd.xmp.LangAlt`.'''
        ...
    
    @overload
    def set_description(self, desc : str):
        '''Adds the description.
        
        :param desc: The description.'''
        ...
    
    @overload
    def set_description(self, desc : aspose.psd.xmp.LangAlt):
        '''Adds the description.
        
        :param desc: The description.'''
        ...
    
    @overload
    def set_subject(self, subject : str):
        '''Adds the subject.
        
        :param subject: The subject.'''
        ...
    
    @overload
    def set_subject(self, subject : List[str]):
        '''Adds the subject.
        
        :param subject: The subject.'''
        ...
    
    @overload
    def set_author(self, author : str):
        '''Adds the author.
        
        :param author: The author.'''
        ...
    
    @overload
    def set_author(self, author : List[str]):
        '''Adds the author.
        
        :param author: The author.'''
        ...
    
    @overload
    def set_publisher(self, publisher : str):
        '''Adds the publisher.
        
        :param publisher: The publisher.'''
        ...
    
    @overload
    def set_publisher(self, publisher : List[str]):
        '''Adds the publisher.
        
        :param publisher: The publisher.'''
        ...
    
    def contains_key(self, key : str) -> bool:
        '''Determines whether the specified key contains key.
        
        :param key: The key to be checked.
        :returns: Returns true if the specified key contains key.'''
        ...
    
    def add_value(self, key : str, value : str):
        '''Adds string property.
        
        :param key: The string representation of key that is identified with added value.
        :param value: The string value.'''
        ...
    
    def remove(self, key : str) -> bool:
        '''Remove the value with the specified key.
        
        :param key: The string representation of key that is identified with removed value.
        :returns: Returns true if the value with the specified key was removed.'''
        ...
    
    def clear(self):
        '''Clears this instance.'''
        ...
    
    def set_value(self, key : str, value : aspose.psd.xmp.IXmlValue):
        '''Sets the value.
        
        :param key: The string representation of key that is identified with added value.
        :param value: The value to add to.'''
        ...
    
    def set_xmp_type_value(self, key : str, value : aspose.psd.xmp.types.XmpTypeBase):
        '''Sets the XMP type value.
        
        :param key: The string representation of key that is identified with set value.
        :param value: The value to set to.'''
        ...
    
    def get_xml_value(self) -> str:
        '''Converts XMP value to the XML representation.
        
        :returns: Returns the XMP value converted to the XML representation.'''
        ...
    
    @property
    def xml_namespace(self) -> str:
        ...
    
    @property
    def prefix(self) -> str:
        '''Gets the prefix.'''
        ...
    
    @property
    def namespace_uri(self) -> str:
        ...
    
    ...

