"""The namespace contains classes suitable for export, save or creation of different file formats."""
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

class BmpOptions(aspose.psd.ImageOptionsBase):
    '''The bmp file format creation options.'''
    
    @overload
    def __init__(self):
        '''Initializes a new instance of the  class.'''
        ...
    
    @overload
    def __init__(self, bmp_options: aspose.psd.imageoptions.BmpOptions):
        '''Initializes a new instance of the  class.
        
        :param bmp_options: The BMP options.'''
        ...
    
    def clone(self) -> aspose.psd.ImageOptionsBase:
        '''Clones this instance.
        
        :returns: Returns shallow copy of this instance'''
        ...
    
    @property
    def disposed(self) -> bool:
        '''Gets a value indicating whether this instance is disposed.'''
        ...
    
    @property
    def default_replacement_font(self) -> str:
        ...
    
    @default_replacement_font.setter
    def default_replacement_font(self, value : str):
        ...
    
    @property
    def xmp_data(self) -> aspose.psd.xmp.XmpPacketWrapper:
        ...
    
    @xmp_data.setter
    def xmp_data(self, value : aspose.psd.xmp.XmpPacketWrapper):
        ...
    
    @property
    def source(self) -> aspose.psd.Source:
        '''Gets the source to create image in.'''
        ...
    
    @source.setter
    def source(self, value : aspose.psd.Source):
        '''Sets the source to create image in.'''
        ...
    
    @property
    def palette(self) -> aspose.psd.IColorPalette:
        '''Gets the color palette.'''
        ...
    
    @palette.setter
    def palette(self, value : aspose.psd.IColorPalette):
        '''Sets the color palette.'''
        ...
    
    @property
    def resolution_settings(self) -> aspose.psd.ResolutionSetting:
        ...
    
    @resolution_settings.setter
    def resolution_settings(self, value : aspose.psd.ResolutionSetting):
        ...
    
    @property
    def vector_rasterization_options(self) -> aspose.psd.imageoptions.VectorRasterizationOptions:
        ...
    
    @vector_rasterization_options.setter
    def vector_rasterization_options(self, value : aspose.psd.imageoptions.VectorRasterizationOptions):
        ...
    
    @property
    def buffer_size_hint(self) -> int:
        ...
    
    @buffer_size_hint.setter
    def buffer_size_hint(self, value : int):
        ...
    
    @property
    def multi_page_options(self) -> aspose.psd.imageoptions.MultiPageOptions:
        ...
    
    @multi_page_options.setter
    def multi_page_options(self, value : aspose.psd.imageoptions.MultiPageOptions):
        ...
    
    @property
    def full_frame(self) -> bool:
        ...
    
    @full_frame.setter
    def full_frame(self, value : bool):
        ...
    
    @property
    def bits_per_pixel(self) -> int:
        ...
    
    @bits_per_pixel.setter
    def bits_per_pixel(self, value : int):
        ...
    
    @property
    def compression(self) -> aspose.psd.fileformats.bmp.BitmapCompression:
        '''Gets the compression.'''
        ...
    
    @compression.setter
    def compression(self, value : aspose.psd.fileformats.bmp.BitmapCompression):
        '''Sets the compression.'''
        ...
    
    ...

class CmxRasterizationOptions(VectorRasterizationOptions):
    '''the CMX exporter options.'''
    
    def __init__(self):
        '''Initializes a new instance of the  class.'''
        ...
    
    def clone(self) -> aspose.psd.ImageOptionsBase:
        '''Clones this instance.
        
        :returns: Returns shallow copy of this instance'''
        ...
    
    def copy_to(self, vector_rasterization_options: aspose.psd.imageoptions.VectorRasterizationOptions):
        '''Copies to.
        
        :param vector_rasterization_options: The vector rasterization options.'''
        ...
    
    @property
    def disposed(self) -> bool:
        '''Gets a value indicating whether this instance is disposed.'''
        ...
    
    @property
    def default_replacement_font(self) -> str:
        ...
    
    @default_replacement_font.setter
    def default_replacement_font(self, value : str):
        ...
    
    @property
    def xmp_data(self) -> aspose.psd.xmp.XmpPacketWrapper:
        ...
    
    @xmp_data.setter
    def xmp_data(self, value : aspose.psd.xmp.XmpPacketWrapper):
        ...
    
    @property
    def source(self) -> aspose.psd.Source:
        '''Gets the source to create image in.'''
        ...
    
    @source.setter
    def source(self, value : aspose.psd.Source):
        '''Sets the source to create image in.'''
        ...
    
    @property
    def palette(self) -> aspose.psd.IColorPalette:
        '''Gets the color palette.'''
        ...
    
    @palette.setter
    def palette(self, value : aspose.psd.IColorPalette):
        '''Sets the color palette.'''
        ...
    
    @property
    def resolution_settings(self) -> aspose.psd.ResolutionSetting:
        ...
    
    @resolution_settings.setter
    def resolution_settings(self, value : aspose.psd.ResolutionSetting):
        ...
    
    @property
    def vector_rasterization_options(self) -> aspose.psd.imageoptions.VectorRasterizationOptions:
        ...
    
    @vector_rasterization_options.setter
    def vector_rasterization_options(self, value : aspose.psd.imageoptions.VectorRasterizationOptions):
        ...
    
    @property
    def buffer_size_hint(self) -> int:
        ...
    
    @buffer_size_hint.setter
    def buffer_size_hint(self, value : int):
        ...
    
    @property
    def multi_page_options(self) -> aspose.psd.imageoptions.MultiPageOptions:
        ...
    
    @multi_page_options.setter
    def multi_page_options(self, value : aspose.psd.imageoptions.MultiPageOptions):
        ...
    
    @property
    def full_frame(self) -> bool:
        ...
    
    @full_frame.setter
    def full_frame(self, value : bool):
        ...
    
    @property
    def border_x(self) -> float:
        ...
    
    @border_x.setter
    def border_x(self, value : float):
        ...
    
    @property
    def border_y(self) -> float:
        ...
    
    @border_y.setter
    def border_y(self, value : float):
        ...
    
    @property
    def center_drawing(self) -> bool:
        ...
    
    @center_drawing.setter
    def center_drawing(self, value : bool):
        ...
    
    @property
    def page_height(self) -> float:
        ...
    
    @page_height.setter
    def page_height(self, value : float):
        ...
    
    @property
    def page_size(self) -> aspose.psd.SizeF:
        ...
    
    @page_size.setter
    def page_size(self, value : aspose.psd.SizeF):
        ...
    
    @property
    def page_width(self) -> float:
        ...
    
    @page_width.setter
    def page_width(self, value : float):
        ...
    
    @property
    def background_color(self) -> aspose.psd.Color:
        ...
    
    @background_color.setter
    def background_color(self, value : aspose.psd.Color):
        ...
    
    @property
    def draw_color(self) -> aspose.psd.Color:
        ...
    
    @draw_color.setter
    def draw_color(self, value : aspose.psd.Color):
        ...
    
    @property
    def smoothing_mode(self) -> aspose.psd.SmoothingMode:
        ...
    
    @smoothing_mode.setter
    def smoothing_mode(self, value : aspose.psd.SmoothingMode):
        ...
    
    @property
    def text_rendering_hint(self) -> aspose.psd.TextRenderingHint:
        ...
    
    @text_rendering_hint.setter
    def text_rendering_hint(self, value : aspose.psd.TextRenderingHint):
        ...
    
    @property
    def positioning(self) -> aspose.psd.imageoptions.PositioningTypes:
        '''Gets the positioning.'''
        ...
    
    @positioning.setter
    def positioning(self, value : aspose.psd.imageoptions.PositioningTypes):
        '''Sets the positioning.'''
        ...
    
    ...

