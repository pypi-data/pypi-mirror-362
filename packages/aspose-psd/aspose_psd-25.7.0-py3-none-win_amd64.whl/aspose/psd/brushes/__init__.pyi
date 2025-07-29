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

class HatchBrush(aspose.psd.Brush):
    '''Defines a rectangular brush with a hatch style, a foreground color, and a background color. This class cannot be inherited.'''
    
    def deep_clone(self) -> aspose.psd.Brush:
        '''Creates a new deep clone of the current :py:class:`aspose.psd.Brush`.
        
        :returns: A new :py:class:`aspose.psd.Brush` which is the deep clone of this :py:class:`aspose.psd.Brush` instance.'''
        ...
    
    @property
    def disposed(self) -> bool:
        '''Gets a value indicating whether this instance is disposed.'''
        ...
    
    @property
    def opacity(self) -> float:
        '''Gets the brush opacity. The value should be between 0 and 1. Value of 0 means that brush is fully visible, value of 1 means the brush is fully opaque.'''
        ...
    
    @opacity.setter
    def opacity(self, value : float):
        '''Sets the brush opacity. The value should be between 0 and 1. Value of 0 means that brush is fully visible, value of 1 means the brush is fully opaque.'''
        ...
    
    @property
    def foreground_color(self) -> aspose.psd.Color:
        ...
    
    @foreground_color.setter
    def foreground_color(self, value : aspose.psd.Color):
        ...
    
    @property
    def background_color(self) -> aspose.psd.Color:
        ...
    
    @background_color.setter
    def background_color(self, value : aspose.psd.Color):
        ...
    
    @property
    def hatch_style(self) -> aspose.psd.HatchStyle:
        ...
    
    @hatch_style.setter
    def hatch_style(self, value : aspose.psd.HatchStyle):
        ...
    
    ...

class LinearGradientBrush(LinearGradientBrushBase):
    '''Encapsulates a :py:class:`aspose.psd.Brush` with a linear gradient. This class cannot be inherited.'''
    
    @overload
    def multiply_transform(self, matrix : aspose.psd.Matrix):
        '''Multiplies the :py:class:`aspose.psd.Matrix` that represents the local geometric transform of this :py:class:`aspose.psd.brushes.LinearGradientBrush` by the specified :py:class:`aspose.psd.Matrix` by prepending the specified :py:class:`aspose.psd.Matrix`.
        
        :param matrix: The :py:class:`aspose.psd.Matrix` by which to multiply the geometric transform.'''
        ...
    
    @overload
    def multiply_transform(self, matrix : aspose.psd.Matrix, order : aspose.psd.MatrixOrder):
        '''Multiplies the :py:class:`aspose.psd.Matrix` that represents the local geometric transform of this :py:class:`aspose.psd.brushes.LinearGradientBrush` by the specified :py:class:`aspose.psd.Matrix` in the specified order.
        
        :param matrix: The :py:class:`aspose.psd.Matrix` by which to multiply the geometric transform.
        :param order: A :py:class:`aspose.psd.MatrixOrder` that specifies in which order to multiply the two matrices.'''
        ...
    
    @overload
    def translate_transform(self, dx : float, dy : float):
        '''Translates the local geometric transform by the specified dimensions. This method prepends the translation to the transform.
        
        :param dx: The value of the translation in x.
        :param dy: The value of the translation in y.'''
        ...
    
    @overload
    def translate_transform(self, dx : float, dy : float, order : aspose.psd.MatrixOrder):
        '''Translates the local geometric transform by the specified dimensions in the specified order.
        
        :param dx: The value of the translation in x.
        :param dy: The value of the translation in y.
        :param order: The order (prepend or append) in which to apply the translation.'''
        ...
    
    @overload
    def scale_transform(self, sx : float, sy : float):
        '''Scales the local geometric transform by the specified amounts. This method prepends the scaling matrix to the transform.
        
        :param sx: The amount by which to scale the transform in the x-axis direction.
        :param sy: The amount by which to scale the transform in the y-axis direction.'''
        ...
    
    @overload
    def scale_transform(self, sx : float, sy : float, order : aspose.psd.MatrixOrder):
        '''Scales the local geometric transform by the specified amounts in the specified order.
        
        :param sx: The amount by which to scale the transform in the x-axis direction.
        :param sy: The amount by which to scale the transform in the y-axis direction.
        :param order: A :py:class:`aspose.psd.MatrixOrder` that specifies whether to append or prepend the scaling matrix.'''
        ...
    
    @overload
    def rotate_transform(self, angle : float):
        '''Rotates the local geometric transform by the specified amount. This method prepends the rotation to the transform.
        
        :param angle: The angle of rotation.'''
        ...
    
    @overload
    def rotate_transform(self, angle : float, order : aspose.psd.MatrixOrder):
        '''Rotates the local geometric transform by the specified amount in the specified order.
        
        :param angle: The angle of rotation.
        :param order: A :py:class:`aspose.psd.MatrixOrder` that specifies whether to append or prepend the rotation matrix.'''
        ...
    
    @overload
    def set_sigma_bell_shape(self, focus : float):
        '''Creates a gradient falloff based on a bell-shaped curve.
        
        :param focus: A value from 0 through 1 that specifies the center of the gradient (the point where the starting color and ending color are blended equally).'''
        ...
    
    @overload
    def set_sigma_bell_shape(self, focus : float, scale : float):
        '''Creates a gradient falloff based on a bell-shaped curve.
        
        :param focus: A value from 0 through 1 that specifies the center of the gradient (the point where the gradient is composed of only the ending color).
        :param scale: A value from 0 through 1 that specifies how fast the colors falloff from the ``focus``.'''
        ...
    
    @overload
    def set_blend_triangular_shape(self, focus : float):
        '''Creates a linear gradient with a center color and a linear falloff to a single color on both ends.
        
        :param focus: A value from 0 through 1 that specifies the center of the gradient (the point where the gradient is composed of only the ending color).'''
        ...
    
    @overload
    def set_blend_triangular_shape(self, focus : float, scale : float):
        '''Creates a linear gradient with a center color and a linear falloff to a single color on both ends.
        
        :param focus: A value from 0 through 1 that specifies the center of the gradient (the point where the gradient is composed of only the ending color).
        :param scale: A value from 0 through1 that specifies how fast the colors falloff from the starting color to ``focus`` (ending color)'''
        ...
    
    def deep_clone(self) -> aspose.psd.Brush:
        '''Creates a new deep clone of the current :py:class:`aspose.psd.Brush`.
        
        :returns: A new :py:class:`aspose.psd.Brush` which is the deep clone of this :py:class:`aspose.psd.Brush` instance.'''
        ...
    
    def reset_transform(self):
        '''Resets the :py:attr:`aspose.psd.brushes.TransformBrush.transform` property to identity.'''
        ...
    
    @property
    def disposed(self) -> bool:
        '''Gets a value indicating whether this instance is disposed.'''
        ...
    
    @property
    def opacity(self) -> float:
        '''Gets the brush opacity. The value should be between 0 and 1. Value of 0 means that brush is fully visible, value of 1 means the brush is fully opaque.'''
        ...
    
    @opacity.setter
    def opacity(self, value : float):
        '''Sets the brush opacity. The value should be between 0 and 1. Value of 0 means that brush is fully visible, value of 1 means the brush is fully opaque.'''
        ...
    
    @property
    def wrap_mode(self) -> aspose.psd.WrapMode:
        ...
    
    @wrap_mode.setter
    def wrap_mode(self, value : aspose.psd.WrapMode):
        ...
    
    @property
    def transform(self) -> aspose.psd.Matrix:
        '''Gets a copy :py:class:`aspose.psd.Matrix` that defines a local geometric transform for this :py:class:`aspose.psd.brushes.TransformBrush`.'''
        ...
    
    @transform.setter
    def transform(self, value : aspose.psd.Matrix):
        '''Sets a copy :py:class:`aspose.psd.Matrix` that defines a local geometric transform for this :py:class:`aspose.psd.brushes.TransformBrush`.'''
        ...
    
    @property
    def is_transform_changed(self) -> bool:
        ...
    
    @property
    def rectangle(self) -> aspose.psd.RectangleF:
        '''Gets a rectangular region that defines the starting and ending points of the gradient.'''
        ...
    
    @rectangle.setter
    def rectangle(self, value : aspose.psd.RectangleF):
        '''Sets a rectangular region that defines the starting and ending points of the gradient.'''
        ...
    
    @property
    def angle(self) -> float:
        '''Gets the gradient angle.'''
        ...
    
    @angle.setter
    def angle(self, value : float):
        '''Sets the gradient angle.'''
        ...
    
    @property
    def is_angle_scalable(self) -> bool:
        ...
    
    @is_angle_scalable.setter
    def is_angle_scalable(self, value : bool):
        ...
    
    @property
    def gamma_correction(self) -> bool:
        ...
    
    @gamma_correction.setter
    def gamma_correction(self, value : bool):
        ...
    
    @property
    def interpolation_colors(self) -> aspose.psd.ColorBlend:
        ...
    
    @interpolation_colors.setter
    def interpolation_colors(self, value : aspose.psd.ColorBlend):
        ...
    
    @property
    def linear_colors(self) -> List[aspose.psd.Color]:
        ...
    
    @linear_colors.setter
    def linear_colors(self, value : List[aspose.psd.Color]):
        ...
    
    @property
    def start_color(self) -> aspose.psd.Color:
        ...
    
    @start_color.setter
    def start_color(self, value : aspose.psd.Color):
        ...
    
    @property
    def end_color(self) -> aspose.psd.Color:
        ...
    
    @end_color.setter
    def end_color(self, value : aspose.psd.Color):
        ...
    
    @property
    def blend(self) -> aspose.psd.Blend:
        '''Gets a :py:class:`aspose.psd.Blend` that specifies positions and factors that define a custom falloff for the gradient.'''
        ...
    
    @blend.setter
    def blend(self, value : aspose.psd.Blend):
        '''Sets a :py:class:`aspose.psd.Blend` that specifies positions and factors that define a custom falloff for the gradient.'''
        ...
    
    ...

