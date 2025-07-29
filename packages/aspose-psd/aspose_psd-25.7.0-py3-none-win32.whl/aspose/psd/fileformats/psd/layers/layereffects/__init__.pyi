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

class BlendingOptions:
    '''BlendingOptions. It's a wrapper for BaseFxResource which provides api for layer effects'''
    
    def add_color_overlay(self) -> aspose.psd.fileformats.psd.layers.layereffects.ColorOverlayEffect:
        '''Adds the color overlay.
        
        :returns: Created :py:class:`aspose.psd.fileformats.psd.layers.layereffects.ColorOverlayEffect` object'''
        ...
    
    def add_gradient_overlay(self) -> aspose.psd.fileformats.psd.layers.layereffects.GradientOverlayEffect:
        '''Adds the Gradient overlay.
        
        :returns: Created :py:class:`aspose.psd.fileformats.psd.layers.layereffects.GradientOverlayEffect` object'''
        ...
    
    def add_pattern_overlay(self) -> aspose.psd.fileformats.psd.layers.layereffects.PatternOverlayEffect:
        '''Adds the Pattern overlay.
        
        :returns: Created :py:class:`aspose.psd.fileformats.psd.layers.layereffects.PatternOverlayEffect` object'''
        ...
    
    def add_drop_shadow(self) -> aspose.psd.fileformats.psd.layers.layereffects.DropShadowEffect:
        '''Adds the drop shadow effect.
        
        :returns: Created :py:class:`aspose.psd.fileformats.psd.layers.layereffects.DropShadowEffect` object'''
        ...
    
    def add_outer_glow(self) -> aspose.psd.fileformats.psd.layers.layereffects.OuterGlowEffect:
        '''Adds the outer glow effect.
        
        :returns: Created :py:class:`aspose.psd.fileformats.psd.layers.layereffects.OuterGlowEffect` object'''
        ...
    
    def add_inner_shadow(self) -> aspose.psd.fileformats.psd.layers.layereffects.InnerShadowEffect:
        '''Adds the inner shadow effect.
        
        :returns: Created :py:class:`aspose.psd.fileformats.psd.layers.layereffects.InnerShadowEffect` object'''
        ...
    
    def add_stroke(self, fill_type : aspose.psd.fileformats.psd.layers.fillsettings.FillType) -> aspose.psd.fileformats.psd.layers.layereffects.StrokeEffect:
        '''Adds the stroke effect.
        
        :param fill_type: The type of fill to fill the stroke.
        :returns: Created :py:class:`aspose.psd.fileformats.psd.layers.layereffects.StrokeEffect` object.'''
        ...
    
    @property
    def effects(self) -> List[aspose.psd.fileformats.psd.layers.layereffects.ILayerEffect]:
        '''Gets the effects.'''
        ...
    
    @effects.setter
    def effects(self, value : List[aspose.psd.fileformats.psd.layers.layereffects.ILayerEffect]):
        '''Gets the effects.'''
        ...
    
    @property
    def are_effects_enabled(self) -> bool:
        ...
    
    @are_effects_enabled.setter
    def are_effects_enabled(self, value : bool):
        ...
    
    ...

class ColorOverlayEffect(ILayerEffect):
    '''Color Overlay Layer effect'''
    
    def get_effect_bounds(self, layer_bounds : aspose.psd.Rectangle, global_angle : int) -> aspose.psd.Rectangle:
        '''Calculate and gets the bounds of effect pixels based on input layer pixels bounds.
        
        :param layer_bounds: The layer pixels bounds.
        :param global_angle: The global angle to calculate global light angle.
        :returns: The bounds of effect pixels based on input layer pixels bounds.'''
        ...
    
    @property
    def effect_type(self) -> aspose.psd.fileformats.psd.layers.layereffects.LayerEffectsTypes:
        ...
    
    @property
    def color(self) -> aspose.psd.Color:
        '''Gets the color.'''
        ...
    
    @color.setter
    def color(self, value : aspose.psd.Color):
        '''Sets the color.'''
        ...
    
    @property
    def blend_mode(self) -> aspose.psd.fileformats.core.blending.BlendMode:
        ...
    
    @blend_mode.setter
    def blend_mode(self, value : aspose.psd.fileformats.core.blending.BlendMode):
        ...
    
    @property
    def is_visible(self) -> bool:
        ...
    
    @is_visible.setter
    def is_visible(self, value : bool):
        ...
    
    @property
    def opacity(self) -> byte:
        '''Gets the opacity.'''
        ...
    
    @opacity.setter
    def opacity(self, value : byte):
        '''Sets the opacity.'''
        ...
    
    ...

