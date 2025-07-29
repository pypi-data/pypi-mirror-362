"""The namespace contains XMP related helper classes, constants and methods used by the Adobe dynamic media group."""
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

class AudioChannelType:
    '''Represents audio channel type.'''
    
    @classmethod
    @property
    def mono(cls) -> aspose.psd.xmp.schemas.xmpdm.AudioChannelType:
        '''Gets the mono audio channel.'''
        ...
    
    @classmethod
    @property
    def stereo(cls) -> aspose.psd.xmp.schemas.xmpdm.AudioChannelType:
        '''Gets the stereo audio channel.'''
        ...
    
    @classmethod
    @property
    def audio51(cls) -> aspose.psd.xmp.schemas.xmpdm.AudioChannelType:
        '''Gets the 5.1 audio channel.'''
        ...
    
    @classmethod
    @property
    def audio71(cls) -> aspose.psd.xmp.schemas.xmpdm.AudioChannelType:
        '''Gets the 7.1 audio channel.'''
        ...
    
    @classmethod
    @property
    def audio_16_channel(cls) -> aspose.psd.xmp.schemas.xmpdm.AudioChannelType:
        ...
    
    @classmethod
    @property
    def other_channel(cls) -> aspose.psd.xmp.schemas.xmpdm.AudioChannelType:
        ...
    
    ...

class AudioSampleType:
    '''Represents Audio sample type in .'''
    
    @classmethod
    @property
    def sample_8_int(cls) -> aspose.psd.xmp.schemas.xmpdm.AudioSampleType:
        ...
    
    @classmethod
    @property
    def sample_16_int(cls) -> aspose.psd.xmp.schemas.xmpdm.AudioSampleType:
        ...
    
    @classmethod
    @property
    def sample_24_int(cls) -> aspose.psd.xmp.schemas.xmpdm.AudioSampleType:
        ...
    
    @classmethod
    @property
    def sample_32_int(cls) -> aspose.psd.xmp.schemas.xmpdm.AudioSampleType:
        ...
    
    @classmethod
    @property
    def sample_32_float(cls) -> aspose.psd.xmp.schemas.xmpdm.AudioSampleType:
        ...
    
    @classmethod
    @property
    def compressed(cls) -> aspose.psd.xmp.schemas.xmpdm.AudioSampleType:
        '''Represents Compressed audio sample.'''
        ...
    
    @classmethod
    @property
    def packed(cls) -> aspose.psd.xmp.schemas.xmpdm.AudioSampleType:
        '''Represents Packed audio sample.'''
        ...
    
    ...

class ProjectLink(aspose.psd.xmp.types.XmpTypeBase):
    '''Represents path of the project.'''
    
    def __init__(self):
        ...
    
    def get_xmp_representation(self) -> str:
        '''Returns string contained value in XMP format.
        
        :returns: Returns string contained value in XMP format.'''
        ...
    
    @property
    def path(self) -> str:
        '''Gets full path to the project.'''
        ...
    
    @path.setter
    def path(self, value : str):
        '''Sets full path to the project.'''
        ...
    
    @property
    def type(self) -> aspose.psd.xmp.schemas.xmpdm.ProjectType:
        '''Gets file type.'''
        ...
    
    @type.setter
    def type(self, value : aspose.psd.xmp.schemas.xmpdm.ProjectType):
        '''Sets file type.'''
        ...
    
    ...

class Time(aspose.psd.xmp.types.XmpTypeBase):
    '''Representation of a time value in seconds.'''
    
    def __init__(self, scale: aspose.psd.xmp.types.derived.Rational, value: int):
        '''Initializes a new instance of the  class.
        
        :param scale: The scale.
        :param value: The value.'''
        ...
    
    def get_xmp_representation(self) -> str:
        '''Gets the string contained value in XMP format.
        
        :returns: Returns the string contained value in XMP format.'''
        ...
    
    @property
    def scale(self) -> aspose.psd.xmp.types.derived.Rational:
        '''Gets scale for the time value.'''
        ...
    
    @scale.setter
    def scale(self, value : aspose.psd.xmp.types.derived.Rational):
        '''Sets scale for the time value.'''
        ...
    
    @property
    def value(self) -> int:
        '''Gets time value in the specified scale.'''
        ...
    
    @value.setter
    def value(self, value : int):
        '''Sets time value in the specified scale.'''
        ...
    
    ...

