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

class IStrokeSettings:
    '''Stroke settings of Shapes.'''
    
    @property
    def line_cap(self) -> aspose.psd.fileformats.psd.layers.layerresources.strokeresources.LineCapType:
        ...
    
    @line_cap.setter
    def line_cap(self, value : aspose.psd.fileformats.psd.layers.layerresources.strokeresources.LineCapType):
        ...
    
    @property
    def line_join(self) -> aspose.psd.fileformats.psd.layers.layerresources.strokeresources.LineJoinType:
        ...
    
    @line_join.setter
    def line_join(self, value : aspose.psd.fileformats.psd.layers.layerresources.strokeresources.LineJoinType):
        ...
    
    @property
    def enabled(self) -> bool:
        '''Stroke is enabled.'''
        ...
    
    @enabled.setter
    def enabled(self, value : bool):
        '''Stroke is enabled.'''
        ...
    
    @property
    def size(self) -> float:
        '''Stroke line width.'''
        ...
    
    @size.setter
    def size(self, value : float):
        '''Stroke line width.'''
        ...
    
    @property
    def line_dash_set(self) -> List[float]:
        ...
    
    @line_dash_set.setter
    def line_dash_set(self, value : List[float]):
        ...
    
    @property
    def fill(self) -> aspose.psd.fileformats.psd.layers.fillsettings.IFillSettings:
        '''Gets Fill settings of the Stroke.'''
        ...
    
    @fill.setter
    def fill(self, value : aspose.psd.fileformats.psd.layers.fillsettings.IFillSettings):
        '''Sets Fill settings of the Stroke.'''
        ...
    
    @property
    def line_alignment(self) -> aspose.psd.fileformats.psd.layers.layereffects.StrokePosition:
        ...
    
    @line_alignment.setter
    def line_alignment(self, value : aspose.psd.fileformats.psd.layers.layereffects.StrokePosition):
        ...
    
    ...

class StrokeSettings(IStrokeSettings):
    '''Stroke settings of Shapes.'''
    
    @property
    def line_cap(self) -> aspose.psd.fileformats.psd.layers.layerresources.strokeresources.LineCapType:
        ...
    
    @line_cap.setter
    def line_cap(self, value : aspose.psd.fileformats.psd.layers.layerresources.strokeresources.LineCapType):
        ...
    
    @property
    def line_join(self) -> aspose.psd.fileformats.psd.layers.layerresources.strokeresources.LineJoinType:
        ...
    
    @line_join.setter
    def line_join(self, value : aspose.psd.fileformats.psd.layers.layerresources.strokeresources.LineJoinType):
        ...
    
    @property
    def enabled(self) -> bool:
        '''Gets Stroke is enabled.'''
        ...
    
    @enabled.setter
    def enabled(self, value : bool):
        '''Sets Stroke is enabled.'''
        ...
    
    @property
    def size(self) -> float:
        '''Gets Stroke line width.'''
        ...
    
    @size.setter
    def size(self, value : float):
        '''Sets Stroke line width.'''
        ...
    
    @property
    def line_dash_set(self) -> List[float]:
        ...
    
    @line_dash_set.setter
    def line_dash_set(self, value : List[float]):
        ...
    
    @property
    def fill(self) -> aspose.psd.fileformats.psd.layers.fillsettings.IFillSettings:
        '''Gets Fill settings of the Stroke.'''
        ...
    
    @fill.setter
    def fill(self, value : aspose.psd.fileformats.psd.layers.fillsettings.IFillSettings):
        '''Sets Fill settings of the Stroke.'''
        ...
    
    @property
    def line_alignment(self) -> aspose.psd.fileformats.psd.layers.layereffects.StrokePosition:
        ...
    
    @line_alignment.setter
    def line_alignment(self, value : aspose.psd.fileformats.psd.layers.layereffects.StrokePosition):
        ...
    
    ...