class GifOptions(aspose.psd.ImageOptionsBase):
    '''The gif file format creation options.'''
    
    @overload
    def __init__(self):
        '''Initializes a new instance of the  class.'''
        ...
    
    @overload
    def __init__(self, gif_options: aspose.psd.imageoptions.GifOptions):
        '''Initializes a new instance of the  class.
        
        :param gif_options: The GIF Options.'''
        ...
    
    def clone(self) -> aspose.psd.ImageOptionsBase:
        '''Clones this instance.
        
        :returns: Returns shallow copy of this instance'''
        ...
    
    @property
    def disposed(self) -> bool:
        '''Gets a value indicating whether this instance is disposed.'''
        ...
    
    @property
    def default_replacement_font(self) -> str:
        ...
    
    @default_replacement_font.setter
    def default_replacement_font(self, value : str):
        ...
    
    @property
    def xmp_data(self) -> aspose.psd.xmp.XmpPacketWrapper:
        ...
    
    @xmp_data.setter
    def xmp_data(self, value : aspose.psd.xmp.XmpPacketWrapper):
        ...
    
    @property
    def source(self) -> aspose.psd.Source:
        '''Gets the source to create image in.'''
        ...
    
    @source.setter
    def source(self, value : aspose.psd.Source):
        '''Sets the source to create image in.'''
        ...
    
    @property
    def palette(self) -> aspose.psd.IColorPalette:
        '''Gets the color palette.'''
        ...
    
    @palette.setter
    def palette(self, value : aspose.psd.IColorPalette):
        '''Sets the color palette.'''
        ...
    
    @property
    def resolution_settings(self) -> aspose.psd.ResolutionSetting:
        ...
    
    @resolution_settings.setter
    def resolution_settings(self, value : aspose.psd.ResolutionSetting):
        ...
    
    @property
    def vector_rasterization_options(self) -> aspose.psd.imageoptions.VectorRasterizationOptions:
        ...
    
    @vector_rasterization_options.setter
    def vector_rasterization_options(self, value : aspose.psd.imageoptions.VectorRasterizationOptions):
        ...
    
    @property
    def buffer_size_hint(self) -> int:
        ...
    
    @buffer_size_hint.setter
    def buffer_size_hint(self, value : int):
        ...
    
    @property
    def multi_page_options(self) -> aspose.psd.imageoptions.MultiPageOptions:
        ...
    
    @multi_page_options.setter
    def multi_page_options(self, value : aspose.psd.imageoptions.MultiPageOptions):
        ...
    
    @property
    def full_frame(self) -> bool:
        ...
    
    @full_frame.setter
    def full_frame(self, value : bool):
        ...
    
    @property
    def do_palette_correction(self) -> bool:
        ...
    
    @do_palette_correction.setter
    def do_palette_correction(self, value : bool):
        ...
    
    @property
    def color_resolution(self) -> byte:
        ...
    
    @color_resolution.setter
    def color_resolution(self, value : byte):
        ...
    
    @property
    def is_palette_sorted(self) -> bool:
        ...
    
    @is_palette_sorted.setter
    def is_palette_sorted(self, value : bool):
        ...
    
    @property
    def pixel_aspect_ratio(self) -> byte:
        ...
    
    @pixel_aspect_ratio.setter
    def pixel_aspect_ratio(self, value : byte):
        ...
    
    @property
    def background_color_index(self) -> byte:
        ...
    
    @background_color_index.setter
    def background_color_index(self, value : byte):
        ...
    
    @property
    def has_trailer(self) -> bool:
        ...
    
    @has_trailer.setter
    def has_trailer(self, value : bool):
        ...
    
    @property
    def interlaced(self) -> bool:
        '''True if image should be interlaced.'''
        ...
    
    @interlaced.setter
    def interlaced(self, value : bool):
        '''True if image should be interlaced.'''
        ...
    
    @property
    def max_diff(self) -> int:
        ...
    
    @max_diff.setter
    def max_diff(self, value : int):
        ...
    
    ...

class GraphicsOptions:
    '''Represents graphics options for embedded bitmap.'''
    
    def __init__(self):
        ...
    
    @property
    def text_rendering_hint(self) -> aspose.psd.TextRenderingHint:
        ...
    
    @text_rendering_hint.setter
    def text_rendering_hint(self, value : aspose.psd.TextRenderingHint):
        ...
    
    @property
    def smoothing_mode(self) -> aspose.psd.SmoothingMode:
        ...
    
    @smoothing_mode.setter
    def smoothing_mode(self, value : aspose.psd.SmoothingMode):
        ...
    
    @property
    def interpolation_mode(self) -> aspose.psd.InterpolationMode:
        ...
    
    @interpolation_mode.setter
    def interpolation_mode(self, value : aspose.psd.InterpolationMode):
        ...
    
    ...

class Jpeg2000Options(aspose.psd.ImageOptionsBase):
    '''The Jpeg2000 file format options.'''
    
    @overload
    def __init__(self):
        '''Initializes a new instance of the  class.'''
        ...
    
    @overload
    def __init__(self, jpeg_2000_options: aspose.psd.imageoptions.Jpeg2000Options):
        '''Initializes a new instance of the  class.
        
        :param jpeg_2000_options: The Jpeg2000 file format options to copy settings from.'''
        ...
    
    def clone(self) -> aspose.psd.ImageOptionsBase:
        '''Clones this instance.
        
        :returns: Returns shallow copy of this instance'''
        ...
    
    @property
    def disposed(self) -> bool:
        '''Gets a value indicating whether this instance is disposed.'''
        ...
    
    @property
    def default_replacement_font(self) -> str:
        ...
    
    @default_replacement_font.setter
    def default_replacement_font(self, value : str):
        ...
    
    @property
    def xmp_data(self) -> aspose.psd.xmp.XmpPacketWrapper:
        ...
    
    @xmp_data.setter
    def xmp_data(self, value : aspose.psd.xmp.XmpPacketWrapper):
        ...
    
    @property
    def source(self) -> aspose.psd.Source:
        '''Gets the source to create image in.'''
        ...
    
    @source.setter
    def source(self, value : aspose.psd.Source):
        '''Sets the source to create image in.'''
        ...
    
    @property
    def palette(self) -> aspose.psd.IColorPalette:
        '''Gets the color palette.'''
        ...
    
    @palette.setter
    def palette(self, value : aspose.psd.IColorPalette):
        '''Sets the color palette.'''
        ...
    
    @property
    def resolution_settings(self) -> aspose.psd.ResolutionSetting:
        ...
    
    @resolution_settings.setter
    def resolution_settings(self, value : aspose.psd.ResolutionSetting):
        ...
    
    @property
    def vector_rasterization_options(self) -> aspose.psd.imageoptions.VectorRasterizationOptions:
        ...
    
    @vector_rasterization_options.setter
    def vector_rasterization_options(self, value : aspose.psd.imageoptions.VectorRasterizationOptions):
        ...
    
    @property
    def buffer_size_hint(self) -> int:
        ...
    
    @buffer_size_hint.setter
    def buffer_size_hint(self, value : int):
        ...
    
    @property
    def multi_page_options(self) -> aspose.psd.imageoptions.MultiPageOptions:
        ...
    
    @multi_page_options.setter
    def multi_page_options(self, value : aspose.psd.imageoptions.MultiPageOptions):
        ...
    
    @property
    def full_frame(self) -> bool:
        ...
    
    @full_frame.setter
    def full_frame(self, value : bool):
        ...
    
    @property
    def comments(self) -> List[str]:
        '''Gets the Jpeg comment markers.'''
        ...
    
    @comments.setter
    def comments(self, value : List[str]):
        '''Sets the Jpeg comment markers.'''
        ...
    
    @property
    def codec(self) -> aspose.psd.fileformats.jpeg2000.Jpeg2000Codec:
        '''Gets the JPEG2000 codec'''
        ...
    
    @codec.setter
    def codec(self, value : aspose.psd.fileformats.jpeg2000.Jpeg2000Codec):
        '''Sets the JPEG2000 codec'''
        ...
    
    @property
    def compression_ratios(self) -> List[int]:
        ...
    
    @compression_ratios.setter
    def compression_ratios(self, value : List[int]):
        ...
    
    @property
    def irreversible(self) -> bool:
        '''Gets a value indicating whether use the irreversible DWT 9-7 (true) or use lossless DWT 5-3 compression (default).'''
        ...
    
    @irreversible.setter
    def irreversible(self, value : bool):
        '''Sets a value indicating whether use the irreversible DWT 9-7 (true) or use lossless DWT 5-3 compression (default).'''
        ...
    
    ...