class DropShadowEffect(IShadowEffect):
    '''Drop Shadow Layer effect'''
    
    def get_effect_bounds(self, layer_bounds : aspose.psd.Rectangle, global_angle : int) -> aspose.psd.Rectangle:
        '''Calculate and gets the bounds of effect pixels based on input layer pixels bounds.
        
        :param layer_bounds: The layer pixels bounds.
        :param global_angle: The global angle to calculate global light angle.
        :returns: The bounds of effect pixels based on input layer pixels bounds.'''
        ...
    
    @property
    def effect_type(self) -> aspose.psd.fileformats.psd.layers.layereffects.LayerEffectsTypes:
        ...
    
    @property
    def color(self) -> aspose.psd.Color:
        '''Gets the color.'''
        ...
    
    @color.setter
    def color(self, value : aspose.psd.Color):
        '''Sets the color.'''
        ...
    
    @property
    def blend_mode(self) -> aspose.psd.fileformats.core.blending.BlendMode:
        ...
    
    @blend_mode.setter
    def blend_mode(self, value : aspose.psd.fileformats.core.blending.BlendMode):
        ...
    
    @property
    def is_visible(self) -> bool:
        ...
    
    @is_visible.setter
    def is_visible(self, value : bool):
        ...
    
    @property
    def opacity(self) -> byte:
        '''Gets the opacity.'''
        ...
    
    @opacity.setter
    def opacity(self, value : byte):
        '''Sets the opacity.'''
        ...
    
    @property
    def angle(self) -> int:
        '''Gets the angle in degrees.'''
        ...
    
    @angle.setter
    def angle(self, value : int):
        '''Sets the angle in degrees.'''
        ...
    
    @property
    def use_global_light(self) -> bool:
        ...
    
    @use_global_light.setter
    def use_global_light(self, value : bool):
        ...
    
    @property
    def distance(self) -> int:
        '''Gets the distance in pixels.'''
        ...
    
    @distance.setter
    def distance(self, value : int):
        '''Sets the distance in pixels.'''
        ...
    
    @property
    def spread(self) -> int:
        '''Gets the intensity as a percent.'''
        ...
    
    @spread.setter
    def spread(self, value : int):
        '''Sets the intensity as a percent.'''
        ...
    
    @property
    def size(self) -> int:
        '''Gets the blur value in pixels.'''
        ...
    
    @size.setter
    def size(self, value : int):
        '''Sets the blur value in pixels.'''
        ...
    
    @property
    def noise(self) -> int:
        '''Gets the noise.'''
        ...
    
    @noise.setter
    def noise(self, value : int):
        '''Sets the noise.'''
        ...
    
    @property
    def knocks_out(self) -> bool:
        ...
    
    @knocks_out.setter
    def knocks_out(self, value : bool):
        ...
    
    ...

class GradientOverlayEffect(ILayerEffect):
    '''Gradient Layer effect'''
    
    def get_effect_bounds(self, layer_bounds : aspose.psd.Rectangle, global_angle : int) -> aspose.psd.Rectangle:
        '''Calculate and gets the bounds of effect pixels based on input layer pixels bounds.
        
        :param layer_bounds: The layer pixels bounds.
        :param global_angle: The global angle to calculate global light angle.
        :returns: The bounds of effect pixels based on input layer pixels bounds.'''
        ...
    
    @property
    def effect_type(self) -> aspose.psd.fileformats.psd.layers.layereffects.LayerEffectsTypes:
        ...
    
    @property
    def settings(self) -> aspose.psd.fileformats.psd.layers.fillsettings.GradientFillSettings:
        '''Gets the settings.'''
        ...
    
    @settings.setter
    def settings(self, value : aspose.psd.fileformats.psd.layers.fillsettings.GradientFillSettings):
        '''Sets the settings.'''
        ...
    
    @property
    def blend_mode(self) -> aspose.psd.fileformats.core.blending.BlendMode:
        ...
    
    @blend_mode.setter
    def blend_mode(self, value : aspose.psd.fileformats.core.blending.BlendMode):
        ...
    
    @property
    def is_visible(self) -> bool:
        ...
    
    @is_visible.setter
    def is_visible(self, value : bool):
        ...
    
    @property
    def opacity(self) -> byte:
        '''Gets the opacity.'''
        ...
    
    @opacity.setter
    def opacity(self, value : byte):
        '''Sets the opacity.'''
        ...
    
    ...