class VscgResource(aspose.psd.fileformats.psd.layers.LayerResource):
    '''Vector Stroke Content Data resource.'''
    
    def save(self, stream_container : aspose.psd.StreamContainer, psd_version : int):
        '''Saves the resource to the specified stream container.
        
        :param stream_container: The stream container to save to.
        :param psd_version: The PSD version.'''
        ...
    
    @property
    def signature(self) -> int:
        '''Gets the signature.'''
        ...
    
    @property
    def key(self) -> int:
        '''Gets the layer resource key.'''
        ...
    
    @property
    def length(self) -> int:
        '''Gets the layer resource length in bytes.'''
        ...
    
    @property
    def psd_version(self) -> int:
        ...
    
    @classmethod
    @property
    def RESOURCE_SIGNATURE(cls) -> int:
        ...
    
    @classmethod
    @property
    def PSB_RESOURCE_SIGNATURE(cls) -> int:
        ...
    
    @property
    def key_for_data(self) -> int:
        ...
    
    @property
    def items(self) -> List[aspose.psd.fileformats.psd.layers.layerresources.OSTypeStructure]:
        '''Gets the array of structure items.
        **Warning:** The `Items` array values must match with the `KeyForData` property, which determines the type of fill settings stored in the structures within `Items`.'''
        ...
    
    @classmethod
    @property
    def TYPE_TOOL_KEY(cls) -> int:
        ...
    
    ...

