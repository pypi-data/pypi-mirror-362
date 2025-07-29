"""The namespace contains different shapes combined from shape segments."""
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

class ArcShape(PieShape):
    '''Represents an arc shape.'''
    
    @overload
    def __init__(self):
        '''Initializes a new instance of the  class.'''
        ...
    
    @overload
    def __init__(self, rectangle: aspose.psd.RectangleF, start_angle: float, sweep_angle: float):
        '''Initializes a new instance of the  class.
        
        :param rectangle: The rectangle.
        :param start_angle: The start angle.
        :param sweep_angle: The sweep angle.'''
        ...
    
    @overload
    def __init__(self, rectangle: aspose.psd.RectangleF, start_angle: float, sweep_angle: float, is_closed: bool):
        '''Initializes a new instance of the  class.
        
        :param rectangle: The rectangle.
        :param start_angle: The start angle.
        :param sweep_angle: The sweep angle.
        :param is_closed: If set to ``true`` the arc is closed. The closed arc is actually degenereates to an ellipse.'''
        ...
    
    @overload
    def get_bounds(self, matrix: aspose.psd.Matrix) -> aspose.psd.RectangleF:
        '''Gets the object's bounds.
        
        :param matrix: The matrix to apply before bounds will be calculated.
        :returns: The estimated object's bounds.'''
        ...
    
    @overload
    def get_bounds(self, matrix: aspose.psd.Matrix, pen: aspose.psd.Pen) -> aspose.psd.RectangleF:
        '''Gets the object's bounds.
        
        :param matrix: The matrix to apply before bounds will be calculated.
        :param pen: The pen to use for object. This can influence the object's bounds size.
        :returns: The estimated object's bounds.'''
        ...
    
    def transform(self, transform: aspose.psd.Matrix):
        '''Applies the specified transformation to the shape.
        
        :param transform: The transformation to apply.'''
        ...
    
    def reverse(self):
        '''Reverses the order of points for this shape.'''
        ...
    
    @property
    def bounds(self) -> aspose.psd.RectangleF:
        '''Gets the object's bounds.'''
        ...
    
    @property
    def center(self) -> aspose.psd.PointF:
        '''Gets the shape's center.'''
        ...
    
    @property
    def segments(self) -> List[aspose.psd.ShapeSegment]:
        '''Gets the shape segments.'''
        ...
    
    @property
    def has_segments(self) -> bool:
        ...
    
    @property
    def left_top(self) -> aspose.psd.PointF:
        ...
    
    @property
    def right_top(self) -> aspose.psd.PointF:
        ...
    
    @property
    def left_bottom(self) -> aspose.psd.PointF:
        ...
    
    @property
    def right_bottom(self) -> aspose.psd.PointF:
        ...
    
    @property
    def rectangle_width(self) -> float:
        ...
    
    @property
    def rectangle_height(self) -> float:
        ...
    
    @property
    def start_angle(self) -> float:
        ...
    
    @start_angle.setter
    def start_angle(self, value : float):
        ...
    
    @property
    def sweep_angle(self) -> float:
        ...
    
    @sweep_angle.setter
    def sweep_angle(self, value : float):
        ...
    
    @property
    def start_point(self) -> aspose.psd.PointF:
        ...
    
    @property
    def end_point(self) -> aspose.psd.PointF:
        ...
    
    @property
    def is_closed(self) -> bool:
        ...
    
    @is_closed.setter
    def is_closed(self, value : bool):
        ...
    
    ...