class ILayerEffect:
    '''Interface for Layer Effects'''
    
    def get_effect_bounds(self, layer_bounds : aspose.psd.Rectangle, global_angle : int) -> aspose.psd.Rectangle:
        '''Calculate and gets the bounds of effect pixels based on input layer pixels bounds.
        
        :param layer_bounds: The layer pixels bounds.
        :param global_angle: The global angle to calculate global light angle.
        :returns: The bounds of effect pixels based on input layer pixels bounds.'''
        ...
    
    @property
    def opacity(self) -> byte:
        '''Gets the opacity where 255 = 100%'''
        ...
    
    @opacity.setter
    def opacity(self, value : byte):
        '''Sets the opacity where 255 = 100%'''
        ...
    
    @property
    def blend_mode(self) -> aspose.psd.fileformats.core.blending.BlendMode:
        ...
    
    @blend_mode.setter
    def blend_mode(self, value : aspose.psd.fileformats.core.blending.BlendMode):
        ...
    
    @property
    def is_visible(self) -> bool:
        ...
    
    @is_visible.setter
    def is_visible(self, value : bool):
        ...
    
    @property
    def effect_type(self) -> aspose.psd.fileformats.psd.layers.layereffects.LayerEffectsTypes:
        ...
    
    ...

class IShadowEffect(ILayerEffect):
    '''Interface for Shadow Layer Effects'''
    
    def get_effect_bounds(self, layer_bounds : aspose.psd.Rectangle, global_angle : int) -> aspose.psd.Rectangle:
        '''Calculate and gets the bounds of effect pixels based on input layer pixels bounds.
        
        :param layer_bounds: The layer pixels bounds.
        :param global_angle: The global angle to calculate global light angle.
        :returns: The bounds of effect pixels based on input layer pixels bounds.'''
        ...
    
    @property
    def color(self) -> aspose.psd.Color:
        '''Gets the color.'''
        ...
    
    @color.setter
    def color(self, value : aspose.psd.Color):
        '''Sets the color.'''
        ...
    
    @property
    def angle(self) -> int:
        '''Gets the angle in degrees.'''
        ...
    
    @angle.setter
    def angle(self, value : int):
        '''Sets the angle in degrees.'''
        ...
    
    @property
    def use_global_light(self) -> bool:
        ...
    
    @use_global_light.setter
    def use_global_light(self, value : bool):
        ...
    
    @property
    def distance(self) -> int:
        '''Gets the distance in pixels.'''
        ...
    
    @distance.setter
    def distance(self, value : int):
        '''Sets the distance in pixels.'''
        ...
    
    @property
    def spread(self) -> int:
        '''Gets the intensity as a percent.'''
        ...
    
    @spread.setter
    def spread(self, value : int):
        '''Sets the intensity as a percent.'''
        ...
    
    @property
    def size(self) -> int:
        '''Gets the blur value in pixels.'''
        ...
    
    @size.setter
    def size(self, value : int):
        '''Sets the blur value in pixels.'''
        ...
    
    @property
    def noise(self) -> int:
        '''Gets the noise.'''
        ...
    
    @noise.setter
    def noise(self, value : int):
        '''Sets the noise.'''
        ...
    
    @property
    def opacity(self) -> byte:
        '''Gets the opacity where 255 = 100%'''
        ...
    
    @opacity.setter
    def opacity(self, value : byte):
        '''Sets the opacity where 255 = 100%'''
        ...
    
    @property
    def blend_mode(self) -> aspose.psd.fileformats.core.blending.BlendMode:
        ...
    
    @blend_mode.setter
    def blend_mode(self, value : aspose.psd.fileformats.core.blending.BlendMode):
        ...
    
    @property
    def is_visible(self) -> bool:
        ...
    
    @is_visible.setter
    def is_visible(self, value : bool):
        ...
    
    @property
    def effect_type(self) -> aspose.psd.fileformats.psd.layers.layereffects.LayerEffectsTypes:
        ...
    
    ...

