"""The namespace contains EXIF related helper classes and methods."""
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

class ExifData(TiffDataTypeController):
    '''EXIF data container.'''
    
    @overload
    def __init__(self):
        '''Initializes a new instance of the  class.'''
        ...
    
    @overload
    def __init__(self, exifdata: List[aspose.psd.fileformats.tiff.TiffDataType]):
        '''Initializes a new instance of the  class with data from array.
        
        :param exifdata: Array of EXIF tags together with common and GPS tags.'''
        ...
    
    @overload
    def __init__(self, common_tags: List[aspose.psd.fileformats.tiff.TiffDataType], exif_tags: List[aspose.psd.fileformats.tiff.TiffDataType], gps_tags: List[aspose.psd.fileformats.tiff.TiffDataType]):
        '''Initializes a new instance of the  class with data from array.
        
        :param common_tags: The common tags.
        :param exif_tags: The EXIF tags.
        :param gps_tags: The GPS tags.'''
        ...
    
    @overload
    def remove_tag(self, tag: aspose.psd.exif.ExifProperties):
        '''Remove tag from container
        
        :param tag: The tag to remove'''
        ...
    
    @overload
    def remove_tag(self, tag_id: int):
        '''Remove tag from container
        
        :param tag_id: The tag identifier to remove.'''
        ...
    
    @property
    def is_big_endian(self) -> bool:
        ...
    
    @is_big_endian.setter
    def is_big_endian(self, value : bool):
        ...
    
    @property
    def aperture_value(self) -> aspose.psd.fileformats.tiff.TiffRational:
        ...
    
    @aperture_value.setter
    def aperture_value(self, value : aspose.psd.fileformats.tiff.TiffRational):
        ...
    
    @property
    def body_serial_number(self) -> str:
        ...
    
    @body_serial_number.setter
    def body_serial_number(self, value : str):
        ...
    
    @property
    def brightness_value(self) -> aspose.psd.fileformats.tiff.TiffSRational:
        ...
    
    @brightness_value.setter
    def brightness_value(self, value : aspose.psd.fileformats.tiff.TiffSRational):
        ...
    
    @property
    def cfa_pattern(self) -> bytes:
        ...
    
    @cfa_pattern.setter
    def cfa_pattern(self, value : bytes):
        ...
    
    @property
    def camera_owner_name(self) -> str:
        ...
    
    @camera_owner_name.setter
    def camera_owner_name(self, value : str):
        ...
    
    @property
    def color_space(self) -> aspose.psd.exif.enums.ExifColorSpace:
        ...
    
    @color_space.setter
    def color_space(self, value : aspose.psd.exif.enums.ExifColorSpace):
        ...
    
    @property
    def components_configuration(self) -> bytes:
        ...
    
    @components_configuration.setter
    def components_configuration(self, value : bytes):
        ...
    
    @property
    def compressed_bits_per_pixel(self) -> aspose.psd.fileformats.tiff.TiffRational:
        ...
    
    @compressed_bits_per_pixel.setter
    def compressed_bits_per_pixel(self, value : aspose.psd.fileformats.tiff.TiffRational):
        ...
    
    @property
    def contrast(self) -> aspose.psd.exif.enums.ExifContrast:
        '''Gets the contrast.'''
        ...
    
    @contrast.setter
    def contrast(self, value : aspose.psd.exif.enums.ExifContrast):
        '''Sets the contrast.'''
        ...
    
    @property
    def custom_rendered(self) -> aspose.psd.exif.enums.ExifCustomRendered:
        ...
    
    @custom_rendered.setter
    def custom_rendered(self, value : aspose.psd.exif.enums.ExifCustomRendered):
        ...
    
    @property
    def date_time_digitized(self) -> str:
        ...
    
    @date_time_digitized.setter
    def date_time_digitized(self, value : str):
        ...
    
    @property
    def date_time_original(self) -> str:
        ...
    
    @date_time_original.setter
    def date_time_original(self, value : str):
        ...
    
    @property
    def device_setting_description(self) -> bytes:
        ...
    
    @device_setting_description.setter
    def device_setting_description(self, value : bytes):
        ...
    
    @property
    def digital_zoom_ratio(self) -> aspose.psd.fileformats.tiff.TiffRational:
        ...
    
    @digital_zoom_ratio.setter
    def digital_zoom_ratio(self, value : aspose.psd.fileformats.tiff.TiffRational):
        ...
    
    @property
    def exif_version(self) -> bytes:
        ...
    
    @exif_version.setter
    def exif_version(self, value : bytes):
        ...
    
    @property
    def exposure_bias_value(self) -> aspose.psd.fileformats.tiff.TiffSRational:
        ...
    
    @exposure_bias_value.setter
    def exposure_bias_value(self, value : aspose.psd.fileformats.tiff.TiffSRational):
        ...
    
    @property
    def exposure_index(self) -> aspose.psd.fileformats.tiff.TiffRational:
        ...
    
    @exposure_index.setter
    def exposure_index(self, value : aspose.psd.fileformats.tiff.TiffRational):
        ...
    
    @property
    def exposure_mode(self) -> aspose.psd.exif.enums.ExifExposureMode:
        ...
    
    @exposure_mode.setter
    def exposure_mode(self, value : aspose.psd.exif.enums.ExifExposureMode):
        ...
    
    @property
    def exposure_program(self) -> aspose.psd.exif.enums.ExifExposureProgram:
        ...
    
    @exposure_program.setter
    def exposure_program(self, value : aspose.psd.exif.enums.ExifExposureProgram):
        ...
    
    @property
    def exposure_time(self) -> aspose.psd.fileformats.tiff.TiffRational:
        ...
    
    @exposure_time.setter
    def exposure_time(self, value : aspose.psd.fileformats.tiff.TiffRational):
        ...
    
    @property
    def f_number(self) -> aspose.psd.fileformats.tiff.TiffRational:
        ...
    
    @f_number.setter
    def f_number(self, value : aspose.psd.fileformats.tiff.TiffRational):
        ...
    
    @property
    def file_source(self) -> aspose.psd.exif.enums.ExifFileSource:
        ...
    
    @file_source.setter
    def file_source(self, value : aspose.psd.exif.enums.ExifFileSource):
        ...
    
    @property
    def flash(self) -> aspose.psd.exif.enums.ExifFlash:
        '''Gets the flash.'''
        ...
    
    @flash.setter
    def flash(self, value : aspose.psd.exif.enums.ExifFlash):
        '''Sets the flash.'''
        ...
    
    @property
    def flash_energy(self) -> aspose.psd.fileformats.tiff.TiffRational:
        ...
    
    @flash_energy.setter
    def flash_energy(self, value : aspose.psd.fileformats.tiff.TiffRational):
        ...
    
    @property
    def flashpix_version(self) -> bytes:
        ...
    
    @flashpix_version.setter
    def flashpix_version(self, value : bytes):
        ...
    
    @property
    def focal_length(self) -> aspose.psd.fileformats.tiff.TiffRational:
        ...
    
    @focal_length.setter
    def focal_length(self, value : aspose.psd.fileformats.tiff.TiffRational):
        ...
    
    @property
    def focal_length_in_35_mm_film(self) -> int:
        ...
    
    @focal_length_in_35_mm_film.setter
    def focal_length_in_35_mm_film(self, value : int):
        ...
    
    @property
    def focal_plane_resolution_unit(self) -> aspose.psd.exif.enums.ExifUnit:
        ...
    
    @focal_plane_resolution_unit.setter
    def focal_plane_resolution_unit(self, value : aspose.psd.exif.enums.ExifUnit):
        ...
    
    @property
    def focal_plane_x_resolution(self) -> aspose.psd.fileformats.tiff.TiffRational:
        ...
    
    @focal_plane_x_resolution.setter
    def focal_plane_x_resolution(self, value : aspose.psd.fileformats.tiff.TiffRational):
        ...
    
    @property
    def focal_plane_y_resolution(self) -> aspose.psd.fileformats.tiff.TiffRational:
        ...
    
    @focal_plane_y_resolution.setter
    def focal_plane_y_resolution(self, value : aspose.psd.fileformats.tiff.TiffRational):
        ...
    
    @property
    def gps_altitude(self) -> aspose.psd.fileformats.tiff.TiffRational:
        ...
    
    @gps_altitude.setter
    def gps_altitude(self, value : aspose.psd.fileformats.tiff.TiffRational):
        ...
    
    @property
    def gps_altitude_ref(self) -> aspose.psd.exif.enums.ExifGPSAltitudeRef:
        ...
    
    @gps_altitude_ref.setter
    def gps_altitude_ref(self, value : aspose.psd.exif.enums.ExifGPSAltitudeRef):
        ...
    
    @property
    def gps_area_information(self) -> bytes:
        ...
    
    @gps_area_information.setter
    def gps_area_information(self, value : bytes):
        ...
    
    @property
    def gpsdop(self) -> aspose.psd.fileformats.tiff.TiffRational:
        '''Gets the GPS DOP (data degree of precision).'''
        ...
    
    @gpsdop.setter
    def gpsdop(self, value : aspose.psd.fileformats.tiff.TiffRational):
        '''Sets the GPS DOP (data degree of precision).'''
        ...
    
    @property
    def gps_dest_bearing(self) -> aspose.psd.fileformats.tiff.TiffRational:
        ...
    
    @gps_dest_bearing.setter
    def gps_dest_bearing(self, value : aspose.psd.fileformats.tiff.TiffRational):
        ...
    
    @property
    def gps_dest_bearing_ref(self) -> str:
        ...
    
    @gps_dest_bearing_ref.setter
    def gps_dest_bearing_ref(self, value : str):
        ...
    
    @property
    def gps_dest_distance(self) -> aspose.psd.fileformats.tiff.TiffRational:
        ...
    
    @gps_dest_distance.setter
    def gps_dest_distance(self, value : aspose.psd.fileformats.tiff.TiffRational):
        ...
    
    @property
    def gps_dest_distance_ref(self) -> str:
        ...
    
    @gps_dest_distance_ref.setter
    def gps_dest_distance_ref(self, value : str):
        ...
    
    @property
    def gps_dest_latitude(self) -> List[aspose.psd.fileformats.tiff.TiffRational]:
        ...
    
    @gps_dest_latitude.setter
    def gps_dest_latitude(self, value : List[aspose.psd.fileformats.tiff.TiffRational]):
        ...
    
    @property
    def gps_dest_latitude_ref(self) -> str:
        ...
    
    @gps_dest_latitude_ref.setter
    def gps_dest_latitude_ref(self, value : str):
        ...
    
    @property
    def gps_dest_longitude(self) -> List[aspose.psd.fileformats.tiff.TiffRational]:
        ...
    
    @gps_dest_longitude.setter
    def gps_dest_longitude(self, value : List[aspose.psd.fileformats.tiff.TiffRational]):
        ...
    
    @property
    def gps_dest_longitude_ref(self) -> str:
        ...
    
    @gps_dest_longitude_ref.setter
    def gps_dest_longitude_ref(self, value : str):
        ...
    
    @property
    def gps_differential(self) -> int:
        ...
    
    @gps_differential.setter
    def gps_differential(self, value : int):
        ...
    
    @property
    def gps_img_direction(self) -> aspose.psd.fileformats.tiff.TiffRational:
        ...
    
    @gps_img_direction.setter
    def gps_img_direction(self, value : aspose.psd.fileformats.tiff.TiffRational):
        ...
    
    @property
    def gps_img_direction_ref(self) -> str:
        ...
    
    @gps_img_direction_ref.setter
    def gps_img_direction_ref(self, value : str):
        ...
    
    @property
    def gps_date_stamp(self) -> str:
        ...
    
    @gps_date_stamp.setter
    def gps_date_stamp(self, value : str):
        ...
    
    @property
    def gps_latitude(self) -> List[aspose.psd.fileformats.tiff.TiffRational]:
        ...
    
    @gps_latitude.setter
    def gps_latitude(self, value : List[aspose.psd.fileformats.tiff.TiffRational]):
        ...
    
    @property
    def gps_latitude_ref(self) -> str:
        ...
    
    @gps_latitude_ref.setter
    def gps_latitude_ref(self, value : str):
        ...
    
    @property
    def gps_longitude(self) -> List[aspose.psd.fileformats.tiff.TiffRational]:
        ...
    
    @gps_longitude.setter
    def gps_longitude(self, value : List[aspose.psd.fileformats.tiff.TiffRational]):
        ...
    
    @property
    def gps_longitude_ref(self) -> str:
        ...
    
    @gps_longitude_ref.setter
    def gps_longitude_ref(self, value : str):
        ...
    
    @property
    def gps_map_datum(self) -> str:
        ...
    
    @gps_map_datum.setter
    def gps_map_datum(self, value : str):
        ...
    
    @property
    def gps_measure_mode(self) -> str:
        ...
    
    @gps_measure_mode.setter
    def gps_measure_mode(self, value : str):
        ...
    
    @property
    def gps_processing_method(self) -> bytes:
        ...
    
    @gps_processing_method.setter
    def gps_processing_method(self, value : bytes):
        ...
    
    @property
    def gps_satellites(self) -> str:
        ...
    
    @gps_satellites.setter
    def gps_satellites(self, value : str):
        ...
    
    @property
    def gps_speed(self) -> aspose.psd.fileformats.tiff.TiffRational:
        ...
    
    @gps_speed.setter
    def gps_speed(self, value : aspose.psd.fileformats.tiff.TiffRational):
        ...
    
    @property
    def gps_speed_ref(self) -> str:
        ...
    
    @gps_speed_ref.setter
    def gps_speed_ref(self, value : str):
        ...
    
    @property
    def gps_status(self) -> str:
        ...
    
    @gps_status.setter
    def gps_status(self, value : str):
        ...
    
    @property
    def gps_timestamp(self) -> List[aspose.psd.fileformats.tiff.TiffRational]:
        ...
    
    @gps_timestamp.setter
    def gps_timestamp(self, value : List[aspose.psd.fileformats.tiff.TiffRational]):
        ...
    
    @property
    def gps_track(self) -> str:
        ...
    
    @gps_track.setter
    def gps_track(self, value : str):
        ...
    
    @property
    def gps_track_ref(self) -> str:
        ...
    
    @gps_track_ref.setter
    def gps_track_ref(self, value : str):
        ...
    
    @property
    def gps_version_id(self) -> bytes:
        ...
    
    @gps_version_id.setter
    def gps_version_id(self, value : bytes):
        ...
    
    @property
    def gain_control(self) -> aspose.psd.exif.enums.ExifGainControl:
        ...
    
    @gain_control.setter
    def gain_control(self, value : aspose.psd.exif.enums.ExifGainControl):
        ...
    
    @property
    def gamma(self) -> aspose.psd.fileformats.tiff.TiffRational:
        '''Gets the gamma.'''
        ...
    
    @gamma.setter
    def gamma(self, value : aspose.psd.fileformats.tiff.TiffRational):
        '''Sets the gamma.'''
        ...
    
    @property
    def iso_speed(self) -> int:
        ...
    
    @iso_speed.setter
    def iso_speed(self, value : int):
        ...
    
    @property
    def iso_speed_latitude_yyy(self) -> int:
        ...
    
    @iso_speed_latitude_yyy.setter
    def iso_speed_latitude_yyy(self, value : int):
        ...
    
    @property
    def iso_speed_latitude_zzz(self) -> int:
        ...
    
    @iso_speed_latitude_zzz.setter
    def iso_speed_latitude_zzz(self, value : int):
        ...
    
    @property
    def photographic_sensitivity(self) -> int:
        ...
    
    @photographic_sensitivity.setter
    def photographic_sensitivity(self, value : int):
        ...
    
    @property
    def image_unique_id(self) -> str:
        ...
    
    @image_unique_id.setter
    def image_unique_id(self, value : str):
        ...
    
    @property
    def lens_make(self) -> str:
        ...
    
    @lens_make.setter
    def lens_make(self, value : str):
        ...
    
    @property
    def lens_model(self) -> str:
        ...
    
    @lens_model.setter
    def lens_model(self, value : str):
        ...
    
    @property
    def lens_serial_number(self) -> str:
        ...
    
    @lens_serial_number.setter
    def lens_serial_number(self, value : str):
        ...
    
    @property
    def lens_specification(self) -> List[aspose.psd.fileformats.tiff.TiffRational]:
        ...
    
    @lens_specification.setter
    def lens_specification(self, value : List[aspose.psd.fileformats.tiff.TiffRational]):
        ...
    
    @property
    def light_source(self) -> aspose.psd.exif.enums.ExifLightSource:
        ...
    
    @light_source.setter
    def light_source(self, value : aspose.psd.exif.enums.ExifLightSource):
        ...
    
    @property
    def maker_note_data(self) -> List[aspose.psd.fileformats.tiff.TiffDataType]:
        ...
    
    @property
    def maker_note_raw_data(self) -> bytes:
        ...
    
    @maker_note_raw_data.setter
    def maker_note_raw_data(self, value : bytes):
        ...
    
    @property
    def max_aperture_value(self) -> aspose.psd.fileformats.tiff.TiffRational:
        ...
    
    @max_aperture_value.setter
    def max_aperture_value(self, value : aspose.psd.fileformats.tiff.TiffRational):
        ...
    
    @property
    def metering_mode(self) -> aspose.psd.exif.enums.ExifMeteringMode:
        ...
    
    @metering_mode.setter
    def metering_mode(self, value : aspose.psd.exif.enums.ExifMeteringMode):
        ...
    
    @property
    def oecf(self) -> bytes:
        '''Gets the Opto-Electric Conversion Function (OECF) specified in ISO 14524.'''
        ...
    
    @oecf.setter
    def oecf(self, value : bytes):
        '''Sets the Opto-Electric Conversion Function (OECF) specified in ISO 14524.'''
        ...
    
    @property
    def pixel_x_dimension(self) -> int:
        ...
    
    @pixel_x_dimension.setter
    def pixel_x_dimension(self, value : int):
        ...
    
    @property
    def pixel_y_dimension(self) -> int:
        ...
    
    @pixel_y_dimension.setter
    def pixel_y_dimension(self, value : int):
        ...
    
    @property
    def properties(self) -> List[aspose.psd.fileformats.tiff.TiffDataType]:
        '''Gets all the EXIF tags (including common and GPS tags).'''
        ...
    
    @properties.setter
    def properties(self, value : List[aspose.psd.fileformats.tiff.TiffDataType]):
        '''Sets all the EXIF tags (including common and GPS tags).'''
        ...
    
    @property
    def recommended_exposure_index(self) -> int:
        ...
    
    @recommended_exposure_index.setter
    def recommended_exposure_index(self, value : int):
        ...
    
    @property
    def related_sound_file(self) -> str:
        ...
    
    @related_sound_file.setter
    def related_sound_file(self, value : str):
        ...
    
    @property
    def saturation(self) -> aspose.psd.exif.enums.ExifSaturation:
        '''Gets the saturation.'''
        ...
    
    @saturation.setter
    def saturation(self, value : aspose.psd.exif.enums.ExifSaturation):
        '''Sets the saturation.'''
        ...
    
    @property
    def scene_capture_type(self) -> aspose.psd.exif.enums.ExifSceneCaptureType:
        ...
    
    @scene_capture_type.setter
    def scene_capture_type(self, value : aspose.psd.exif.enums.ExifSceneCaptureType):
        ...
    
    @property
    def scene_type(self) -> byte:
        ...
    
    @scene_type.setter
    def scene_type(self, value : byte):
        ...
    
    @property
    def sensing_method(self) -> aspose.psd.exif.enums.ExifSensingMethod:
        ...
    
    @sensing_method.setter
    def sensing_method(self, value : aspose.psd.exif.enums.ExifSensingMethod):
        ...
    
    @property
    def sensitivity_type(self) -> int:
        ...
    
    @sensitivity_type.setter
    def sensitivity_type(self, value : int):
        ...
    
    @property
    def sharpness(self) -> int:
        '''Gets the sharpness.'''
        ...
    
    @sharpness.setter
    def sharpness(self, value : int):
        '''Sets the sharpness.'''
        ...
    
    @property
    def shutter_speed_value(self) -> aspose.psd.fileformats.tiff.TiffSRational:
        ...
    
    @shutter_speed_value.setter
    def shutter_speed_value(self, value : aspose.psd.fileformats.tiff.TiffSRational):
        ...
    
    @property
    def spatial_frequency_response(self) -> bytes:
        ...
    
    @spatial_frequency_response.setter
    def spatial_frequency_response(self, value : bytes):
        ...
    
    @property
    def spectral_sensitivity(self) -> str:
        ...
    
    @spectral_sensitivity.setter
    def spectral_sensitivity(self, value : str):
        ...
    
    @property
    def standard_output_sensitivity(self) -> int:
        ...
    
    @standard_output_sensitivity.setter
    def standard_output_sensitivity(self, value : int):
        ...
    
    @property
    def subject_area(self) -> List[int]:
        ...
    
    @subject_area.setter
    def subject_area(self, value : List[int]):
        ...
    
    @property
    def subject_distance(self) -> aspose.psd.fileformats.tiff.TiffRational:
        ...
    
    @subject_distance.setter
    def subject_distance(self, value : aspose.psd.fileformats.tiff.TiffRational):
        ...
    
    @property
    def subject_distance_range(self) -> aspose.psd.exif.enums.ExifSubjectDistanceRange:
        ...
    
    @subject_distance_range.setter
    def subject_distance_range(self, value : aspose.psd.exif.enums.ExifSubjectDistanceRange):
        ...
    
    @property
    def subject_location(self) -> List[int]:
        ...
    
    @subject_location.setter
    def subject_location(self, value : List[int]):
        ...
    
    @property
    def subsec_time(self) -> str:
        ...
    
    @subsec_time.setter
    def subsec_time(self, value : str):
        ...
    
    @property
    def subsec_time_digitized(self) -> str:
        ...
    
    @subsec_time_digitized.setter
    def subsec_time_digitized(self, value : str):
        ...
    
    @property
    def subsec_time_original(self) -> str:
        ...
    
    @subsec_time_original.setter
    def subsec_time_original(self, value : str):
        ...
    
    @property
    def user_comment(self) -> str:
        ...
    
    @user_comment.setter
    def user_comment(self, value : str):
        ...
    
    @property
    def white_balance(self) -> aspose.psd.exif.enums.ExifWhiteBalance:
        ...
    
    @white_balance.setter
    def white_balance(self, value : aspose.psd.exif.enums.ExifWhiteBalance):
        ...
    
    @property
    def white_point(self) -> List[aspose.psd.fileformats.tiff.TiffRational]:
        ...
    
    @white_point.setter
    def white_point(self, value : List[aspose.psd.fileformats.tiff.TiffRational]):
        ...
    
    @property
    def common_tags(self) -> List[aspose.psd.fileformats.tiff.TiffDataType]:
        ...
    
    @common_tags.setter
    def common_tags(self, value : List[aspose.psd.fileformats.tiff.TiffDataType]):
        ...
    
    @property
    def exif_tags(self) -> List[aspose.psd.fileformats.tiff.TiffDataType]:
        ...
    
    @exif_tags.setter
    def exif_tags(self, value : List[aspose.psd.fileformats.tiff.TiffDataType]):
        ...
    
    @property
    def gps_tags(self) -> List[aspose.psd.fileformats.tiff.TiffDataType]:
        ...
    
    @gps_tags.setter
    def gps_tags(self, value : List[aspose.psd.fileformats.tiff.TiffDataType]):
        ...
    
    ...