class JpegOptions(aspose.psd.ImageOptionsBase):
    '''The jpeg file format create options.'''
    
    @overload
    def __init__(self):
        '''Initializes a new instance of the  class.'''
        ...
    
    @overload
    def __init__(self, jpeg_options: aspose.psd.imageoptions.JpegOptions):
        '''Initializes a new instance of the  class.
        
        :param jpeg_options: The JPEG options.'''
        ...
    
    def clone(self) -> aspose.psd.ImageOptionsBase:
        '''Clones this instance.
        
        :returns: Returns shallow copy of this instance'''
        ...
    
    @property
    def disposed(self) -> bool:
        '''Gets a value indicating whether this instance is disposed.'''
        ...
    
    @property
    def default_replacement_font(self) -> str:
        ...
    
    @default_replacement_font.setter
    def default_replacement_font(self, value : str):
        ...
    
    @property
    def xmp_data(self) -> aspose.psd.xmp.XmpPacketWrapper:
        ...
    
    @xmp_data.setter
    def xmp_data(self, value : aspose.psd.xmp.XmpPacketWrapper):
        ...
    
    @property
    def source(self) -> aspose.psd.Source:
        '''Gets the source to create image in.'''
        ...
    
    @source.setter
    def source(self, value : aspose.psd.Source):
        '''Sets the source to create image in.'''
        ...
    
    @property
    def palette(self) -> aspose.psd.IColorPalette:
        '''Gets the color palette.'''
        ...
    
    @palette.setter
    def palette(self, value : aspose.psd.IColorPalette):
        '''Sets the color palette.'''
        ...
    
    @property
    def resolution_settings(self) -> aspose.psd.ResolutionSetting:
        ...
    
    @resolution_settings.setter
    def resolution_settings(self, value : aspose.psd.ResolutionSetting):
        ...
    
    @property
    def vector_rasterization_options(self) -> aspose.psd.imageoptions.VectorRasterizationOptions:
        ...
    
    @vector_rasterization_options.setter
    def vector_rasterization_options(self, value : aspose.psd.imageoptions.VectorRasterizationOptions):
        ...
    
    @property
    def buffer_size_hint(self) -> int:
        ...
    
    @buffer_size_hint.setter
    def buffer_size_hint(self, value : int):
        ...
    
    @property
    def multi_page_options(self) -> aspose.psd.imageoptions.MultiPageOptions:
        ...
    
    @multi_page_options.setter
    def multi_page_options(self, value : aspose.psd.imageoptions.MultiPageOptions):
        ...
    
    @property
    def full_frame(self) -> bool:
        ...
    
    @full_frame.setter
    def full_frame(self, value : bool):
        ...
    
    @property
    def default_memory_allocation_limit(self) -> int:
        ...
    
    @default_memory_allocation_limit.setter
    def default_memory_allocation_limit(self, value : int):
        ...
    
    @property
    def jfif(self) -> aspose.psd.fileformats.jpeg.JFIFData:
        '''Gets the jfif.'''
        ...
    
    @jfif.setter
    def jfif(self, value : aspose.psd.fileformats.jpeg.JFIFData):
        '''Sets the jfif.'''
        ...
    
    @property
    def comment(self) -> str:
        '''Gets the jpeg file comment.'''
        ...
    
    @comment.setter
    def comment(self, value : str):
        '''Sets the jpeg file comment.'''
        ...
    
    @property
    def exif_data(self) -> aspose.psd.exif.JpegExifData:
        ...
    
    @exif_data.setter
    def exif_data(self, value : aspose.psd.exif.JpegExifData):
        ...
    
    @property
    def compression_type(self) -> aspose.psd.fileformats.jpeg.JpegCompressionMode:
        ...
    
    @compression_type.setter
    def compression_type(self, value : aspose.psd.fileformats.jpeg.JpegCompressionMode):
        ...
    
    @property
    def color_type(self) -> aspose.psd.fileformats.jpeg.JpegCompressionColorMode:
        ...
    
    @color_type.setter
    def color_type(self, value : aspose.psd.fileformats.jpeg.JpegCompressionColorMode):
        ...
    
    @property
    def bits_per_channel(self) -> byte:
        ...
    
    @bits_per_channel.setter
    def bits_per_channel(self, value : byte):
        ...
    
    @property
    def quality(self) -> int:
        '''Gets image quality.'''
        ...
    
    @quality.setter
    def quality(self, value : int):
        '''Sets image quality.'''
        ...
    
    @property
    def scaled_quality(self) -> int:
        ...
    
    @property
    def rd_opt_settings(self) -> aspose.psd.imageoptions.RdOptimizerSettings:
        ...
    
    @rd_opt_settings.setter
    def rd_opt_settings(self, value : aspose.psd.imageoptions.RdOptimizerSettings):
        ...
    
    @property
    def rgb_color_profile(self) -> aspose.psd.sources.StreamSource:
        ...
    
    @rgb_color_profile.setter
    def rgb_color_profile(self, value : aspose.psd.sources.StreamSource):
        ...
    
    @property
    def cmyk_color_profile(self) -> aspose.psd.sources.StreamSource:
        ...
    
    @cmyk_color_profile.setter
    def cmyk_color_profile(self, value : aspose.psd.sources.StreamSource):
        ...
    
    @property
    def jpeg_ls_allowed_lossy_error(self) -> int:
        ...
    
    @jpeg_ls_allowed_lossy_error.setter
    def jpeg_ls_allowed_lossy_error(self, value : int):
        ...
    
    @property
    def jpeg_ls_interleave_mode(self) -> aspose.psd.fileformats.jpeg.JpegLsInterleaveMode:
        ...
    
    @jpeg_ls_interleave_mode.setter
    def jpeg_ls_interleave_mode(self, value : aspose.psd.fileformats.jpeg.JpegLsInterleaveMode):
        ...
    
    @property
    def jpeg_ls_preset(self) -> aspose.psd.fileformats.jpeg.JpegLsPresetCodingParameters:
        ...
    
    @jpeg_ls_preset.setter
    def jpeg_ls_preset(self, value : aspose.psd.fileformats.jpeg.JpegLsPresetCodingParameters):
        ...
    
    @property
    def horizontal_sampling(self) -> bytes:
        ...
    
    @horizontal_sampling.setter
    def horizontal_sampling(self, value : bytes):
        ...
    
    @property
    def vertical_sampling(self) -> bytes:
        ...
    
    @vertical_sampling.setter
    def vertical_sampling(self, value : bytes):
        ...
    
    @property
    def sample_rounding_mode(self) -> aspose.psd.fileformats.jpeg.SampleRoundingMode:
        ...
    
    @sample_rounding_mode.setter
    def sample_rounding_mode(self, value : aspose.psd.fileformats.jpeg.SampleRoundingMode):
        ...
    
    @property
    def preblend_alpha_if_present(self) -> bool:
        ...
    
    @preblend_alpha_if_present.setter
    def preblend_alpha_if_present(self, value : bool):
        ...
    
    @property
    def resolution_unit(self) -> aspose.psd.ResolutionUnit:
        ...
    
    @resolution_unit.setter
    def resolution_unit(self, value : aspose.psd.ResolutionUnit):
        ...
    
    ...