class BezierShape(PolygonShape):
    '''Represents a bezier spline.'''
    
    @overload
    def __init__(self):
        '''Initializes a new instance of the  class.'''
        ...
    
    @overload
    def __init__(self, points: List[aspose.psd.PointF]):
        '''Initializes a new instance of the  class.
        
        :param points: The points array.'''
        ...
    
    @overload
    def __init__(self, points: List[aspose.psd.PointF], is_closed: bool):
        '''Initializes a new instance of the  class.
        
        :param points: The points array.
        :param is_closed: If set to ``true`` the bezier spline is closed.'''
        ...
    
    @overload
    def get_bounds(self, matrix: aspose.psd.Matrix) -> aspose.psd.RectangleF:
        '''Gets the object's bounds.
        
        :param matrix: The matrix to apply before bounds will be calculated.
        :returns: The estimated object's bounds.'''
        ...
    
    @overload
    def get_bounds(self, matrix: aspose.psd.Matrix, pen: aspose.psd.Pen) -> aspose.psd.RectangleF:
        '''Gets the object's bounds.
        
        :param matrix: The matrix to apply before bounds will be calculated.
        :param pen: The pen to use for object. This can influence the object's bounds size.
        :returns: The estimated object's bounds.'''
        ...
    
    def transform(self, transform: aspose.psd.Matrix):
        '''Applies the specified transformation to the shape.
        
        :param transform: The transformation to apply.'''
        ...
    
    def reverse(self):
        '''Reverses the order of points for this shape.'''
        ...
    
    @property
    def bounds(self) -> aspose.psd.RectangleF:
        '''Gets the object's bounds.'''
        ...
    
    @property
    def center(self) -> aspose.psd.PointF:
        '''Gets the shape's center.'''
        ...
    
    @property
    def segments(self) -> List[aspose.psd.ShapeSegment]:
        '''Gets the shape segments.'''
        ...
    
    @property
    def has_segments(self) -> bool:
        ...
    
    @property
    def points(self) -> List[aspose.psd.PointF]:
        '''Gets the curve points.'''
        ...
    
    @points.setter
    def points(self, value : List[aspose.psd.PointF]):
        '''Sets the curve points.'''
        ...
    
    @property
    def is_closed(self) -> bool:
        ...
    
    @is_closed.setter
    def is_closed(self, value : bool):
        ...
    
    @property
    def start_point(self) -> aspose.psd.PointF:
        ...
    
    @property
    def end_point(self) -> aspose.psd.PointF:
        ...
    
    ...

class CurveShape(PolygonShape):
    '''Represents a curved spline shape.'''
    
    @overload
    def __init__(self):
        '''Initializes a new instance of the  class.'''
        ...
    
    @overload
    def __init__(self, points: List[aspose.psd.PointF]):
        '''Initializes a new instance of the  class. The default tension of 0.5 is used.
        
        :param points: The points array.'''
        ...
    
    @overload
    def __init__(self, points: List[aspose.psd.PointF], is_closed: bool):
        '''Initializes a new instance of the  class. The default tension of 0.5 is used.
        
        :param points: The points array.
        :param is_closed: if set to ``true`` the curve is closed.'''
        ...
    
    @overload
    def __init__(self, points: List[aspose.psd.PointF], tension: float):
        '''Initializes a new instance of the  class.
        
        :param points: The points array.
        :param tension: The curve tension.'''
        ...
    
    @overload
    def __init__(self, points: List[aspose.psd.PointF], tension: float, is_closed: bool):
        '''Initializes a new instance of the  class.
        
        :param points: The points array.
        :param tension: The curve tension.
        :param is_closed: if set to ``true`` the curve is closed.'''
        ...
    
    @overload
    def get_bounds(self, matrix: aspose.psd.Matrix) -> aspose.psd.RectangleF:
        '''Gets the object's bounds.
        
        :param matrix: The matrix to apply before bounds will be calculated.
        :returns: The estimated object's bounds.'''
        ...
    
    @overload
    def get_bounds(self, matrix: aspose.psd.Matrix, pen: aspose.psd.Pen) -> aspose.psd.RectangleF:
        '''Gets the object's bounds.
        
        :param matrix: The matrix to apply before bounds will be calculated.
        :param pen: The pen to use for object. This can influence the object's bounds size.
        :returns: The estimated object's bounds.'''
        ...
    
    def transform(self, transform: aspose.psd.Matrix):
        '''Applies the specified transformation to the shape.
        
        :param transform: The transformation to apply.'''
        ...
    
    def reverse(self):
        '''Reverses the order of points for this shape.'''
        ...
    
    @property
    def bounds(self) -> aspose.psd.RectangleF:
        '''Gets the object's bounds.'''
        ...
    
    @property
    def center(self) -> aspose.psd.PointF:
        '''Gets the shape's center.'''
        ...
    
    @property
    def segments(self) -> List[aspose.psd.ShapeSegment]:
        '''Gets the shape segments.'''
        ...
    
    @property
    def has_segments(self) -> bool:
        ...
    
    @property
    def points(self) -> List[aspose.psd.PointF]:
        '''Gets the curve points.'''
        ...
    
    @points.setter
    def points(self, value : List[aspose.psd.PointF]):
        '''Sets the curve points.'''
        ...
    
    @property
    def is_closed(self) -> bool:
        ...
    
    @is_closed.setter
    def is_closed(self, value : bool):
        ...
    
    @property
    def start_point(self) -> aspose.psd.PointF:
        ...
    
    @property
    def end_point(self) -> aspose.psd.PointF:
        ...
    
    @property
    def tension(self) -> float:
        '''Gets the curve tension.'''
        ...
    
    @tension.setter
    def tension(self, value : float):
        '''Sets the curve tension.'''
        ...
    
    ...

