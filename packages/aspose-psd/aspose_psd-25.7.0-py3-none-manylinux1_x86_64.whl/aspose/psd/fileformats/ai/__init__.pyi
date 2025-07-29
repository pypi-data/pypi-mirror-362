"""The namespace handles Adobe Illustrator (AI) file format processing."""
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

class AiDataSection(aspose.psd.DisposableObject):
    '''The Ai format Data Section'''
    
    def get_data(self) -> str:
        '''Gets the string data.
        
        :returns: The string data of section'''
        ...
    
    @property
    def disposed(self) -> bool:
        '''Gets a value indicating whether this instance is disposed.'''
        ...
    
    ...

class AiFinalizeSection(AiSection):
    '''The Ai format Finalize Section'''
    
    def get_data(self) -> str:
        '''Gets the string data.
        
        :returns: The string data of section'''
        ...
    
    ...

class AiHeader:
    '''The Adobe illustrator File Header'''
    
    @property
    def creator(self) -> str:
        '''Gets the creator.'''
        ...
    
    @creator.setter
    def creator(self, value : str):
        '''Sets the creator.'''
        ...
    
    @property
    def title(self) -> str:
        '''Gets the title.'''
        ...
    
    @title.setter
    def title(self, value : str):
        '''Sets the title.'''
        ...
    
    @property
    def creation_date(self) -> str:
        ...
    
    @creation_date.setter
    def creation_date(self, value : str):
        ...
    
    @property
    def document_process_colors(self) -> str:
        ...
    
    @document_process_colors.setter
    def document_process_colors(self, value : str):
        ...
    
    @property
    def document_proc_sets(self) -> str:
        ...
    
    @document_proc_sets.setter
    def document_proc_sets(self, value : str):
        ...
    
    @property
    def bounding_box(self) -> aspose.psd.Rectangle:
        ...
    
    @bounding_box.setter
    def bounding_box(self, value : aspose.psd.Rectangle):
        ...
    
    @property
    def color_usage(self) -> str:
        ...
    
    @color_usage.setter
    def color_usage(self, value : str):
        ...
    
    @property
    def template_box(self) -> aspose.psd.RectangleF:
        ...
    
    @template_box.setter
    def template_box(self, value : aspose.psd.RectangleF):
        ...
    
    @property
    def tile_box(self) -> aspose.psd.RectangleF:
        ...
    
    @tile_box.setter
    def tile_box(self, value : aspose.psd.RectangleF):
        ...
    
    @property
    def document_preview(self) -> str:
        ...
    
    @document_preview.setter
    def document_preview(self, value : str):
        ...
    
    ...