class MultiPageOptions:
    '''Base class for multiple pages supported formats'''
    
    @overload
    def __init__(self):
        '''Initializes a new instance of the  class.'''
        ...
    
    @overload
    def __init__(self, pages: List[int]):
        '''Initializes a new instance of the  class.
        
        :param pages: The pages.'''
        ...
    
    @overload
    def __init__(self, pages: List[int], export_area: aspose.psd.Rectangle):
        '''Initializes a new instance of the  class.
        
        :param pages: The array of pages.
        :param export_area: The export area.'''
        ...
    
    @overload
    def __init__(self, page_titles: List[str]):
        '''Initializes a new instance of the  class.
        
        :param page_titles: The page titles.'''
        ...
    
    @overload
    def __init__(self, page_titles: List[str], export_area: aspose.psd.Rectangle):
        '''Initializes a new instance of the  class.
        
        :param page_titles: The page titles.
        :param export_area: The export area.'''
        ...
    
    @overload
    def __init__(self, ranges: List[aspose.psd.IntRange]):
        '''Initializes a new instance of the  class.
        
        :param ranges: The .'''
        ...
    
    @overload
    def __init__(self, ranges: List[aspose.psd.IntRange], export_area: aspose.psd.Rectangle):
        '''Initializes a new instance of the  class.
        
        :param ranges: The .
        :param export_area: The export area.'''
        ...
    
    @overload
    def __init__(self, range: aspose.psd.IntRange):
        '''Initializes a new instance of the  class.
        
        :param range: The .'''
        ...
    
    @overload
    def __init__(self, range: aspose.psd.IntRange, export_area: aspose.psd.Rectangle):
        '''Initializes a new instance of the  class.
        
        :param range: The .
        :param export_area: The export area.'''
        ...
    
    @overload
    def __init__(self, page: int):
        '''Initializes a new instance of the  class.
        
        :param page: The page index.'''
        ...
    
    @overload
    def __init__(self, page: int, export_area: aspose.psd.Rectangle):
        '''Initializes a new instance of the  class.
        
        :param page: The page index.
        :param export_area: The export area.'''
        ...
    
    def init_pages(self, ranges: List[aspose.psd.IntRange]):
        '''Initializes the pages from ranges array
        
        :param ranges: The ranges.'''
        ...
    
    @property
    def pages(self) -> List[int]:
        '''Gets the pages.'''
        ...
    
    @pages.setter
    def pages(self, value : List[int]):
        '''Sets the pages.'''
        ...
    
    @property
    def page_titles(self) -> List[str]:
        ...
    
    @page_titles.setter
    def page_titles(self, value : List[str]):
        ...
    
    @property
    def page_rasterization_options(self) -> List[aspose.psd.imageoptions.VectorRasterizationOptions]:
        ...
    
    @page_rasterization_options.setter
    def page_rasterization_options(self, value : List[aspose.psd.imageoptions.VectorRasterizationOptions]):
        ...
    
    @property
    def export_area(self) -> aspose.psd.Rectangle:
        ...
    
    @export_area.setter
    def export_area(self, value : aspose.psd.Rectangle):
        ...
    
    @property
    def mode(self) -> aspose.psd.imageoptions.MultiPageMode:
        '''Gets the mode.'''
        ...
    
    @mode.setter
    def mode(self, value : aspose.psd.imageoptions.MultiPageMode):
        '''Sets the mode.'''
        ...
    
    @property
    def output_layers_names(self) -> List[str]:
        ...
    
    @output_layers_names.setter
    def output_layers_names(self, value : List[str]):
        ...
    
    @property
    def merge_layers(self) -> bool:
        ...
    
    @merge_layers.setter
    def merge_layers(self, value : bool):
        ...
    
    ...

class PdfOptions(aspose.psd.ImageOptionsBase):
    '''The PDF options.'''
    
    def __init__(self):
        '''Initializes a new instance of the  class.'''
        ...
    
    def clone(self) -> aspose.psd.ImageOptionsBase:
        '''Clones this instance.
        
        :returns: Returns shallow copy of this instance'''
        ...
    
    @property
    def disposed(self) -> bool:
        '''Gets a value indicating whether this instance is disposed.'''
        ...
    
    @property
    def default_replacement_font(self) -> str:
        ...
    
    @default_replacement_font.setter
    def default_replacement_font(self, value : str):
        ...
    
    @property
    def xmp_data(self) -> aspose.psd.xmp.XmpPacketWrapper:
        ...
    
    @xmp_data.setter
    def xmp_data(self, value : aspose.psd.xmp.XmpPacketWrapper):
        ...
    
    @property
    def source(self) -> aspose.psd.Source:
        '''Gets the source to create image in.'''
        ...
    
    @source.setter
    def source(self, value : aspose.psd.Source):
        '''Sets the source to create image in.'''
        ...
    
    @property
    def palette(self) -> aspose.psd.IColorPalette:
        '''Gets the color palette.'''
        ...
    
    @palette.setter
    def palette(self, value : aspose.psd.IColorPalette):
        '''Sets the color palette.'''
        ...
    
    @property
    def resolution_settings(self) -> aspose.psd.ResolutionSetting:
        ...
    
    @resolution_settings.setter
    def resolution_settings(self, value : aspose.psd.ResolutionSetting):
        ...
    
    @property
    def vector_rasterization_options(self) -> aspose.psd.imageoptions.VectorRasterizationOptions:
        ...
    
    @vector_rasterization_options.setter
    def vector_rasterization_options(self, value : aspose.psd.imageoptions.VectorRasterizationOptions):
        ...
    
    @property
    def buffer_size_hint(self) -> int:
        ...
    
    @buffer_size_hint.setter
    def buffer_size_hint(self, value : int):
        ...
    
    @property
    def multi_page_options(self) -> aspose.psd.imageoptions.MultiPageOptions:
        ...
    
    @multi_page_options.setter
    def multi_page_options(self, value : aspose.psd.imageoptions.MultiPageOptions):
        ...
    
    @property
    def full_frame(self) -> bool:
        ...
    
    @full_frame.setter
    def full_frame(self, value : bool):
        ...
    
    @property
    def pdf_document_info(self) -> aspose.psd.fileformats.pdf.PdfDocumentInfo:
        ...
    
    @pdf_document_info.setter
    def pdf_document_info(self, value : aspose.psd.fileformats.pdf.PdfDocumentInfo):
        ...
    
    @property
    def pdf_core_options(self) -> aspose.psd.fileformats.pdf.PdfCoreOptions:
        ...
    
    @pdf_core_options.setter
    def pdf_core_options(self, value : aspose.psd.fileformats.pdf.PdfCoreOptions):
        ...
    
    @property
    def page_size(self) -> aspose.psd.SizeF:
        ...
    
    @page_size.setter
    def page_size(self, value : aspose.psd.SizeF):
        ...
    
    ...

class PngOptions(aspose.psd.ImageOptionsBase):
    '''The png file format create options.'''
    
    @overload
    def __init__(self):
        '''Initializes a new instance of the  class.'''
        ...
    
    @overload
    def __init__(self, png_options: aspose.psd.imageoptions.PngOptions):
        '''Initializes a new instance of the  class.
        
        :param png_options: The PNG options.'''
        ...
    
    def clone(self) -> aspose.psd.ImageOptionsBase:
        '''Clones this instance.
        
        :returns: Returns shallow copy of this instance'''
        ...
    
    @property
    def disposed(self) -> bool:
        '''Gets a value indicating whether this instance is disposed.'''
        ...
    
    @property
    def default_replacement_font(self) -> str:
        ...
    
    @default_replacement_font.setter
    def default_replacement_font(self, value : str):
        ...
    
    @property
    def xmp_data(self) -> aspose.psd.xmp.XmpPacketWrapper:
        ...
    
    @xmp_data.setter
    def xmp_data(self, value : aspose.psd.xmp.XmpPacketWrapper):
        ...
    
    @property
    def source(self) -> aspose.psd.Source:
        '''Gets the source to create image in.'''
        ...
    
    @source.setter
    def source(self, value : aspose.psd.Source):
        '''Sets the source to create image in.'''
        ...
    
    @property
    def palette(self) -> aspose.psd.IColorPalette:
        '''Gets the color palette.'''
        ...
    
    @palette.setter
    def palette(self, value : aspose.psd.IColorPalette):
        '''Sets the color palette.'''
        ...
    
    @property
    def resolution_settings(self) -> aspose.psd.ResolutionSetting:
        ...
    
    @resolution_settings.setter
    def resolution_settings(self, value : aspose.psd.ResolutionSetting):
        ...
    
    @property
    def vector_rasterization_options(self) -> aspose.psd.imageoptions.VectorRasterizationOptions:
        ...
    
    @vector_rasterization_options.setter
    def vector_rasterization_options(self, value : aspose.psd.imageoptions.VectorRasterizationOptions):
        ...
    
    @property
    def buffer_size_hint(self) -> int:
        ...
    
    @buffer_size_hint.setter
    def buffer_size_hint(self, value : int):
        ...
    
    @property
    def multi_page_options(self) -> aspose.psd.imageoptions.MultiPageOptions:
        ...
    
    @multi_page_options.setter
    def multi_page_options(self, value : aspose.psd.imageoptions.MultiPageOptions):
        ...
    
    @property
    def full_frame(self) -> bool:
        ...
    
    @full_frame.setter
    def full_frame(self, value : bool):
        ...
    
    @property
    def color_type(self) -> aspose.psd.fileformats.png.PngColorType:
        ...
    
    @color_type.setter
    def color_type(self, value : aspose.psd.fileformats.png.PngColorType):
        ...
    
    @property
    def progressive(self) -> bool:
        '''Gets a value indicating whether this  is progressive.'''
        ...
    
    @progressive.setter
    def progressive(self, value : bool):
        '''Sets a value indicating whether this  is progressive.'''
        ...
    
    @property
    def filter_type(self) -> aspose.psd.fileformats.png.PngFilterType:
        ...
    
    @filter_type.setter
    def filter_type(self, value : aspose.psd.fileformats.png.PngFilterType):
        ...
    
    @property
    def compression_level(self) -> int:
        ...
    
    @compression_level.setter
    def compression_level(self, value : int):
        ...
    
    @property
    def bit_depth(self) -> byte:
        ...
    
    @bit_depth.setter
    def bit_depth(self, value : byte):
        ...
    
    @classmethod
    @property
    def DEFAULT_COMPRESSION_LEVEL(cls) -> int:
        ...
    
    ...

