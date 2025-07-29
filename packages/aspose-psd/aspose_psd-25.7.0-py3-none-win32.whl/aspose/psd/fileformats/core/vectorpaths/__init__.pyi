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

class BezierKnotRecord(VectorPathRecord):
    '''Bezier Knot Record Class, used to read/write Bezier knots data from resource.'''
    
    @property
    def type(self) -> aspose.psd.fileformats.core.vectorpaths.VectorPathType:
        '''Gets the type.'''
        ...
    
    @property
    def path_points(self) -> List[aspose.psd.PointF]:
        ...
    
    @path_points.setter
    def path_points(self, value : List[aspose.psd.PointF]):
        ...
    
    @property
    def points(self) -> List[aspose.psd.Point]:
        '''Gets the points.'''
        ...
    
    @points.setter
    def points(self, value : List[aspose.psd.Point]):
        '''Sets the points.'''
        ...
    
    @property
    def is_closed(self) -> bool:
        ...
    
    @is_closed.setter
    def is_closed(self, value : bool):
        ...
    
    @property
    def is_linked(self) -> bool:
        ...
    
    @is_linked.setter
    def is_linked(self, value : bool):
        ...
    
    @property
    def is_open(self) -> bool:
        ...
    
    @is_open.setter
    def is_open(self, value : bool):
        ...
    
    ...

class ClipboardRecord(VectorPathRecord):
    '''Clipboard Record Class'''
    
    @property
    def type(self) -> aspose.psd.fileformats.core.vectorpaths.VectorPathType:
        '''Gets the type.'''
        ...
    
    @property
    def bounding_rect(self) -> aspose.psd.RectangleF:
        ...
    
    @bounding_rect.setter
    def bounding_rect(self, value : aspose.psd.RectangleF):
        ...
    
    @property
    def resolution(self) -> float:
        '''Gets the resolution.'''
        ...
    
    @resolution.setter
    def resolution(self, value : float):
        '''Sets the resolution.'''
        ...
    
    ...

class IVectorPathData:
    '''The interface for access to the vector path data.'''
    
    @property
    def paths(self) -> List[aspose.psd.fileformats.core.vectorpaths.VectorPathRecord]:
        '''Gets the path records.'''
        ...
    
    @paths.setter
    def paths(self, value : List[aspose.psd.fileformats.core.vectorpaths.VectorPathRecord]):
        '''Sets the path records.'''
        ...
    
    @property
    def version(self) -> int:
        '''Gets the version.'''
        ...
    
    @version.setter
    def version(self, value : int):
        '''Sets the version.'''
        ...
    
    @property
    def is_disabled(self) -> bool:
        ...
    
    @is_disabled.setter
    def is_disabled(self, value : bool):
        ...
    
    @property
    def is_not_linked(self) -> bool:
        ...
    
    @is_not_linked.setter
    def is_not_linked(self, value : bool):
        ...
    
    @property
    def is_inverted(self) -> bool:
        ...
    
    @is_inverted.setter
    def is_inverted(self, value : bool):
        ...
    
    ...

class InitialFillRuleRecord(VectorPathRecord):
    '''Initial Fill Rule Record Class'''
    
    @property
    def type(self) -> aspose.psd.fileformats.core.vectorpaths.VectorPathType:
        '''Gets the type.'''
        ...
    
    @property
    def is_fill_starts_with_all_pixels(self) -> bool:
        ...
    
    @is_fill_starts_with_all_pixels.setter
    def is_fill_starts_with_all_pixels(self, value : bool):
        ...
    
    ...

class LengthRecord(VectorPathRecord):
    '''Subpath Length Record Class.'''
    
    @property
    def type(self) -> aspose.psd.fileformats.core.vectorpaths.VectorPathType:
        '''Gets the type.'''
        ...
    
    @property
    def is_closed(self) -> bool:
        ...
    
    @is_closed.setter
    def is_closed(self, value : bool):
        ...
    
    @property
    def is_open(self) -> bool:
        ...
    
    @is_open.setter
    def is_open(self, value : bool):
        ...
    
    @property
    def record_count(self) -> int:
        ...
    
    @record_count.setter
    def record_count(self, value : int):
        ...
    
    @property
    def bezier_knot_records_count(self) -> int:
        ...
    
    @bezier_knot_records_count.setter
    def bezier_knot_records_count(self, value : int):
        ...
    
    @property
    def path_operations(self) -> aspose.psd.fileformats.core.vectorpaths.PathOperations:
        ...
    
    @path_operations.setter
    def path_operations(self, value : aspose.psd.fileformats.core.vectorpaths.PathOperations):
        ...
    
    @property
    def shape_index(self) -> int:
        ...
    
    @shape_index.setter
    def shape_index(self, value : int):
        ...
    
    ...