class EllipseShape(RectangleShape):
    '''Represents an ellipse shape.'''
    
    @overload
    def __init__(self):
        '''Initializes a new instance of the  class.'''
        ...
    
    @overload
    def __init__(self, rectangle: aspose.psd.RectangleF):
        '''Initializes a new instance of the  class.
        
        :param rectangle: The rectangle.'''
        ...
    
    @overload
    def get_bounds(self, matrix: aspose.psd.Matrix) -> aspose.psd.RectangleF:
        '''Gets the object's bounds.
        
        :param matrix: The matrix to apply before bounds will be calculated.
        :returns: The estimated object's bounds.'''
        ...
    
    @overload
    def get_bounds(self, matrix: aspose.psd.Matrix, pen: aspose.psd.Pen) -> aspose.psd.RectangleF:
        '''Gets the object's bounds.
        
        :param matrix: The matrix to apply before bounds will be calculated.
        :param pen: The pen to use for object. This can influence the object's bounds size.
        :returns: The estimated object's bounds.'''
        ...
    
    def transform(self, transform: aspose.psd.Matrix):
        '''Applies the specified transformation to the shape.
        
        :param transform: The transformation to apply.'''
        ...
    
    @property
    def bounds(self) -> aspose.psd.RectangleF:
        '''Gets the object's bounds.'''
        ...
    
    @property
    def center(self) -> aspose.psd.PointF:
        '''Gets the shape's center.'''
        ...
    
    @property
    def segments(self) -> List[aspose.psd.ShapeSegment]:
        '''Gets the shape segments.'''
        ...
    
    @property
    def has_segments(self) -> bool:
        ...
    
    @property
    def left_top(self) -> aspose.psd.PointF:
        ...
    
    @property
    def right_top(self) -> aspose.psd.PointF:
        ...
    
    @property
    def left_bottom(self) -> aspose.psd.PointF:
        ...
    
    @property
    def right_bottom(self) -> aspose.psd.PointF:
        ...
    
    @property
    def rectangle_width(self) -> float:
        ...
    
    @property
    def rectangle_height(self) -> float:
        ...
    
    ...