class LinearGradientBrushBase(TransformBrush):
    '''Represents a :py:class:`aspose.psd.Brush` with gradient capabilities and appropriate properties.'''
    
    @overload
    def multiply_transform(self, matrix : aspose.psd.Matrix):
        '''Multiplies the :py:class:`aspose.psd.Matrix` that represents the local geometric transform of this :py:class:`aspose.psd.brushes.LinearGradientBrush` by the specified :py:class:`aspose.psd.Matrix` by prepending the specified :py:class:`aspose.psd.Matrix`.
        
        :param matrix: The :py:class:`aspose.psd.Matrix` by which to multiply the geometric transform.'''
        ...
    
    @overload
    def multiply_transform(self, matrix : aspose.psd.Matrix, order : aspose.psd.MatrixOrder):
        '''Multiplies the :py:class:`aspose.psd.Matrix` that represents the local geometric transform of this :py:class:`aspose.psd.brushes.LinearGradientBrush` by the specified :py:class:`aspose.psd.Matrix` in the specified order.
        
        :param matrix: The :py:class:`aspose.psd.Matrix` by which to multiply the geometric transform.
        :param order: A :py:class:`aspose.psd.MatrixOrder` that specifies in which order to multiply the two matrices.'''
        ...
    
    @overload
    def translate_transform(self, dx : float, dy : float):
        '''Translates the local geometric transform by the specified dimensions. This method prepends the translation to the transform.
        
        :param dx: The value of the translation in x.
        :param dy: The value of the translation in y.'''
        ...
    
    @overload
    def translate_transform(self, dx : float, dy : float, order : aspose.psd.MatrixOrder):
        '''Translates the local geometric transform by the specified dimensions in the specified order.
        
        :param dx: The value of the translation in x.
        :param dy: The value of the translation in y.
        :param order: The order (prepend or append) in which to apply the translation.'''
        ...
    
    @overload
    def scale_transform(self, sx : float, sy : float):
        '''Scales the local geometric transform by the specified amounts. This method prepends the scaling matrix to the transform.
        
        :param sx: The amount by which to scale the transform in the x-axis direction.
        :param sy: The amount by which to scale the transform in the y-axis direction.'''
        ...
    
    @overload
    def scale_transform(self, sx : float, sy : float, order : aspose.psd.MatrixOrder):
        '''Scales the local geometric transform by the specified amounts in the specified order.
        
        :param sx: The amount by which to scale the transform in the x-axis direction.
        :param sy: The amount by which to scale the transform in the y-axis direction.
        :param order: A :py:class:`aspose.psd.MatrixOrder` that specifies whether to append or prepend the scaling matrix.'''
        ...
    
    @overload
    def rotate_transform(self, angle : float):
        '''Rotates the local geometric transform by the specified amount. This method prepends the rotation to the transform.
        
        :param angle: The angle of rotation.'''
        ...
    
    @overload
    def rotate_transform(self, angle : float, order : aspose.psd.MatrixOrder):
        '''Rotates the local geometric transform by the specified amount in the specified order.
        
        :param angle: The angle of rotation.
        :param order: A :py:class:`aspose.psd.MatrixOrder` that specifies whether to append or prepend the rotation matrix.'''
        ...
    
    def deep_clone(self) -> aspose.psd.Brush:
        '''Creates a new deep clone of the current :py:class:`aspose.psd.Brush`.
        
        :returns: A new :py:class:`aspose.psd.Brush` which is the deep clone of this :py:class:`aspose.psd.Brush` instance.'''
        ...
    
    def reset_transform(self):
        '''Resets the :py:attr:`aspose.psd.brushes.TransformBrush.transform` property to identity.'''
        ...
    
    @property
    def disposed(self) -> bool:
        '''Gets a value indicating whether this instance is disposed.'''
        ...
    
    @property
    def opacity(self) -> float:
        '''Gets the brush opacity. The value should be between 0 and 1. Value of 0 means that brush is fully visible, value of 1 means the brush is fully opaque.'''
        ...
    
    @opacity.setter
    def opacity(self, value : float):
        '''Sets the brush opacity. The value should be between 0 and 1. Value of 0 means that brush is fully visible, value of 1 means the brush is fully opaque.'''
        ...
    
    @property
    def wrap_mode(self) -> aspose.psd.WrapMode:
        ...
    
    @wrap_mode.setter
    def wrap_mode(self, value : aspose.psd.WrapMode):
        ...
    
    @property
    def transform(self) -> aspose.psd.Matrix:
        '''Gets a copy :py:class:`aspose.psd.Matrix` that defines a local geometric transform for this :py:class:`aspose.psd.brushes.TransformBrush`.'''
        ...
    
    @transform.setter
    def transform(self, value : aspose.psd.Matrix):
        '''Sets a copy :py:class:`aspose.psd.Matrix` that defines a local geometric transform for this :py:class:`aspose.psd.brushes.TransformBrush`.'''
        ...
    
    @property
    def is_transform_changed(self) -> bool:
        ...
    
    @property
    def rectangle(self) -> aspose.psd.RectangleF:
        '''Gets a rectangular region that defines the starting and ending points of the gradient.'''
        ...
    
    @rectangle.setter
    def rectangle(self, value : aspose.psd.RectangleF):
        '''Sets a rectangular region that defines the starting and ending points of the gradient.'''
        ...
    
    @property
    def angle(self) -> float:
        '''Gets the gradient angle.'''
        ...
    
    @angle.setter
    def angle(self, value : float):
        '''Sets the gradient angle.'''
        ...
    
    @property
    def is_angle_scalable(self) -> bool:
        ...
    
    @is_angle_scalable.setter
    def is_angle_scalable(self, value : bool):
        ...
    
    @property
    def gamma_correction(self) -> bool:
        ...
    
    @gamma_correction.setter
    def gamma_correction(self, value : bool):
        ...
    
    ...