class PathFillRuleRecord(VectorPathRecord):
    '''Path Fill Rule Record Class'''
    
    @property
    def type(self) -> aspose.psd.fileformats.core.vectorpaths.VectorPathType:
        '''Gets the type.'''
        ...
    
    ...

class VectorPathRecord:
    '''Vector Path Record Class'''
    
    @property
    def type(self) -> aspose.psd.fileformats.core.vectorpaths.VectorPathType:
        '''Gets the type.'''
        ...
    
    ...

class VectorPathRecordFactory:
    '''Vector Path Record Factory Class.'''
    
    @staticmethod
    def produce_path_record(data : bytes) -> aspose.psd.fileformats.core.vectorpaths.VectorPathRecord:
        '''Produces the path record.
        
        :param data: The record data.
        :returns: Created :py:class:`aspose.psd.fileformats.core.vectorpaths.VectorPathRecord`.'''
        ...
    
    ...

class VectorShapeBoundingBox:
    '''Defines vector shape bounding box class.'''
    
    @property
    def left(self) -> float:
        '''Gets the left.'''
        ...
    
    @left.setter
    def left(self, value : float):
        '''Sets the left.'''
        ...
    
    @property
    def top(self) -> float:
        '''Gets the top.'''
        ...
    
    @top.setter
    def top(self, value : float):
        '''Sets the top.'''
        ...
    
    @property
    def right(self) -> float:
        '''Gets the right.'''
        ...
    
    @right.setter
    def right(self, value : float):
        '''Sets the right.'''
        ...
    
    @property
    def bottom(self) -> float:
        '''Gets the bottom.'''
        ...
    
    @bottom.setter
    def bottom(self, value : float):
        '''Sets the bottom.'''
        ...
    
    @property
    def quad_version(self) -> int:
        ...
    
    @quad_version.setter
    def quad_version(self, value : int):
        ...
    
    @property
    def points_unit_type(self) -> aspose.psd.fileformats.psd.layers.layerresources.typetoolinfostructures.UnitTypes:
        ...
    
    @points_unit_type.setter
    def points_unit_type(self, value : aspose.psd.fileformats.psd.layers.layerresources.typetoolinfostructures.UnitTypes):
        ...
    
    @property
    def bounds(self) -> aspose.psd.Rectangle:
        '''Gets the bounds of the shape bounding box.'''
        ...
    
    @bounds.setter
    def bounds(self, value : aspose.psd.Rectangle):
        '''Sets the bounds of the shape bounding box.'''
        ...
    
    ...

class VectorShapeOriginSettings:
    '''Vector shape origination settings.'''
    
    @property
    def is_shape_invalidated(self) -> bool:
        ...
    
    @is_shape_invalidated.setter
    def is_shape_invalidated(self, value : bool):
        ...
    
    @property
    def origin_index(self) -> int:
        ...
    
    @origin_index.setter
    def origin_index(self, value : int):
        ...
    
    @property
    def origin_type(self) -> int:
        ...
    
    @origin_type.setter
    def origin_type(self, value : int):
        ...
    
    @property
    def origin_resolution(self) -> float:
        ...
    
    @origin_resolution.setter
    def origin_resolution(self, value : float):
        ...
    
    @property
    def origin_shape_box(self) -> aspose.psd.fileformats.core.vectorpaths.VectorShapeBoundingBox:
        ...
    
    @origin_shape_box.setter
    def origin_shape_box(self, value : aspose.psd.fileformats.core.vectorpaths.VectorShapeBoundingBox):
        ...
    
    @property
    def origin_radii_rectangle(self) -> aspose.psd.fileformats.core.vectorpaths.VectorShapeRadiiRectangle:
        ...
    
    @origin_radii_rectangle.setter
    def origin_radii_rectangle(self, value : aspose.psd.fileformats.core.vectorpaths.VectorShapeRadiiRectangle):
        ...
    
    @property
    def transform(self) -> aspose.psd.fileformats.core.vectorpaths.VectorShapeTransform:
        '''Gets the transformation matrix.'''
        ...
    
    @transform.setter
    def transform(self, value : aspose.psd.fileformats.core.vectorpaths.VectorShapeTransform):
        '''Sets the transformation matrix.'''
        ...
    
    @property
    def is_shape_invalidated_present(self) -> bool:
        ...
    
    @property
    def is_origin_index_present(self) -> bool:
        ...
    
    @property
    def is_origin_type_present(self) -> bool:
        ...
    
    @property
    def is_origin_resolution_present(self) -> bool:
        ...
    
    @property
    def is_origin_radii_rectangle_present(self) -> bool:
        ...
    
    @property
    def is_origin_shape_b_box_present(self) -> bool:
        ...
    
    @property
    def is_origin_box_corners_present(self) -> bool:
        ...
    
    @property
    def is_transform_present(self) -> bool:
        ...
    
    @property
    def origin_box_corners(self) -> List[float]:
        ...
    
    @origin_box_corners.setter
    def origin_box_corners(self, value : List[float]):
        ...
    
    ...