class PieShape(EllipseShape):
    '''Represents a pie shape.'''
    
    @overload
    def __init__(self):
        '''Initializes a new instance of the  class.'''
        ...
    
    @overload
    def __init__(self, rectangle: aspose.psd.RectangleF, start_angle: float, sweep_angle: float):
        '''Initializes a new instance of the  class.
        
        :param rectangle: The rectangle.
        :param start_angle: The start angle.
        :param sweep_angle: The sweep angle.'''
        ...
    
    @overload
    def get_bounds(self, matrix: aspose.psd.Matrix) -> aspose.psd.RectangleF:
        '''Gets the object's bounds.
        
        :param matrix: The matrix to apply before bounds will be calculated.
        :returns: The estimated object's bounds.'''
        ...
    
    @overload
    def get_bounds(self, matrix: aspose.psd.Matrix, pen: aspose.psd.Pen) -> aspose.psd.RectangleF:
        '''Gets the object's bounds.
        
        :param matrix: The matrix to apply before bounds will be calculated.
        :param pen: The pen to use for object. This can influence the object's bounds size.
        :returns: The estimated object's bounds.'''
        ...
    
    def transform(self, transform: aspose.psd.Matrix):
        '''Applies the specified transformation to the shape.
        
        :param transform: The transformation to apply.'''
        ...
    
    @property
    def bounds(self) -> aspose.psd.RectangleF:
        '''Gets the object's bounds.'''
        ...
    
    @property
    def center(self) -> aspose.psd.PointF:
        '''Gets the shape's center.'''
        ...
    
    @property
    def segments(self) -> List[aspose.psd.ShapeSegment]:
        '''Gets the shape segments.'''
        ...
    
    @property
    def has_segments(self) -> bool:
        ...
    
    @property
    def left_top(self) -> aspose.psd.PointF:
        ...
    
    @property
    def right_top(self) -> aspose.psd.PointF:
        ...
    
    @property
    def left_bottom(self) -> aspose.psd.PointF:
        ...
    
    @property
    def right_bottom(self) -> aspose.psd.PointF:
        ...
    
    @property
    def rectangle_width(self) -> float:
        ...
    
    @property
    def rectangle_height(self) -> float:
        ...
    
    @property
    def start_angle(self) -> float:
        ...
    
    @start_angle.setter
    def start_angle(self, value : float):
        ...
    
    @property
    def sweep_angle(self) -> float:
        ...
    
    @sweep_angle.setter
    def sweep_angle(self, value : float):
        ...
    
    ...

class PolygonShape(aspose.psd.Shape):
    '''Represents a polygon shape.'''
    
    @overload
    def __init__(self):
        '''Initializes a new instance of the  class.'''
        ...
    
    @overload
    def __init__(self, points: List[aspose.psd.PointF]):
        '''Initializes a new instance of the  class.
        
        :param points: The points array.'''
        ...
    
    @overload
    def __init__(self, points: List[aspose.psd.PointF], is_closed: bool):
        '''Initializes a new instance of the  class.
        
        :param points: The points array.
        :param is_closed: If set to ``true`` the polygon is closed.'''
        ...
    
    @overload
    def get_bounds(self, matrix: aspose.psd.Matrix) -> aspose.psd.RectangleF:
        '''Gets the object's bounds.
        
        :param matrix: The matrix to apply before bounds will be calculated.
        :returns: The estimated object's bounds.'''
        ...
    
    @overload
    def get_bounds(self, matrix: aspose.psd.Matrix, pen: aspose.psd.Pen) -> aspose.psd.RectangleF:
        '''Gets the object's bounds.
        
        :param matrix: The matrix to apply before bounds will be calculated.
        :param pen: The pen to use for object. This can influence the object's bounds size.
        :returns: The estimated object's bounds.'''
        ...
    
    def transform(self, transform: aspose.psd.Matrix):
        '''Applies the specified transformation to the shape.
        
        :param transform: The transformation to apply.'''
        ...
    
    def reverse(self):
        '''Reverses the order of points for this shape.'''
        ...
    
    @property
    def bounds(self) -> aspose.psd.RectangleF:
        '''Gets the object's bounds.'''
        ...
    
    @property
    def center(self) -> aspose.psd.PointF:
        '''Gets the shape's center.'''
        ...
    
    @property
    def segments(self) -> List[aspose.psd.ShapeSegment]:
        '''Gets the shape segments.'''
        ...
    
    @property
    def has_segments(self) -> bool:
        ...
    
    @property
    def points(self) -> List[aspose.psd.PointF]:
        '''Gets the curve points.'''
        ...
    
    @points.setter
    def points(self, value : List[aspose.psd.PointF]):
        '''Sets the curve points.'''
        ...
    
    @property
    def is_closed(self) -> bool:
        ...
    
    @is_closed.setter
    def is_closed(self, value : bool):
        ...
    
    @property
    def start_point(self) -> aspose.psd.PointF:
        ...
    
    @property
    def end_point(self) -> aspose.psd.PointF:
        ...
    
    ...