class LinearMulticolorGradientBrush(LinearGradientBrushBase):
    '''Represents a :py:class:`aspose.psd.Brush` with linear gradient defined by multiple colors and appropriate positions. This class cannot be inherited.'''
    
    @overload
    def multiply_transform(self, matrix : aspose.psd.Matrix):
        '''Multiplies the :py:class:`aspose.psd.Matrix` that represents the local geometric transform of this :py:class:`aspose.psd.brushes.LinearGradientBrush` by the specified :py:class:`aspose.psd.Matrix` by prepending the specified :py:class:`aspose.psd.Matrix`.
        
        :param matrix: The :py:class:`aspose.psd.Matrix` by which to multiply the geometric transform.'''
        ...
    
    @overload
    def multiply_transform(self, matrix : aspose.psd.Matrix, order : aspose.psd.MatrixOrder):
        '''Multiplies the :py:class:`aspose.psd.Matrix` that represents the local geometric transform of this :py:class:`aspose.psd.brushes.LinearGradientBrush` by the specified :py:class:`aspose.psd.Matrix` in the specified order.
        
        :param matrix: The :py:class:`aspose.psd.Matrix` by which to multiply the geometric transform.
        :param order: A :py:class:`aspose.psd.MatrixOrder` that specifies in which order to multiply the two matrices.'''
        ...
    
    @overload
    def translate_transform(self, dx : float, dy : float):
        '''Translates the local geometric transform by the specified dimensions. This method prepends the translation to the transform.
        
        :param dx: The value of the translation in x.
        :param dy: The value of the translation in y.'''
        ...
    
    @overload
    def translate_transform(self, dx : float, dy : float, order : aspose.psd.MatrixOrder):
        '''Translates the local geometric transform by the specified dimensions in the specified order.
        
        :param dx: The value of the translation in x.
        :param dy: The value of the translation in y.
        :param order: The order (prepend or append) in which to apply the translation.'''
        ...
    
    @overload
    def scale_transform(self, sx : float, sy : float):
        '''Scales the local geometric transform by the specified amounts. This method prepends the scaling matrix to the transform.
        
        :param sx: The amount by which to scale the transform in the x-axis direction.
        :param sy: The amount by which to scale the transform in the y-axis direction.'''
        ...
    
    @overload
    def scale_transform(self, sx : float, sy : float, order : aspose.psd.MatrixOrder):
        '''Scales the local geometric transform by the specified amounts in the specified order.
        
        :param sx: The amount by which to scale the transform in the x-axis direction.
        :param sy: The amount by which to scale the transform in the y-axis direction.
        :param order: A :py:class:`aspose.psd.MatrixOrder` that specifies whether to append or prepend the scaling matrix.'''
        ...
    
    @overload
    def rotate_transform(self, angle : float):
        '''Rotates the local geometric transform by the specified amount. This method prepends the rotation to the transform.
        
        :param angle: The angle of rotation.'''
        ...
    
    @overload
    def rotate_transform(self, angle : float, order : aspose.psd.MatrixOrder):
        '''Rotates the local geometric transform by the specified amount in the specified order.
        
        :param angle: The angle of rotation.
        :param order: A :py:class:`aspose.psd.MatrixOrder` that specifies whether to append or prepend the rotation matrix.'''
        ...
    
    def deep_clone(self) -> aspose.psd.Brush:
        '''Creates a new deep clone of the current :py:class:`aspose.psd.Brush`.
        
        :returns: A new :py:class:`aspose.psd.Brush` which is the deep clone of this :py:class:`aspose.psd.Brush` instance.'''
        ...
    
    def reset_transform(self):
        '''Resets the :py:attr:`aspose.psd.brushes.TransformBrush.transform` property to identity.'''
        ...
    
    @property
    def disposed(self) -> bool:
        '''Gets a value indicating whether this instance is disposed.'''
        ...
    
    @property
    def opacity(self) -> float:
        '''Gets the brush opacity. The value should be between 0 and 1. Value of 0 means that brush is fully visible, value of 1 means the brush is fully opaque.'''
        ...
    
    @opacity.setter
    def opacity(self, value : float):
        '''Sets the brush opacity. The value should be between 0 and 1. Value of 0 means that brush is fully visible, value of 1 means the brush is fully opaque.'''
        ...
    
    @property
    def wrap_mode(self) -> aspose.psd.WrapMode:
        ...
    
    @wrap_mode.setter
    def wrap_mode(self, value : aspose.psd.WrapMode):
        ...
    
    @property
    def transform(self) -> aspose.psd.Matrix:
        '''Gets a copy :py:class:`aspose.psd.Matrix` that defines a local geometric transform for this :py:class:`aspose.psd.brushes.TransformBrush`.'''
        ...
    
    @transform.setter
    def transform(self, value : aspose.psd.Matrix):
        '''Sets a copy :py:class:`aspose.psd.Matrix` that defines a local geometric transform for this :py:class:`aspose.psd.brushes.TransformBrush`.'''
        ...
    
    @property
    def is_transform_changed(self) -> bool:
        ...
    
    @property
    def rectangle(self) -> aspose.psd.RectangleF:
        '''Gets a rectangular region that defines the starting and ending points of the gradient.'''
        ...
    
    @rectangle.setter
    def rectangle(self, value : aspose.psd.RectangleF):
        '''Sets a rectangular region that defines the starting and ending points of the gradient.'''
        ...
    
    @property
    def angle(self) -> float:
        '''Gets the gradient angle.'''
        ...
    
    @angle.setter
    def angle(self, value : float):
        '''Sets the gradient angle.'''
        ...
    
    @property
    def is_angle_scalable(self) -> bool:
        ...
    
    @is_angle_scalable.setter
    def is_angle_scalable(self, value : bool):
        ...
    
    @property
    def gamma_correction(self) -> bool:
        ...
    
    @gamma_correction.setter
    def gamma_correction(self, value : bool):
        ...
    
    @property
    def interpolation_colors(self) -> aspose.psd.ColorBlend:
        ...
    
    @interpolation_colors.setter
    def interpolation_colors(self, value : aspose.psd.ColorBlend):
        ...
    
    ...