class TimeFormat:
    '''Represents time format in .'''
    
    def equals(self, other: aspose.psd.xmp.schemas.xmpdm.TimeFormat) -> bool:
        '''Indicates whether the current object is equal to another object of the same type.
        
        :param other: An object to compare with this object.
        :returns: true if the current object is equal to the ``other`` parameter; otherwise, false.'''
        ...
    
    @classmethod
    @property
    def timecode24(cls) -> aspose.psd.xmp.schemas.xmpdm.TimeFormat:
        '''Gets the timecode24.'''
        ...
    
    @classmethod
    @property
    def timecode25(cls) -> aspose.psd.xmp.schemas.xmpdm.TimeFormat:
        '''Gets the timecode25.'''
        ...
    
    @classmethod
    @property
    def drop_timecode2997(cls) -> aspose.psd.xmp.schemas.xmpdm.TimeFormat:
        ...
    
    @classmethod
    @property
    def non_drop_timecode2997(cls) -> aspose.psd.xmp.schemas.xmpdm.TimeFormat:
        ...
    
    @classmethod
    @property
    def timecode30(cls) -> aspose.psd.xmp.schemas.xmpdm.TimeFormat:
        '''Gets the timecode30.'''
        ...
    
    @classmethod
    @property
    def timecode50(cls) -> aspose.psd.xmp.schemas.xmpdm.TimeFormat:
        '''Gets the timecode50.'''
        ...
    
    @classmethod
    @property
    def drop_timecode5994(cls) -> aspose.psd.xmp.schemas.xmpdm.TimeFormat:
        ...
    
    @classmethod
    @property
    def non_drop_timecode5994(cls) -> aspose.psd.xmp.schemas.xmpdm.TimeFormat:
        ...
    
    @classmethod
    @property
    def timecode60(cls) -> aspose.psd.xmp.schemas.xmpdm.TimeFormat:
        '''Gets the timecode60.'''
        ...
    
    @classmethod
    @property
    def timecode23976(cls) -> aspose.psd.xmp.schemas.xmpdm.TimeFormat:
        '''Gets the timecode23976.'''
        ...
    
    ...

class Timecode(aspose.psd.xmp.types.XmpTypeBase):
    '''Represents timecode value in video.'''
    
    def __init__(self, format: aspose.psd.xmp.schemas.xmpdm.TimeFormat, time_value: str):
        '''Initializes a new instance of the  class.
        
        :param format: The time format.
        :param time_value: The time value.'''
        ...
    
    def get_xmp_representation(self) -> str:
        '''Returns the string contained value in XMP format.
        
        :returns: Returns the string contained value in XMP format.'''
        ...
    
    def equals(self, other: aspose.psd.xmp.schemas.xmpdm.Timecode) -> bool:
        '''Indicates whether the current object is equal to another object of the same type.
        
        :param other: An object to compare with this object.
        :returns: true if the current object is equal to the ``other`` parameter; otherwise, false.'''
        ...
    
    @property
    def format(self) -> aspose.psd.xmp.schemas.xmpdm.TimeFormat:
        '''Gets the format used in the .'''
        ...
    
    @format.setter
    def format(self, value : aspose.psd.xmp.schemas.xmpdm.TimeFormat):
        '''Sets the format used in the .'''
        ...
    
    @property
    def time_value(self) -> str:
        ...
    
    @time_value.setter
    def time_value(self, value : str):
        ...
    
    ...

