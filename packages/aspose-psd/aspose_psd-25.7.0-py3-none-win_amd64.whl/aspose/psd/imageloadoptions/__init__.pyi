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

class Jpeg2000LoadOptions(aspose.psd.LoadOptions):
    '''JPEG2000 load options'''
    
    @property
    def data_recovery_mode(self) -> aspose.psd.DataRecoveryMode:
        ...
    
    @data_recovery_mode.setter
    def data_recovery_mode(self, value : aspose.psd.DataRecoveryMode):
        ...
    
    @property
    def data_background_color(self) -> aspose.psd.Color:
        ...
    
    @data_background_color.setter
    def data_background_color(self, value : aspose.psd.Color):
        ...
    
    @property
    def use_icc_profile_conversion(self) -> bool:
        ...
    
    @use_icc_profile_conversion.setter
    def use_icc_profile_conversion(self, value : bool):
        ...
    
    @property
    def buffer_size_hint(self) -> int:
        ...
    
    @buffer_size_hint.setter
    def buffer_size_hint(self, value : int):
        ...
    
    @property
    def maximum_decoding_time(self) -> int:
        ...
    
    @maximum_decoding_time.setter
    def maximum_decoding_time(self, value : int):
        ...
    
    ...

class PngLoadOptions(aspose.psd.LoadOptions):
    '''The png load options.'''
    
    @property
    def data_recovery_mode(self) -> aspose.psd.DataRecoveryMode:
        ...
    
    @data_recovery_mode.setter
    def data_recovery_mode(self, value : aspose.psd.DataRecoveryMode):
        ...
    
    @property
    def data_background_color(self) -> aspose.psd.Color:
        ...
    
    @data_background_color.setter
    def data_background_color(self, value : aspose.psd.Color):
        ...
    
    @property
    def use_icc_profile_conversion(self) -> bool:
        ...
    
    @use_icc_profile_conversion.setter
    def use_icc_profile_conversion(self, value : bool):
        ...
    
    @property
    def buffer_size_hint(self) -> int:
        ...
    
    @buffer_size_hint.setter
    def buffer_size_hint(self, value : int):
        ...
    
    @property
    def strict_mode(self) -> bool:
        ...
    
    @strict_mode.setter
    def strict_mode(self, value : bool):
        ...
    
    ...

class PsdLoadOptions(aspose.psd.LoadOptions):
    '''Psd load options'''
    
    @property
    def data_recovery_mode(self) -> aspose.psd.DataRecoveryMode:
        ...
    
    @data_recovery_mode.setter
    def data_recovery_mode(self, value : aspose.psd.DataRecoveryMode):
        ...
    
    @property
    def data_background_color(self) -> aspose.psd.Color:
        ...
    
    @data_background_color.setter
    def data_background_color(self, value : aspose.psd.Color):
        ...
    
    @property
    def use_icc_profile_conversion(self) -> bool:
        ...
    
    @use_icc_profile_conversion.setter
    def use_icc_profile_conversion(self, value : bool):
        ...
    
    @property
    def buffer_size_hint(self) -> int:
        ...
    
    @buffer_size_hint.setter
    def buffer_size_hint(self, value : int):
        ...
    
    @property
    def load_effects_resource(self) -> bool:
        ...
    
    @load_effects_resource.setter
    def load_effects_resource(self, value : bool):
        ...
    
    @property
    def use_disk_for_load_effects_resource(self) -> bool:
        ...
    
    @use_disk_for_load_effects_resource.setter
    def use_disk_for_load_effects_resource(self, value : bool):
        ...
    
    @property
    def read_only_mode(self) -> bool:
        ...
    
    @read_only_mode.setter
    def read_only_mode(self, value : bool):
        ...
    
    @property
    def ignore_text_layer_width_on_update(self) -> bool:
        ...
    
    @ignore_text_layer_width_on_update.setter
    def ignore_text_layer_width_on_update(self, value : bool):
        ...
    
    @property
    def ignore_alpha_channel(self) -> bool:
        ...
    
    @ignore_alpha_channel.setter
    def ignore_alpha_channel(self, value : bool):
        ...
    
    @property
    def allow_warp_repaint(self) -> bool:
        ...
    
    @allow_warp_repaint.setter
    def allow_warp_repaint(self, value : bool):
        ...
    
    @property
    def allow_non_changed_layer_repaint(self) -> bool:
        ...
    
    @allow_non_changed_layer_repaint.setter
    def allow_non_changed_layer_repaint(self, value : bool):
        ...
    
    ...