class PathGradientBrush(PathGradientBrushBase):
    '''Encapsulates a :py:class:`aspose.psd.Brush` object with a gradient. This class cannot be inherited.'''
    
    @overload
    def multiply_transform(self, matrix : aspose.psd.Matrix):
        '''Multiplies the :py:class:`aspose.psd.Matrix` that represents the local geometric transform of this :py:class:`aspose.psd.brushes.LinearGradientBrush` by the specified :py:class:`aspose.psd.Matrix` by prepending the specified :py:class:`aspose.psd.Matrix`.
        
        :param matrix: The :py:class:`aspose.psd.Matrix` by which to multiply the geometric transform.'''
        ...
    
    @overload
    def multiply_transform(self, matrix : aspose.psd.Matrix, order : aspose.psd.MatrixOrder):
        '''Multiplies the :py:class:`aspose.psd.Matrix` that represents the local geometric transform of this :py:class:`aspose.psd.brushes.LinearGradientBrush` by the specified :py:class:`aspose.psd.Matrix` in the specified order.
        
        :param matrix: The :py:class:`aspose.psd.Matrix` by which to multiply the geometric transform.
        :param order: A :py:class:`aspose.psd.MatrixOrder` that specifies in which order to multiply the two matrices.'''
        ...
    
    @overload
    def translate_transform(self, dx : float, dy : float):
        '''Translates the local geometric transform by the specified dimensions. This method prepends the translation to the transform.
        
        :param dx: The value of the translation in x.
        :param dy: The value of the translation in y.'''
        ...
    
    @overload
    def translate_transform(self, dx : float, dy : float, order : aspose.psd.MatrixOrder):
        '''Translates the local geometric transform by the specified dimensions in the specified order.
        
        :param dx: The value of the translation in x.
        :param dy: The value of the translation in y.
        :param order: The order (prepend or append) in which to apply the translation.'''
        ...
    
    @overload
    def scale_transform(self, sx : float, sy : float):
        '''Scales the local geometric transform by the specified amounts. This method prepends the scaling matrix to the transform.
        
        :param sx: The amount by which to scale the transform in the x-axis direction.
        :param sy: The amount by which to scale the transform in the y-axis direction.'''
        ...
    
    @overload
    def scale_transform(self, sx : float, sy : float, order : aspose.psd.MatrixOrder):
        '''Scales the local geometric transform by the specified amounts in the specified order.
        
        :param sx: The amount by which to scale the transform in the x-axis direction.
        :param sy: The amount by which to scale the transform in the y-axis direction.
        :param order: A :py:class:`aspose.psd.MatrixOrder` that specifies whether to append or prepend the scaling matrix.'''
        ...
    
    @overload
    def rotate_transform(self, angle : float):
        '''Rotates the local geometric transform by the specified amount. This method prepends the rotation to the transform.
        
        :param angle: The angle of rotation.'''
        ...
    
    @overload
    def rotate_transform(self, angle : float, order : aspose.psd.MatrixOrder):
        '''Rotates the local geometric transform by the specified amount in the specified order.
        
        :param angle: The angle of rotation.
        :param order: A :py:class:`aspose.psd.MatrixOrder` that specifies whether to append or prepend the rotation matrix.'''
        ...
    
    @overload
    def set_sigma_bell_shape(self, focus : float):
        '''Creates a gradient brush that changes color starting from the center of the path outward to the path's boundary. The transition from one color to another is based on a bell-shaped curve.
        
        :param focus: A value from 0 through 1 that specifies where, along any radial from the center of the path to the path's boundary, the center color will be at its highest intensity. A value of 1 (the default) places the highest intensity at the center of the path.'''
        ...
    
    @overload
    def set_sigma_bell_shape(self, focus : float, scale : float):
        '''Creates a gradient brush that changes color starting from the center of the path outward to the path's boundary. The transition from one color to another is based on a bell-shaped curve.
        
        :param focus: A value from 0 through 1 that specifies where, along any radial from the center of the path to the path's boundary, the center color will be at its highest intensity. A value of 1 (the default) places the highest intensity at the center of the path.
        :param scale: A value from 0 through 1 that specifies the maximum intensity of the center color that gets blended with the boundary color. A value of 1 causes the highest possible intensity of the center color, and it is the default value.'''
        ...
    
    @overload
    def set_blend_triangular_shape(self, focus : float):
        '''Creates a gradient with a center color and a linear falloff to one surrounding color.
        
        :param focus: A value from 0 through 1 that specifies where, along any radial from the center of the path to the path's boundary, the center color will be at its highest intensity. A value of 1 (the default) places the highest intensity at the center of the path.'''
        ...
    
    @overload
    def set_blend_triangular_shape(self, focus : float, scale : float):
        '''Creates a gradient with a center color and a linear falloff to each surrounding color.
        
        :param focus: A value from 0 through 1 that specifies where, along any radial from the center of the path to the path's boundary, the center color will be at its highest intensity. A value of 1 (the default) places the highest intensity at the center of the path.
        :param scale: A value from 0 through 1 that specifies the maximum intensity of the center color that gets blended with the boundary color. A value of 1 causes the highest possible intensity of the center color, and it is the default value.'''
        ...
    
    def deep_clone(self) -> aspose.psd.Brush:
        '''Creates a new deep clone of the current :py:class:`aspose.psd.Brush`.
        
        :returns: A new :py:class:`aspose.psd.Brush` which is the deep clone of this :py:class:`aspose.psd.Brush` instance.'''
        ...
    
    def reset_transform(self):
        '''Resets the :py:attr:`aspose.psd.brushes.TransformBrush.transform` property to identity.'''
        ...
    
    @property
    def disposed(self) -> bool:
        '''Gets a value indicating whether this instance is disposed.'''
        ...
    
    @property
    def opacity(self) -> float:
        '''Gets the brush opacity. The value should be between 0 and 1. Value of 0 means that brush is fully visible, value of 1 means the brush is fully opaque.'''
        ...
    
    @opacity.setter
    def opacity(self, value : float):
        '''Sets the brush opacity. The value should be between 0 and 1. Value of 0 means that brush is fully visible, value of 1 means the brush is fully opaque.'''
        ...
    
    @property
    def wrap_mode(self) -> aspose.psd.WrapMode:
        ...
    
    @wrap_mode.setter
    def wrap_mode(self, value : aspose.psd.WrapMode):
        ...
    
    @property
    def transform(self) -> aspose.psd.Matrix:
        '''Gets a copy :py:class:`aspose.psd.Matrix` that defines a local geometric transform for this :py:class:`aspose.psd.brushes.TransformBrush`.'''
        ...
    
    @transform.setter
    def transform(self, value : aspose.psd.Matrix):
        '''Sets a copy :py:class:`aspose.psd.Matrix` that defines a local geometric transform for this :py:class:`aspose.psd.brushes.TransformBrush`.'''
        ...
    
    @property
    def is_transform_changed(self) -> bool:
        ...
    
    @property
    def path_points(self) -> List[aspose.psd.PointF]:
        ...
    
    @property
    def graphics_path(self) -> aspose.psd.GraphicsPath:
        ...
    
    @property
    def center_point(self) -> aspose.psd.PointF:
        ...
    
    @center_point.setter
    def center_point(self, value : aspose.psd.PointF):
        ...
    
    @property
    def focus_scales(self) -> aspose.psd.PointF:
        ...
    
    @focus_scales.setter
    def focus_scales(self, value : aspose.psd.PointF):
        ...
    
    @property
    def interpolation_colors(self) -> aspose.psd.ColorBlend:
        ...
    
    @interpolation_colors.setter
    def interpolation_colors(self, value : aspose.psd.ColorBlend):
        ...
    
    @property
    def center_color(self) -> aspose.psd.Color:
        ...
    
    @center_color.setter
    def center_color(self, value : aspose.psd.Color):
        ...
    
    @property
    def surround_colors(self) -> List[aspose.psd.Color]:
        ...
    
    @surround_colors.setter
    def surround_colors(self, value : List[aspose.psd.Color]):
        ...
    
    @property
    def blend(self) -> aspose.psd.Blend:
        '''Gets a :py:class:`aspose.psd.Blend` that specifies positions and factors that define a custom falloff for the gradient.'''
        ...
    
    @blend.setter
    def blend(self, value : aspose.psd.Blend):
        '''Sets a :py:class:`aspose.psd.Blend` that specifies positions and factors that define a custom falloff for the gradient.'''
        ...
    
    ...