class XmpDynamicMediaPackage(aspose.psd.xmp.XmpPackage):
    '''Represents XMP Dynamic Media namespace.'''
    
    def __init__(self):
        ...
    
    def contains_key(self, key: str) -> bool:
        '''Determines whether the specified key contains key.
        
        :param key: The key to be checked.
        :returns: Returns true if the specified key contains key.'''
        ...
    
    def add_value(self, key: str, value: str):
        '''Adds string property.
        
        :param key: The string representation of key that is identified with added value.
        :param value: The string value.'''
        ...
    
    def remove(self, key: str) -> bool:
        '''Remove the value with the specified key.
        
        :param key: The string representation of key that is identified with removed value.
        :returns: Returns true if the value with the specified key was removed.'''
        ...
    
    def clear(self):
        '''Clears this instance.'''
        ...
    
    def set_value(self, key: str, value: aspose.psd.xmp.IXmlValue):
        '''Sets the value.
        
        :param key: The string representation of key that is identified with added value.
        :param value: The value to add to.'''
        ...
    
    def set_xmp_type_value(self, key: str, value: aspose.psd.xmp.types.XmpTypeBase):
        '''Sets the XMP type value.
        
        :param key: The string representation of key that is identified with set value.
        :param value: The value to set to.'''
        ...
    
    def get_xml_value(self) -> str:
        '''Converts XMP value to the XML representation.
        
        :returns: Returns the XMP value converted to the XML representation.'''
        ...
    
    def set_abs_peak_audio_file_path(self, uri: str):
        '''Sets the absolute peak audio file path.
        
        :param uri: The absolute path to the file’s peak audio file.'''
        ...
    
    def set_alblum(self, album: str):
        '''Sets the alblum.
        
        :param album: The album.'''
        ...
    
    def set_alt_tape_name(self, alt_tape_name: str):
        '''Sets the alternative tape name.
        
        :param alt_tape_name: Alternative tape name.'''
        ...
    
    def set_alt_time_code(self, timecode: aspose.psd.xmp.schemas.xmpdm.Timecode):
        '''Sets the alternative time code.
        
        :param timecode: Time code.'''
        ...
    
    def set_artist(self, artist: str):
        '''Sets the artist.
        
        :param artist: The artist.'''
        ...
    
    def set_audio_channel_type(self, audio_channel_type: aspose.psd.xmp.schemas.xmpdm.AudioChannelType):
        '''Sets the audio channel type.
        
        :param audio_channel_type: Audio channel type.'''
        ...
    
    def set_audio_sample_rate(self, rate: int):
        '''Sets the audio sample rate.
        
        :param rate: The audio sample rate.'''
        ...
    
    def set_audio_sample_type(self, audio_sample_type: aspose.psd.xmp.schemas.xmpdm.AudioSampleType):
        '''Sets the audio sample type.
        
        :param audio_sample_type: The audio sample type.'''
        ...
    
    def set_camera_angle(self, camera_angle: str):
        '''Sets the camera angle.
        
        :param camera_angle: The camera angle.'''
        ...
    
    def set_camera_label(self, camera_label: str):
        '''Sets the camera label.
        
        :param camera_label: The camera label.'''
        ...
    
    def set_camera_move(self, camera_move: str):
        '''Sets the camera move.
        
        :param camera_move: The camera move.'''
        ...
    
    def set_client(self, client: str):
        '''Sets the client.
        
        :param client: The client.'''
        ...
    
    def set_comment(self, comment: str):
        '''Sets the comment.
        
        :param comment: The comment.'''
        ...
    
    def set_composer(self, composer: str):
        '''Sets the composer.
        
        :param composer: The composer.'''
        ...
    
    def set_director(self, director: str):
        '''Sets the director.
        
        :param director: The director.'''
        ...
    
    def set_director_photography(self, director_photography: str):
        '''Sets the director of photography.
        
        :param director_photography: The director of photography.'''
        ...
    
    def set_duration(self, duration: aspose.psd.xmp.schemas.xmpdm.Time):
        '''Sets the duration.
        
        :param duration: The duration.'''
        ...
    
    def set_engineer(self, engineer: str):
        '''Sets the engineer.
        
        :param engineer: The engineer.'''
        ...
    
    def set_file_data_rate(self, rate: aspose.psd.xmp.types.derived.Rational):
        '''Sets the file data rate.
        
        :param rate: The file data rate in megabytes per second.'''
        ...
    
    def set_genre(self, genre: str):
        '''Sets the genre.
        
        :param genre: The genre.'''
        ...
    
    def set_good(self, good: bool):
        '''Sets the good.
        
        :param good: if set to ``true`` a shot is a keeper.'''
        ...
    
    def set_instrument(self, instrument: str):
        '''Sets the instrument.
        
        :param instrument: The instrument.'''
        ...
    
    def set_intro_time(self, intro_time: aspose.psd.xmp.schemas.xmpdm.Time):
        '''Sets the intro time.
        
        :param intro_time: The intro time.'''
        ...
    
    def set_key(self, key: str):
        '''Sets the audio’s musical key.
        
        :param key: The audio’s musical key. One of: C, C#, D, D#, E, F, F#, G, G#, A, A#, and B.'''
        ...
    
    def set_log_comment(self, comment: str):
        '''Sets the user's log comment.
        
        :param comment: The comment.'''
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

class ProjectType(enum.Enum):
    MOVIE = enum.auto()
    '''The movie project type'''
    STILL = enum.auto()
    '''The still project type'''
    AUDIO = enum.auto()
    '''The audio project type'''
    CUSTOM = enum.auto()
    '''The custom project type'''

