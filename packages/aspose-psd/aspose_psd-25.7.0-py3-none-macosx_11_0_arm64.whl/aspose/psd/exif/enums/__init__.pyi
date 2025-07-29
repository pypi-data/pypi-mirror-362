"""The namespace contains EXIF enumerations."""
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

class ExifColorSpace(enum.Enum):
    S_RGB = enum.auto()
    '''SRGB color space.'''
    ADOBE_RGB = enum.auto()
    '''Adobe rgb color space.'''
    UNCALIBRATED = enum.auto()
    '''Uncalibrated color space.'''

class ExifContrast(enum.Enum):
    NORMAL = enum.auto()
    '''Normal contrast.'''
    LOW = enum.auto()
    '''Low contrast.'''
    HIGH = enum.auto()
    '''High contrast.'''

class ExifCustomRendered(enum.Enum):
    NORMAL_PROCESS = enum.auto()
    '''Normal render process.'''
    CUSTOM_PROCESS = enum.auto()
    '''Custom render process.'''

class ExifExposureMode(enum.Enum):
    AUTO = enum.auto()
    '''Auto exposure.'''
    MANUAL = enum.auto()
    '''Manual exposure.'''
    AUTO_BRACKET = enum.auto()
    '''Auto bracket.'''

class ExifExposureProgram(enum.Enum):
    NOTDEFINED = enum.auto()
    '''Not defined.'''
    MANUAL = enum.auto()
    '''Manual program.'''
    AUTO = enum.auto()
    '''Auto exposure.'''
    APERTUREPRIORITY = enum.auto()
    '''Aperture priority.'''
    SHUTTERPRIORITY = enum.auto()
    '''Shutter priority.'''
    CREATIVEPROGRAM = enum.auto()
    '''Creative program.'''
    ACTIONPROGRAM = enum.auto()
    '''Action program.'''
    PORTRAITMODE = enum.auto()
    '''Portrait mode.'''
    LANDSCAPEMODE = enum.auto()
    '''Landscape mode.'''

class ExifFileSource(enum.Enum):
    OTHERS = enum.auto()
    '''The others.'''
    FILM_SCANNER = enum.auto()
    '''Film scanner.'''
    REFLEXION_PRINT_SCANNER = enum.auto()
    '''Reflexion print scanner.'''
    DIGITAL_STILL_CAMERA = enum.auto()
    '''Digital still camera.'''

class ExifFlash(enum.Enum):
    NOFLASH = enum.auto()
    '''No flash fired.'''
    FIRED = enum.auto()
    '''Flash fired.'''
    FIRED_RETURN_LIGHT_NOT_DETECTED = enum.auto()
    '''Flash fired, return light not detected.'''
    FIRED_RETURN_LIGHT_DETECTED = enum.auto()
    '''Flash fired, return light detected.'''
    YES_COMPULSORY = enum.auto()
    '''Flash fired, compulsory flash mode.'''
    YES_COMPULSORY_RETURN_LIGHT_NOT_DETECTED = enum.auto()
    '''Flash fired, compulsory mode, return light not detected.'''
    YES_COMPULSORY_RETURN_LIGHT_DETECTED = enum.auto()
    '''Flash fired, compulsory mode, return light detected.'''
    NO_COMPULSORY = enum.auto()
    '''Flash did not fire, compulsory flash mode.'''
    NO_DID_NOT_FIRE_RETURN_LIGHT_NOT_DETECTED = enum.auto()
    '''Flash did not fire, return light not detected.'''
    NO_AUTO = enum.auto()
    '''Flash did not fire, auto mode.'''
    YES_AUTO = enum.auto()
    '''Flash firedm auto mode.'''
    YES_AUTO_RETURN_LIGHT_NOT_DETECTED = enum.auto()
    '''Flash fired, auto mode, return light not detected.'''
    YES_AUTO_RETURN_LIGHT_DETECTED = enum.auto()
    '''Flash fired, auto mode, return light detected.'''
    NO_FLASH_FUNCTION = enum.auto()
    '''No flash function.'''

class ExifGPSAltitudeRef(enum.Enum):
    ABOVE_SEA_LEVEL = enum.auto()
    '''Above sea level.'''
    BELOW_SEA_LEVEL = enum.auto()
    '''Below sea level.'''

class ExifGainControl(enum.Enum):
    NONE = enum.auto()
    '''No gain control.'''
    LOW_GAIN_UP = enum.auto()
    '''Low gain up.'''
    HIGH_GAIN_UP = enum.auto()
    '''High gain up.'''
    LOW_GAIN_DOWN = enum.auto()
    '''Low gain down.'''
    HIGH_GAIN_DOWN = enum.auto()
    '''High gain down.'''

