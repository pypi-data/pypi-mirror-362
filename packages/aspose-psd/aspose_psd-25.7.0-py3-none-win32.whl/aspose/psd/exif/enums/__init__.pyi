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

class ExifColorSpace:
    '''exif color space enum.'''
    
    @classmethod
    @property
    def S_RGB(cls) -> ExifColorSpace:
        '''SRGB color space.'''
        ...
    
    @classmethod
    @property
    def ADOBE_RGB(cls) -> ExifColorSpace:
        '''Adobe rgb color space.'''
        ...
    
    @classmethod
    @property
    def UNCALIBRATED(cls) -> ExifColorSpace:
        '''Uncalibrated color space.'''
        ...
    
    ...

class ExifContrast:
    '''exif normal soft hard enum.'''
    
    @classmethod
    @property
    def NORMAL(cls) -> ExifContrast:
        '''Normal contrast.'''
        ...
    
    @classmethod
    @property
    def LOW(cls) -> ExifContrast:
        '''Low contrast.'''
        ...
    
    @classmethod
    @property
    def HIGH(cls) -> ExifContrast:
        '''High contrast.'''
        ...
    
    ...

class ExifCustomRendered:
    '''exif custom rendered enum.'''
    
    @classmethod
    @property
    def NORMAL_PROCESS(cls) -> ExifCustomRendered:
        '''Normal render process.'''
        ...
    
    @classmethod
    @property
    def CUSTOM_PROCESS(cls) -> ExifCustomRendered:
        '''Custom render process.'''
        ...
    
    ...

class ExifExposureMode:
    '''exif exposure mode enum.'''
    
    @classmethod
    @property
    def AUTO(cls) -> ExifExposureMode:
        '''Auto exposure.'''
        ...
    
    @classmethod
    @property
    def MANUAL(cls) -> ExifExposureMode:
        '''Manual exposure.'''
        ...
    
    @classmethod
    @property
    def AUTO_BRACKET(cls) -> ExifExposureMode:
        '''Auto bracket.'''
        ...
    
    ...

class ExifExposureProgram:
    '''exif exposure program enum.'''
    
    @classmethod
    @property
    def NOTDEFINED(cls) -> ExifExposureProgram:
        '''Not defined.'''
        ...
    
    @classmethod
    @property
    def MANUAL(cls) -> ExifExposureProgram:
        '''Manual program.'''
        ...
    
    @classmethod
    @property
    def AUTO(cls) -> ExifExposureProgram:
        '''Auto exposure.'''
        ...
    
    @classmethod
    @property
    def APERTUREPRIORITY(cls) -> ExifExposureProgram:
        '''Aperture priority.'''
        ...
    
    @classmethod
    @property
    def SHUTTERPRIORITY(cls) -> ExifExposureProgram:
        '''Shutter priority.'''
        ...
    
    @classmethod
    @property
    def CREATIVEPROGRAM(cls) -> ExifExposureProgram:
        '''Creative program.'''
        ...
    
    @classmethod
    @property
    def ACTIONPROGRAM(cls) -> ExifExposureProgram:
        '''Action program.'''
        ...
    
    @classmethod
    @property
    def PORTRAITMODE(cls) -> ExifExposureProgram:
        '''Portrait mode.'''
        ...
    
    @classmethod
    @property
    def LANDSCAPEMODE(cls) -> ExifExposureProgram:
        '''Landscape mode.'''
        ...
    
    ...

class ExifFileSource:
    '''exif file source enum.'''
    
    @classmethod
    @property
    def OTHERS(cls) -> ExifFileSource:
        '''The others.'''
        ...
    
    @classmethod
    @property
    def FILM_SCANNER(cls) -> ExifFileSource:
        '''Film scanner.'''
        ...
    
    @classmethod
    @property
    def REFLEXION_PRINT_SCANNER(cls) -> ExifFileSource:
        '''Reflexion print scanner.'''
        ...
    
    @classmethod
    @property
    def DIGITAL_STILL_CAMERA(cls) -> ExifFileSource:
        '''Digital still camera.'''
        ...
    
    ...

