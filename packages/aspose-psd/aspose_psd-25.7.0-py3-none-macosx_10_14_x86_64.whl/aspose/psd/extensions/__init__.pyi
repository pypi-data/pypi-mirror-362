"""The namespace contains extension methods."""
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

class BrushExtensions:
    '''Contains extension methods for  and .'''
    
    @staticmethod
    def to_gdi_brush(brush: aspose.psd.Brush) -> aspose.pydrawing.Brush:
        ...
    
    ...

class ColorBlendExtensions:
    '''Contains  extension methods.'''
    
    @staticmethod
    def to_gdi_color_blend(color_blend: aspose.psd.ColorBlend) -> aspose.pydrawing.drawing2d.ColorBlend:
        ...
    
    ...

class ColorExtensions:
    '''The  extension methods.'''
    
    @staticmethod
    def to_gdi_color(color: aspose.psd.Color) -> aspose.pydrawing.Color:
        '''Converts the  to the .
        
        :param color: The to convert.
        :returns: The converted .'''
        ...
    
    @staticmethod
    def to_gdi_colors(colors: List[aspose.psd.Color]) -> aspose.pydrawing.Color[]:
        '''Converts the  array to the  array.
        
        :param colors: The array to convert.
        :returns: The converted  array.'''
        ...
    
    ...

class ColorMapExtensions:
    '''The  extension methods.'''
    
    @staticmethod
    def to_gdi_color_map(color_map: aspose.psd.ColorMap) -> aspose.pydrawing.imaging.ColorMap:
        ...
    
    @staticmethod
    def to_gdi_color_maps(color_maps: List[aspose.psd.ColorMap]) -> aspose.pydrawing.imaging.ColorMap[]:
        ...
    
    ...

class ColorMatrixExtensions:
    '''The  extension methods.'''
    
    @staticmethod
    def to_gdi_color_matrix(color_matrix: aspose.psd.ColorMatrix) -> aspose.pydrawing.imaging.ColorMatrix:
        ...
    
    ...

class FileFormatExtensions:
    '''Contains  extension methods.'''
    
    @staticmethod
    def is_single_format_defined(file_format: aspose.psd.FileFormat) -> bool:
        '''Determines whether single file format is defined.
        
        :param file_format: The file format to check.
        :returns: ``True`` if single file format is defined; otherwise, ``false``.'''
        ...
    
    ...

class FontExtensions:
    '''Contains extension methods for the  class.'''
    
    @overload
    @staticmethod
    def to_gdi_font(font: aspose.psd.Font) -> aspose.pydrawing.Font:
        ...
    
    @overload
    @staticmethod
    def to_gdi_font(font: aspose.psd.Font, font_unit: aspose.pydrawing.GraphicsUnit) -> aspose.pydrawing.Font:
        ...
    
    ...

class GraphicsPathExtensions:
    '''Contains the  extension methods.'''
    
    @staticmethod
    def to_gdi_graphics_path(graphics_path: aspose.psd.GraphicsPath) -> aspose.pydrawing.drawing2d.GraphicsPath:
        ...
    
    ...

class ImageAttributesExtensions:
    '''Contains extension methods for  and .'''
    
    @staticmethod
    def to_gdi_image_attributes(image_attributes: aspose.psd.ImageAttributes) -> aspose.pydrawing.imaging.ImageAttributes:
        ...
    
    ...

class ImageExtensions:
    '''Contains extension methods for conversions based on  and .'''
    
    @staticmethod
    def to_gdi_image(image: aspose.psd.Image) -> aspose.pydrawing.Image:
        ...
    
    ...

class MatrixExtensions:
    '''Contains the  class extensions.'''
    
    @staticmethod
    def to_gdi_matrix(matrix: aspose.psd.Matrix) -> aspose.pydrawing.drawing2d.Matrix:
        ...
    
    ...

class PenExtensions:
    '''Contains extension methods for  and .'''
    
    @staticmethod
    def to_gdi_pen(pen: aspose.psd.Pen) -> aspose.pydrawing.Pen:
        ...
    
    ...

class PointExtensions:
    '''Contains extension methods for  and  structures.'''
    
    @staticmethod
    def to_points_array(points: List[aspose.psd.Point]) -> List[aspose.psd.PointF]:
        '''Converts the  array to the  array.
        
        :param points: The  array to convert.
        :returns: The converted  array.'''
        ...
    
    @staticmethod
    def to_gdi_points(points: List[aspose.psd.PointF]) -> aspose.pydrawing.PointF[]:
        '''Converts the  array to the  array.
        
        :param points: The  array to convert.
        :returns: The converted  array.'''
        ...
    
    @staticmethod
    def to_gdi_point(point: aspose.psd.PointF) -> aspose.pydrawing.PointF:
        '''Converts the  to .
        
        :param point: The  to convert.
        :returns: The converted .'''
        ...
    
    ...

class RectangleExtensions:
    '''Contains extension methods for .'''
    
    @overload
    @staticmethod
    def to_gdi_rectangle(rectangle: aspose.psd.Rectangle) -> aspose.pydrawing.Rectangle:
        '''Converts the  to the .
        
        :param rectangle: The rectangle to convert.
        :returns: The converted .'''
        ...
    
    @overload
    @staticmethod
    def to_gdi_rectangle(rectangle: aspose.psd.RectangleF) -> aspose.pydrawing.RectangleF:
        '''Converts the  to the .
        
        :param rectangle: The rectangle to convert.
        :returns: The converted .'''
        ...
    
    @staticmethod
    def union_with(rectangle: aspose.psd.RectangleF, other_rectangle: aspose.psd.RectangleF) -> aspose.psd.RectangleF:
        '''Unions two rectangle.
        
        :param rectangle: The first rectangle.
        :param other_rectangle: The second rectangle.
        :returns: New rectangle as union operation result'''
        ...
    
    ...

class RegionExtensions:
    '''Contains extension methods for the  class.'''
    
    @staticmethod
    def to_gdi_region(region: aspose.psd.Region) -> aspose.pydrawing.Region:
        ...
    
    ...

class RotateFlipExtensions:
    '''Contains extension methods for conversion the  and the  classes.'''
    
    @staticmethod
    def to_gdi_rotate_flip_type(rotate_flip_type: aspose.psd.RotateFlipType) -> aspose.pydrawing.RotateFlipType:
        ...
    
    ...

class StringFormatExtensions:
    '''Contains extension methods for the  class.'''
    
    @staticmethod
    def to_gdi_string_format(string_format: aspose.psd.StringFormat) -> aspose.pydrawing.StringFormat:
        ...
    
    ...