class PathGradientBrushBase(TransformBrush):
    '''Represents a :py:class:`aspose.psd.Brush` with base path gradient functionality.'''
    
    @overload
    def multiply_transform(self, matrix : aspose.psd.Matrix):
        '''Multiplies the :py:class:`aspose.psd.Matrix` that represents the local geometric transform of this :py:class:`aspose.psd.brushes.LinearGradientBrush` by the specified :py:class:`aspose.psd.Matrix` by prepending the specified :py:class:`aspose.psd.Matrix`.
        
        :param matrix: The :py:class:`aspose.psd.Matrix` by which to multiply the geometric transform.'''
        ...
    
    @overload
    def multiply_transform(self, matrix : aspose.psd.Matrix, order : aspose.psd.MatrixOrder):
        '''Multiplies the :py:class:`aspose.psd.Matrix` that represents the local geometric transform of this :py:class:`aspose.psd.brushes.LinearGradientBrush` by the specified :py:class:`aspose.psd.Matrix` in the specified order.
        
        :param matrix: The :py:class:`aspose.psd.Matrix` by which to multiply the geometric transform.
        :param order: A :py:class:`aspose.psd.MatrixOrder` that specifies in which order to multiply the two matrices.'''
        ...
    
    @overload
    def translate_transform(self, dx : float, dy : float):
        '''Translates the local geometric transform by the specified dimensions. This method prepends the translation to the transform.
        
        :param dx: The value of the translation in x.
        :param dy: The value of the translation in y.'''
        ...
    
    @overload
    def translate_transform(self, dx : float, dy : float, order : aspose.psd.MatrixOrder):
        '''Translates the local geometric transform by the specified dimensions in the specified order.
        
        :param dx: The value of the translation in x.
        :param dy: The value of the translation in y.
        :param order: The order (prepend or append) in which to apply the translation.'''
        ...
    
    @overload
    def scale_transform(self, sx : float, sy : float):
        '''Scales the local geometric transform by the specified amounts. This method prepends the scaling matrix to the transform.
        
        :param sx: The amount by which to scale the transform in the x-axis direction.
        :param sy: The amount by which to scale the transform in the y-axis direction.'''
        ...
    
    @overload
    def scale_transform(self, sx : float, sy : float, order : aspose.psd.MatrixOrder):
        '''Scales the local geometric transform by the specified amounts in the specified order.
        
        :param sx: The amount by which to scale the transform in the x-axis direction.
        :param sy: The amount by which to scale the transform in the y-axis direction.
        :param order: A :py:class:`aspose.psd.MatrixOrder` that specifies whether to append or prepend the scaling matrix.'''
        ...
    
    @overload
    def rotate_transform(self, angle : float):
        '''Rotates the local geometric transform by the specified amount. This method prepends the rotation to the transform.
        
        :param angle: The angle of rotation.'''
        ...
    
    @overload
    def rotate_transform(self, angle : float, order : aspose.psd.MatrixOrder):
        '''Rotates the local geometric transform by the specified amount in the specified order.
        
        :param angle: The angle of rotation.
        :param order: A :py:class:`aspose.psd.MatrixOrder` that specifies whether to append or prepend the rotation matrix.'''
        ...
    
    def deep_clone(self) -> aspose.psd.Brush:
        '''Creates a new deep clone of the current :py:class:`aspose.psd.Brush`.
        
        :returns: A new :py:class:`aspose.psd.Brush` which is the deep clone of this :py:class:`aspose.psd.Brush` instance.'''
        ...
    
    def reset_transform(self):
        '''Resets the :py:attr:`aspose.psd.brushes.TransformBrush.transform` property to identity.'''
        ...
    
    @property
    def disposed(self) -> bool:
        '''Gets a value indicating whether this instance is disposed.'''
        ...
    
    @property
    def opacity(self) -> float:
        '''Gets the brush opacity. The value should be between 0 and 1. Value of 0 means that brush is fully visible, value of 1 means the brush is fully opaque.'''
        ...
    
    @opacity.setter
    def opacity(self, value : float):
        '''Sets the brush opacity. The value should be between 0 and 1. Value of 0 means that brush is fully visible, value of 1 means the brush is fully opaque.'''
        ...
    
    @property
    def wrap_mode(self) -> aspose.psd.WrapMode:
        ...
    
    @wrap_mode.setter
    def wrap_mode(self, value : aspose.psd.WrapMode):
        ...
    
    @property
    def transform(self) -> aspose.psd.Matrix:
        '''Gets a copy :py:class:`aspose.psd.Matrix` that defines a local geometric transform for this :py:class:`aspose.psd.brushes.TransformBrush`.'''
        ...
    
    @transform.setter
    def transform(self, value : aspose.psd.Matrix):
        '''Sets a copy :py:class:`aspose.psd.Matrix` that defines a local geometric transform for this :py:class:`aspose.psd.brushes.TransformBrush`.'''
        ...
    
    @property
    def is_transform_changed(self) -> bool:
        ...
    
    @property
    def path_points(self) -> List[aspose.psd.PointF]:
        ...
    
    @property
    def graphics_path(self) -> aspose.psd.GraphicsPath:
        ...
    
    @property
    def center_point(self) -> aspose.psd.PointF:
        ...
    
    @center_point.setter
    def center_point(self, value : aspose.psd.PointF):
        ...
    
    @property
    def focus_scales(self) -> aspose.psd.PointF:
        ...
    
    @focus_scales.setter
    def focus_scales(self, value : aspose.psd.PointF):
        ...
    
    ...