class PsdOptions(aspose.psd.ImageOptionsBase):
    '''The psd file format create options.'''
    
    @overload
    def __init__(self):
        '''Initializes a new instance of the  class.'''
        ...
    
    @overload
    def __init__(self, options: aspose.psd.imageoptions.PsdOptions):
        '''Initializes a new instance of the  class.
        
        :param options: The options.'''
        ...
    
    @overload
    def __init__(self, image: aspose.psd.fileformats.psd.PsdImage):
        '''Initializes a new instance of the  class.
        
        :param image: The image.'''
        ...
    
    def clone(self) -> aspose.psd.ImageOptionsBase:
        '''Clones this instance.
        
        :returns: Returns shallow copy of this instance'''
        ...
    
    @property
    def disposed(self) -> bool:
        '''Gets a value indicating whether this instance is disposed.'''
        ...
    
    @property
    def default_replacement_font(self) -> str:
        ...
    
    @default_replacement_font.setter
    def default_replacement_font(self, value : str):
        ...
    
    @property
    def xmp_data(self) -> aspose.psd.xmp.XmpPacketWrapper:
        ...
    
    @xmp_data.setter
    def xmp_data(self, value : aspose.psd.xmp.XmpPacketWrapper):
        ...
    
    @property
    def source(self) -> aspose.psd.Source:
        '''Gets the source to create image in.'''
        ...
    
    @source.setter
    def source(self, value : aspose.psd.Source):
        '''Sets the source to create image in.'''
        ...
    
    @property
    def palette(self) -> aspose.psd.IColorPalette:
        '''Gets the color palette.'''
        ...
    
    @palette.setter
    def palette(self, value : aspose.psd.IColorPalette):
        '''Sets the color palette.'''
        ...
    
    @property
    def resolution_settings(self) -> aspose.psd.ResolutionSetting:
        ...
    
    @resolution_settings.setter
    def resolution_settings(self, value : aspose.psd.ResolutionSetting):
        ...
    
    @property
    def vector_rasterization_options(self) -> aspose.psd.imageoptions.VectorRasterizationOptions:
        ...
    
    @vector_rasterization_options.setter
    def vector_rasterization_options(self, value : aspose.psd.imageoptions.VectorRasterizationOptions):
        ...
    
    @property
    def buffer_size_hint(self) -> int:
        ...
    
    @buffer_size_hint.setter
    def buffer_size_hint(self, value : int):
        ...
    
    @property
    def multi_page_options(self) -> aspose.psd.imageoptions.MultiPageOptions:
        ...
    
    @multi_page_options.setter
    def multi_page_options(self, value : aspose.psd.imageoptions.MultiPageOptions):
        ...
    
    @property
    def full_frame(self) -> bool:
        ...
    
    @full_frame.setter
    def full_frame(self, value : bool):
        ...
    
    @property
    def resources(self) -> List[aspose.psd.fileformats.psd.ResourceBlock]:
        '''Gets the psd resources.'''
        ...
    
    @resources.setter
    def resources(self, value : List[aspose.psd.fileformats.psd.ResourceBlock]):
        '''Sets the psd resources.'''
        ...
    
    @property
    def version(self) -> int:
        '''Gets the psd file version.'''
        ...
    
    @version.setter
    def version(self, value : int):
        '''Sets the psd file version.'''
        ...
    
    @property
    def compression_method(self) -> aspose.psd.fileformats.psd.CompressionMethod:
        ...
    
    @compression_method.setter
    def compression_method(self, value : aspose.psd.fileformats.psd.CompressionMethod):
        ...
    
    @property
    def psd_version(self) -> aspose.psd.fileformats.psd.PsdVersion:
        ...
    
    @psd_version.setter
    def psd_version(self, value : aspose.psd.fileformats.psd.PsdVersion):
        ...
    
    @property
    def color_mode(self) -> aspose.psd.fileformats.psd.ColorModes:
        ...
    
    @color_mode.setter
    def color_mode(self, value : aspose.psd.fileformats.psd.ColorModes):
        ...
    
    @property
    def channel_bits_count(self) -> int:
        ...
    
    @channel_bits_count.setter
    def channel_bits_count(self, value : int):
        ...
    
    @property
    def channels_count(self) -> int:
        ...
    
    @channels_count.setter
    def channels_count(self, value : int):
        ...
    
    @property
    def remove_global_text_engine_resource(self) -> bool:
        ...
    
    @remove_global_text_engine_resource.setter
    def remove_global_text_engine_resource(self, value : bool):
        ...
    
    @property
    def refresh_image_preview_data(self) -> bool:
        ...
    
    @refresh_image_preview_data.setter
    def refresh_image_preview_data(self, value : bool):
        ...
    
    @property
    def update_metadata(self) -> bool:
        ...
    
    @update_metadata.setter
    def update_metadata(self, value : bool):
        ...
    
    @property
    def background_contents(self) -> aspose.psd.fileformats.psd.core.rawcolor.RawColor:
        ...
    
    @background_contents.setter
    def background_contents(self, value : aspose.psd.fileformats.psd.core.rawcolor.RawColor):
        ...
    
    ...

class RdOptimizerSettings:
    '''RD optimizer settings class'''
    
    def __init__(self):
        ...
    
    @staticmethod
    def create() -> aspose.psd.imageoptions.RdOptimizerSettings:
        '''Creates this instance.
        
        :returns: returns RDOptimizerSettings class instance'''
        ...
    
    @property
    def bpp_scale(self) -> int:
        ...
    
    @bpp_scale.setter
    def bpp_scale(self, value : int):
        ...
    
    @property
    def bpp_max(self) -> float:
        ...
    
    @bpp_max.setter
    def bpp_max(self, value : float):
        ...
    
    @property
    def max_q(self) -> int:
        ...
    
    @max_q.setter
    def max_q(self, value : int):
        ...
    
    @property
    def min_q(self) -> int:
        ...
    
    @property
    def max_pixel_value(self) -> int:
        ...
    
    @property
    def psnr_max(self) -> int:
        ...
    
    @property
    def discretized_bpp_max(self) -> int:
        ...
    
    ...

class RenderResult:
    '''Represents information with results of rendering'''
    
    def __init__(self):
        ...
    
    @property
    def message(self) -> str:
        '''Gets string message'''
        ...
    
    @message.setter
    def message(self, value : str):
        '''Sets string message'''
        ...
    
    @property
    def render_code(self) -> aspose.psd.imageoptions.RenderErrorCode:
        ...
    
    @render_code.setter
    def render_code(self, value : aspose.psd.imageoptions.RenderErrorCode):
        ...
    
    ...