class InnerShadowEffect(IShadowEffect):
    '''Inner Shadow Layer effect'''
    
    def get_effect_bounds(self, layer_bounds : aspose.psd.Rectangle, global_angle : int) -> aspose.psd.Rectangle:
        '''Calculate and gets the bounds of effect pixels based on input layer pixels bounds.
        
        :param layer_bounds: The layer pixels bounds.
        :param global_angle: The global angle to calculate global light angle.
        :returns: The bounds of effect pixels based on input layer pixels bounds.'''
        ...
    
    @property
    def effect_type(self) -> aspose.psd.fileformats.psd.layers.layereffects.LayerEffectsTypes:
        ...
    
    @property
    def color(self) -> aspose.psd.Color:
        '''Gets the color.'''
        ...
    
    @color.setter
    def color(self, value : aspose.psd.Color):
        '''Sets the color.'''
        ...
    
    @property
    def blend_mode(self) -> aspose.psd.fileformats.core.blending.BlendMode:
        ...
    
    @blend_mode.setter
    def blend_mode(self, value : aspose.psd.fileformats.core.blending.BlendMode):
        ...
    
    @property
    def is_visible(self) -> bool:
        ...
    
    @is_visible.setter
    def is_visible(self, value : bool):
        ...
    
    @property
    def opacity(self) -> byte:
        '''Gets the opacity.'''
        ...
    
    @opacity.setter
    def opacity(self, value : byte):
        '''Sets the opacity.'''
        ...
    
    @property
    def angle(self) -> int:
        '''Gets the angle in degrees.'''
        ...
    
    @angle.setter
    def angle(self, value : int):
        '''Sets the angle in degrees.'''
        ...
    
    @property
    def use_global_light(self) -> bool:
        ...
    
    @use_global_light.setter
    def use_global_light(self, value : bool):
        ...
    
    @property
    def distance(self) -> int:
        '''Gets the distance in pixels.'''
        ...
    
    @distance.setter
    def distance(self, value : int):
        '''Sets the distance in pixels.'''
        ...
    
    @property
    def spread(self) -> int:
        '''Gets the spread (choke) as percentage.'''
        ...
    
    @spread.setter
    def spread(self, value : int):
        '''Sets the spread (choke) as percentage.'''
        ...
    
    @property
    def size(self) -> int:
        '''Gets the blur value in pixels.'''
        ...
    
    @size.setter
    def size(self, value : int):
        '''Sets the blur value in pixels.'''
        ...
    
    @property
    def noise(self) -> int:
        '''Gets the noise.'''
        ...
    
    @noise.setter
    def noise(self, value : int):
        '''Sets the noise.'''
        ...
    
    ...

class OuterGlowEffect(ILayerEffect):
    '''Outer Glow Layer effect'''
    
    def get_effect_bounds(self, layer_bounds : aspose.psd.Rectangle, global_angle : int) -> aspose.psd.Rectangle:
        '''Calculate and gets the bounds of effect pixels based on input layer pixels bounds.
        
        :param layer_bounds: The layer pixels bounds.
        :param global_angle: The global angle to calculate global light angle.
        :returns: The bounds of effect pixels based on input layer pixels bounds.'''
        ...
    
    @property
    def fill_color(self) -> aspose.psd.fileformats.psd.layers.fillsettings.IFillSettings:
        ...
    
    @fill_color.setter
    def fill_color(self, value : aspose.psd.fileformats.psd.layers.fillsettings.IFillSettings):
        ...
    
    @property
    def blend_mode(self) -> aspose.psd.fileformats.core.blending.BlendMode:
        ...
    
    @blend_mode.setter
    def blend_mode(self, value : aspose.psd.fileformats.core.blending.BlendMode):
        ...
    
    @property
    def is_visible(self) -> bool:
        ...
    
    @is_visible.setter
    def is_visible(self, value : bool):
        ...
    
    @property
    def effect_type(self) -> aspose.psd.fileformats.psd.layers.layereffects.LayerEffectsTypes:
        ...
    
    @property
    def opacity(self) -> byte:
        '''Gets the opacity.'''
        ...
    
    @opacity.setter
    def opacity(self, value : byte):
        '''Sets the opacity.'''
        ...
    
    @property
    def intensity(self) -> int:
        '''Gets the angle in degrees.'''
        ...
    
    @intensity.setter
    def intensity(self, value : int):
        '''Sets the angle in degrees.'''
        ...
    
    @property
    def is_anti_aliasing(self) -> bool:
        ...
    
    @is_anti_aliasing.setter
    def is_anti_aliasing(self, value : bool):
        ...
    
    @property
    def spread(self) -> int:
        '''Gets the intensity as a percent.'''
        ...
    
    @spread.setter
    def spread(self, value : int):
        '''Sets the intensity as a percent.'''
        ...
    
    @property
    def size(self) -> int:
        '''Gets the blur value in pixels.'''
        ...
    
    @size.setter
    def size(self, value : int):
        '''Gets the blur value in pixels.'''
        ...
    
    @property
    def noise(self) -> int:
        '''Gets the noise.'''
        ...
    
    @noise.setter
    def noise(self, value : int):
        '''Sets the noise.'''
        ...
    
    @property
    def is_soft_blend(self) -> bool:
        ...
    
    @is_soft_blend.setter
    def is_soft_blend(self, value : bool):
        ...
    
    @property
    def range(self) -> int:
        '''Gets the noise.'''
        ...
    
    @range.setter
    def range(self, value : int):
        '''Sets the noise.'''
        ...
    
    @property
    def jitter(self) -> int:
        '''Gets the noise.'''
        ...
    
    @jitter.setter
    def jitter(self, value : int):
        '''Sets the noise.'''
        ...
    
    ...