class VstkResource(aspose.psd.fileformats.psd.layers.LayerResource):
    '''Resource class VstkResource. Contains information about Vector Stroke Data.
    Resource should be initialized either by AssignItems method from ResourceLoader,
    either by assigning values to properties of the class.'''
    
    def save(self, stream_container : aspose.psd.StreamContainer, psd_version : int):
        '''Saves the resource to the specified stream container.
        
        :param stream_container: The stream container to save to.
        :param psd_version: The PSD version.'''
        ...
    
    @property
    def signature(self) -> int:
        '''Gets the signature.'''
        ...
    
    @property
    def key(self) -> int:
        '''Gets the layer resource key.'''
        ...
    
    @property
    def length(self) -> int:
        '''Gets the layer resource length in bytes.'''
        ...
    
    @property
    def psd_version(self) -> int:
        ...
    
    @classmethod
    @property
    def RESOURCE_SIGNATURE(cls) -> int:
        ...
    
    @classmethod
    @property
    def PSB_RESOURCE_SIGNATURE(cls) -> int:
        ...
    
    @property
    def stroke_style_version(self) -> int:
        ...
    
    @stroke_style_version.setter
    def stroke_style_version(self, value : int):
        ...
    
    @property
    def stroke_enabled(self) -> bool:
        ...
    
    @stroke_enabled.setter
    def stroke_enabled(self, value : bool):
        ...
    
    @property
    def fill_enabled(self) -> bool:
        ...
    
    @fill_enabled.setter
    def fill_enabled(self, value : bool):
        ...
    
    @property
    def stroke_style_line_dash_offset(self) -> int:
        ...
    
    @stroke_style_line_dash_offset.setter
    def stroke_style_line_dash_offset(self, value : int):
        ...
    
    @property
    def stroke_style_miter_limit(self) -> float:
        ...
    
    @stroke_style_miter_limit.setter
    def stroke_style_miter_limit(self, value : float):
        ...
    
    @property
    def stroke_style_line_cap_type(self) -> aspose.psd.fileformats.psd.layers.layerresources.strokeresources.LineCapType:
        ...
    
    @stroke_style_line_cap_type.setter
    def stroke_style_line_cap_type(self, value : aspose.psd.fileformats.psd.layers.layerresources.strokeresources.LineCapType):
        ...
    
    @property
    def stroke_style_line_cap_width(self) -> float:
        ...
    
    @stroke_style_line_cap_width.setter
    def stroke_style_line_cap_width(self, value : float):
        ...
    
    @property
    def stroke_style_line_width(self) -> float:
        ...
    
    @stroke_style_line_width.setter
    def stroke_style_line_width(self, value : float):
        ...
    
    @property
    def stroke_style_line_join_type(self) -> aspose.psd.fileformats.psd.layers.layerresources.strokeresources.LineJoinType:
        ...
    
    @stroke_style_line_join_type.setter
    def stroke_style_line_join_type(self, value : aspose.psd.fileformats.psd.layers.layerresources.strokeresources.LineJoinType):
        ...
    
    @property
    def stroke_style_line_alignment(self) -> aspose.psd.fileformats.psd.layers.layereffects.StrokePosition:
        ...
    
    @stroke_style_line_alignment.setter
    def stroke_style_line_alignment(self, value : aspose.psd.fileformats.psd.layers.layereffects.StrokePosition):
        ...
    
    @property
    def stroke_style_scale_lock(self) -> bool:
        ...
    
    @stroke_style_scale_lock.setter
    def stroke_style_scale_lock(self, value : bool):
        ...
    
    @property
    def stroke_style_stroke_adjust(self) -> bool:
        ...
    
    @stroke_style_stroke_adjust.setter
    def stroke_style_stroke_adjust(self, value : bool):
        ...
    
    @property
    def stroke_style_blend_mode(self) -> aspose.psd.fileformats.core.blending.BlendMode:
        ...
    
    @stroke_style_blend_mode.setter
    def stroke_style_blend_mode(self, value : aspose.psd.fileformats.core.blending.BlendMode):
        ...
    
    @property
    def stroke_style_opacity(self) -> int:
        ...
    
    @stroke_style_opacity.setter
    def stroke_style_opacity(self, value : int):
        ...
    
    @property
    def stroke_style_resolution(self) -> float:
        ...
    
    @stroke_style_resolution.setter
    def stroke_style_resolution(self, value : float):
        ...
    
    @property
    def fill_settings(self) -> aspose.psd.fileformats.psd.layers.fillsettings.IFillSettings:
        ...
    
    @fill_settings.setter
    def fill_settings(self, value : aspose.psd.fileformats.psd.layers.fillsettings.IFillSettings):
        ...
    
    @property
    def stroke_style_content(self) -> aspose.psd.fileformats.psd.layers.layerresources.typetoolinfostructures.DescriptorStructure:
        ...
    
    @stroke_style_content.setter
    def stroke_style_content(self, value : aspose.psd.fileformats.psd.layers.layerresources.typetoolinfostructures.DescriptorStructure):
        ...
    
    @property
    def stroke_style_line_dash_set(self) -> List[float]:
        ...
    
    @stroke_style_line_dash_set.setter
    def stroke_style_line_dash_set(self, value : List[float]):
        ...
    
    @classmethod
    @property
    def TYPE_TOOL_KEY(cls) -> int:
        ...
    
    ...

class LineCapType:
    '''Line Cap type.'''
    
    @classmethod
    @property
    def ROUND_CAP(cls) -> LineCapType:
        '''Round cap type.'''
        ...
    
    @classmethod
    @property
    def SQUARE_CAP(cls) -> LineCapType:
        '''Square cap type.'''
        ...
    
    @classmethod
    @property
    def BUTT_CAP(cls) -> LineCapType:
        '''Butt cap type.'''
        ...
    
    ...

class LineJoinType:
    '''Line Join type.'''
    
    @classmethod
    @property
    def BEVEL_JOIN(cls) -> LineJoinType:
        '''Bevel join type.'''
        ...
    
    @classmethod
    @property
    def ROUND_JOIN(cls) -> LineJoinType:
        '''Rounnd join type.'''
        ...
    
    @classmethod
    @property
    def MITER_JOIN(cls) -> LineJoinType:
        '''Miter join type.'''
        ...
    
    ...