class JpegExifData(ExifData):
    '''EXIF data container for jpeg files.'''
    
    @overload
    def __init__(self):
        '''Initializes a new instance of the  class.'''
        ...
    
    @overload
    def __init__(self, exifdata: List[aspose.psd.fileformats.tiff.TiffDataType]):
        '''Initializes a new instance of the  class with data from array.
        
        :param exifdata: Array of EXIF tags together with common and GPS tags.'''
        ...
    
    @overload
    def __init__(self, common_tags: List[aspose.psd.fileformats.tiff.TiffDataType], exif_tags: List[aspose.psd.fileformats.tiff.TiffDataType], gps_tags: List[aspose.psd.fileformats.tiff.TiffDataType]):
        '''Initializes a new instance of the  class with data from array.
        
        :param common_tags: The common tags.
        :param exif_tags: The EXIF tags.
        :param gps_tags: The GPS tags.'''
        ...
    
    @overload
    def remove_tag(self, tag: aspose.psd.exif.ExifProperties):
        '''Remove tag from container
        
        :param tag: The tag to remove'''
        ...
    
    @overload
    def remove_tag(self, tag_id: int):
        '''Remove tag from container
        
        :param tag_id: The tag identifier to remove.'''
        ...
    
    def serialize_exif_data(self) -> bytes:
        '''Serializes the EXIF data. Writes the tags values and contents. The most influencing size tag is Thumbnail tag contents.
        
        :returns: The serialized EXIF data.'''
        ...
    
    @property
    def is_big_endian(self) -> bool:
        ...
    
    @is_big_endian.setter
    def is_big_endian(self, value : bool):
        ...
    
    @property
    def aperture_value(self) -> aspose.psd.fileformats.tiff.TiffRational:
        ...
    
    @aperture_value.setter
    def aperture_value(self, value : aspose.psd.fileformats.tiff.TiffRational):
        ...
    
    @property
    def body_serial_number(self) -> str:
        ...
    
    @body_serial_number.setter
    def body_serial_number(self, value : str):
        ...
    
    @property
    def brightness_value(self) -> aspose.psd.fileformats.tiff.TiffSRational:
        ...
    
    @brightness_value.setter
    def brightness_value(self, value : aspose.psd.fileformats.tiff.TiffSRational):
        ...
    
    @property
    def cfa_pattern(self) -> bytes:
        ...
    
    @cfa_pattern.setter
    def cfa_pattern(self, value : bytes):
        ...
    
    @property
    def camera_owner_name(self) -> str:
        ...
    
    @camera_owner_name.setter
    def camera_owner_name(self, value : str):
        ...
    
    @property
    def color_space(self) -> aspose.psd.exif.enums.ExifColorSpace:
        ...
    
    @color_space.setter
    def color_space(self, value : aspose.psd.exif.enums.ExifColorSpace):
        ...
    
    @property
    def components_configuration(self) -> bytes:
        ...
    
    @components_configuration.setter
    def components_configuration(self, value : bytes):
        ...
    
    @property
    def compressed_bits_per_pixel(self) -> aspose.psd.fileformats.tiff.TiffRational:
        ...
    
    @compressed_bits_per_pixel.setter
    def compressed_bits_per_pixel(self, value : aspose.psd.fileformats.tiff.TiffRational):
        ...
    
    @property
    def contrast(self) -> aspose.psd.exif.enums.ExifContrast:
        '''Gets the contrast.'''
        ...
    
    @contrast.setter
    def contrast(self, value : aspose.psd.exif.enums.ExifContrast):
        '''Sets the contrast.'''
        ...
    
    @property
    def custom_rendered(self) -> aspose.psd.exif.enums.ExifCustomRendered:
        ...
    
    @custom_rendered.setter
    def custom_rendered(self, value : aspose.psd.exif.enums.ExifCustomRendered):
        ...
    
    @property
    def date_time_digitized(self) -> str:
        ...
    
    @date_time_digitized.setter
    def date_time_digitized(self, value : str):
        ...
    
    @property
    def date_time_original(self) -> str:
        ...
    
    @date_time_original.setter
    def date_time_original(self, value : str):
        ...
    
    @property
    def device_setting_description(self) -> bytes:
        ...
    
    @device_setting_description.setter
    def device_setting_description(self, value : bytes):
        ...
    
    @property
    def digital_zoom_ratio(self) -> aspose.psd.fileformats.tiff.TiffRational:
        ...
    
    @digital_zoom_ratio.setter
    def digital_zoom_ratio(self, value : aspose.psd.fileformats.tiff.TiffRational):
        ...
    
    @property
    def exif_version(self) -> bytes:
        ...
    
    @exif_version.setter
    def exif_version(self, value : bytes):
        ...
    
    @property
    def exposure_bias_value(self) -> aspose.psd.fileformats.tiff.TiffSRational:
        ...
    
    @exposure_bias_value.setter
    def exposure_bias_value(self, value : aspose.psd.fileformats.tiff.TiffSRational):
        ...
    
    @property
    def exposure_index(self) -> aspose.psd.fileformats.tiff.TiffRational:
        ...
    
    @exposure_index.setter
    def exposure_index(self, value : aspose.psd.fileformats.tiff.TiffRational):
        ...
    
    @property
    def exposure_mode(self) -> aspose.psd.exif.enums.ExifExposureMode:
        ...
    
    @exposure_mode.setter
    def exposure_mode(self, value : aspose.psd.exif.enums.ExifExposureMode):
        ...
    
    @property
    def exposure_program(self) -> aspose.psd.exif.enums.ExifExposureProgram:
        ...
    
    @exposure_program.setter
    def exposure_program(self, value : aspose.psd.exif.enums.ExifExposureProgram):
        ...
    
    @property
    def exposure_time(self) -> aspose.psd.fileformats.tiff.TiffRational:
        ...
    
    @exposure_time.setter
    def exposure_time(self, value : aspose.psd.fileformats.tiff.TiffRational):
        ...
    
    @property
    def f_number(self) -> aspose.psd.fileformats.tiff.TiffRational:
        ...
    
    @f_number.setter
    def f_number(self, value : aspose.psd.fileformats.tiff.TiffRational):
        ...
    
    @property
    def file_source(self) -> aspose.psd.exif.enums.ExifFileSource:
        ...
    
    @file_source.setter
    def file_source(self, value : aspose.psd.exif.enums.ExifFileSource):
        ...
    
    @property
    def flash(self) -> aspose.psd.exif.enums.ExifFlash:
        '''Gets the flash.'''
        ...
    
    @flash.setter
    def flash(self, value : aspose.psd.exif.enums.ExifFlash):
        '''Sets the flash.'''
        ...
    
    @property
    def flash_energy(self) -> aspose.psd.fileformats.tiff.TiffRational:
        ...
    
    @flash_energy.setter
    def flash_energy(self, value : aspose.psd.fileformats.tiff.TiffRational):
        ...
    
    @property
    def flashpix_version(self) -> bytes:
        ...
    
    @flashpix_version.setter
    def flashpix_version(self, value : bytes):
        ...
    
    @property
    def focal_length(self) -> aspose.psd.fileformats.tiff.TiffRational:
        ...
    
    @focal_length.setter
    def focal_length(self, value : aspose.psd.fileformats.tiff.TiffRational):
        ...
    
    @property
    def focal_length_in_35_mm_film(self) -> int:
        ...
    
    @focal_length_in_35_mm_film.setter
    def focal_length_in_35_mm_film(self, value : int):
        ...
    
    @property
    def focal_plane_resolution_unit(self) -> aspose.psd.exif.enums.ExifUnit:
        ...
    
    @focal_plane_resolution_unit.setter
    def focal_plane_resolution_unit(self, value : aspose.psd.exif.enums.ExifUnit):
        ...
    
    @property
    def focal_plane_x_resolution(self) -> aspose.psd.fileformats.tiff.TiffRational:
        ...
    
    @focal_plane_x_resolution.setter
    def focal_plane_x_resolution(self, value : aspose.psd.fileformats.tiff.TiffRational):
        ...
    
    @property
    def focal_plane_y_resolution(self) -> aspose.psd.fileformats.tiff.TiffRational:
        ...
    
    @focal_plane_y_resolution.setter
    def focal_plane_y_resolution(self, value : aspose.psd.fileformats.tiff.TiffRational):
        ...
    
    @property
    def gps_altitude(self) -> aspose.psd.fileformats.tiff.TiffRational:
        ...
    
    @gps_altitude.setter
    def gps_altitude(self, value : aspose.psd.fileformats.tiff.TiffRational):
        ...
    
    @property
    def gps_altitude_ref(self) -> aspose.psd.exif.enums.ExifGPSAltitudeRef:
        ...
    
    @gps_altitude_ref.setter
    def gps_altitude_ref(self, value : aspose.psd.exif.enums.ExifGPSAltitudeRef):
        ...
    
    @property
    def gps_area_information(self) -> bytes:
        ...
    
    @gps_area_information.setter
    def gps_area_information(self, value : bytes):
        ...
    
    @property
    def gpsdop(self) -> aspose.psd.fileformats.tiff.TiffRational:
        '''Gets the GPS DOP (data degree of precision).'''
        ...
    
    @gpsdop.setter
    def gpsdop(self, value : aspose.psd.fileformats.tiff.TiffRational):
        '''Sets the GPS DOP (data degree of precision).'''
        ...
    
    @property
    def gps_dest_bearing(self) -> aspose.psd.fileformats.tiff.TiffRational:
        ...
    
    @gps_dest_bearing.setter
    def gps_dest_bearing(self, value : aspose.psd.fileformats.tiff.TiffRational):
        ...
    
    @property
    def gps_dest_bearing_ref(self) -> str:
        ...
    
    @gps_dest_bearing_ref.setter
    def gps_dest_bearing_ref(self, value : str):
        ...
    
    @property
    def gps_dest_distance(self) -> aspose.psd.fileformats.tiff.TiffRational:
        ...
    
    @gps_dest_distance.setter
    def gps_dest_distance(self, value : aspose.psd.fileformats.tiff.TiffRational):
        ...
    
    @property
    def gps_dest_distance_ref(self) -> str:
        ...
    
    @gps_dest_distance_ref.setter
    def gps_dest_distance_ref(self, value : str):
        ...
    
    @property
    def gps_dest_latitude(self) -> List[aspose.psd.fileformats.tiff.TiffRational]:
        ...
    
    @gps_dest_latitude.setter
    def gps_dest_latitude(self, value : List[aspose.psd.fileformats.tiff.TiffRational]):
        ...
    
    @property
    def gps_dest_latitude_ref(self) -> str:
        ...
    
    @gps_dest_latitude_ref.setter
    def gps_dest_latitude_ref(self, value : str):
        ...
    
    @property
    def gps_dest_longitude(self) -> List[aspose.psd.fileformats.tiff.TiffRational]:
        ...
    
    @gps_dest_longitude.setter
    def gps_dest_longitude(self, value : List[aspose.psd.fileformats.tiff.TiffRational]):
        ...
    
    @property
    def gps_dest_longitude_ref(self) -> str:
        ...
    
    @gps_dest_longitude_ref.setter
    def gps_dest_longitude_ref(self, value : str):
        ...
    
    @property
    def gps_differential(self) -> int:
        ...
    
    @gps_differential.setter
    def gps_differential(self, value : int):
        ...
    
    @property
    def gps_img_direction(self) -> aspose.psd.fileformats.tiff.TiffRational:
        ...
    
    @gps_img_direction.setter
    def gps_img_direction(self, value : aspose.psd.fileformats.tiff.TiffRational):
        ...
    
    @property
    def gps_img_direction_ref(self) -> str:
        ...
    
    @gps_img_direction_ref.setter
    def gps_img_direction_ref(self, value : str):
        ...
    
    @property
    def gps_date_stamp(self) -> str:
        ...
    
    @gps_date_stamp.setter
    def gps_date_stamp(self, value : str):
        ...
    
    @property
    def gps_latitude(self) -> List[aspose.psd.fileformats.tiff.TiffRational]:
        ...
    
    @gps_latitude.setter
    def gps_latitude(self, value : List[aspose.psd.fileformats.tiff.TiffRational]):
        ...
    
    @property
    def gps_latitude_ref(self) -> str:
        ...
    
    @gps_latitude_ref.setter
    def gps_latitude_ref(self, value : str):
        ...
    
    @property
    def gps_longitude(self) -> List[aspose.psd.fileformats.tiff.TiffRational]:
        ...
    
    @gps_longitude.setter
    def gps_longitude(self, value : List[aspose.psd.fileformats.tiff.TiffRational]):
        ...
    
    @property
    def gps_longitude_ref(self) -> str:
        ...
    
    @gps_longitude_ref.setter
    def gps_longitude_ref(self, value : str):
        ...
    
    @property
    def gps_map_datum(self) -> str:
        ...
    
    @gps_map_datum.setter
    def gps_map_datum(self, value : str):
        ...
    
    @property
    def gps_measure_mode(self) -> str:
        ...
    
    @gps_measure_mode.setter
    def gps_measure_mode(self, value : str):
        ...
    
    @property
    def gps_processing_method(self) -> bytes:
        ...
    
    @gps_processing_method.setter
    def gps_processing_method(self, value : bytes):
        ...
    
    @property
    def gps_satellites(self) -> str:
        ...
    
    @gps_satellites.setter
    def gps_satellites(self, value : str):
        ...
    
    @property
    def gps_speed(self) -> aspose.psd.fileformats.tiff.TiffRational:
        ...
    
    @gps_speed.setter
    def gps_speed(self, value : aspose.psd.fileformats.tiff.TiffRational):
        ...
    
    @property
    def gps_speed_ref(self) -> str:
        ...
    
    @gps_speed_ref.setter
    def gps_speed_ref(self, value : str):
        ...
    
    @property
    def gps_status(self) -> str:
        ...
    
    @gps_status.setter
    def gps_status(self, value : str):
        ...
    
    @property
    def gps_timestamp(self) -> List[aspose.psd.fileformats.tiff.TiffRational]:
        ...
    
    @gps_timestamp.setter
    def gps_timestamp(self, value : List[aspose.psd.fileformats.tiff.TiffRational]):
        ...
    
    @property
    def gps_track(self) -> str:
        ...
    
    @gps_track.setter
    def gps_track(self, value : str):
        ...
    
    @property
    def gps_track_ref(self) -> str:
        ...
    
    @gps_track_ref.setter
    def gps_track_ref(self, value : str):
        ...
    
    @property
    def gps_version_id(self) -> bytes:
        ...
    
    @gps_version_id.setter
    def gps_version_id(self, value : bytes):
        ...
    
    @property
    def gain_control(self) -> aspose.psd.exif.enums.ExifGainControl:
        ...
    
    @gain_control.setter
    def gain_control(self, value : aspose.psd.exif.enums.ExifGainControl):
        ...
    
    @property
    def gamma(self) -> aspose.psd.fileformats.tiff.TiffRational:
        '''Gets the gamma.'''
        ...
    
    @gamma.setter
    def gamma(self, value : aspose.psd.fileformats.tiff.TiffRational):
        '''Sets the gamma.'''
        ...
    
    @property
    def iso_speed(self) -> int:
        ...
    
    @iso_speed.setter
    def iso_speed(self, value : int):
        ...
    
    @property
    def iso_speed_latitude_yyy(self) -> int:
        ...
    
    @iso_speed_latitude_yyy.setter
    def iso_speed_latitude_yyy(self, value : int):
        ...
    
    @property
    def iso_speed_latitude_zzz(self) -> int:
        ...
    
    @iso_speed_latitude_zzz.setter
    def iso_speed_latitude_zzz(self, value : int):
        ...
    
    @property
    def photographic_sensitivity(self) -> int:
        ...
    
    @photographic_sensitivity.setter
    def photographic_sensitivity(self, value : int):
        ...
    
    @property
    def image_unique_id(self) -> str:
        ...
    
    @image_unique_id.setter
    def image_unique_id(self, value : str):
        ...
    
    @property
    def lens_make(self) -> str:
        ...
    
    @lens_make.setter
    def lens_make(self, value : str):
        ...
    
    @property
    def lens_model(self) -> str:
        ...
    
    @lens_model.setter
    def lens_model(self, value : str):
        ...
    
    @property
    def lens_serial_number(self) -> str:
        ...
    
    @lens_serial_number.setter
    def lens_serial_number(self, value : str):
        ...
    
    @property
    def lens_specification(self) -> List[aspose.psd.fileformats.tiff.TiffRational]:
        ...
    
    @lens_specification.setter
    def lens_specification(self, value : List[aspose.psd.fileformats.tiff.TiffRational]):
        ...
    
    @property
    def light_source(self) -> aspose.psd.exif.enums.ExifLightSource:
        ...
    
    @light_source.setter
    def light_source(self, value : aspose.psd.exif.enums.ExifLightSource):
        ...
    
    @property
    def maker_note_data(self) -> List[aspose.psd.fileformats.tiff.TiffDataType]:
        ...
    
    @property
    def maker_note_raw_data(self) -> bytes:
        ...
    
    @maker_note_raw_data.setter
    def maker_note_raw_data(self, value : bytes):
        ...
    
    @property
    def max_aperture_value(self) -> aspose.psd.fileformats.tiff.TiffRational:
        ...
    
    @max_aperture_value.setter
    def max_aperture_value(self, value : aspose.psd.fileformats.tiff.TiffRational):
        ...
    
    @property
    def metering_mode(self) -> aspose.psd.exif.enums.ExifMeteringMode:
        ...
    
    @metering_mode.setter
    def metering_mode(self, value : aspose.psd.exif.enums.ExifMeteringMode):
        ...
    
    @property
    def oecf(self) -> bytes:
        '''Gets the Opto-Electric Conversion Function (OECF) specified in ISO 14524.'''
        ...
    
    @oecf.setter
    def oecf(self, value : bytes):
        '''Sets the Opto-Electric Conversion Function (OECF) specified in ISO 14524.'''
        ...
    
    @property
    def pixel_x_dimension(self) -> int:
        ...
    
    @pixel_x_dimension.setter
    def pixel_x_dimension(self, value : int):
        ...
    
    @property
    def pixel_y_dimension(self) -> int:
        ...
    
    @pixel_y_dimension.setter
    def pixel_y_dimension(self, value : int):
        ...
    
    @property
    def properties(self) -> List[aspose.psd.fileformats.tiff.TiffDataType]:
        '''Gets all the EXIF tags (including common and GPS tags).'''
        ...
    
    @properties.setter
    def properties(self, value : List[aspose.psd.fileformats.tiff.TiffDataType]):
        '''Sets all the EXIF tags (including common and GPS tags).'''
        ...
    
    @property
    def recommended_exposure_index(self) -> int:
        ...
    
    @recommended_exposure_index.setter
    def recommended_exposure_index(self, value : int):
        ...
    
    @property
    def related_sound_file(self) -> str:
        ...
    
    @related_sound_file.setter
    def related_sound_file(self, value : str):
        ...
    
    @property
    def saturation(self) -> aspose.psd.exif.enums.ExifSaturation:
        '''Gets the saturation.'''
        ...
    
    @saturation.setter
    def saturation(self, value : aspose.psd.exif.enums.ExifSaturation):
        '''Sets the saturation.'''
        ...
    
    @property
    def scene_capture_type(self) -> aspose.psd.exif.enums.ExifSceneCaptureType:
        ...
    
    @scene_capture_type.setter
    def scene_capture_type(self, value : aspose.psd.exif.enums.ExifSceneCaptureType):
        ...
    
    @property
    def scene_type(self) -> byte:
        ...
    
    @scene_type.setter
    def scene_type(self, value : byte):
        ...
    
    @property
    def sensing_method(self) -> aspose.psd.exif.enums.ExifSensingMethod:
        ...
    
    @sensing_method.setter
    def sensing_method(self, value : aspose.psd.exif.enums.ExifSensingMethod):
        ...
    
    @property
    def sensitivity_type(self) -> int:
        ...
    
    @sensitivity_type.setter
    def sensitivity_type(self, value : int):
        ...
    
    @property
    def sharpness(self) -> int:
        '''Gets the sharpness.'''
        ...
    
    @sharpness.setter
    def sharpness(self, value : int):
        '''Sets the sharpness.'''
        ...
    
    @property
    def shutter_speed_value(self) -> aspose.psd.fileformats.tiff.TiffSRational:
        ...
    
    @shutter_speed_value.setter
    def shutter_speed_value(self, value : aspose.psd.fileformats.tiff.TiffSRational):
        ...
    
    @property
    def spatial_frequency_response(self) -> bytes:
        ...
    
    @spatial_frequency_response.setter
    def spatial_frequency_response(self, value : bytes):
        ...
    
    @property
    def spectral_sensitivity(self) -> str:
        ...
    
    @spectral_sensitivity.setter
    def spectral_sensitivity(self, value : str):
        ...
    
    @property
    def standard_output_sensitivity(self) -> int:
        ...
    
    @standard_output_sensitivity.setter
    def standard_output_sensitivity(self, value : int):
        ...
    
    @property
    def subject_area(self) -> List[int]:
        ...
    
    @subject_area.setter
    def subject_area(self, value : List[int]):
        ...
    
    @property
    def subject_distance(self) -> aspose.psd.fileformats.tiff.TiffRational:
        ...
    
    @subject_distance.setter
    def subject_distance(self, value : aspose.psd.fileformats.tiff.TiffRational):
        ...
    
    @property
    def subject_distance_range(self) -> aspose.psd.exif.enums.ExifSubjectDistanceRange:
        ...
    
    @subject_distance_range.setter
    def subject_distance_range(self, value : aspose.psd.exif.enums.ExifSubjectDistanceRange):
        ...
    
    @property
    def subject_location(self) -> List[int]:
        ...
    
    @subject_location.setter
    def subject_location(self, value : List[int]):
        ...
    
    @property
    def subsec_time(self) -> str:
        ...
    
    @subsec_time.setter
    def subsec_time(self, value : str):
        ...
    
    @property
    def subsec_time_digitized(self) -> str:
        ...
    
    @subsec_time_digitized.setter
    def subsec_time_digitized(self, value : str):
        ...
    
    @property
    def subsec_time_original(self) -> str:
        ...
    
    @subsec_time_original.setter
    def subsec_time_original(self, value : str):
        ...
    
    @property
    def user_comment(self) -> str:
        ...
    
    @user_comment.setter
    def user_comment(self, value : str):
        ...
    
    @property
    def white_balance(self) -> aspose.psd.exif.enums.ExifWhiteBalance:
        ...
    
    @white_balance.setter
    def white_balance(self, value : aspose.psd.exif.enums.ExifWhiteBalance):
        ...
    
    @property
    def white_point(self) -> List[aspose.psd.fileformats.tiff.TiffRational]:
        ...
    
    @white_point.setter
    def white_point(self, value : List[aspose.psd.fileformats.tiff.TiffRational]):
        ...
    
    @property
    def common_tags(self) -> List[aspose.psd.fileformats.tiff.TiffDataType]:
        ...
    
    @common_tags.setter
    def common_tags(self, value : List[aspose.psd.fileformats.tiff.TiffDataType]):
        ...
    
    @property
    def exif_tags(self) -> List[aspose.psd.fileformats.tiff.TiffDataType]:
        ...
    
    @exif_tags.setter
    def exif_tags(self, value : List[aspose.psd.fileformats.tiff.TiffDataType]):
        ...
    
    @property
    def gps_tags(self) -> List[aspose.psd.fileformats.tiff.TiffDataType]:
        ...
    
    @gps_tags.setter
    def gps_tags(self, value : List[aspose.psd.fileformats.tiff.TiffDataType]):
        ...
    
    @property
    def artist(self) -> str:
        '''Gets the artist.'''
        ...
    
    @artist.setter
    def artist(self, value : str):
        '''Sets the artist.'''
        ...
    
    @property
    def bits_per_sample(self) -> List[int]:
        ...
    
    @bits_per_sample.setter
    def bits_per_sample(self, value : List[int]):
        ...
    
    @property
    def compression(self) -> int:
        '''Gets the compression.'''
        ...
    
    @compression.setter
    def compression(self, value : int):
        '''Sets the compression.'''
        ...
    
    @property
    def copyright(self) -> str:
        '''Gets the copyright.'''
        ...
    
    @copyright.setter
    def copyright(self, value : str):
        '''Sets the copyright.'''
        ...
    
    @property
    def date_time(self) -> str:
        ...
    
    @date_time.setter
    def date_time(self, value : str):
        ...
    
    @property
    def image_description(self) -> str:
        ...
    
    @image_description.setter
    def image_description(self, value : str):
        ...
    
    @property
    def image_length(self) -> int:
        ...
    
    @image_length.setter
    def image_length(self, value : int):
        ...
    
    @property
    def image_width(self) -> int:
        ...
    
    @image_width.setter
    def image_width(self, value : int):
        ...
    
    @property
    def make(self) -> str:
        '''Gets the manufacturer of the recording equipment.'''
        ...
    
    @make.setter
    def make(self, value : str):
        '''Sets the manufacturer of the recording equipment.'''
        ...
    
    @property
    def model(self) -> str:
        '''Gets the model.'''
        ...
    
    @model.setter
    def model(self, value : str):
        '''Sets the model.'''
        ...
    
    @property
    def orientation(self) -> aspose.psd.exif.enums.ExifOrientation:
        '''Gets the orientation.'''
        ...
    
    @orientation.setter
    def orientation(self, value : aspose.psd.exif.enums.ExifOrientation):
        '''Sets the orientation.'''
        ...
    
    @property
    def photometric_interpretation(self) -> int:
        ...
    
    @photometric_interpretation.setter
    def photometric_interpretation(self, value : int):
        ...
    
    @property
    def planar_configuration(self) -> int:
        ...
    
    @planar_configuration.setter
    def planar_configuration(self, value : int):
        ...
    
    @property
    def primary_chromaticities(self) -> List[aspose.psd.fileformats.tiff.TiffRational]:
        ...
    
    @primary_chromaticities.setter
    def primary_chromaticities(self, value : List[aspose.psd.fileformats.tiff.TiffRational]):
        ...
    
    @property
    def reference_black_white(self) -> List[aspose.psd.fileformats.tiff.TiffRational]:
        ...
    
    @reference_black_white.setter
    def reference_black_white(self, value : List[aspose.psd.fileformats.tiff.TiffRational]):
        ...
    
    @property
    def resolution_unit(self) -> aspose.psd.exif.enums.ExifUnit:
        ...
    
    @resolution_unit.setter
    def resolution_unit(self, value : aspose.psd.exif.enums.ExifUnit):
        ...
    
    @property
    def samples_per_pixel(self) -> int:
        ...
    
    @samples_per_pixel.setter
    def samples_per_pixel(self, value : int):
        ...
    
    @property
    def software(self) -> str:
        '''Gets the software.'''
        ...
    
    @software.setter
    def software(self, value : str):
        '''Sets the software.'''
        ...
    
    @property
    def thumbnail(self) -> aspose.psd.RasterImage:
        '''Gets the thumbnail image.'''
        ...
    
    @thumbnail.setter
    def thumbnail(self, value : aspose.psd.RasterImage):
        '''Sets the thumbnail image.'''
        ...
    
    @property
    def transfer_function(self) -> List[int]:
        ...
    
    @transfer_function.setter
    def transfer_function(self, value : List[int]):
        ...
    
    @property
    def x_resolution(self) -> aspose.psd.fileformats.tiff.TiffRational:
        ...
    
    @x_resolution.setter
    def x_resolution(self, value : aspose.psd.fileformats.tiff.TiffRational):
        ...
    
    @property
    def y_cb_cr_coefficients(self) -> List[aspose.psd.fileformats.tiff.TiffRational]:
        ...
    
    @y_cb_cr_coefficients.setter
    def y_cb_cr_coefficients(self, value : List[aspose.psd.fileformats.tiff.TiffRational]):
        ...
    
    @property
    def y_cb_cr_positioning(self) -> aspose.psd.exif.enums.ExifYCbCrPositioning:
        ...
    
    @y_cb_cr_positioning.setter
    def y_cb_cr_positioning(self, value : aspose.psd.exif.enums.ExifYCbCrPositioning):
        ...
    
    @property
    def y_cb_cr_sub_sampling(self) -> List[int]:
        ...
    
    @y_cb_cr_sub_sampling.setter
    def y_cb_cr_sub_sampling(self, value : List[int]):
        ...
    
    @property
    def y_resolution(self) -> aspose.psd.fileformats.tiff.TiffRational:
        ...
    
    @y_resolution.setter
    def y_resolution(self, value : aspose.psd.fileformats.tiff.TiffRational):
        ...
    
    @classmethod
    @property
    def MAX_EXIF_SEGMENT_SIZE(cls) -> int:
        ...
    
    ...