class PatternOverlayEffect(ILayerEffect):
    '''Pattern Layer effect'''
    
    def get_effect_bounds(self, layer_bounds : aspose.psd.Rectangle, global_angle : int) -> aspose.psd.Rectangle:
        '''Calculate and gets the bounds of effect pixels based on input layer pixels bounds.
        
        :param layer_bounds: The layer pixels bounds.
        :param global_angle: The global angle to calculate global light angle.
        :returns: The bounds of effect pixels based on input layer pixels bounds.'''
        ...
    
    @property
    def effect_type(self) -> aspose.psd.fileformats.psd.layers.layereffects.LayerEffectsTypes:
        ...
    
    @property
    def settings(self) -> aspose.psd.fileformats.psd.layers.fillsettings.PatternFillSettings:
        '''Gets the settings.'''
        ...
    
    @settings.setter
    def settings(self, value : aspose.psd.fileformats.psd.layers.fillsettings.PatternFillSettings):
        '''Sets the settings.'''
        ...
    
    @property
    def blend_mode(self) -> aspose.psd.fileformats.core.blending.BlendMode:
        ...
    
    @blend_mode.setter
    def blend_mode(self, value : aspose.psd.fileformats.core.blending.BlendMode):
        ...
    
    @property
    def is_visible(self) -> bool:
        ...
    
    @is_visible.setter
    def is_visible(self, value : bool):
        ...
    
    @property
    def opacity(self) -> byte:
        '''Gets the opacity.'''
        ...
    
    @opacity.setter
    def opacity(self, value : byte):
        '''Sets the opacity.'''
        ...
    
    ...