class TiffOptions(aspose.psd.ImageOptionsBase):
    '''The tiff file format options.
    Note that width and height tags will get overwritten on image creation by width and height parameters so there is no need to specify them directly.
    Note that many options return a default value but that does not mean that this option is set explicitly as a tag value. To verify the tag is present use Tags property or the corresponding IsTagPresent method.'''
    
    @overload
    def __init__(self, expected_format: aspose.psd.fileformats.tiff.enums.TiffExpectedFormat, byte_order: aspose.psd.fileformats.tiff.enums.TiffByteOrder):
        '''Initializes a new instance of the  class.
        
        :param expected_format: The expected tiff file format.
        :param byte_order: The tiff file format byte order to use.'''
        ...
    
    @overload
    def __init__(self, expected_format: aspose.psd.fileformats.tiff.enums.TiffExpectedFormat):
        '''Initializes a new instance of the  class. By default little endian convention is used.
        
        :param expected_format: The expected tiff file format.'''
        ...
    
    @overload
    def __init__(self, options: aspose.psd.imageoptions.TiffOptions):
        '''Initializes a new instance of the  class.
        
        :param options: The options to copy from.'''
        ...
    
    @overload
    def __init__(self, tags: List[aspose.psd.fileformats.tiff.TiffDataType]):
        '''Initializes a new instance of the  class.
        
        :param tags: The tags to initialize options with.'''
        ...
    
    def clone(self) -> aspose.psd.ImageOptionsBase:
        '''Clones this instance.
        
        :returns: Returns shallow copy of this instance'''
        ...
    
    def is_tag_present(self, tag: aspose.psd.fileformats.tiff.enums.TiffTags) -> bool:
        '''Determines whether tag is present in the options or not.
        
        :param tag: The tag id to check.
        :returns: ``true`` if tag is present; otherwise, ``false``.'''
        ...
    
    @staticmethod
    def get_valid_tags_count(tags: List[aspose.psd.fileformats.tiff.TiffDataType]) -> int:
        '''Gets the valid tags count.
        
        :param tags: The tags to validate.
        :returns: The valid tags count.'''
        ...
    
    def remove_tag(self, tag: aspose.psd.fileformats.tiff.enums.TiffTags) -> bool:
        '''Removes the tag.
        
        :param tag: The tag to remove.
        :returns: true if successfully removed'''
        ...
    
    def validate(self):
        '''Validates if options have valid combination of tags'''
        ...
    
    def add_tags(self, tags_to_add: List[aspose.psd.fileformats.tiff.TiffDataType]):
        '''Adds the tags.
        
        :param tags_to_add: The tags to add.'''
        ...
    
    def add_tag(self, tag_to_add: aspose.psd.fileformats.tiff.TiffDataType):
        '''Adds a new tag.
        
        :param tag_to_add: The tag to add.'''
        ...
    
    def get_tag_by_type(self, tag_key: aspose.psd.fileformats.tiff.enums.TiffTags) -> aspose.psd.fileformats.tiff.TiffDataType:
        '''Gets the instance of the tag by type.
        
        :param tag_key: The tag key.
        :returns: Instance of the tag if exists or null otherwise.'''
        ...
    
    @property
    def disposed(self) -> bool:
        '''Gets a value indicating whether this instance is disposed.'''
        ...
    
    @property
    def default_replacement_font(self) -> str:
        ...
    
    @default_replacement_font.setter
    def default_replacement_font(self, value : str):
        ...
    
    @property
    def xmp_data(self) -> aspose.psd.xmp.XmpPacketWrapper:
        ...
    
    @xmp_data.setter
    def xmp_data(self, value : aspose.psd.xmp.XmpPacketWrapper):
        ...
    
    @property
    def source(self) -> aspose.psd.Source:
        '''Gets the source to create image in.'''
        ...
    
    @source.setter
    def source(self, value : aspose.psd.Source):
        '''Sets the source to create image in.'''
        ...
    
    @property
    def palette(self) -> aspose.psd.IColorPalette:
        '''Gets the color palette.'''
        ...
    
    @palette.setter
    def palette(self, value : aspose.psd.IColorPalette):
        '''Sets the color palette.'''
        ...
    
    @property
    def resolution_settings(self) -> aspose.psd.ResolutionSetting:
        ...
    
    @resolution_settings.setter
    def resolution_settings(self, value : aspose.psd.ResolutionSetting):
        ...
    
    @property
    def vector_rasterization_options(self) -> aspose.psd.imageoptions.VectorRasterizationOptions:
        ...
    
    @vector_rasterization_options.setter
    def vector_rasterization_options(self, value : aspose.psd.imageoptions.VectorRasterizationOptions):
        ...
    
    @property
    def buffer_size_hint(self) -> int:
        ...
    
    @buffer_size_hint.setter
    def buffer_size_hint(self, value : int):
        ...
    
    @property
    def multi_page_options(self) -> aspose.psd.imageoptions.MultiPageOptions:
        ...
    
    @multi_page_options.setter
    def multi_page_options(self, value : aspose.psd.imageoptions.MultiPageOptions):
        ...
    
    @property
    def full_frame(self) -> bool:
        ...
    
    @full_frame.setter
    def full_frame(self, value : bool):
        ...
    
    @property
    def file_standard(self) -> aspose.psd.fileformats.tiff.enums.TiffFileStandards:
        ...
    
    @file_standard.setter
    def file_standard(self, value : aspose.psd.fileformats.tiff.enums.TiffFileStandards):
        ...
    
    @property
    def default_memory_allocation_limit(self) -> int:
        ...
    
    @default_memory_allocation_limit.setter
    def default_memory_allocation_limit(self, value : int):
        ...
    
    @property
    def premultiply_components(self) -> bool:
        ...
    
    @premultiply_components.setter
    def premultiply_components(self, value : bool):
        ...
    
    @property
    def is_valid(self) -> bool:
        ...
    
    @property
    def y_cb_cr_subsampling(self) -> List[int]:
        ...
    
    @y_cb_cr_subsampling.setter
    def y_cb_cr_subsampling(self, value : List[int]):
        ...
    
    @property
    def y_cb_cr_coefficients(self) -> List[aspose.psd.fileformats.tiff.TiffRational]:
        ...
    
    @y_cb_cr_coefficients.setter
    def y_cb_cr_coefficients(self, value : List[aspose.psd.fileformats.tiff.TiffRational]):
        ...
    
    @property
    def is_tiled(self) -> bool:
        ...
    
    @property
    def artist(self) -> str:
        '''Gets the artist.'''
        ...
    
    @artist.setter
    def artist(self, value : str):
        '''Sets the artist.'''
        ...
    
    @property
    def byte_order(self) -> aspose.psd.fileformats.tiff.enums.TiffByteOrder:
        ...
    
    @byte_order.setter
    def byte_order(self, value : aspose.psd.fileformats.tiff.enums.TiffByteOrder):
        ...
    
    @property
    def bits_per_sample(self) -> List[int]:
        ...
    
    @bits_per_sample.setter
    def bits_per_sample(self, value : List[int]):
        ...
    
    @property
    def compression(self) -> aspose.psd.fileformats.tiff.enums.TiffCompressions:
        '''Gets the compression.'''
        ...
    
    @compression.setter
    def compression(self, value : aspose.psd.fileformats.tiff.enums.TiffCompressions):
        '''Sets the compression.'''
        ...
    
    @property
    def compressed_quality(self) -> int:
        ...
    
    @compressed_quality.setter
    def compressed_quality(self, value : int):
        ...
    
    @property
    def copyright(self) -> str:
        '''Gets the copyright.'''
        ...
    
    @copyright.setter
    def copyright(self, value : str):
        '''Sets the copyright.'''
        ...
    
    @property
    def color_map(self) -> List[int]:
        ...
    
    @color_map.setter
    def color_map(self, value : List[int]):
        ...
    
    @property
    def date_time(self) -> str:
        ...
    
    @date_time.setter
    def date_time(self, value : str):
        ...
    
    @property
    def document_name(self) -> str:
        ...
    
    @document_name.setter
    def document_name(self, value : str):
        ...
    
    @property
    def alpha_storage(self) -> aspose.psd.fileformats.tiff.enums.TiffAlphaStorage:
        ...
    
    @alpha_storage.setter
    def alpha_storage(self, value : aspose.psd.fileformats.tiff.enums.TiffAlphaStorage):
        ...
    
    @property
    def is_extra_samples_present(self) -> bool:
        ...
    
    @property
    def fill_order(self) -> aspose.psd.fileformats.tiff.enums.TiffFillOrders:
        ...
    
    @fill_order.setter
    def fill_order(self, value : aspose.psd.fileformats.tiff.enums.TiffFillOrders):
        ...
    
    @property
    def half_tone_hints(self) -> List[int]:
        ...
    
    @half_tone_hints.setter
    def half_tone_hints(self, value : List[int]):
        ...
    
    @property
    def image_description(self) -> str:
        ...
    
    @image_description.setter
    def image_description(self, value : str):
        ...
    
    @property
    def ink_names(self) -> str:
        ...
    
    @ink_names.setter
    def ink_names(self, value : str):
        ...
    
    @property
    def scanner_manufacturer(self) -> str:
        ...
    
    @scanner_manufacturer.setter
    def scanner_manufacturer(self, value : str):
        ...
    
    @property
    def max_sample_value(self) -> List[int]:
        ...
    
    @max_sample_value.setter
    def max_sample_value(self, value : List[int]):
        ...
    
    @property
    def min_sample_value(self) -> List[int]:
        ...
    
    @min_sample_value.setter
    def min_sample_value(self, value : List[int]):
        ...
    
    @property
    def scanner_model(self) -> str:
        ...
    
    @scanner_model.setter
    def scanner_model(self, value : str):
        ...
    
    @property
    def orientation(self) -> aspose.psd.fileformats.tiff.enums.TiffOrientations:
        '''Gets the orientation.'''
        ...
    
    @orientation.setter
    def orientation(self, value : aspose.psd.fileformats.tiff.enums.TiffOrientations):
        '''Sets the orientation.'''
        ...
    
    @property
    def page_name(self) -> str:
        ...
    
    @page_name.setter
    def page_name(self, value : str):
        ...
    
    @property
    def page_number(self) -> List[int]:
        ...
    
    @page_number.setter
    def page_number(self, value : List[int]):
        ...
    
    @property
    def photometric(self) -> aspose.psd.fileformats.tiff.enums.TiffPhotometrics:
        '''Gets the photometric.'''
        ...
    
    @photometric.setter
    def photometric(self, value : aspose.psd.fileformats.tiff.enums.TiffPhotometrics):
        '''Sets the photometric.'''
        ...
    
    @property
    def planar_configuration(self) -> aspose.psd.fileformats.tiff.enums.TiffPlanarConfigs:
        ...
    
    @planar_configuration.setter
    def planar_configuration(self, value : aspose.psd.fileformats.tiff.enums.TiffPlanarConfigs):
        ...
    
    @property
    def resolution_unit(self) -> aspose.psd.fileformats.tiff.enums.TiffResolutionUnits:
        ...
    
    @resolution_unit.setter
    def resolution_unit(self, value : aspose.psd.fileformats.tiff.enums.TiffResolutionUnits):
        ...
    
    @property
    def rows_per_strip(self) -> int:
        ...
    
    @rows_per_strip.setter
    def rows_per_strip(self, value : int):
        ...
    
    @property
    def tile_width(self) -> int:
        ...
    
    @tile_width.setter
    def tile_width(self, value : int):
        ...
    
    @property
    def tile_length(self) -> int:
        ...
    
    @tile_length.setter
    def tile_length(self, value : int):
        ...
    
    @property
    def sample_format(self) -> List[aspose.psd.fileformats.tiff.enums.TiffSampleFormats]:
        ...
    
    @sample_format.setter
    def sample_format(self, value : List[aspose.psd.fileformats.tiff.enums.TiffSampleFormats]):
        ...
    
    @property
    def samples_per_pixel(self) -> int:
        ...
    
    @property
    def smax_sample_value(self) -> List[int]:
        ...
    
    @smax_sample_value.setter
    def smax_sample_value(self, value : List[int]):
        ...
    
    @property
    def smin_sample_value(self) -> List[int]:
        ...
    
    @smin_sample_value.setter
    def smin_sample_value(self, value : List[int]):
        ...
    
    @property
    def software_type(self) -> str:
        ...
    
    @software_type.setter
    def software_type(self, value : str):
        ...
    
    @property
    def strip_byte_counts(self) -> List[int]:
        ...
    
    @strip_byte_counts.setter
    def strip_byte_counts(self, value : List[int]):
        ...
    
    @property
    def strip_offsets(self) -> List[int]:
        ...
    
    @strip_offsets.setter
    def strip_offsets(self, value : List[int]):
        ...
    
    @property
    def tile_byte_counts(self) -> List[int]:
        ...
    
    @tile_byte_counts.setter
    def tile_byte_counts(self, value : List[int]):
        ...
    
    @property
    def tile_offsets(self) -> List[int]:
        ...
    
    @tile_offsets.setter
    def tile_offsets(self, value : List[int]):
        ...
    
    @property
    def sub_file_type(self) -> aspose.psd.fileformats.tiff.enums.TiffNewSubFileTypes:
        ...
    
    @sub_file_type.setter
    def sub_file_type(self, value : aspose.psd.fileformats.tiff.enums.TiffNewSubFileTypes):
        ...
    
    @property
    def target_printer(self) -> str:
        ...
    
    @target_printer.setter
    def target_printer(self, value : str):
        ...
    
    @property
    def threshholding(self) -> aspose.psd.fileformats.tiff.enums.TiffThresholds:
        '''Gets the threshholding.'''
        ...
    
    @threshholding.setter
    def threshholding(self, value : aspose.psd.fileformats.tiff.enums.TiffThresholds):
        '''Sets the threshholding.'''
        ...
    
    @property
    def total_pages(self) -> int:
        ...
    
    @property
    def xposition(self) -> aspose.psd.fileformats.tiff.TiffRational:
        '''Gets the x position.'''
        ...
    
    @xposition.setter
    def xposition(self, value : aspose.psd.fileformats.tiff.TiffRational):
        '''Sets the x position.'''
        ...
    
    @property
    def xresolution(self) -> aspose.psd.fileformats.tiff.TiffRational:
        '''Gets the x resolution.'''
        ...
    
    @xresolution.setter
    def xresolution(self, value : aspose.psd.fileformats.tiff.TiffRational):
        '''Sets the x resolution.'''
        ...
    
    @property
    def yposition(self) -> aspose.psd.fileformats.tiff.TiffRational:
        '''Gets the y position.'''
        ...
    
    @yposition.setter
    def yposition(self, value : aspose.psd.fileformats.tiff.TiffRational):
        '''Sets the y position.'''
        ...
    
    @property
    def yresolution(self) -> aspose.psd.fileformats.tiff.TiffRational:
        '''Gets the y resolution.'''
        ...
    
    @yresolution.setter
    def yresolution(self, value : aspose.psd.fileformats.tiff.TiffRational):
        '''Sets the y resolution.'''
        ...
    
    @property
    def fax_t4_options(self) -> aspose.psd.fileformats.tiff.enums.Group3Options:
        ...
    
    @fax_t4_options.setter
    def fax_t4_options(self, value : aspose.psd.fileformats.tiff.enums.Group3Options):
        ...
    
    @property
    def predictor(self) -> aspose.psd.fileformats.tiff.enums.TiffPredictor:
        '''Gets the predictor for LZW compression.'''
        ...
    
    @predictor.setter
    def predictor(self, value : aspose.psd.fileformats.tiff.enums.TiffPredictor):
        '''Sets the predictor for LZW compression.'''
        ...
    
    @property
    def image_length(self) -> int:
        ...
    
    @image_length.setter
    def image_length(self, value : int):
        ...
    
    @property
    def image_width(self) -> int:
        ...
    
    @image_width.setter
    def image_width(self, value : int):
        ...
    
    @property
    def exif_ifd(self) -> aspose.psd.fileformats.tiff.TiffExifIfd:
        ...
    
    @property
    def tags(self) -> List[aspose.psd.fileformats.tiff.TiffDataType]:
        '''Gets the tags.'''
        ...
    
    @tags.setter
    def tags(self, value : List[aspose.psd.fileformats.tiff.TiffDataType]):
        '''Sets the tags.'''
        ...
    
    @property
    def valid_tag_count(self) -> int:
        ...
    
    @property
    def bits_per_pixel(self) -> int:
        ...
    
    @property
    def xp_title(self) -> str:
        ...
    
    @xp_title.setter
    def xp_title(self, value : str):
        ...
    
    @property
    def xp_comment(self) -> str:
        ...
    
    @xp_comment.setter
    def xp_comment(self, value : str):
        ...
    
    @property
    def xp_author(self) -> str:
        ...
    
    @xp_author.setter
    def xp_author(self, value : str):
        ...
    
    @property
    def xp_keywords(self) -> str:
        ...
    
    @xp_keywords.setter
    def xp_keywords(self, value : str):
        ...
    
    @property
    def xp_subject(self) -> str:
        ...
    
    @xp_subject.setter
    def xp_subject(self, value : str):
        ...
    
    ...