class PathMulticolorGradientBrush(PathGradientBrushBase):
    '''Encapsulates a :py:class:`aspose.psd.Brush` object with a gradient. This class cannot be inherited.'''
    
    @overload
    def multiply_transform(self, matrix : aspose.psd.Matrix):
        '''Multiplies the :py:class:`aspose.psd.Matrix` that represents the local geometric transform of this :py:class:`aspose.psd.brushes.LinearGradientBrush` by the specified :py:class:`aspose.psd.Matrix` by prepending the specified :py:class:`aspose.psd.Matrix`.
        
        :param matrix: The :py:class:`aspose.psd.Matrix` by which to multiply the geometric transform.'''
        ...
    
    @overload
    def multiply_transform(self, matrix : aspose.psd.Matrix, order : aspose.psd.MatrixOrder):
        '''Multiplies the :py:class:`aspose.psd.Matrix` that represents the local geometric transform of this :py:class:`aspose.psd.brushes.LinearGradientBrush` by the specified :py:class:`aspose.psd.Matrix` in the specified order.
        
        :param matrix: The :py:class:`aspose.psd.Matrix` by which to multiply the geometric transform.
        :param order: A :py:class:`aspose.psd.MatrixOrder` that specifies in which order to multiply the two matrices.'''
        ...
    
    @overload
    def translate_transform(self, dx : float, dy : float):
        '''Translates the local geometric transform by the specified dimensions. This method prepends the translation to the transform.
        
        :param dx: The value of the translation in x.
        :param dy: The value of the translation in y.'''
        ...
    
    @overload
    def translate_transform(self, dx : float, dy : float, order : aspose.psd.MatrixOrder):
        '''Translates the local geometric transform by the specified dimensions in the specified order.
        
        :param dx: The value of the translation in x.
        :param dy: The value of the translation in y.
        :param order: The order (prepend or append) in which to apply the translation.'''
        ...
    
    @overload
    def scale_transform(self, sx : float, sy : float):
        '''Scales the local geometric transform by the specified amounts. This method prepends the scaling matrix to the transform.
        
        :param sx: The amount by which to scale the transform in the x-axis direction.
        :param sy: The amount by which to scale the transform in the y-axis direction.'''
        ...
    
    @overload
    def scale_transform(self, sx : float, sy : float, order : aspose.psd.MatrixOrder):
        '''Scales the local geometric transform by the specified amounts in the specified order.
        
        :param sx: The amount by which to scale the transform in the x-axis direction.
        :param sy: The amount by which to scale the transform in the y-axis direction.
        :param order: A :py:class:`aspose.psd.MatrixOrder` that specifies whether to append or prepend the scaling matrix.'''
        ...
    
    @overload
    def rotate_transform(self, angle : float):
        '''Rotates the local geometric transform by the specified amount. This method prepends the rotation to the transform.
        
        :param angle: The angle of rotation.'''
        ...
    
    @overload
    def rotate_transform(self, angle : float, order : aspose.psd.MatrixOrder):
        '''Rotates the local geometric transform by the specified amount in the specified order.
        
        :param angle: The angle of rotation.
        :param order: A :py:class:`aspose.psd.MatrixOrder` that specifies whether to append or prepend the rotation matrix.'''
        ...
    
    def deep_clone(self) -> aspose.psd.Brush:
        '''Creates a new deep clone of the current :py:class:`aspose.psd.Brush`.
        
        :returns: A new :py:class:`aspose.psd.Brush` which is the deep clone of this :py:class:`aspose.psd.Brush` instance.'''
        ...
    
    def reset_transform(self):
        '''Resets the :py:attr:`aspose.psd.brushes.TransformBrush.transform` property to identity.'''
        ...
    
    @property
    def disposed(self) -> bool:
        '''Gets a value indicating whether this instance is disposed.'''
        ...
    
    @property
    def opacity(self) -> float:
        '''Gets the brush opacity. The value should be between 0 and 1. Value of 0 means that brush is fully visible, value of 1 means the brush is fully opaque.'''
        ...
    
    @opacity.setter
    def opacity(self, value : float):
        '''Sets the brush opacity. The value should be between 0 and 1. Value of 0 means that brush is fully visible, value of 1 means the brush is fully opaque.'''
        ...
    
    @property
    def wrap_mode(self) -> aspose.psd.WrapMode:
        ...
    
    @wrap_mode.setter
    def wrap_mode(self, value : aspose.psd.WrapMode):
        ...
    
    @property
    def transform(self) -> aspose.psd.Matrix:
        '''Gets a copy :py:class:`aspose.psd.Matrix` that defines a local geometric transform for this :py:class:`aspose.psd.brushes.TransformBrush`.'''
        ...
    
    @transform.setter
    def transform(self, value : aspose.psd.Matrix):
        '''Sets a copy :py:class:`aspose.psd.Matrix` that defines a local geometric transform for this :py:class:`aspose.psd.brushes.TransformBrush`.'''
        ...
    
    @property
    def is_transform_changed(self) -> bool:
        ...
    
    @property
    def path_points(self) -> List[aspose.psd.PointF]:
        ...
    
    @property
    def graphics_path(self) -> aspose.psd.GraphicsPath:
        ...
    
    @property
    def center_point(self) -> aspose.psd.PointF:
        ...
    
    @center_point.setter
    def center_point(self, value : aspose.psd.PointF):
        ...
    
    @property
    def focus_scales(self) -> aspose.psd.PointF:
        ...
    
    @focus_scales.setter
    def focus_scales(self, value : aspose.psd.PointF):
        ...
    
    @property
    def interpolation_colors(self) -> aspose.psd.ColorBlend:
        ...
    
    @interpolation_colors.setter
    def interpolation_colors(self, value : aspose.psd.ColorBlend):
        ...
    
    ...

