"""The namespace contains Fill Layers"""
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

class FillLayer(aspose.psd.fileformats.psd.layers.Layer):
    '''Fill layer. Color Fill, Gradient Fill or Pattern Fill Layer which differs by'''
    
    @overload
    def save(self, stream: io.RawIOBase):
        '''Saves the object's data to the specified stream.
        
        :param stream: The stream to save the object's data to.'''
        ...
    
    @overload
    def save(self, file_path: str, options: aspose.psd.ImageOptionsBase):
        '''Saves the object's data to the specified file location in the specified file format according to save options.
        
        :param file_path: The file path.
        :param options: The options.'''
        ...
    
    @overload
    def save(self, file_path: str, over_write: bool):
        '''Saves the object's data to the specified file location.
        
        :param file_path: The file path to save the object's data to.
        :param over_write: if set to ``true`` over write the file contents, otherwise append will occur.'''
        ...
    
    @overload
    def save(self, stream: io.RawIOBase, options_base: aspose.psd.ImageOptionsBase, bounds_rectangle: aspose.psd.Rectangle):
        '''Saves the image's data to the specified stream in the specified file format according to save options.
        
        :param stream: The stream to save the image's data to.
        :param options_base: The save options.
        :param bounds_rectangle: The destination image bounds rectangle. Set the empty rectangle for use source bounds.'''
        ...
    
    @overload
    def save(self, file_path: str, options: aspose.psd.ImageOptionsBase, bounds_rectangle: aspose.psd.Rectangle):
        '''Saves the object's data to the specified file location in the specified file format according to save options.
        
        :param file_path: The file path.
        :param options: The options.
        :param bounds_rectangle: The destination image bounds rectangle. Set the empty rectangle for use source bounds.'''
        ...
    
    @overload
    def save(self):
        '''Saves the image data to the underlying stream.'''
        ...
    
    @overload
    def save(self, stream: io.RawIOBase, options_base: aspose.psd.ImageOptionsBase):
        '''Saves the image's data to the specified stream in the specified file format according to save options.
        
        :param stream: The stream to save the image's data to.
        :param options_base: The save options.'''
        ...
    
    @overload
    def save(self, file_path: str):
        '''Saves the object's data to the specified file location.
        
        :param file_path: The file path to save the object's data to.'''
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
    
    @overload
    def dither(self, dithering_method: aspose.psd.DitheringMethod, bits_count: int, custom_palette: aspose.psd.IColorPalette):
        '''Performs dithering on the current image.
        
        :param dithering_method: The dithering method.
        :param bits_count: The final bits count for dithering.
        :param custom_palette: The custom palette for dithering.'''
        ...
    
    @overload
    def dither(self, dithering_method: aspose.psd.DitheringMethod, bits_count: int):
        '''Performs dithering on the current image.
        
        :param dithering_method: The dithering method.
        :param bits_count: The final bits count for dithering.'''
        ...
    
    @overload
    def get_default_raw_data(self, rectangle: aspose.psd.Rectangle, partial_raw_data_loader: aspose.psd.IPartialRawDataLoader, raw_data_settings: aspose.psd.RawDataSettings):
        '''Gets the default raw data array using partial pixel loader.
        
        :param rectangle: The rectangle to get pixels for.
        :param partial_raw_data_loader: The partial raw data loader.
        :param raw_data_settings: The raw data settings.'''
        ...
    
    @overload
    def get_default_raw_data(self, rectangle: aspose.psd.Rectangle, raw_data_settings: aspose.psd.RawDataSettings) -> bytes:
        '''Gets the default raw data array.
        
        :param rectangle: The rectangle to get raw data for.
        :param raw_data_settings: The raw data settings.
        :returns: The default raw data array.'''
        ...
    
    @overload
    def load_raw_data(self, rectangle: aspose.psd.Rectangle, raw_data_settings: aspose.psd.RawDataSettings, raw_data_loader: aspose.psd.IPartialRawDataLoader):
        '''Loads raw data.
        
        :param rectangle: The rectangle to load raw data from.
        :param raw_data_settings: The raw data settings to use for loaded data. Note if data is not in the format specified then data conversion will be performed.
        :param raw_data_loader: The raw data loader.'''
        ...
    
    @overload
    def load_raw_data(self, rectangle: aspose.psd.Rectangle, dest_image_bounds: aspose.psd.Rectangle, raw_data_settings: aspose.psd.RawDataSettings, raw_data_loader: aspose.psd.IPartialRawDataLoader):
        '''Loads raw data.
        
        :param rectangle: The rectangle to load raw data from.
        :param dest_image_bounds: The dest image bounds.
        :param raw_data_settings: The raw data settings to use for loaded data. Note if data is not in the format specified then data conversion will be performed.
        :param raw_data_loader: The raw data loader.'''
        ...
    
    @overload
    def crop(self, rectangle: aspose.psd.Rectangle):
        '''Cropping the image.
        
        :param rectangle: The rectangle.'''
        ...
    
    @overload
    def crop(self, left_shift: int, right_shift: int, top_shift: int, bottom_shift: int):
        ...
    
    @overload
    def binarize_bradley(self, brightness_difference: float, window_size: int):
        '''Binarization of an image using Bradley's adaptive thresholding algorithm using the integral image thresholding
        
        :param brightness_difference: The brightness difference between pixel and the average of an s x s window of pixels centered around this pixel.
        :param window_size: The size of s x s window of pixels centered around this pixel'''
        ...
    
    @overload
    def binarize_bradley(self, brightness_difference: float):
        '''Binarization of an image using Bradley's adaptive thresholding algorithm using the integral image thresholding
        
        :param brightness_difference: The brightness difference between pixel and the average of an s x s window of pixels centered around this pixel.'''
        ...
    
    @overload
    def adjust_gamma(self, gamma_red: float, gamma_green: float, gamma_blue: float):
        '''Gamma-correction of an image.
        
        :param gamma_red: Gamma for red channel coefficient
        :param gamma_green: Gamma for green channel coefficient
        :param gamma_blue: Gamma for blue channel coefficient'''
        ...
    
    @overload
    def adjust_gamma(self, gamma: float):
        '''Gamma-correction of an image.
        
        :param gamma: Gamma for red, green and blue channels coefficient'''
        ...
    
    @overload
    def rotate(self, angle: float, resize_proportionally: bool, background_color: aspose.psd.Color):
        '''Rotate image around the center.
        
        :param angle: The rotate angle in degrees. Positive values will rotate clockwise.
        :param resize_proportionally: if set to ``true`` you will have your image size changed according to rotated rectangle (corner points) projections in other case that leaves dimensions untouched and only internal image contents are rotated.
        :param background_color: Color of the background.'''
        ...
    
    @overload
    def rotate(self, angle: float):
        ...
    
    @overload
    def normalize_angle(self):
        ...
    
    @overload
    def normalize_angle(self, resize_proportionally: bool, background_color: aspose.psd.Color):
        ...
    
    @overload
    def replace_color(self, old_color: aspose.psd.Color, old_color_diff: byte, new_color: aspose.psd.Color):
        ...
    
    @overload
    def replace_color(self, old_color_argb: int, old_color_diff: byte, new_color_argb: int):
        ...
    
    @overload
    def replace_non_transparent_colors(self, new_color_argb: int):
        '''Replaces all non-transparent colors with new color and preserves original alpha value to save smooth edges.
        Note: if you use it on images without transparency, all colors will be replaced with a single one.
        
        :param new_color_argb: New color ARGB value to replace non transparent colors with.'''
        ...
    
    @overload
    def replace_non_transparent_colors(self, new_color: aspose.psd.Color):
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
        
        :param rotate_flip_type: The rotate flip type.'''
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
    
    def get_modify_date(self, use_default: bool) -> DateTime:
        '''Gets the date and time the resource image was last modified.
        
        :param use_default: if set to ``true`` uses the information from FileInfo as default value.
        :returns: The date and time the resource image was last modified.'''
        ...
    
    def get_default_pixels(self, rectangle: aspose.psd.Rectangle, partial_pixel_loader: aspose.psd.IPartialArgb32PixelLoader):
        '''Gets the default pixels array using partial pixel loader.
        
        :param rectangle: The rectangle to get pixels for.
        :param partial_pixel_loader: The partial pixel loader.'''
        ...
    
    def get_default_argb_32_pixels(self, rectangle: aspose.psd.Rectangle) -> List[int]:
        '''Gets the default 32-bit ARGB pixels array.
        
        :param rectangle: The rectangle to get pixels for.
        :returns: The default pixels array.'''
        ...
    
    def get_argb_32_pixel(self, x: int, y: int) -> int:
        '''Gets an image 32-bit ARGB pixel.
        
        :param x: The pixel x location.
        :param y: The pixel y location.
        :returns: The 32-bit ARGB pixel for the specified location.'''
        ...
    
    def get_pixel(self, x: int, y: int) -> aspose.psd.Color:
        '''Gets an image pixel.
        Performance Warning: Avoid using this method to iterate over all image pixels as it can lead to significant performance issues.
        For more efficient pixel manipulation, use the `LoadArgb32Pixels` method to retrieve the entire pixel array simultaneously.
        
        :param x: The pixel x location.
        :param y: The pixel y location.
        :returns: The pixel color for the specified location.'''
        ...
    
    def set_argb_32_pixel(self, x: int, y: int, argb_32_color: int):
        '''Sets an image 32-bit ARGB pixel for the specified position.
        
        :param x: The pixel x location.
        :param y: The pixel y location.
        :param argb_32_color: The 32-bit ARGB pixel for the specified position.'''
        ...
    
    def set_pixel(self, x: int, y: int, color: aspose.psd.Color):
        '''Sets an image pixel for the specified position.
        
        :param x: The pixel x location.
        :param y: The pixel y location.
        :param color: The pixel color for the specified position.'''
        ...
    
    def read_scan_line(self, scan_line_index: int) -> List[aspose.psd.Color]:
        '''Reads the whole scan line by the specified scan line index.
        
        :param scan_line_index: Zero based index of the scan line.
        :returns: The scan line pixel color values array.'''
        ...
    
    def read_argb_32_scan_line(self, scan_line_index: int) -> List[int]:
        '''Reads the whole scan line by the specified scan line index.
        
        :param scan_line_index: Zero based index of the scan line.
        :returns: The scan line 32-bit ARGB color values array.'''
        ...
    
    def write_scan_line(self, scan_line_index: int, pixels: List[aspose.psd.Color]):
        '''Writes the whole scan line to the specified scan line index.
        
        :param scan_line_index: Zero based index of the scan line.
        :param pixels: The pixel colors array to write.'''
        ...
    
    def write_argb_32_scan_line(self, scan_line_index: int, argb_32_pixels: List[int]):
        '''Writes the whole scan line to the specified scan line index.
        
        :param scan_line_index: Zero based index of the scan line.
        :param argb_32_pixels: The 32-bit ARGB colors array to write.'''
        ...
    
    def load_partial_argb_32_pixels(self, rectangle: aspose.psd.Rectangle, partial_pixel_loader: aspose.psd.IPartialArgb32PixelLoader):
        '''Loads 32-bit ARGB pixels partially by packs.
        
        :param rectangle: The desired rectangle.
        :param partial_pixel_loader: The 32-bit ARGB pixel loader.'''
        ...
    
    def load_partial_pixels(self, desired_rectangle: aspose.psd.Rectangle, pixel_loader: aspose.psd.IPartialPixelLoader):
        '''Loads pixels partially by packs.
        
        :param desired_rectangle: The desired rectangle.
        :param pixel_loader: The pixel loader.'''
        ...
    
    def load_argb_32_pixels(self, rectangle: aspose.psd.Rectangle) -> List[int]:
        '''Loads 32-bit ARGB pixels.
        
        :param rectangle: The rectangle to load pixels from.
        :returns: The loaded 32-bit ARGB pixels array.'''
        ...
    
    def load_argb_64_pixels(self, rectangle: aspose.psd.Rectangle) -> List[int]:
        '''Loads 64-bit ARGB pixels.
        
        :param rectangle: The rectangle to load pixels from.
        :returns: The loaded 64-bit ARGB pixels array.'''
        ...
    
    def load_pixels(self, rectangle: aspose.psd.Rectangle) -> List[aspose.psd.Color]:
        '''Loads pixels.
        
        :param rectangle: The rectangle to load pixels from.
        :returns: The loaded pixels array.'''
        ...
    
    def load_cmyk_pixels(self, rectangle: aspose.psd.Rectangle) -> List[aspose.psd.CmykColor]:
        '''Loads pixels in CMYK format.
        This method is deprecated. Please use more effective the  method.
        
        :param rectangle: The rectangle to load pixels from.
        :returns: The loaded CMYK pixels array.'''
        ...
    
    def load_cmyk_32_pixels(self, rectangle: aspose.psd.Rectangle) -> List[int]:
        '''Loads pixels in CMYK format.
        
        :param rectangle: The rectangle to load pixels from.
        :returns: The loaded CMYK pixels presentes as 32-bit inateger values.'''
        ...
    
    def save_raw_data(self, data: bytes, data_offset: int, rectangle: aspose.psd.Rectangle, raw_data_settings: aspose.psd.RawDataSettings):
        '''Saves the raw data.
        
        :param data: The raw data.
        :param data_offset: The starting raw data offset.
        :param rectangle: The raw data rectangle.
        :param raw_data_settings: The raw data settings the data is in.'''
        ...
    
    def save_argb_32_pixels(self, rectangle: aspose.psd.Rectangle, pixels: List[int]):
        '''Saves the 32-bit ARGB pixels.
        
        :param rectangle: The rectangle to save pixels to.
        :param pixels: The 32-bit ARGB pixels array.'''
        ...
    
    def save_pixels(self, rectangle: aspose.psd.Rectangle, pixels: List[aspose.psd.Color]):
        '''Saves the pixels.
        
        :param rectangle: The rectangle to save pixels to.
        :param pixels: The pixels array.'''
        ...
    
    def to_bitmap(self) -> aspose.pydrawing.Bitmap:
        ...
    
    def save_cmyk_pixels(self, rectangle: aspose.psd.Rectangle, pixels: List[aspose.psd.CmykColor]):
        ...
    
    def save_cmyk_32_pixels(self, rectangle: aspose.psd.Rectangle, pixels: List[int]):
        ...
    
    def set_resolution(self, dpi_x: float, dpi_y: float):
        ...
    
    def binarize_fixed(self, threshold: byte):
        '''Binarization of an image with predefined threshold
        
        :param threshold: Threshold value. If corresponding gray value of a pixel is greater than threshold, a value of 255 will be assigned to it, 0 otherwise.'''
        ...
    
    def binarize_otsu(self):
        '''Binarization of an image with Otsu thresholding'''
        ...
    
    def grayscale(self):
        '''Transformation of an image to its grayscale representation'''
        ...
    
    def adjust_brightness(self, brightness: int):
        '''Adjust of a brightness for image.
        
        :param brightness: Brightness value.'''
        ...
    
    def adjust_contrast(self, contrast: float):
        '''Image contrasting
        
        :param contrast: Contrast value (in range [-100; 100])'''
        ...
    
    def get_skew_angle(self) -> float:
        ...
    
    def filter(self, rectangle: aspose.psd.Rectangle, options: aspose.psd.imagefilters.filteroptions.FilterOptionsBase):
        ...
    
    def shallow_copy(self) -> aspose.psd.fileformats.psd.layers.Layer:
        '''Creates a shallow copy of the current Layer.
        Please  for explanation.
        
        :returns: A shallow copy of the current Layer.'''
        ...
    
    def add_layer_mask(self, layer_mask: aspose.psd.fileformats.psd.layers.LayerMaskData):
        '''Adds the mask to current layer.
        
        :param layer_mask: The layer mask.'''
        ...
    
    def apply_layer_mask(self):
        '''Applies the layer mask to layer, then deletes the mask.'''
        ...
    
    def merge_layer_to(self, layer_to_merge_into: aspose.psd.fileformats.psd.layers.Layer):
        '''Merges the layer to specified layer
        
        :param layer_to_merge_into: The layer to merge into.'''
        ...
    
    def draw_image(self, location: aspose.psd.Point, image: aspose.psd.RasterImage):
        '''Draws the image on layer.
        
        :param location: The location.
        :param image: The image.'''
        ...
    
    @staticmethod
    def create_instance(fill_type: aspose.psd.fileformats.psd.layers.fillsettings.FillType) -> aspose.psd.fileformats.psd.layers.filllayers.FillLayer:
        '''Build a new instance of the  class by type of fill.
        
        :param fill_type: The type of fill layer.
        :returns: Returns a new instance of the  class by type of fill.'''
        ...
    
    def update(self):
        '''Updates the pixel data of the fill layer based on the current .'''
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
    def premultiply_components(self) -> bool:
        ...
    
    @premultiply_components.setter
    def premultiply_components(self, value : bool):
        ...
    
    @property
    def use_raw_data(self) -> bool:
        ...
    
    @use_raw_data.setter
    def use_raw_data(self, value : bool):
        ...
    
    @property
    def update_xmp_data(self) -> bool:
        ...
    
    @update_xmp_data.setter
    def update_xmp_data(self, value : bool):
        ...
    
    @property
    def xmp_data(self) -> aspose.psd.xmp.XmpPacketWrapper:
        ...
    
    @xmp_data.setter
    def xmp_data(self, value : aspose.psd.xmp.XmpPacketWrapper):
        ...
    
    @property
    def raw_indexed_color_converter(self) -> aspose.psd.IIndexedColorConverter:
        ...
    
    @raw_indexed_color_converter.setter
    def raw_indexed_color_converter(self, value : aspose.psd.IIndexedColorConverter):
        ...
    
    @property
    def raw_custom_color_converter(self) -> aspose.psd.IColorConverter:
        ...
    
    @raw_custom_color_converter.setter
    def raw_custom_color_converter(self, value : aspose.psd.IColorConverter):
        ...
    
    @property
    def raw_fallback_index(self) -> int:
        ...
    
    @raw_fallback_index.setter
    def raw_fallback_index(self, value : int):
        ...
    
    @property
    def raw_data_settings(self) -> aspose.psd.RawDataSettings:
        ...
    
    @property
    def raw_data_format(self) -> aspose.psd.PixelDataFormat:
        ...
    
    @property
    def raw_line_size(self) -> int:
        ...
    
    @property
    def is_raw_data_available(self) -> bool:
        ...
    
    @property
    def horizontal_resolution(self) -> float:
        ...
    
    @horizontal_resolution.setter
    def horizontal_resolution(self, value : float):
        ...
    
    @property
    def vertical_resolution(self) -> float:
        ...
    
    @vertical_resolution.setter
    def vertical_resolution(self, value : float):
        ...
    
    @property
    def has_transparent_color(self) -> bool:
        ...
    
    @has_transparent_color.setter
    def has_transparent_color(self, value : bool):
        ...
    
    @property
    def has_alpha(self) -> bool:
        ...
    
    @property
    def transparent_color(self) -> aspose.psd.Color:
        ...
    
    @transparent_color.setter
    def transparent_color(self, value : aspose.psd.Color):
        ...
    
    @property
    def image_opacity(self) -> float:
        ...
    
    @property
    def resources(self) -> List[aspose.psd.fileformats.psd.layers.LayerResource]:
        '''Gets the layer resources.'''
        ...
    
    @resources.setter
    def resources(self, value : List[aspose.psd.fileformats.psd.layers.LayerResource]):
        '''Sets the layer resources.'''
        ...
    
    @property
    def name(self) -> str:
        '''Gets the layer name.'''
        ...
    
    @name.setter
    def name(self, value : str):
        '''Sets the layer name.'''
        ...
    
    @property
    def blending_options(self) -> aspose.psd.fileformats.psd.layers.layereffects.BlendingOptions:
        ...
    
    @property
    def display_name(self) -> str:
        ...
    
    @display_name.setter
    def display_name(self, value : str):
        ...
    
    @property
    def fill_opacity(self) -> int:
        ...
    
    @fill_opacity.setter
    def fill_opacity(self, value : int):
        ...
    
    @property
    def layer_creation_date_time(self) -> DateTime:
        ...
    
    @layer_creation_date_time.setter
    def layer_creation_date_time(self, value : DateTime):
        ...
    
    @property
    def sheet_color_highlight(self) -> aspose.psd.fileformats.psd.layers.layerresources.SheetColorHighlightEnum:
        ...
    
    @sheet_color_highlight.setter
    def sheet_color_highlight(self, value : aspose.psd.fileformats.psd.layers.layerresources.SheetColorHighlightEnum):
        ...
    
    @property
    def top(self) -> int:
        '''Gets the top layer position.'''
        ...
    
    @top.setter
    def top(self, value : int):
        '''Sets the top layer position.'''
        ...
    
    @property
    def left(self) -> int:
        '''Gets the left layer position.'''
        ...
    
    @left.setter
    def left(self, value : int):
        '''Sets the left layer position.'''
        ...
    
    @property
    def bottom(self) -> int:
        '''Gets the bottom layer position.'''
        ...
    
    @bottom.setter
    def bottom(self, value : int):
        '''Sets the bottom layer position.'''
        ...
    
    @property
    def right(self) -> int:
        '''Gets the right layer position.'''
        ...
    
    @right.setter
    def right(self, value : int):
        '''Sets the right layer position.'''
        ...
    
    @property
    def channels_count(self) -> int:
        ...
    
    @property
    def channel_information(self) -> List[aspose.psd.fileformats.psd.layers.ChannelInformation]:
        ...
    
    @channel_information.setter
    def channel_information(self, value : List[aspose.psd.fileformats.psd.layers.ChannelInformation]):
        ...
    
    @property
    def blend_mode_signature(self) -> int:
        ...
    
    @property
    def blend_mode_key(self) -> aspose.psd.fileformats.core.blending.BlendMode:
        ...
    
    @blend_mode_key.setter
    def blend_mode_key(self, value : aspose.psd.fileformats.core.blending.BlendMode):
        ...
    
    @property
    def opacity(self) -> byte:
        '''Gets the layer opacity. 0 = transparent, 255 = opaque.'''
        ...
    
    @opacity.setter
    def opacity(self, value : byte):
        '''Sets the layer opacity. 0 = transparent, 255 = opaque.'''
        ...
    
    @property
    def clipping(self) -> byte:
        '''Gets the layer clipping. 0 = base, 1 = non-base.'''
        ...
    
    @clipping.setter
    def clipping(self, value : byte):
        '''Sets the layer clipping. 0 = base, 1 = non-base.'''
        ...
    
    @property
    def flags(self) -> aspose.psd.fileformats.psd.layers.LayerFlags:
        '''Gets the layer flags.
        bit 0 = transparency protected;
        bit 1 = visible;
        bit 2 = obsolete;
        bit 3 = 1 for Photoshop 5.0 and later, tells if bit 4 has useful information;
        bit 4 = pixel data irrelevant to appearance of document.'''
        ...
    
    @flags.setter
    def flags(self, value : aspose.psd.fileformats.psd.layers.LayerFlags):
        '''Sets the layer flags.
        bit 0 = transparency protected;
        bit 1 = visible;
        bit 2 = obsolete;
        bit 3 = 1 for Photoshop 5.0 and later, tells if bit 4 has useful information;
        bit 4 = pixel data irrelevant to appearance of document.'''
        ...
    
    @property
    def filler(self) -> byte:
        '''Gets the layer filler.'''
        ...
    
    @filler.setter
    def filler(self, value : byte):
        '''Sets the layer filler.'''
        ...
    
    @property
    def length(self) -> int:
        '''Gets the overall layer length in bytes.'''
        ...
    
    @property
    def extra_length(self) -> int:
        ...
    
    @property
    def layer_mask_data(self) -> aspose.psd.fileformats.psd.layers.LayerMaskData:
        ...
    
    @layer_mask_data.setter
    def layer_mask_data(self, value : aspose.psd.fileformats.psd.layers.LayerMaskData):
        ...
    
    @property
    def layer_blending_ranges_data(self) -> aspose.psd.fileformats.psd.layers.LayerBlendingRangesData:
        ...
    
    @layer_blending_ranges_data.setter
    def layer_blending_ranges_data(self, value : aspose.psd.fileformats.psd.layers.LayerBlendingRangesData):
        ...
    
    @property
    def layer_options(self) -> aspose.psd.imageoptions.PsdOptions:
        ...
    
    @property
    def is_visible(self) -> bool:
        ...
    
    @is_visible.setter
    def is_visible(self, value : bool):
        ...
    
    @property
    def is_visible_in_group(self) -> bool:
        ...
    
    @property
    def layer_lock(self) -> aspose.psd.fileformats.psd.layers.layerresources.LayerLockType:
        ...
    
    @layer_lock.setter
    def layer_lock(self, value : aspose.psd.fileformats.psd.layers.layerresources.LayerLockType):
        ...
    
    @property
    def blend_clipped_elements(self) -> bool:
        ...
    
    @blend_clipped_elements.setter
    def blend_clipped_elements(self, value : bool):
        ...
    
    @classmethod
    @property
    def LAYER_HEADER_SIZE(cls) -> int:
        ...
    
    @classmethod
    @property
    def BLEND_SIGNATURE(cls) -> int:
        ...
    
    @property
    def fill_settings(self) -> aspose.psd.fileformats.psd.layers.fillsettings.IFillSettings:
        ...
    
    @fill_settings.setter
    def fill_settings(self, value : aspose.psd.fileformats.psd.layers.fillsettings.IFillSettings):
        ...
    
    @property
    def fill_type(self) -> aspose.psd.fileformats.psd.layers.fillsettings.FillType:
        ...
    
    ...