class AiImage(aspose.psd.Image):
    '''The Adobe Illustrator (AI)  Image.'''
    
    def __init__(self):
        '''Initializes a new instance of the  class.'''
        ...
    
    @overload
    def save(self):
        '''Saves the image data to the underlying stream.'''
        ...
    
    @overload
    def save(self, file_path: str, options: aspose.psd.ImageOptionsBase):
        '''Saves the object's data to the specified file location in the specified file format according to save options.
        
        :param file_path: The file path.
        :param options: The options.'''
        ...
    
    @overload
    def save(self, file_path: str, options: aspose.psd.ImageOptionsBase, bounds_rectangle: aspose.psd.Rectangle):
        '''Saves the object's data to the specified file location in the specified file format according to save options.
        
        :param file_path: The file path.
        :param options: The options.
        :param bounds_rectangle: The destination image bounds rectangle. Set the empty rectangle for use sourse bounds.'''
        ...
    
    @overload
    def save(self, stream: io.RawIOBase, options_base: aspose.psd.ImageOptionsBase):
        '''Saves the image's data to the specified stream in the specified file format according to save options.
        
        :param stream: The stream to save the image's data to.
        :param options_base: The save options.'''
        ...
    
    @overload
    def save(self, stream: io.RawIOBase, options_base: aspose.psd.ImageOptionsBase, bounds_rectangle: aspose.psd.Rectangle):
        '''Saves the image's data to the specified stream in the specified file format according to save options.
        
        :param stream: The stream to save the image's data to.
        :param options_base: The save options.
        :param bounds_rectangle: The destination image bounds rectangle. Set the empty rectangle for use source bounds.'''
        ...
    
    @overload
    def save(self, stream: io.RawIOBase):
        '''Saves the object's data to the specified stream.
        
        :param stream: The stream to save the object's data to.'''
        ...
    
    @overload
    def save(self, file_path: str):
        '''Saves the object's data to the specified file location.
        
        :param file_path: The file path to save the object's data to.'''
        ...
    
    @overload
    def save(self, file_path: str, over_write: bool):
        '''Saves the object's data to the specified file location.
        
        :param file_path: The file path to save the object's data to.
        :param over_write: if set to ``true`` over write the file contents, otherwise append will occur.'''
        ...
    
    @overload
    @staticmethod
    def can_load(file_path: str) -> bool:
        '''Determines whether image can be loaded from the specified file path.
        
        :param file_path: The file path.
        :returns: ``true`` if image can be loaded from the specified file; otherwise, ``false``.'''
        ...
    
    @overload
    @staticmethod
    def can_load(file_path: str, load_options: aspose.psd.LoadOptions) -> bool:
        '''Determines whether image can be loaded from the specified file path and optionally using the specified open options.
        
        :param file_path: The file path.
        :param load_options: The load options.
        :returns: ``true`` if image can be loaded from the specified file; otherwise, ``false``.'''
        ...
    
    @overload
    @staticmethod
    def can_load(stream: io.RawIOBase) -> bool:
        '''Determines whether image can be loaded from the specified stream.
        
        :param stream: The stream to load from.
        :returns: ``true`` if image can be loaded from the specified stream; otherwise, ``false``.'''
        ...
    
    @overload
    @staticmethod
    def can_load(stream: io.RawIOBase, load_options: aspose.psd.LoadOptions) -> bool:
        '''Determines whether image can be loaded from the specified stream and optionally using the specified ``loadOptions``.
        
        :param stream: The stream to load from.
        :param load_options: The load options.
        :returns: ``true`` if image can be loaded from the specified stream; otherwise, ``false``.'''
        ...
    
    @overload
    @staticmethod
    def get_file_format(file_path: str) -> aspose.psd.FileFormat:
        '''Gets the file format.
        
        :param file_path: The file path.
        :returns: The determined file format.'''
        ...
    
    @overload
    @staticmethod
    def get_file_format(stream: io.RawIOBase) -> aspose.psd.FileFormat:
        '''Gets the file format.
        
        :param stream: The stream.
        :returns: The determined file format.'''
        ...
    
    @overload
    @staticmethod
    def get_fitting_rectangle(rectangle: aspose.psd.Rectangle, width: int, height: int) -> aspose.psd.Rectangle:
        '''Gets rectangle which fits the current image.
        
        :param rectangle: The rectangle to get fitting rectangle for.
        :param width: The object width.
        :param height: The object height.
        :returns: The fitting rectangle or exception if no fitting rectangle can be found.'''
        ...
    
    @overload
    @staticmethod
    def get_fitting_rectangle(rectangle: aspose.psd.Rectangle, pixels: List[int], width: int, height: int) -> aspose.psd.Rectangle:
        '''Gets rectangle which fits the current image.
        
        :param rectangle: The rectangle to get fitting rectangle for.
        :param pixels: The 32-bit ARGB pixels.
        :param width: The object width.
        :param height: The object height.
        :returns: The fitting rectangle or exception if no fitting rectangle can be found.'''
        ...
    
    @overload
    @staticmethod
    def load(file_path: str, load_options: aspose.psd.LoadOptions) -> aspose.psd.Image:
        '''Loads a new image from the specified file.
        
        :param file_path: The file path to load image from.
        :param load_options: The load options.
        :returns: The loaded image.'''
        ...
    
    @overload
    @staticmethod
    def load(file_path: str) -> aspose.psd.Image:
        '''Loads a new image from the specified file.
        
        :param file_path: The file path to load image from.
        :returns: The loaded image.'''
        ...
    
    @overload
    @staticmethod
    def load(stream: io.RawIOBase, load_options: aspose.psd.LoadOptions) -> aspose.psd.Image:
        '''Loads a new image from the specified stream.
        
        :param stream: The stream to load image from.
        :param load_options: The load options.
        :returns: The loaded image.'''
        ...
    
    @overload
    @staticmethod
    def load(stream: io.RawIOBase) -> aspose.psd.Image:
        '''Loads a new image from the specified stream.
        
        :param stream: The stream to load image from.
        :returns: The loaded image.'''
        ...
    
    @overload
    def resize(self, new_width: int, new_height: int, resize_type: aspose.psd.ResizeType):
        '''Resizes the image.
        
        :param new_width: The new width.
        :param new_height: The new height.
        :param resize_type: The resize type.'''
        ...
    
    @overload
    def resize(self, new_width: int, new_height: int, settings: aspose.psd.ImageResizeSettings):
        '''Resizes the image.
        
        :param new_width: The new width.
        :param new_height: The new height.
        :param settings: The resize settings.'''
        ...
    
    @overload
    def resize(self, new_width: int, new_height: int):
        '''Resizes the image. The default  is used.
        
        :param new_width: The new width.
        :param new_height: The new height.'''
        ...
    
    @overload
    def resize_width_proportionally(self, new_width: int):
        '''Resizes the width proportionally. The default  is used.
        
        :param new_width: The new width.'''
        ...
    
    @overload
    def resize_width_proportionally(self, new_width: int, resize_type: aspose.psd.ResizeType):
        '''Resizes the width proportionally.
        
        :param new_width: The new width.
        :param resize_type: Type of the resize.'''
        ...
    
    @overload
    def resize_width_proportionally(self, new_width: int, settings: aspose.psd.ImageResizeSettings):
        '''Resizes the width proportionally.
        
        :param new_width: The new width.
        :param settings: The image resize settings.'''
        ...
    
    @overload
    def resize_height_proportionally(self, new_height: int):
        '''Resizes the height proportionally.
        
        :param new_height: The new height.'''
        ...
    
    @overload
    def resize_height_proportionally(self, new_height: int, resize_type: aspose.psd.ResizeType):
        '''Resizes the height proportionally.
        
        :param new_height: The new height.
        :param resize_type: Type of the resize.'''
        ...
    
    @overload
    def resize_height_proportionally(self, new_height: int, settings: aspose.psd.ImageResizeSettings):
        '''Resizes the height proportionally.
        
        :param new_height: The new height.
        :param settings: The image resize settings.'''
        ...
    
    def cache_data(self):
        '''Caches the data and ensures no additional data loading will be performed from the underlying .'''
        ...
    
    @staticmethod
    def create(image_options: aspose.psd.ImageOptionsBase, width: int, height: int) -> aspose.psd.Image:
        '''Creates a new image using the specified create options.
        
        :param image_options: The image options.
        :param width: The width.
        :param height: The height.
        :returns: The newly created image.'''
        ...
    
    def can_save(self, options: aspose.psd.ImageOptionsBase) -> bool:
        '''Determines whether image can be saved to the specified file format represented by the passed save options.
        
        :param options: The save options to use.
        :returns: ``true`` if image can be saved to the specified file format represented by the passed save options; otherwise, ``false``.'''
        ...
    
    def get_default_options(self, args: List[any]) -> aspose.psd.ImageOptionsBase:
        '''Gets the default options.
        
        :param args: The arguments.
        :returns: Default options'''
        ...
    
    def get_original_options(self) -> aspose.psd.ImageOptionsBase:
        '''Gets the options based on the original file settings.
        This can be helpful to keep bit-depth and other parameters of the original image unchanged.
        For example, if we load a black-white PNG image with 1 bit per pixel and then save it using the
        method, the output PNG image with 8-bit per pixel will be produced.
        To avoid it and save PNG image with 1-bit per pixel, use this method to get corresponding saving options and pass them
        to the  method as the second parameter.
        
        :returns: The options based on the original file settings.'''
        ...
    
    def rotate_flip(self, rotate_flip_type: aspose.psd.RotateFlipType):
        '''Rotates, flips, or rotates and flips the image.
        
        :param rotate_flip_type: Type of the rotate flip.'''
        ...
    
    def set_palette(self, palette: aspose.psd.IColorPalette, update_colors: bool):
        '''Sets the image palette.
        
        :param palette: The palette to set.
        :param update_colors: if set to ``true`` colors will be updated according to the new palette; otherwise color indexes remain unchanged. Note that unchanged indexes may crash the image on loading if some indexes have no corresponding palette entries.'''
        ...
    
    @staticmethod
    def get_proportional_width(width: int, height: int, new_height: int) -> int:
        '''Gets a proportional width.
        
        :param width: The width.
        :param height: The height.
        :param new_height: The new height.
        :returns: The proportional width.'''
        ...
    
    @staticmethod
    def get_proportional_height(width: int, height: int, new_width: int) -> int:
        '''Gets a proportional height.
        
        :param width: The width.
        :param height: The height.
        :param new_width: The new width.
        :returns: The proportional height.'''
        ...
    
    def add_layer(self, layer: aspose.psd.fileformats.ai.AiLayerSection):
        '''Adds the AI layer section.
        
        :param layer: The AI layer section.'''
        ...
    
    @property
    def disposed(self) -> bool:
        '''Gets a value indicating whether this instance is disposed.'''
        ...
    
    @property
    def data_stream_container(self) -> aspose.psd.StreamContainer:
        ...
    
    @property
    def is_cached(self) -> bool:
        ...
    
    @property
    def bits_per_pixel(self) -> int:
        ...
    
    @property
    def bounds(self) -> aspose.psd.Rectangle:
        '''Gets the image bounds.'''
        ...
    
    @property
    def container(self) -> aspose.psd.Image:
        '''Gets the  container.'''
        ...
    
    @property
    def height(self) -> int:
        '''Gets the image height.'''
        ...
    
    @property
    def palette(self) -> aspose.psd.IColorPalette:
        '''Gets the color palette. The color palette is not used when pixels are represented directly.'''
        ...
    
    @palette.setter
    def palette(self, value : aspose.psd.IColorPalette):
        '''Sets the color palette. The color palette is not used when pixels are represented directly.'''
        ...
    
    @property
    def use_palette(self) -> bool:
        ...
    
    @property
    def size(self) -> aspose.psd.Size:
        '''Gets the image size.'''
        ...
    
    @property
    def width(self) -> int:
        '''Gets the image width.'''
        ...
    
    @property
    def interrupt_monitor(self) -> aspose.psd.multithreading.InterruptMonitor:
        ...
    
    @interrupt_monitor.setter
    def interrupt_monitor(self, value : aspose.psd.multithreading.InterruptMonitor):
        ...
    
    @property
    def buffer_size_hint(self) -> int:
        ...
    
    @buffer_size_hint.setter
    def buffer_size_hint(self, value : int):
        ...
    
    @property
    def auto_adjust_palette(self) -> bool:
        ...
    
    @auto_adjust_palette.setter
    def auto_adjust_palette(self, value : bool):
        ...
    
    @property
    def has_background_color(self) -> bool:
        ...
    
    @has_background_color.setter
    def has_background_color(self, value : bool):
        ...
    
    @property
    def file_format(self) -> aspose.psd.FileFormat:
        ...
    
    @property
    def background_color(self) -> aspose.psd.Color:
        ...
    
    @background_color.setter
    def background_color(self, value : aspose.psd.Color):
        ...
    
    @property
    def version(self) -> aspose.psd.fileformats.ai.AiFormatVersion:
        '''Gets the version of Adobe Illustrator format.'''
        ...
    
    @property
    def header(self) -> aspose.psd.fileformats.ai.AiHeader:
        '''Gets the header.'''
        ...
    
    @property
    def setup_section(self) -> aspose.psd.fileformats.ai.AiSetupSection:
        ...
    
    @property
    def finalize_section(self) -> aspose.psd.fileformats.ai.AiFinalizeSection:
        ...
    
    @property
    def data_section(self) -> aspose.psd.fileformats.ai.AiDataSection:
        ...
    
    @property
    def layers(self) -> List[aspose.psd.fileformats.ai.AiLayerSection]:
        '''Gets the layer sections.'''
        ...
    
    @property
    def xmp_data(self) -> aspose.psd.xmp.XmpPacketWrapper:
        ...
    
    @property
    def active_page_index(self) -> int:
        ...
    
    @active_page_index.setter
    def active_page_index(self, value : int):
        ...
    
    @property
    def page_count(self) -> int:
        ...
    
    ...