class StrokeEffect(ILayerEffect):
    '''The Adobe® Photoshop® stroke effect for the PSD layer.'''
    
    def get_effect_bounds(self, layer_bounds : aspose.psd.Rectangle, global_angle : int) -> aspose.psd.Rectangle:
        '''Calculate and gets the bounds of effect pixels based on input layer pixels bounds.
        
        :param layer_bounds: The layer pixels bounds.
        :param global_angle: The global angle to calculate global light angle.
        :returns: The bounds of effect pixels based on input layer pixels bounds.'''
        ...
    
    @property
    def effect_type(self) -> aspose.psd.fileformats.psd.layers.layereffects.LayerEffectsTypes:
        ...
    
    @property
    def overprint(self) -> bool:
        '''Gets a value indicating whether this :py:class:`aspose.psd.fileformats.psd.layers.layereffects.StrokeEffect` will blend stroke against current layer contents.'''
        ...
    
    @overprint.setter
    def overprint(self, value : bool):
        '''Sets a value indicating whether this :py:class:`aspose.psd.fileformats.psd.layers.layereffects.StrokeEffect` will blend stroke against current layer contents.'''
        ...
    
    @property
    def position(self) -> aspose.psd.fileformats.psd.layers.layereffects.StrokePosition:
        '''Gets the position of the stroke effect to control the alignment of your stroke to the PSD layer content.
        The value can be :py:attr:`aspose.psd.fileformats.psd.layers.layereffects.StrokePosition.INSIDE` to draw stroke inside of the PSD layer content,
        or :py:attr:`aspose.psd.fileformats.psd.layers.layereffects.StrokePosition.OUTSIDE` to draw stroke around of PSD layer content,
        and :py:attr:`aspose.psd.fileformats.psd.layers.layereffects.StrokePosition.CENTER` to draw stroke both inside and outside.'''
        ...
    
    @position.setter
    def position(self, value : aspose.psd.fileformats.psd.layers.layereffects.StrokePosition):
        '''Sets the position of the stroke effect to control the alignment of your stroke to the PSD layer content.
        The value can be :py:attr:`aspose.psd.fileformats.psd.layers.layereffects.StrokePosition.INSIDE` to draw stroke inside of the PSD layer content,
        or :py:attr:`aspose.psd.fileformats.psd.layers.layereffects.StrokePosition.OUTSIDE` to draw stroke around of PSD layer content,
        and :py:attr:`aspose.psd.fileformats.psd.layers.layereffects.StrokePosition.CENTER` to draw stroke both inside and outside.'''
        ...
    
    @property
    def size(self) -> int:
        '''Gets the width of stroke effect.'''
        ...
    
    @size.setter
    def size(self, value : int):
        '''Sets the width of stroke effect.'''
        ...
    
    @property
    def blend_mode(self) -> aspose.psd.fileformats.core.blending.BlendMode:
        ...
    
    @blend_mode.setter
    def blend_mode(self, value : aspose.psd.fileformats.core.blending.BlendMode):
        ...
    
    @property
    def is_visible(self) -> bool:
        ...
    
    @is_visible.setter
    def is_visible(self, value : bool):
        ...
    
    @property
    def fill_settings(self) -> aspose.psd.fileformats.psd.layers.fillsettings.BaseFillSettings:
        ...
    
    @fill_settings.setter
    def fill_settings(self, value : aspose.psd.fileformats.psd.layers.fillsettings.BaseFillSettings):
        ...
    
    @property
    def opacity(self) -> byte:
        '''Gets the opacity.'''
        ...
    
    @opacity.setter
    def opacity(self, value : byte):
        '''Sets the opacity.'''
        ...
    
    ...

class LayerEffectsTypes:
    '''Layer blending effects.'''
    
    @classmethod
    @property
    def DROP_SHADOW(cls) -> LayerEffectsTypes:
        '''The drop shadow.'''
        ...
    
    @classmethod
    @property
    def OUTER_GLOW(cls) -> LayerEffectsTypes:
        '''The outer glow.'''
        ...
    
    @classmethod
    @property
    def PATTERN_OVERLAY(cls) -> LayerEffectsTypes:
        '''The pattern overlay.'''
        ...
    
    @classmethod
    @property
    def GRADIENT_OVERLAY(cls) -> LayerEffectsTypes:
        '''The gradient overlay.'''
        ...
    
    @classmethod
    @property
    def COLOR_OVERLAY(cls) -> LayerEffectsTypes:
        '''The color overlay.'''
        ...
    
    @classmethod
    @property
    def SATIN(cls) -> LayerEffectsTypes:
        '''The satin Effect Type.'''
        ...
    
    @classmethod
    @property
    def INNER_GLOW(cls) -> LayerEffectsTypes:
        '''The inner glow.'''
        ...
    
    @classmethod
    @property
    def INNER_SHADOW(cls) -> LayerEffectsTypes:
        '''The inner shadow.'''
        ...
    
    @classmethod
    @property
    def STROKE(cls) -> LayerEffectsTypes:
        '''The stroke.'''
        ...
    
    @classmethod
    @property
    def BEVEL_EMBOSS(cls) -> LayerEffectsTypes:
        '''The bevel emboss.'''
        ...
    
    ...

class StrokePosition:
    '''The position setting controls the alignment of your stroke to the layer it's applied to in the :py:class:`aspose.psd.fileformats.psd.layers.layereffects.StrokeEffect`.'''
    
    @classmethod
    @property
    def INSIDE(cls) -> StrokePosition:
        '''The stroke will be created from the edge of the shape and grow inward, to the center of the object.'''
        ...
    
    @classmethod
    @property
    def CENTER(cls) -> StrokePosition:
        '''The stroke will be created from the edge of the shape and grow both inwards and outwards.'''
        ...
    
    @classmethod
    @property
    def OUTSIDE(cls) -> StrokePosition:
        '''The stroke will be created from the edge of the shape and will grow outwards, away from the object.'''
        ...
    
    ...