class RectangleProjectedShape(aspose.psd.Shape):
    '''Represents a shape which is projected over rectangle turned to a particular orientation.
    Specified by four points which can be rotated in space maintaining the same edges length and 90 degrees between adjacent edges.'''
    
    @overload
    def get_bounds(self, matrix: aspose.psd.Matrix) -> aspose.psd.RectangleF:
        '''Gets the object's bounds.
        
        :param matrix: The matrix to apply before bounds will be calculated.
        :returns: The estimated object's bounds.'''
        ...
    
    @overload
    def get_bounds(self, matrix: aspose.psd.Matrix, pen: aspose.psd.Pen) -> aspose.psd.RectangleF:
        '''Gets the object's bounds.
        
        :param matrix: The matrix to apply before bounds will be calculated.
        :param pen: The pen to use for object. This can influence the object's bounds size.
        :returns: The estimated object's bounds.'''
        ...
    
    def transform(self, transform: aspose.psd.Matrix):
        '''Applies the specified transformation to the shape.
        
        :param transform: The transformation to apply.'''
        ...
    
    @property
    def bounds(self) -> aspose.psd.RectangleF:
        '''Gets the object's bounds.'''
        ...
    
    @property
    def center(self) -> aspose.psd.PointF:
        '''Gets the shape's center.'''
        ...
    
    @property
    def segments(self) -> List[aspose.psd.ShapeSegment]:
        '''Gets the shape segments.'''
        ...
    
    @property
    def has_segments(self) -> bool:
        ...
    
    @property
    def left_top(self) -> aspose.psd.PointF:
        ...
    
    @property
    def right_top(self) -> aspose.psd.PointF:
        ...
    
    @property
    def left_bottom(self) -> aspose.psd.PointF:
        ...
    
    @property
    def right_bottom(self) -> aspose.psd.PointF:
        ...
    
    @property
    def rectangle_width(self) -> float:
        ...
    
    @property
    def rectangle_height(self) -> float:
        ...
    
    ...

class RectangleShape(RectangleProjectedShape):
    '''Represents a rectangular shape.'''
    
    @overload
    def __init__(self):
        '''Initializes a new instance of the  class.'''
        ...
    
    @overload
    def __init__(self, rectangle: aspose.psd.RectangleF):
        '''Initializes a new instance of the  class.
        
        :param rectangle: The rectangle.'''
        ...
    
    @overload
    def get_bounds(self, matrix: aspose.psd.Matrix) -> aspose.psd.RectangleF:
        '''Gets the object's bounds.
        
        :param matrix: The matrix to apply before bounds will be calculated.
        :returns: The estimated object's bounds.'''
        ...
    
    @overload
    def get_bounds(self, matrix: aspose.psd.Matrix, pen: aspose.psd.Pen) -> aspose.psd.RectangleF:
        '''Gets the object's bounds.
        
        :param matrix: The matrix to apply before bounds will be calculated.
        :param pen: The pen to use for object. This can influence the object's bounds size.
        :returns: The estimated object's bounds.'''
        ...
    
    def transform(self, transform: aspose.psd.Matrix):
        '''Applies the specified transformation to the shape.
        
        :param transform: The transformation to apply.'''
        ...
    
    @property
    def bounds(self) -> aspose.psd.RectangleF:
        '''Gets the object's bounds.'''
        ...
    
    @property
    def center(self) -> aspose.psd.PointF:
        '''Gets the shape's center.'''
        ...
    
    @property
    def segments(self) -> List[aspose.psd.ShapeSegment]:
        '''Gets the shape segments.'''
        ...
    
    @property
    def has_segments(self) -> bool:
        ...
    
    @property
    def left_top(self) -> aspose.psd.PointF:
        ...
    
    @property
    def right_top(self) -> aspose.psd.PointF:
        ...
    
    @property
    def left_bottom(self) -> aspose.psd.PointF:
        ...
    
    @property
    def right_bottom(self) -> aspose.psd.PointF:
        ...
    
    @property
    def rectangle_width(self) -> float:
        ...
    
    @property
    def rectangle_height(self) -> float:
        ...
    
    ...