class TiffOptionsUtils:
    '''The tiff file format options utility class.'''
    
    def __init__(self):
        ...
    
    @staticmethod
    def get_valid_tags_count(tags: List[aspose.psd.fileformats.tiff.TiffDataType]) -> int:
        '''Gets the valid tags count.
        
        :param tags: The tags to validate.
        :returns: The valid tags count.'''
        ...
    
    ...

class VectorRasterizationOptions(aspose.psd.ImageOptionsBase):
    '''The vector rasterization options.'''
    
    def clone(self) -> aspose.psd.ImageOptionsBase:
        '''Clones this instance.
        
        :returns: Returns shallow copy of this instance'''
        ...
    
    def copy_to(self, vector_rasterization_options: aspose.psd.imageoptions.VectorRasterizationOptions):
        '''Copies to.
        
        :param vector_rasterization_options: The vector rasterization options.'''
        ...
    
    @property
    def disposed(self) -> bool:
        '''Gets a value indicating whether this instance is disposed.'''
        ...
    
    @property
    def default_replacement_font(self) -> str:
        ...
    
    @default_replacement_font.setter
    def default_replacement_font(self, value : str):
        ...
    
    @property
    def xmp_data(self) -> aspose.psd.xmp.XmpPacketWrapper:
        ...
    
    @xmp_data.setter
    def xmp_data(self, value : aspose.psd.xmp.XmpPacketWrapper):
        ...
    
    @property
    def source(self) -> aspose.psd.Source:
        '''Gets the source to create image in.'''
        ...
    
    @source.setter
    def source(self, value : aspose.psd.Source):
        '''Sets the source to create image in.'''
        ...
    
    @property
    def palette(self) -> aspose.psd.IColorPalette:
        '''Gets the color palette.'''
        ...
    
    @palette.setter
    def palette(self, value : aspose.psd.IColorPalette):
        '''Sets the color palette.'''
        ...
    
    @property
    def resolution_settings(self) -> aspose.psd.ResolutionSetting:
        ...
    
    @resolution_settings.setter
    def resolution_settings(self, value : aspose.psd.ResolutionSetting):
        ...
    
    @property
    def vector_rasterization_options(self) -> aspose.psd.imageoptions.VectorRasterizationOptions:
        ...
    
    @vector_rasterization_options.setter
    def vector_rasterization_options(self, value : aspose.psd.imageoptions.VectorRasterizationOptions):
        ...
    
    @property
    def buffer_size_hint(self) -> int:
        ...
    
    @buffer_size_hint.setter
    def buffer_size_hint(self, value : int):
        ...
    
    @property
    def multi_page_options(self) -> aspose.psd.imageoptions.MultiPageOptions:
        ...
    
    @multi_page_options.setter
    def multi_page_options(self, value : aspose.psd.imageoptions.MultiPageOptions):
        ...
    
    @property
    def full_frame(self) -> bool:
        ...
    
    @full_frame.setter
    def full_frame(self, value : bool):
        ...
    
    @property
    def border_x(self) -> float:
        ...
    
    @border_x.setter
    def border_x(self, value : float):
        ...
    
    @property
    def border_y(self) -> float:
        ...
    
    @border_y.setter
    def border_y(self, value : float):
        ...
    
    @property
    def center_drawing(self) -> bool:
        ...
    
    @center_drawing.setter
    def center_drawing(self, value : bool):
        ...
    
    @property
    def page_height(self) -> float:
        ...
    
    @page_height.setter
    def page_height(self, value : float):
        ...
    
    @property
    def page_size(self) -> aspose.psd.SizeF:
        ...
    
    @page_size.setter
    def page_size(self, value : aspose.psd.SizeF):
        ...
    
    @property
    def page_width(self) -> float:
        ...
    
    @page_width.setter
    def page_width(self, value : float):
        ...
    
    @property
    def background_color(self) -> aspose.psd.Color:
        ...
    
    @background_color.setter
    def background_color(self, value : aspose.psd.Color):
        ...
    
    @property
    def draw_color(self) -> aspose.psd.Color:
        ...
    
    @draw_color.setter
    def draw_color(self, value : aspose.psd.Color):
        ...
    
    @property
    def smoothing_mode(self) -> aspose.psd.SmoothingMode:
        ...
    
    @smoothing_mode.setter
    def smoothing_mode(self, value : aspose.psd.SmoothingMode):
        ...
    
    @property
    def text_rendering_hint(self) -> aspose.psd.TextRenderingHint:
        ...
    
    @text_rendering_hint.setter
    def text_rendering_hint(self, value : aspose.psd.TextRenderingHint):
        ...
    
    ...

