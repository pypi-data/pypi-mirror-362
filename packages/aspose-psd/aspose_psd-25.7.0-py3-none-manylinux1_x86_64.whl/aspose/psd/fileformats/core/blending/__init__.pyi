"""The namespace handles Blending Types, Classes and other utilities. 
            Aspose.PSD supports all PSD Blending modes."""
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

class BlendMode(enum.Enum):
    NORMAL = enum.auto()
    '''Normal blend mode.'''
    DARKEN = enum.auto()
    '''Darken blend mode.'''
    LIGHTEN = enum.auto()
    '''Lighten blend mode.'''
    HUE = enum.auto()
    '''Hue blend mode.'''
    SATURATION = enum.auto()
    '''Saturation blend mode.'''
    COLOR = enum.auto()
    '''Color blend mode.'''
    LUMINOSITY = enum.auto()
    '''Luminosity blend mode.'''
    MULTIPLY = enum.auto()
    '''Multiply blend mode.'''
    SCREEN = enum.auto()
    '''Screen blend mode.'''
    DISSOLVE = enum.auto()
    '''Dissolve blend mode.'''
    OVERLAY = enum.auto()
    '''Overlay blend mode.'''
    HARD_LIGHT = enum.auto()
    '''Hard light blend mode.'''
    SOFT_LIGHT = enum.auto()
    '''Soft light blend mode.'''
    DIFFERENCE = enum.auto()
    '''Difference blend mode.'''
    EXCLUSION = enum.auto()
    '''Exclusion blend mode.'''
    COLOR_DODGE = enum.auto()
    '''Color dodge blend mode.'''
    COLOR_BURN = enum.auto()
    '''Color burn blend mode.'''
    LINEAR_BURN = enum.auto()
    '''Linear burn blend mode.'''
    LINEAR_DODGE = enum.auto()
    '''Linear dodge blend mode.'''
    VIVID_LIGHT = enum.auto()
    '''Vivid light blend mode.'''
    LINEAR_LIGHT = enum.auto()
    '''Linear light blend mode.'''
    PIN_LIGHT = enum.auto()
    '''Pin light blend mode.'''
    HARD_MIX = enum.auto()
    '''Hard mix blend mode.'''
    PASS_THROUGH = enum.auto()
    '''Pass through blend mode.'''
    DARKER_COLOR = enum.auto()
    '''Darker color blend mode.'''
    LIGHTER_COLOR = enum.auto()
    '''Lighter color blend mode.'''
    SUBTRACT = enum.auto()
    '''Subtract blend mode.'''
    DIVIDE = enum.auto()
    '''Divide blend mode.'''
    ABSENT = enum.auto()
    '''Blend mode is absent or not set yet.'''