class ExifFlash:
    '''Flash mode.'''
    
    @classmethod
    @property
    def NOFLASH(cls) -> ExifFlash:
        '''No flash fired.'''
        ...
    
    @classmethod
    @property
    def FIRED(cls) -> ExifFlash:
        '''Flash fired.'''
        ...
    
    @classmethod
    @property
    def FIRED_RETURN_LIGHT_NOT_DETECTED(cls) -> ExifFlash:
        '''Flash fired, return light not detected.'''
        ...
    
    @classmethod
    @property
    def FIRED_RETURN_LIGHT_DETECTED(cls) -> ExifFlash:
        '''Flash fired, return light detected.'''
        ...
    
    @classmethod
    @property
    def YES_COMPULSORY(cls) -> ExifFlash:
        '''Flash fired, compulsory flash mode.'''
        ...
    
    @classmethod
    @property
    def YES_COMPULSORY_RETURN_LIGHT_NOT_DETECTED(cls) -> ExifFlash:
        '''Flash fired, compulsory mode, return light not detected.'''
        ...
    
    @classmethod
    @property
    def YES_COMPULSORY_RETURN_LIGHT_DETECTED(cls) -> ExifFlash:
        '''Flash fired, compulsory mode, return light detected.'''
        ...
    
    @classmethod
    @property
    def NO_COMPULSORY(cls) -> ExifFlash:
        '''Flash did not fire, compulsory flash mode.'''
        ...
    
    @classmethod
    @property
    def NO_DID_NOT_FIRE_RETURN_LIGHT_NOT_DETECTED(cls) -> ExifFlash:
        '''Flash did not fire, return light not detected.'''
        ...
    
    @classmethod
    @property
    def NO_AUTO(cls) -> ExifFlash:
        '''Flash did not fire, auto mode.'''
        ...
    
    @classmethod
    @property
    def YES_AUTO(cls) -> ExifFlash:
        '''Flash firedm auto mode.'''
        ...
    
    @classmethod
    @property
    def YES_AUTO_RETURN_LIGHT_NOT_DETECTED(cls) -> ExifFlash:
        '''Flash fired, auto mode, return light not detected.'''
        ...
    
    @classmethod
    @property
    def YES_AUTO_RETURN_LIGHT_DETECTED(cls) -> ExifFlash:
        '''Flash fired, auto mode, return light detected.'''
        ...
    
    @classmethod
    @property
    def NO_FLASH_FUNCTION(cls) -> ExifFlash:
        '''No flash function.'''
        ...
    
    ...

class ExifGPSAltitudeRef:
    '''exif gps altitude ref enum.'''
    
    @classmethod
    @property
    def ABOVE_SEA_LEVEL(cls) -> ExifGPSAltitudeRef:
        '''Above sea level.'''
        ...
    
    @classmethod
    @property
    def BELOW_SEA_LEVEL(cls) -> ExifGPSAltitudeRef:
        '''Below sea level.'''
        ...
    
    ...

class ExifGainControl:
    '''exif gain control enum.'''
    
    @classmethod
    @property
    def NONE(cls) -> ExifGainControl:
        '''No gain control.'''
        ...
    
    @classmethod
    @property
    def LOW_GAIN_UP(cls) -> ExifGainControl:
        '''Low gain up.'''
        ...
    
    @classmethod
    @property
    def HIGH_GAIN_UP(cls) -> ExifGainControl:
        '''High gain up.'''
        ...
    
    @classmethod
    @property
    def LOW_GAIN_DOWN(cls) -> ExifGainControl:
        '''Low gain down.'''
        ...
    
    @classmethod
    @property
    def HIGH_GAIN_DOWN(cls) -> ExifGainControl:
        '''High gain down.'''
        ...
    
    ...