class ExifLightSource(enum.Enum):
    UNKNOWN = enum.auto()
    '''The unknown.'''
    DAYLIGHT = enum.auto()
    '''The daylight.'''
    FLUORESCENT = enum.auto()
    '''The fluorescent.'''
    TUNGSTEN = enum.auto()
    '''The tungsten.'''
    FLASH = enum.auto()
    '''The flash.'''
    FINEWEATHER = enum.auto()
    '''The fineweather.'''
    CLOUDYWEATHER = enum.auto()
    '''The cloudyweather.'''
    SHADE = enum.auto()
    '''The shade.'''
    DAYLIGHT_FLUORESCENT = enum.auto()
    '''The daylight fluorescent.'''
    DAY_WHITE_FLUORESCENT = enum.auto()
    '''The day white fluorescent.'''
    COOL_WHITE_FLUORESCENT = enum.auto()
    '''The cool white fluorescent.'''
    WHITE_FLUORESCENT = enum.auto()
    '''The white fluorescent.'''
    STANDARDLIGHT_A = enum.auto()
    '''The standardlight a.'''
    STANDARDLIGHT_B = enum.auto()
    '''The standardlight b.'''
    STANDARDLIGHT_C = enum.auto()
    '''The standardlight c.'''
    D55 = enum.auto()
    '''The d55 value(5500K).'''
    D65 = enum.auto()
    '''The d65 value(6500K).'''
    D75 = enum.auto()
    '''The d75 value(7500K).'''
    D50 = enum.auto()
    '''The d50 value(5000K).'''
    IS_OSTUDIOTUNGSTEN = enum.auto()
    '''The iso studio tungsten lightsource.'''
    OTHERLIGHTSOURCE = enum.auto()
    '''The otherlightsource.'''

class ExifMeteringMode(enum.Enum):
    UNKNOWN = enum.auto()
    '''Undefined mode'''
    AVERAGE = enum.auto()
    '''Average metering'''
    CENTERWEIGHTEDAVERAGE = enum.auto()
    '''Center weighted average.'''
    SPOT = enum.auto()
    '''Spot metering'''
    MULTI_SPOT = enum.auto()
    '''Multi spot metering'''
    MULTI_SEGMENT = enum.auto()
    '''Multi segment metering.'''
    PARTIAL = enum.auto()
    '''Partial metering.'''
    OTHER = enum.auto()
    '''For other modes.'''

class ExifOrientation(enum.Enum):
    TOP_LEFT = enum.auto()
    '''Top left. Default orientation.'''
    TOP_RIGHT = enum.auto()
    '''Top right. Horizontally reversed.'''
    BOTTOM_RIGHT = enum.auto()
    '''Bottom right. Rotated by 180 degrees.'''
    BOTTOM_LEFT = enum.auto()
    '''Bottom left. Rotated by 180 degrees and then horizontally reversed.'''
    LEFT_TOP = enum.auto()
    '''Left top. Rotated by 90 degrees counterclockwise and then horizontally reversed.'''
    RIGHT_TOP = enum.auto()
    '''Right top. Rotated by 90 degrees clockwise.'''
    RIGHT_BOTTOM = enum.auto()
    '''Right bottom. Rotated by 90 degrees clockwise and then horizontally reversed.'''
    LEFT_BOTTOM = enum.auto()
    '''Left bottom. Rotated by 90 degrees counterclockwise.'''

class ExifSaturation(enum.Enum):
    NORMAL = enum.auto()
    '''Normal saturation.'''
    LOW = enum.auto()
    '''Low saturation.'''
    HIGH = enum.auto()
    '''High saturation.'''

class ExifSceneCaptureType(enum.Enum):
    STANDARD = enum.auto()
    '''Standard scene.'''
    LANDSCAPE = enum.auto()
    '''Landscape scene.'''
    PORTRAIT = enum.auto()
    '''Portrait scene.'''
    NIGHT_SCENE = enum.auto()
    '''Night scene.'''

class ExifSensingMethod(enum.Enum):
    NOTDEFINED = enum.auto()
    '''Not defined.'''
    ONE_CHIP_COLOR_AREA = enum.auto()
    '''One chip color area.'''
    TWO_CHIP_COLOR_AREA = enum.auto()
    '''Two chip color area.'''
    THREE_CHIP_COLOR_AREA = enum.auto()
    '''Three chip color area.'''
    COLORSEQUENTIALAREA = enum.auto()
    '''Color Sequential area.'''
    TRILINEARSENSOR = enum.auto()
    '''Trilinear sensor.'''
    COLORSEQUENTIALLINEAR = enum.auto()
    '''Color sequential linear sensor.'''

class ExifSubjectDistanceRange(enum.Enum):
    UNKNOWN = enum.auto()
    '''Unknown subject distance range'''
    MACRO = enum.auto()
    '''Macro range'''
    CLOSE_VIEW = enum.auto()
    '''Close view.'''
    DISTANT_VIEW = enum.auto()
    '''Distant view.'''

class ExifUnit(enum.Enum):
    NONE = enum.auto()
    '''Undefined units'''
    INCH = enum.auto()
    '''Inch units'''
    CM = enum.auto()
    '''Metric centimeter units'''

class ExifWhiteBalance(enum.Enum):
    AUTO = enum.auto()
    '''Auto white balance'''
    MANUAL = enum.auto()
    '''Manual  white balance'''

class ExifYCbCrPositioning(enum.Enum):
    CENTERED = enum.auto()
    '''Centered YCbCr'''
    CO_SITED = enum.auto()
    '''Co-sited position'''