class TiffDataTypeController:
    '''Represents general class for working with tiff data types.'''
    
    def __init__(self):
        ...
    
    ...

class ExifProperties(enum.Enum):
    IMAGE_WIDTH = enum.auto()
    '''The number of columns of image data, equal to the number of pixels per row.'''
    IMAGE_LENGTH = enum.auto()
    '''The number of rows of image data.'''
    BITS_PER_SAMPLE = enum.auto()
    '''The number of bits per image component. In this standard each component of the image is 8 bits, so the value for this tag is 8.'''
    COMPRESSION = enum.auto()
    '''The compression scheme used for the image data. When a primary image is JPEG compressed, this designation is not necessary and is omitted.'''
    PHOTOMETRIC_INTERPRETATION = enum.auto()
    '''The pixel composition.'''
    IMAGE_DESCRIPTION = enum.auto()
    '''A character string giving the title of the image. It may be a comment such as "1988 company picnic" or the like.'''
    MAKE = enum.auto()
    '''The manufacturer of the recording equipment. This is the manufacturer of the DSC, scanner, video digitizer or other equipment that generated the image. When the field is left blank, it is treated as unknown.'''
    MODEL = enum.auto()
    '''The model name or model number of the equipment. This is the model name or number of the DSC, scanner, video digitizer or other equipment that generated the image. When the field is left blank, it is treated as unknown.'''
    ORIENTATION = enum.auto()
    '''The image orientation viewed in terms of rows and columns.'''
    SAMPLES_PER_PIXEL = enum.auto()
    '''The number of components per pixel. Since this standard applies to RGB and YCbCr images, the value set for this tag is 3.'''
    X_RESOLUTION = enum.auto()
    '''The number of pixels per ResolutionUnit in the ImageWidth direction. When the image resolution is unknown, 72 [dpi] is designated.'''
    Y_RESOLUTION = enum.auto()
    '''The number of pixels per ResolutionUnit in the ImageLength direction. The same value as XResolution is designated.'''
    PLANAR_CONFIGURATION = enum.auto()
    '''Indicates whether pixel components are recorded in a chunky or planar format. If this field does not exist, the TIFF default of 1 (chunky) is assumed.'''
    RESOLUTION_UNIT = enum.auto()
    '''The unit for measuring XResolution and YResolution. The same unit is used for both XResolution and YResolution. If the image resolution is unknown, 2 (inches) is designated.'''
    TRANSFER_FUNCTION = enum.auto()
    '''A transfer function for the image, described in tabular style. Normally this tag is not necessary, since color space is specified in the color space information ColorSpace tag.'''
    SOFTWARE = enum.auto()
    '''This tag records the name and version of the software or firmware of the camera or image input device used to generate the image. The detailed format is not specified, but it is recommended that the example shown below be followed. When the field is left blank, it is treated as unknown.'''
    DATE_TIME = enum.auto()
    '''The date and time of image creation. In Exif standard, it is the date and time the file was changed.'''
    ARTIST = enum.auto()
    '''This tag records the name of the camera owner, photographer or image creator. The detailed format is not specified, but it is recommended that the information be written as in the example below for ease of Interoperability. When the field is left blank, it is treated as unknown. Ex.) "Camera owner, John Smith; Photographer, Michael Brown; Image creator, Ken James"'''
    WHITE_POINT = enum.auto()
    '''The chromaticity of the white point of the image. Normally this tag is not necessary, since color space is specified in the colorspace information ColorSpace tag.'''
    PRIMARY_CHROMATICITIES = enum.auto()
    '''The chromaticity of the three primary colors of the image. Normally this tag is not necessary, since colorspace is specified in the colorspace information ColorSpace tag.'''
    Y_CB_CR_COEFFICIENTS = enum.auto()
    '''The matrix coefficients for transformation from RGB to YCbCr image data.'''
    Y_CB_CR_SUB_SAMPLING = enum.auto()
    '''The sampling ratio of chrominance components in relation to the luminance component.'''
    Y_CB_CR_POSITIONING = enum.auto()
    '''The position of chrominance components in relation to the
    luminance component. This field is designated only for
    JPEG compressed data or uncompressed YCbCr data. The TIFF
    default is 1 (centered); but when Y:Cb:Cr = 4:2:2 it is
    recommended in this standard that 2 (co-sited) be used to
    record data, in order to improve the image quality when viewed
    on TV systems. When this field does not exist, the reader shall
    assume the TIFF default. In the case of Y:Cb:Cr = 4:2:0, the
    TIFF default (centered) is recommended. If the reader
    does not have the capability of supporting both kinds of
    YCbCrPositioning, it shall follow the TIFF default regardless
    of the value in this field. It is preferable that readers "
    be able to support both centered and co-sited positioning.'''
    REFERENCE_BLACK_WHITE = enum.auto()
    '''The reference black point value and reference white point
    value. No defaults are given in TIFF, but the values below are given as defaults here.
    The color space is declared
    in a color space information tag, with the default
    being the value that gives the optimal image characteristics
    Interoperability these conditions'''
    COPYRIGHT = enum.auto()
    '''Copyright information. In this standard the tag is used to
    indicate both the photographer and editor copyrights. It is
    the copyright notice of the person or organization claiming
    rights to the image. The Interoperability copyright
    statement including date and rights should be written in this
    field; e.g., "Copyright, John Smith, 19xx. All rights
    reserved.". In this standard the field records both the
    photographer and editor copyrights, with each recorded in a
    separate part of the statement. When there is a clear distinction
    between the photographer and editor copyrights, these are to be
    written in the order of photographer followed by editor copyright,
    separated by NULL (in this case since the statement also ends with
    a NULL, there are two NULL codes). When only the photographer
    copyright is given, it is terminated by one NULL code . When only
    the editor copyright is given, the photographer copyright part
    consists of one space followed by a terminating NULL code, then
    the editor copyright is given. When the field is left blank, it is
    treated as unknown.'''
    EXPOSURE_TIME = enum.auto()
    '''Exposure time, given in seconds.'''
    F_NUMBER = enum.auto()
    '''The F number.'''
    EXPOSURE_PROGRAM = enum.auto()
    '''The class of the program used by the camera to set exposure when the picture is taken.'''
    SPECTRAL_SENSITIVITY = enum.auto()
    '''Indicates the spectral sensitivity of each channel of the camera used.'''
    PHOTOGRAPHIC_SENSITIVITY = enum.auto()
    '''Indicates the ISO Speed and ISO Latitude of the camera or input device as specified in ISO 12232.'''
    OECF = enum.auto()
    '''Indicates the Opto-Electric Conversion Function (OECF) specified in ISO 14524.'''
    EXIF_VERSION = enum.auto()
    '''The exif version.'''
    DATE_TIME_ORIGINAL = enum.auto()
    '''The date and time when the original image data was generated.'''
    DATE_TIME_DIGITIZED = enum.auto()
    '''The date time digitized.'''
    COMPONENTS_CONFIGURATION = enum.auto()
    '''The components configuration.'''
    COMPRESSED_BITS_PER_PIXEL = enum.auto()
    '''Specific to compressed data; states the compressed bits per pixel.'''
    SHUTTER_SPEED_VALUE = enum.auto()
    '''The shutter speed value.'''
    APERTURE_VALUE = enum.auto()
    '''The lens aperture value.'''
    BRIGHTNESS_VALUE = enum.auto()
    '''The brightness value.'''
    EXPOSURE_BIAS_VALUE = enum.auto()
    '''The exposure bias value.'''
    MAX_APERTURE_VALUE = enum.auto()
    '''The max aperture value.'''
    SUBJECT_DISTANCE = enum.auto()
    '''The distance to the subject, given in meters.'''
    METERING_MODE = enum.auto()
    '''The metering mode.'''
    LIGHT_SOURCE = enum.auto()
    '''The kind light source.'''
    FLASH = enum.auto()
    '''Indicates the status of flash when the image was shot.'''
    FOCAL_LENGTH = enum.auto()
    '''The actual focal length of the lens, in mm.'''
    SUBJECT_AREA = enum.auto()
    '''This tag indicates the location and area of the main subject in the overall scene.'''
    MAKER_NOTE = enum.auto()
    '''A tag for manufacturers of Exif writers to record any desired information. The contents are up to the manufacturer, but this tag should not be used for any other than its intended purpose.'''
    USER_COMMENT = enum.auto()
    '''A tag for Exif users to write keywords or comments on the image besides those in ImageDescription, and without the character code limitations of the ImageDescription tag.'''
    SUBSEC_TIME = enum.auto()
    '''A tag used to record fractions of seconds for the DateTime tag.'''
    SUBSEC_TIME_ORIGINAL = enum.auto()
    '''A tag used to record fractions of seconds for the DateTimeOriginal tag.'''
    SUBSEC_TIME_DIGITIZED = enum.auto()
    '''A tag used to record fractions of seconds for the DateTimeDigitized tag.'''
    FLASHPIX_VERSION = enum.auto()
    '''The Flashpix format version supported by a FPXR file.'''
    COLOR_SPACE = enum.auto()
    '''The color space information tag (ColorSpace) is always recorded as the color space specifier.'''
    RELATED_SOUND_FILE = enum.auto()
    '''The related sound file.'''
    FLASH_ENERGY = enum.auto()
    '''Indicates the strobe energy at the time the image is captured, as measured in Beam Candle Power Seconds(BCPS).'''
    SPATIAL_FREQUENCY_RESPONSE = enum.auto()
    '''This tag records the camera or input device spatial frequency table and SFR values in the direction of image width, image height, and diagonal direction, as specified in ISO 12233.'''
    FOCAL_PLANE_X_RESOLUTION = enum.auto()
    '''Indicates the number of pixels in the image width (X) direction per FocalPlaneResolutionUnit on the camera focal plane.'''
    FOCAL_PLANE_Y_RESOLUTION = enum.auto()
    '''Indicates the number of pixels in the image height (Y) direction per FocalPlaneResolutionUnit on the camera focal plane.'''
    FOCAL_PLANE_RESOLUTION_UNIT = enum.auto()
    '''Indicates the unit for measuring FocalPlaneXResolution and FocalPlaneYResolution. This value is the same as the ResolutionUnit.'''
    SUBJECT_LOCATION = enum.auto()
    '''Indicates the location of the main subject in the scene. The value of this tag represents the pixel at the center of the main subject relative to the left edge, prior to rotation processing as per the Rotation tag.'''
    EXPOSURE_INDEX = enum.auto()
    '''Indicates the exposure index selected on the camera or input device at the time the image is captured.'''
    SENSING_METHOD = enum.auto()
    '''Indicates the image sensor type on the camera or input device.'''
    FILE_SOURCE = enum.auto()
    '''The file source.'''
    SCENE_TYPE = enum.auto()
    '''Indicates the type of scene. If a DSC recorded the image, this tag value shall always be set to 1, indicating that the image was directly photographed.'''
    CFA_PATTERN = enum.auto()
    '''Indicates the color filter array (CFA) geometric pattern of the image sensor when a one-chip color area sensor is used. It does not apply to all sensing methods.'''
    CUSTOM_RENDERED = enum.auto()
    '''This tag indicates the use of special processing on image data, such as rendering geared to output. When special processing is performed, the reader is expected to disable or minimize any further processing.'''
    EXPOSURE_MODE = enum.auto()
    '''This tag indicates the exposure mode set when the image was shot. In auto-bracketing mode, the camera shoots a series of frames of the same scene at different exposure settings.'''
    WHITE_BALANCE = enum.auto()
    '''This tag indicates the white balance mode set when the image was shot.'''
    DIGITAL_ZOOM_RATIO = enum.auto()
    '''This tag indicates the digital zoom ratio when the image was shot. If the numerator of the recorded value is 0, this indicates that digital zoom was not used.'''
    FOCAL_LENGTH_IN_35_MM_FILM = enum.auto()
    '''This tag indicates the equivalent focal length assuming a 35mm film camera, in mm. A value of 0 means the focal length is unknown. Note that this tag differs from the FocalLength tag.'''
    SCENE_CAPTURE_TYPE = enum.auto()
    '''This tag indicates the type of scene that was shot. It can also be used to record the mode in which the image was shot.'''
    GAIN_CONTROL = enum.auto()
    '''This tag indicates the degree of overall image gain adjustment.'''
    CONTRAST = enum.auto()
    '''This tag indicates the direction of contrast processing applied by the camera when the image was shot.'''
    SATURATION = enum.auto()
    '''This tag indicates the direction of saturation processing applied by the camera when the image was shot.'''
    SHARPNESS = enum.auto()
    '''This tag indicates the direction of sharpness processing applied by the camera when the image was shot'''
    DEVICE_SETTING_DESCRIPTION = enum.auto()
    '''This tag indicates information on the picture-taking conditions of a particular camera model. The tag is used only to indicate the picture-taking conditions in the reader.'''
    SUBJECT_DISTANCE_RANGE = enum.auto()
    '''This tag indicates the distance to the subject.'''
    IMAGE_UNIQUE_ID = enum.auto()
    '''The image unique id.'''
    GPS_VERSION_ID = enum.auto()
    '''Indicates the version of GPSInfoIFD.'''
    GPS_LATITUDE_REF = enum.auto()
    '''Indicates whether the latitude is north or south latitude.'''
    GPS_LATITUDE = enum.auto()
    '''Indicates the latitude. The latitude is expressed as three RATIONAL values giving the degrees, minutes, and
    seconds, respectively. If latitude is expressed as degrees, minutes and seconds, a typical format would be
    dd/1,mm/1,ss/1. When degrees and minutes are used and, for example, fractions of minutes are given up to two
    decimal places, the format would be dd/1,mmmm/100,0/1.'''
    GPS_LONGITUDE_REF = enum.auto()
    '''Indicates whether the longitude is east or west longitude.'''
    GPS_LONGITUDE = enum.auto()
    '''Indicates the longitude. The longitude is expressed as three RATIONAL values giving the degrees, minutes, and
    seconds, respectively. If longitude is expressed as degrees, minutes and seconds, a typical format would be
    ddd/1,mm/1,ss/1. When degrees and minutes are used and, for example, fractions of minutes are given up to two
    decimal places, the format would be ddd/1,mmmm/100,0/1.'''
    GPS_ALTITUDE_REF = enum.auto()
    '''Indicates the altitude used as the reference altitude. If the reference is sea level and the altitude is above sea level,
    0 is given. If the altitude is below sea level, a value of 1 is given and the altitude is indicated as an absolute value in
    the GPSAltitude tag.'''
    GPS_ALTITUDE = enum.auto()
    '''Indicates the altitude based on the reference in GPSAltitudeRef. Altitude is expressed as one RATIONAL value.
    The reference unit is meters.'''
    GPS_TIMESTAMP = enum.auto()
    '''Indicates the time as UTC (Coordinated Universal Time). TimeStamp is expressed as three RATIONAL values
    giving the hour, minute, and second.'''
    GPS_SATELLITES = enum.auto()
    '''Indicates the GPS satellites used for measurements. This tag can be used to describe the number of satellites,
    their ID number, angle of elevation, azimuth, SNR and other information in ASCII notation. The format is not
    specified. If the GPS receiver is incapable of taking measurements, value of the tag shall be set to NULL.'''
    GPS_STATUS = enum.auto()
    '''Indicates the status of the GPS receiver when the image is recorded.'''
    GPS_MEASURE_MODE = enum.auto()
    '''Indicates the GPS measurement mode. - 2- or 3- dimensional.'''
    GPSDOP = enum.auto()
    '''Indicates the GPS DOP (data degree of precision). An HDOP value is written during two-dimensional measurement,
    and PDOP during three-dimensional measurement.'''
    GPS_SPEED_REF = enum.auto()
    '''Indicates the unit used to express the GPS receiver speed of movement. 'K' 'M' and 'N' represents kilometers per
    hour, miles per hour, and knots.'''
    GPS_SPEED = enum.auto()
    '''Indicates the speed of GPS receiver movement.'''
    GPS_TRACK_REF = enum.auto()
    '''Indicates the reference for giving the direction of GPS receiver movement. 'T' denotes true direction and 'M' is
    magnetic direction.'''
    GPS_TRACK = enum.auto()
    '''Indicates the direction of GPS receiver movement. The range of values is from 0.00 to 359.99.'''
    GPS_IMG_DIRECTION_REF = enum.auto()
    '''Indicates the reference for giving the direction of the image when it is captured. 'T' denotes true direction and 'M' is
    magnetic direction.'''
    GPS_IMG_DIRECTION = enum.auto()
    '''Indicates the direction of the image when it was captured. The range of values is from 0.00 to 359.99.'''
    GPS_MAP_DATUM = enum.auto()
    '''Indicates the geodetic survey data used by the GPS receiver.'''
    GPS_DEST_LATITUDE_REF = enum.auto()
    '''Indicates whether the latitude of the destination point is north or south latitude. The ASCII value 'N' indicates north
    latitude, and 'S' is south latitude.'''
    GPS_DEST_LATITUDE = enum.auto()
    '''Indicates the latitude of the destination point. The latitude is expressed as three RATIONAL values giving the
    degrees, minutes, and seconds, respectively. If latitude is expressed as degrees, minutes and seconds, a typical
    format would be dd/1,mm/1,ss/1. When degrees and minutes are used and, for example, fractions of minutes are
    given up to two decimal places, the format would be dd/1,mmmm/100,0/1.'''
    GPS_DEST_LONGITUDE_REF = enum.auto()
    '''Indicates whether the longitude of the destination point is east or west longitude. ASCII 'E' indicates east longitude,
    and 'W' is west longitude.'''
    GPS_DEST_LONGITUDE = enum.auto()
    '''Indicates the longitude of the destination point. The longitude is expressed as three RATIONAL values giving the
    degrees, minutes, and seconds, respectively. If longitude is expressed as degrees, minutes and seconds, a typical
    format would be ddd/1,mm/1,ss/1. When degrees and minutes are used and, for example, fractions of minutes are
    given up to two decimal places, the format would be ddd/1,mmmm/100,0/1.'''
    GPS_DEST_BEARING_REF = enum.auto()
    '''Indicates the reference used for giving the bearing to the destination point. 'T' denotes true direction and 'M' is
    magnetic direction.'''
    GPS_DEST_BEARING = enum.auto()
    '''Indicates the bearing to the destination point. The range of values is from 0.00 to 359.99.'''
    GPS_DEST_DISTANCE_REF = enum.auto()
    '''Indicates the unit used to express the distance to the destination point. 'K', 'M' and 'N' represent kilometers, miles
    and knots.'''
    GPS_DEST_DISTANCE = enum.auto()
    '''Indicates the distance to the destination point.'''
    GPS_PROCESSING_METHOD = enum.auto()
    '''A character string recording the name of the method used for location finding.
    The first byte indicates the character code used, and this is followed by the name
    of the method.'''
    GPS_AREA_INFORMATION = enum.auto()
    '''A character string recording the name of the GPS area. The first byte indicates
    the character code used, and this is followed by the name of the GPS area.'''
    GPS_DATE_STAMP = enum.auto()
    '''A character string recording date and time information relative to UTC
    (Coordinated Universal Time). The format is YYYY:MM:DD.'''
    GPS_DIFFERENTIAL = enum.auto()
    '''Indicates whether differential correction is applied to the GPS receiver.'''
    STRIP_OFFSETS = enum.auto()
    '''For each strip, the byte offset of that strip. It is recommended that this be selected so the number of strip bytes does not exceed 64 Kbytes.
    Aux tag.'''
    JPEG_INTERCHANGE_FORMAT = enum.auto()
    '''The offset to the start byte (SOI) of JPEG compressed thumbnail data. This is not used for primary image JPEG data.'''
    JPEG_INTERCHANGE_FORMAT_LENGTH = enum.auto()
    '''The number of bytes of JPEG compressed thumbnail data. This is not used for primary image JPEG data. JPEG thumbnails are not divided but are recorded as a continuous JPEG bitstream from SOI to EOI. Appn and COM markers should not be recorded. Compressed thumbnails must be recorded in no more than 64 Kbytes, including all other data to be recorded in APP1.'''
    EXIF_IFD_POINTER = enum.auto()
    '''A pointer to the Exif IFD. Interoperability, Exif IFD has the same structure as that of the IFD specified in TIFF. ordinarily, however, it does not contain image data as in the case of TIFF.'''
    GPS_IFD_POINTER = enum.auto()
    '''The gps ifd pointer.'''
    ROWS_PER_STRIP = enum.auto()
    '''The number of rows per strip. This is the number of rows in the image of one strip when an image is divided into strips.'''
    STRIP_BYTE_COUNTS = enum.auto()
    '''The total number of bytes in each strip.'''
    PIXEL_X_DIMENSION = enum.auto()
    '''Information specific to compressed data. When a compressed file is recorded, the valid width of the meaningful image shall be recorded in this tag, whether or not there is padding data or a restart marker.'''
    PIXEL_Y_DIMENSION = enum.auto()
    '''Information specific to compressed data. When a compressed file is recorded, the valid height of the meaningful image shall be recorded in this tag'''
    GAMMA = enum.auto()
    '''Gamma value'''
    SENSITIVITY_TYPE = enum.auto()
    '''Type of photographic sensitivity'''
    STANDARD_OUTPUT_SENSITIVITY = enum.auto()
    '''Indicates standard output sensitivity of camera'''
    RECOMMENDED_EXPOSURE_INDEX = enum.auto()
    '''Indicates recommended exposure index'''
    ISO_SPEED = enum.auto()
    '''Information about iso speed value as defined in ISO 12232'''
    ISO_SPEED_LATITUDE_YYY = enum.auto()
    '''This tag indicates ISO speed latitude yyy value as defined in ISO 12232'''
    ISO_SPEED_LATITUDE_ZZZ = enum.auto()
    '''This tag indicates ISO speed latitude zzz value as defined in ISO 12232'''
    CAMERA_OWNER_NAME = enum.auto()
    '''Contains camera owner name'''
    BODY_SERIAL_NUMBER = enum.auto()
    '''Contains camera body serial number'''
    LENS_MAKE = enum.auto()
    '''This tag records lens manufacturer'''
    LENS_MODEL = enum.auto()
    '''This tag records lens`s model name and model number'''
    LENS_SERIAL_NUMBER = enum.auto()
    '''This tag records the serial number of interchangable lens'''
    LENS_SPECIFICATION = enum.auto()
    '''This tag notes minimum focal length, maximum focal length, minimum F number in the minimum focal length and minimum F number in maximum focal length'''