class SolidBrush(aspose.psd.Brush):
    '''Solid brush is intended for drawing continiously with specific color. This class cannot be inherited.'''
    
    def deep_clone(self) -> aspose.psd.Brush:
        '''Creates a new deep clone of the current :py:class:`aspose.psd.Brush`.
        
        :returns: A new :py:class:`aspose.psd.Brush` which is the deep clone of this :py:class:`aspose.psd.Brush` instance.'''
        ...
    
    @property
    def disposed(self) -> bool:
        '''Gets a value indicating whether this instance is disposed.'''
        ...
    
    @property
    def opacity(self) -> float:
        '''Gets the brush opacity. The value should be between 0 and 1. Value of 0 means that brush is fully visible, value of 1 means the brush is fully opaque.'''
        ...
    
    @opacity.setter
    def opacity(self, value : float):
        '''Sets the brush opacity. The value should be between 0 and 1. Value of 0 means that brush is fully visible, value of 1 means the brush is fully opaque.'''
        ...
    
    @property
    def color(self) -> aspose.psd.Color:
        '''Gets the brush color.'''
        ...
    
    @color.setter
    def color(self, value : aspose.psd.Color):
        '''Sets the brush color.'''
        ...
    
    ...

class TextureBrush(TransformBrush):
    '''Each property of the :py:class:`aspose.psd.brushes.TextureBrush` class is a :py:class:`aspose.psd.Brush` object that uses an image to fill the interior of a shape. This class cannot be inherited.'''
    
    @overload
    def multiply_transform(self, matrix : aspose.psd.Matrix):
        '''Multiplies the :py:class:`aspose.psd.Matrix` that represents the local geometric transform of this :py:class:`aspose.psd.brushes.LinearGradientBrush` by the specified :py:class:`aspose.psd.Matrix` by prepending the specified :py:class:`aspose.psd.Matrix`.
        
        :param matrix: The :py:class:`aspose.psd.Matrix` by which to multiply the geometric transform.'''
        ...
    
    @overload
    def multiply_transform(self, matrix : aspose.psd.Matrix, order : aspose.psd.MatrixOrder):
        '''Multiplies the :py:class:`aspose.psd.Matrix` that represents the local geometric transform of this :py:class:`aspose.psd.brushes.LinearGradientBrush` by the specified :py:class:`aspose.psd.Matrix` in the specified order.
        
        :param matrix: The :py:class:`aspose.psd.Matrix` by which to multiply the geometric transform.
        :param order: A :py:class:`aspose.psd.MatrixOrder` that specifies in which order to multiply the two matrices.'''
        ...
    
    @overload
    def translate_transform(self, dx : float, dy : float):
        '''Translates the local geometric transform by the specified dimensions. This method prepends the translation to the transform.
        
        :param dx: The value of the translation in x.
        :param dy: The value of the translation in y.'''
        ...
    
    @overload
    def translate_transform(self, dx : float, dy : float, order : aspose.psd.MatrixOrder):
        '''Translates the local geometric transform by the specified dimensions in the specified order.
        
        :param dx: The value of the translation in x.
        :param dy: The value of the translation in y.
        :param order: The order (prepend or append) in which to apply the translation.'''
        ...
    
    @overload
    def scale_transform(self, sx : float, sy : float):
        '''Scales the local geometric transform by the specified amounts. This method prepends the scaling matrix to the transform.
        
        :param sx: The amount by which to scale the transform in the x-axis direction.
        :param sy: The amount by which to scale the transform in the y-axis direction.'''
        ...
    
    @overload
    def scale_transform(self, sx : float, sy : float, order : aspose.psd.MatrixOrder):
        '''Scales the local geometric transform by the specified amounts in the specified order.
        
        :param sx: The amount by which to scale the transform in the x-axis direction.
        :param sy: The amount by which to scale the transform in the y-axis direction.
        :param order: A :py:class:`aspose.psd.MatrixOrder` that specifies whether to append or prepend the scaling matrix.'''
        ...
    
    @overload
    def rotate_transform(self, angle : float):
        '''Rotates the local geometric transform by the specified amount. This method prepends the rotation to the transform.
        
        :param angle: The angle of rotation.'''
        ...
    
    @overload
    def rotate_transform(self, angle : float, order : aspose.psd.MatrixOrder):
        '''Rotates the local geometric transform by the specified amount in the specified order.
        
        :param angle: The angle of rotation.
        :param order: A :py:class:`aspose.psd.MatrixOrder` that specifies whether to append or prepend the rotation matrix.'''
        ...
    
    def deep_clone(self) -> aspose.psd.Brush:
        '''Creates a new deep clone of the current :py:class:`aspose.psd.Brush`.
        
        :returns: A new :py:class:`aspose.psd.Brush` which is the deep clone of this :py:class:`aspose.psd.Brush` instance.'''
        ...
    
    def reset_transform(self):
        '''Resets the :py:attr:`aspose.psd.brushes.TransformBrush.transform` property to identity.'''
        ...
    
    @property
    def disposed(self) -> bool:
        '''Gets a value indicating whether this instance is disposed.'''
        ...
    
    @property
    def opacity(self) -> float:
        '''Gets the brush opacity. The value should be between 0 and 1. Value of 0 means that brush is fully visible, value of 1 means the brush is fully opaque.'''
        ...
    
    @opacity.setter
    def opacity(self, value : float):
        '''Sets the brush opacity. The value should be between 0 and 1. Value of 0 means that brush is fully visible, value of 1 means the brush is fully opaque.'''
        ...
    
    @property
    def wrap_mode(self) -> aspose.psd.WrapMode:
        ...
    
    @wrap_mode.setter
    def wrap_mode(self, value : aspose.psd.WrapMode):
        ...
    
    @property
    def transform(self) -> aspose.psd.Matrix:
        '''Gets a copy :py:class:`aspose.psd.Matrix` that defines a local geometric transform for this :py:class:`aspose.psd.brushes.TransformBrush`.'''
        ...
    
    @transform.setter
    def transform(self, value : aspose.psd.Matrix):
        '''Sets a copy :py:class:`aspose.psd.Matrix` that defines a local geometric transform for this :py:class:`aspose.psd.brushes.TransformBrush`.'''
        ...
    
    @property
    def is_transform_changed(self) -> bool:
        ...
    
    @property
    def image(self) -> aspose.psd.Image:
        '''Gets the :py:class:`aspose.psd.Image` object associated with this :py:class:`aspose.psd.brushes.TextureBrush` object.'''
        ...
    
    @property
    def image_attributes(self) -> aspose.psd.ImageAttributes:
        ...
    
    @property
    def image_rectangle(self) -> aspose.psd.RectangleF:
        ...
    
    ...