class ExifLightSource:
    '''The exif light source.'''
    
    @classmethod
    @property
    def UNKNOWN(cls) -> ExifLightSource:
        '''The unknown.'''
        ...
    
    @classmethod
    @property
    def DAYLIGHT(cls) -> ExifLightSource:
        '''The daylight.'''
        ...
    
    @classmethod
    @property
    def FLUORESCENT(cls) -> ExifLightSource:
        '''The fluorescent.'''
        ...
    
    @classmethod
    @property
    def TUNGSTEN(cls) -> ExifLightSource:
        '''The tungsten.'''
        ...
    
    @classmethod
    @property
    def FLASH(cls) -> ExifLightSource:
        '''The flash.'''
        ...
    
    @classmethod
    @property
    def FINEWEATHER(cls) -> ExifLightSource:
        '''The fineweather.'''
        ...
    
    @classmethod
    @property
    def CLOUDYWEATHER(cls) -> ExifLightSource:
        '''The cloudyweather.'''
        ...
    
    @classmethod
    @property
    def SHADE(cls) -> ExifLightSource:
        '''The shade.'''
        ...
    
    @classmethod
    @property
    def DAYLIGHT_FLUORESCENT(cls) -> ExifLightSource:
        '''The daylight fluorescent.'''
        ...
    
    @classmethod
    @property
    def DAY_WHITE_FLUORESCENT(cls) -> ExifLightSource:
        '''The day white fluorescent.'''
        ...
    
    @classmethod
    @property
    def COOL_WHITE_FLUORESCENT(cls) -> ExifLightSource:
        '''The cool white fluorescent.'''
        ...
    
    @classmethod
    @property
    def WHITE_FLUORESCENT(cls) -> ExifLightSource:
        '''The white fluorescent.'''
        ...
    
    @classmethod
    @property
    def STANDARDLIGHT_A(cls) -> ExifLightSource:
        '''The standardlight a.'''
        ...
    
    @classmethod
    @property
    def STANDARDLIGHT_B(cls) -> ExifLightSource:
        '''The standardlight b.'''
        ...
    
    @classmethod
    @property
    def STANDARDLIGHT_C(cls) -> ExifLightSource:
        '''The standardlight c.'''
        ...
    
    @classmethod
    @property
    def D55(cls) -> ExifLightSource:
        '''The d55 value(5500K).'''
        ...
    
    @classmethod
    @property
    def D65(cls) -> ExifLightSource:
        '''The d65 value(6500K).'''
        ...
    
    @classmethod
    @property
    def D75(cls) -> ExifLightSource:
        '''The d75 value(7500K).'''
        ...
    
    @classmethod
    @property
    def D50(cls) -> ExifLightSource:
        '''The d50 value(5000K).'''
        ...
    
    @classmethod
    @property
    def IS_OSTUDIOTUNGSTEN(cls) -> ExifLightSource:
        '''The iso studio tungsten lightsource.'''
        ...
    
    @classmethod
    @property
    def OTHERLIGHTSOURCE(cls) -> ExifLightSource:
        '''The otherlightsource.'''
        ...
    
    ...

class ExifMeteringMode:
    '''exif metering mode enum.'''
    
    @classmethod
    @property
    def UNKNOWN(cls) -> ExifMeteringMode:
        '''Undefined mode'''
        ...
    
    @classmethod
    @property
    def AVERAGE(cls) -> ExifMeteringMode:
        '''Average metering'''
        ...
    
    @classmethod
    @property
    def CENTERWEIGHTEDAVERAGE(cls) -> ExifMeteringMode:
        '''Center weighted average.'''
        ...
    
    @classmethod
    @property
    def SPOT(cls) -> ExifMeteringMode:
        '''Spot metering'''
        ...
    
    @classmethod
    @property
    def MULTI_SPOT(cls) -> ExifMeteringMode:
        '''Multi spot metering'''
        ...
    
    @classmethod
    @property
    def MULTI_SEGMENT(cls) -> ExifMeteringMode:
        '''Multi segment metering.'''
        ...
    
    @classmethod
    @property
    def PARTIAL(cls) -> ExifMeteringMode:
        '''Partial metering.'''
        ...
    
    @classmethod
    @property
    def OTHER(cls) -> ExifMeteringMode:
        '''For other modes.'''
        ...
    
    ...

class ExifOrientation:
    '''Exif image orientation.'''
    
    @classmethod
    @property
    def TOP_LEFT(cls) -> ExifOrientation:
        '''Top left. Default orientation.'''
        ...
    
    @classmethod
    @property
    def TOP_RIGHT(cls) -> ExifOrientation:
        '''Top right. Horizontally reversed.'''
        ...
    
    @classmethod
    @property
    def BOTTOM_RIGHT(cls) -> ExifOrientation:
        '''Bottom right. Rotated by 180 degrees.'''
        ...
    
    @classmethod
    @property
    def BOTTOM_LEFT(cls) -> ExifOrientation:
        '''Bottom left. Rotated by 180 degrees and then horizontally reversed.'''
        ...
    
    @classmethod
    @property
    def LEFT_TOP(cls) -> ExifOrientation:
        '''Left top. Rotated by 90 degrees counterclockwise and then horizontally reversed.'''
        ...
    
    @classmethod
    @property
    def RIGHT_TOP(cls) -> ExifOrientation:
        '''Right top. Rotated by 90 degrees clockwise.'''
        ...
    
    @classmethod
    @property
    def RIGHT_BOTTOM(cls) -> ExifOrientation:
        '''Right bottom. Rotated by 90 degrees clockwise and then horizontally reversed.'''
        ...
    
    @classmethod
    @property
    def LEFT_BOTTOM(cls) -> ExifOrientation:
        '''Left bottom. Rotated by 90 degrees counterclockwise.'''
        ...
    
    ...