class AiLayerSection(AiDataSection):
    '''The Ai format Layer Section'''
    
    def get_data(self) -> str:
        '''Gets the string data.
        
        :returns: The string data of section'''
        ...
    
    def add_raster_image(self, raster_image: aspose.psd.fileformats.ai.AiRasterImageSection):
        '''Adds the raster image.
        
        :param raster_image: The raster image.'''
        ...
    
    @property
    def disposed(self) -> bool:
        '''Gets a value indicating whether this instance is disposed.'''
        ...
    
    @property
    def is_template(self) -> bool:
        ...
    
    @is_template.setter
    def is_template(self, value : bool):
        ...
    
    @property
    def is_locked(self) -> bool:
        ...
    
    @is_locked.setter
    def is_locked(self, value : bool):
        ...
    
    @property
    def is_shown(self) -> bool:
        ...
    
    @is_shown.setter
    def is_shown(self, value : bool):
        ...
    
    @property
    def is_printed(self) -> bool:
        ...
    
    @is_printed.setter
    def is_printed(self, value : bool):
        ...
    
    @property
    def is_preview(self) -> bool:
        ...
    
    @is_preview.setter
    def is_preview(self, value : bool):
        ...
    
    @property
    def is_images_dimmed(self) -> bool:
        ...
    
    @is_images_dimmed.setter
    def is_images_dimmed(self, value : bool):
        ...
    
    @property
    def dim_value(self) -> int:
        ...
    
    @dim_value.setter
    def dim_value(self, value : int):
        ...
    
    @property
    def name(self) -> str:
        '''Gets the layer name.
        Specifies the name of the item as it appears in the Layers panel.'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Sets the layer name.
        Specifies the name of the item as it appears in the Layers panel.'''
        ...
    
    @property
    def color_number(self) -> int:
        ...
    
    @color_number.setter
    def color_number(self, value : int):
        ...
    
    @property
    def has_multi_layer_masks(self) -> bool:
        ...
    
    @has_multi_layer_masks.setter
    def has_multi_layer_masks(self, value : bool):
        ...
    
    @property
    def color_index(self) -> int:
        ...
    
    @color_index.setter
    def color_index(self, value : int):
        ...
    
    @property
    def red(self) -> int:
        '''Gets the red color component.'''
        ...
    
    @red.setter
    def red(self, value : int):
        '''Sets the red color component.'''
        ...
    
    @property
    def green(self) -> int:
        '''Gets the green color component.'''
        ...
    
    @green.setter
    def green(self, value : int):
        '''Sets the green color component.'''
        ...
    
    @property
    def blue(self) -> int:
        '''Gets the blue color component.'''
        ...
    
    @blue.setter
    def blue(self, value : int):
        '''Sets the blue color component.'''
        ...
    
    @property
    def raster_images(self) -> List[aspose.psd.fileformats.ai.AiRasterImageSection]:
        ...
    
    ...