class TransformBrush(aspose.psd.Brush):
    '''A :py:class:`aspose.psd.Brush` with transform capabilities.'''
    
    @overload
    def multiply_transform(self, matrix : aspose.psd.Matrix):
        '''Multiplies the :py:class:`aspose.psd.Matrix` that represents the local geometric transform of this :py:class:`aspose.psd.brushes.LinearGradientBrush` by the specified :py:class:`aspose.psd.Matrix` by prepending the specified :py:class:`aspose.psd.Matrix`.
        
        :param matrix: The :py:class:`aspose.psd.Matrix` by which to multiply the geometric transform.'''
        ...
    
    @overload
    def multiply_transform(self, matrix : aspose.psd.Matrix, order : aspose.psd.MatrixOrder):
        '''Multiplies the :py:class:`aspose.psd.Matrix` that represents the local geometric transform of this :py:class:`aspose.psd.brushes.LinearGradientBrush` by the specified :py:class:`aspose.psd.Matrix` in the specified order.
        
        :param matrix: The :py:class:`aspose.psd.Matrix` by which to multiply the geometric transform.
        :param order: A :py:class:`aspose.psd.MatrixOrder` that specifies in which order to multiply the two matrices.'''
        ...
    
    @overload
    def translate_transform(self, dx : float, dy : float):
        '''Translates the local geometric transform by the specified dimensions. This method prepends the translation to the transform.
        
        :param dx: The value of the translation in x.
        :param dy: The value of the translation in y.'''
        ...
    
    @overload
    def translate_transform(self, dx : float, dy : float, order : aspose.psd.MatrixOrder):
        '''Translates the local geometric transform by the specified dimensions in the specified order.
        
        :param dx: The value of the translation in x.
        :param dy: The value of the translation in y.
        :param order: The order (prepend or append) in which to apply the translation.'''
        ...
    
    @overload
    def scale_transform(self, sx : float, sy : float):
        '''Scales the local geometric transform by the specified amounts. This method prepends the scaling matrix to the transform.
        
        :param sx: The amount by which to scale the transform in the x-axis direction.
        :param sy: The amount by which to scale the transform in the y-axis direction.'''
        ...
    
    @overload
    def scale_transform(self, sx : float, sy : float, order : aspose.psd.MatrixOrder):
        '''Scales the local geometric transform by the specified amounts in the specified order.
        
        :param sx: The amount by which to scale the transform in the x-axis direction.
        :param sy: The amount by which to scale the transform in the y-axis direction.
        :param order: A :py:class:`aspose.psd.MatrixOrder` that specifies whether to append or prepend the scaling matrix.'''
        ...
    
    @overload
    def rotate_transform(self, angle : float):
        '''Rotates the local geometric transform by the specified amount. This method prepends the rotation to the transform.
        
        :param angle: The angle of rotation.'''
        ...
    
    @overload
    def rotate_transform(self, angle : float, order : aspose.psd.MatrixOrder):
        '''Rotates the local geometric transform by the specified amount in the specified order.
        
        :param angle: The angle of rotation.
        :param order: A :py:class:`aspose.psd.MatrixOrder` that specifies whether to append or prepend the rotation matrix.'''
        ...
    
    def deep_clone(self) -> aspose.psd.Brush:
        '''Creates a new deep clone of the current :py:class:`aspose.psd.Brush`.
        
        :returns: A new :py:class:`aspose.psd.Brush` which is the deep clone of this :py:class:`aspose.psd.Brush` instance.'''
        ...
    
    def reset_transform(self):
        '''Resets the :py:attr:`aspose.psd.brushes.TransformBrush.transform` property to identity.'''
        ...
    
    @property
    def disposed(self) -> bool:
        '''Gets a value indicating whether this instance is disposed.'''
        ...
    
    @property
    def opacity(self) -> float:
        '''Gets the brush opacity. The value should be between 0 and 1. Value of 0 means that brush is fully visible, value of 1 means the brush is fully opaque.'''
        ...
    
    @opacity.setter
    def opacity(self, value : float):
        '''Sets the brush opacity. The value should be between 0 and 1. Value of 0 means that brush is fully visible, value of 1 means the brush is fully opaque.'''
        ...
    
    @property
    def wrap_mode(self) -> aspose.psd.WrapMode:
        ...
    
    @wrap_mode.setter
    def wrap_mode(self, value : aspose.psd.WrapMode):
        ...
    
    @property
    def transform(self) -> aspose.psd.Matrix:
        '''Gets a copy :py:class:`aspose.psd.Matrix` that defines a local geometric transform for this :py:class:`aspose.psd.brushes.TransformBrush`.'''
        ...
    
    @transform.setter
    def transform(self, value : aspose.psd.Matrix):
        '''Sets a copy :py:class:`aspose.psd.Matrix` that defines a local geometric transform for this :py:class:`aspose.psd.brushes.TransformBrush`.'''
        ...
    
    @property
    def is_transform_changed(self) -> bool:
        ...
    
    ...