class TextShape(RectangleProjectedShape):
    '''Represents a text shape.'''
    
    @overload
    def __init__(self):
        '''Initializes a new instance of the  class.'''
        ...
    
    @overload
    def __init__(self, text: str, rectangle: aspose.psd.RectangleF, font: aspose.psd.Font, string_format: aspose.psd.StringFormat):
        '''Initializes a new instance of the  class.
        
        :param text: The text to draw.
        :param rectangle: The text rectangle.
        :param font: The font to use.
        :param string_format: The string format.'''
        ...
    
    @overload
    def get_bounds(self, matrix: aspose.psd.Matrix) -> aspose.psd.RectangleF:
        '''Gets the object's bounds.
        
        :param matrix: The matrix to apply before bounds will be calculated.
        :returns: The estimated object's bounds.'''
        ...
    
    @overload
    def get_bounds(self, matrix: aspose.psd.Matrix, pen: aspose.psd.Pen) -> aspose.psd.RectangleF:
        '''Gets the object's bounds.
        
        :param matrix: The matrix to apply before bounds will be calculated.
        :param pen: The pen to use for object. This can influence the object's bounds size.
        :returns: The estimated object's bounds.'''
        ...
    
    def transform(self, transform: aspose.psd.Matrix):
        '''Applies the specified transformation to the shape.
        
        :param transform: The transformation to apply.'''
        ...
    
    @property
    def bounds(self) -> aspose.psd.RectangleF:
        '''Gets the object's bounds.'''
        ...
    
    @property
    def center(self) -> aspose.psd.PointF:
        '''Gets the shape's center.'''
        ...
    
    @property
    def segments(self) -> List[aspose.psd.ShapeSegment]:
        '''Gets the shape segments.'''
        ...
    
    @property
    def has_segments(self) -> bool:
        ...
    
    @property
    def left_top(self) -> aspose.psd.PointF:
        ...
    
    @property
    def right_top(self) -> aspose.psd.PointF:
        ...
    
    @property
    def left_bottom(self) -> aspose.psd.PointF:
        ...
    
    @property
    def right_bottom(self) -> aspose.psd.PointF:
        ...
    
    @property
    def rectangle_width(self) -> float:
        ...
    
    @property
    def rectangle_height(self) -> float:
        ...
    
    @property
    def text(self) -> str:
        '''Gets the drawn text.'''
        ...
    
    @text.setter
    def text(self, value : str):
        '''Sets the drawn text.'''
        ...
    
    @property
    def font(self) -> aspose.psd.Font:
        '''Gets the font used to draw the text.'''
        ...
    
    @font.setter
    def font(self, value : aspose.psd.Font):
        '''Sets the font used to draw the text.'''
        ...
    
    @property
    def text_format(self) -> aspose.psd.StringFormat:
        ...
    
    @text_format.setter
    def text_format(self, value : aspose.psd.StringFormat):
        ...
    
    ...