class AiRasterImageSection:
    '''The AI Raster Image Section'''
    
    @property
    def name(self) -> str:
        '''Gets the name of the raster image.'''
        ...
    
    @property
    def pixels(self) -> List[int]:
        '''Gets the array of int color pixels.'''
        ...
    
    @property
    def offset_x(self) -> float:
        ...
    
    @property
    def offset_y(self) -> float:
        ...
    
    @property
    def width(self) -> float:
        '''Gets the width.'''
        ...
    
    @property
    def angle(self) -> float:
        '''Gets the angle.'''
        ...
    
    @property
    def left_bottom_shift(self) -> float:
        ...
    
    @property
    def height(self) -> float:
        '''Gets the height.'''
        ...
    
    @property
    def image_rectangle(self) -> aspose.psd.Rectangle:
        ...
    
    ...

class AiSection:
    '''The Ai format base section'''
    
    def get_data(self) -> str:
        '''Gets the string data.
        
        :returns: The string data of section'''
        ...
    
    ...

class AiSetupSection(AiSection):
    '''The Ai format Setup Section'''
    
    def get_data(self) -> str:
        '''Gets the string data.
        
        :returns: The string data of section'''
        ...
    
    ...

class AiFormatVersion(enum.Enum):
    PS_ADOBE_EPSF = enum.auto()
    '''The PS-Adobe EPSF Header'''
    PS_ADOBE20 = enum.auto()
    '''The PS-Adobe-2.0 Header'''
    PS_ADOBE30 = enum.auto()
    '''The PS-Adobe-3.0 Header'''
    PDF14 = enum.auto()
    '''The PDF-1.4 Header'''
    PDF15 = enum.auto()
    '''The PDF-1.5 Header'''
    PDF16 = enum.auto()
    '''The PDF-1.6 Header'''
    PDF17 = enum.auto()
    '''The PDF-1.7 Header'''