class VectorShapeRadiiRectangle:
    '''Defines vector shape radii rectangle class'''
    
    @property
    def top_left(self) -> float:
        ...
    
    @top_left.setter
    def top_left(self, value : float):
        ...
    
    @property
    def top_right(self) -> float:
        ...
    
    @top_right.setter
    def top_right(self, value : float):
        ...
    
    @property
    def bottom_right(self) -> float:
        ...
    
    @bottom_right.setter
    def bottom_right(self, value : float):
        ...
    
    @property
    def bottom_left(self) -> float:
        ...
    
    @bottom_left.setter
    def bottom_left(self, value : float):
        ...
    
    @property
    def quad_version(self) -> int:
        ...
    
    @quad_version.setter
    def quad_version(self, value : int):
        ...
    
    ...

class VectorShapeTransform:
    '''Defines vector shape transformation matrix class'''
    
    @property
    def xx(self) -> float:
        '''Gets the XX value.'''
        ...
    
    @xx.setter
    def xx(self, value : float):
        '''Sets the XX value.'''
        ...
    
    @property
    def xy(self) -> float:
        '''Gets the XY value.'''
        ...
    
    @xy.setter
    def xy(self, value : float):
        '''Sets the XY value.'''
        ...
    
    @property
    def yx(self) -> float:
        '''Gets the YX value.'''
        ...
    
    @yx.setter
    def yx(self, value : float):
        '''Sets the YX value.'''
        ...
    
    @property
    def yy(self) -> float:
        '''Gets the YY value.'''
        ...
    
    @yy.setter
    def yy(self, value : float):
        '''Sets the YY value.'''
        ...
    
    @property
    def tx(self) -> float:
        '''Gets the TX value.'''
        ...
    
    @tx.setter
    def tx(self, value : float):
        '''Sets the TX value.'''
        ...
    
    @property
    def ty(self) -> float:
        '''Gets the TY value.'''
        ...
    
    @ty.setter
    def ty(self, value : float):
        '''Sets the TY value.'''
        ...
    
    ...

class PathOperations:
    '''The operations for the path shapes combining (Boolean operations).'''
    
    @classmethod
    @property
    def EXCLUDE_OVERLAPPING_SHAPES(cls) -> PathOperations:
        '''Exclude Overlapping Shapes (XOR operation).'''
        ...
    
    @classmethod
    @property
    def COMBINE_SHAPES(cls) -> PathOperations:
        '''Combine Shapes (OR operation). This is default value in Photoshop.'''
        ...
    
    @classmethod
    @property
    def SUBTRACT_FRONT_SHAPE(cls) -> PathOperations:
        '''Subtract Front Shape (NOT operation).'''
        ...
    
    @classmethod
    @property
    def INTERSECT_SHAPE_AREAS(cls) -> PathOperations:
        '''Intersect Shape Areas (AND operation).'''
        ...
    
    ...

class VectorPathType:
    '''Vector Path Type according to PSD Format Specification'''
    
    @classmethod
    @property
    def CLOSED_SUBPATH_LENGTH_RECORD(cls) -> VectorPathType:
        '''The closed subpath length record'''
        ...
    
    @classmethod
    @property
    def CLOSED_SUBPATH_BEZIER_KNOT_LINKED(cls) -> VectorPathType:
        '''The closed subpath bezier knot linked'''
        ...
    
    @classmethod
    @property
    def CLOSED_SUBPATH_BEZIER_KNOT_UNLINKED(cls) -> VectorPathType:
        '''The closed subpath bezier knot unlinked'''
        ...
    
    @classmethod
    @property
    def OPEN_SUBPATH_LENGTH_RECORD(cls) -> VectorPathType:
        '''The open subpath length record'''
        ...
    
    @classmethod
    @property
    def OPEN_SUBPATH_BEZIER_KNOT_LINKED(cls) -> VectorPathType:
        '''The open subpath bezier knot linked'''
        ...
    
    @classmethod
    @property
    def OPEN_SUBPATH_BEZIER_KNOT_UNLINKED(cls) -> VectorPathType:
        '''The open subpath bezier knot unlinked'''
        ...
    
    @classmethod
    @property
    def PATH_FILL_RULE_RECORD(cls) -> VectorPathType:
        '''The path fill rule record'''
        ...
    
    @classmethod
    @property
    def CLIPBOARD_RECORD(cls) -> VectorPathType:
        '''The clipboard record'''
        ...
    
    @classmethod
    @property
    def INITIAL_FILL_RULE_RECORD(cls) -> VectorPathType:
        '''The initial fill rule record'''
        ...
    
    ...