class ExifSaturation:
    '''exif saturation enum.'''
    
    @classmethod
    @property
    def NORMAL(cls) -> ExifSaturation:
        '''Normal saturation.'''
        ...
    
    @classmethod
    @property
    def LOW(cls) -> ExifSaturation:
        '''Low saturation.'''
        ...
    
    @classmethod
    @property
    def HIGH(cls) -> ExifSaturation:
        '''High saturation.'''
        ...
    
    ...

class ExifSceneCaptureType:
    '''exif scene capture type enum.'''
    
    @classmethod
    @property
    def STANDARD(cls) -> ExifSceneCaptureType:
        '''Standard scene.'''
        ...
    
    @classmethod
    @property
    def LANDSCAPE(cls) -> ExifSceneCaptureType:
        '''Landscape scene.'''
        ...
    
    @classmethod
    @property
    def PORTRAIT(cls) -> ExifSceneCaptureType:
        '''Portrait scene.'''
        ...
    
    @classmethod
    @property
    def NIGHT_SCENE(cls) -> ExifSceneCaptureType:
        '''Night scene.'''
        ...
    
    ...

class ExifSensingMethod:
    '''exif sensing method enum.'''
    
    @classmethod
    @property
    def NOTDEFINED(cls) -> ExifSensingMethod:
        '''Not defined.'''
        ...
    
    @classmethod
    @property
    def ONE_CHIP_COLOR_AREA(cls) -> ExifSensingMethod:
        '''One chip color area.'''
        ...
    
    @classmethod
    @property
    def TWO_CHIP_COLOR_AREA(cls) -> ExifSensingMethod:
        '''Two chip color area.'''
        ...
    
    @classmethod
    @property
    def THREE_CHIP_COLOR_AREA(cls) -> ExifSensingMethod:
        '''Three chip color area.'''
        ...
    
    @classmethod
    @property
    def COLORSEQUENTIALAREA(cls) -> ExifSensingMethod:
        '''Color Sequential area.'''
        ...
    
    @classmethod
    @property
    def TRILINEARSENSOR(cls) -> ExifSensingMethod:
        '''Trilinear sensor.'''
        ...
    
    @classmethod
    @property
    def COLORSEQUENTIALLINEAR(cls) -> ExifSensingMethod:
        '''Color sequential linear sensor.'''
        ...
    
    ...

class ExifSubjectDistanceRange:
    '''exif subject distance range enum.'''
    
    @classmethod
    @property
    def UNKNOWN(cls) -> ExifSubjectDistanceRange:
        '''Unknown subject distance range'''
        ...
    
    @classmethod
    @property
    def MACRO(cls) -> ExifSubjectDistanceRange:
        '''Macro range'''
        ...
    
    @classmethod
    @property
    def CLOSE_VIEW(cls) -> ExifSubjectDistanceRange:
        '''Close view.'''
        ...
    
    @classmethod
    @property
    def DISTANT_VIEW(cls) -> ExifSubjectDistanceRange:
        '''Distant view.'''
        ...
    
    ...

class ExifUnit:
    '''exif unit enum.'''
    
    @classmethod
    @property
    def NONE(cls) -> ExifUnit:
        '''Undefined units'''
        ...
    
    @classmethod
    @property
    def INCH(cls) -> ExifUnit:
        '''Inch units'''
        ...
    
    @classmethod
    @property
    def CM(cls) -> ExifUnit:
        '''Metric centimeter units'''
        ...
    
    ...

class ExifWhiteBalance:
    '''exif white balance enum.'''
    
    @classmethod
    @property
    def AUTO(cls) -> ExifWhiteBalance:
        '''Auto white balance'''
        ...
    
    @classmethod
    @property
    def MANUAL(cls) -> ExifWhiteBalance:
        '''Manual  white balance'''
        ...
    
    ...

class ExifYCbCrPositioning:
    '''exif y cb cr positioning enum.'''
    
    @classmethod
    @property
    def CENTERED(cls) -> ExifYCbCrPositioning:
        '''Centered YCbCr'''
        ...
    
    @classmethod
    @property
    def CO_SITED(cls) -> ExifYCbCrPositioning:
        '''Co-sited position'''
        ...
    
    ...