class MultiPageMode(enum.Enum):
    PAGES = enum.auto()
    '''Used page indicies'''
    TITLES = enum.auto()
    '''Used page titles'''
    RANGE = enum.auto()
    '''Used range of pages'''
    ALL_PAGES = enum.auto()
    '''Used all pages'''

class PositioningTypes(enum.Enum):
    DEFINED_BY_DOCUMENT = enum.auto()
    '''The absolute positioning on the page that is defined by document page settings.'''
    DEFINED_BY_OPTIONS = enum.auto()
    '''The absolute positioning on the page that is defined by options page settings.'''
    RELATIVE = enum.auto()
    '''The relative positioning and size. Determined by the boundary of all graphics objects.'''

class RenderErrorCode(enum.Enum):
    MISSING_HEADER = enum.auto()
    '''Header is missing'''
    MISSING_LAYOUTS = enum.auto()
    '''Layouts information is missing'''
    MISSING_BLOCKS = enum.auto()
    '''Block information is missing'''
    MISSING_DIMENSION_STYLES = enum.auto()
    '''Dimension styles information is missing'''
    MISSING_STYLES = enum.auto()
    '''Styles information is missing'''

class TiffOptionsError(enum.Enum):
    NO_ERROR = enum.auto()
    '''No error code.'''
    NO_COLOR_MAP = enum.auto()
    '''The color map is not defined.'''
    COLOR_MAP_LENGTH_INVALID = enum.auto()
    '''The color map length is invalid.'''
    COMPRESSION_SPP_MISMATCH = enum.auto()
    '''The compression does not match the samples per pixel count.'''
    PHOTOMETRIC_COMPRESSION_MISMATCH = enum.auto()
    '''The compression does not match the photometric settings.'''
    PHOTOMETRIC_SPP_MISMATCH = enum.auto()
    '''The photometric does not match the samples per pixel count.'''
    NOT_SUPPORTED_ALPHA_STORAGE = enum.auto()
    '''The alpha storage is not supported.'''
    PHOTOMETRIC_BITS_PER_SAMPLE_MISMATCH = enum.auto()
    '''The photometric bits per sample is invalid'''
    BASELINE_6_OPTIONS_MISMATCH = enum.auto()
    '''The specified TIFF options parameters don't conform to TIFF Baseline 6.0 standard'''

class TypeOfEntities(enum.Enum):
    ENTITIES_2D = enum.auto()
    '''Render 2D entities'''
    ENTITIES_3D = enum.auto()
    '''Render 3D entities'''

