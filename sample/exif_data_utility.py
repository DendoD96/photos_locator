import logging

from PIL import Image
import re
import unidecode
import functools
from geopy.geocoders import Nominatim
from typing import Dict
import overpy
from geopy import distance as compute_distance

api = overpy.Overpass()

DATETIME_DECIMAL_IFD_TAG = 36867
DATETIME_DECIMAL_TIFF_TAG = 306

GPS_DECIMAL_IFD_TAG = 34853

OVERPASS_RADIUS = 250

NOMINATIM_ZOOM = 14

NOMINATIM_GEO_LOCATOR = Nominatim(user_agent='photoslocator')


def _none_not_allowed(original_function):
    @functools.wraps(original_function)
    def new_function(*args, **kwargs):
        if None in args:
            raise ValueError("None is not a valid parameter")
        return original_function(*args, **kwargs)

    return new_function


def _gps_degrees_minutes_seconds_to_decimal(d, m, s):
    return d + float(m) / 60 + float(s) / 3600


def _get_longitude(gps_info: dict):
    return _gps_degrees_minutes_seconds_to_decimal(gps_info[4][0], gps_info[4][1], gps_info[4][2])


def _get_latitude(gps_info: dict):
    return _gps_degrees_minutes_seconds_to_decimal(gps_info[2][0], gps_info[2][1], gps_info[2][2])


@_none_not_allowed
def _get_overpass_poi(latitude, longitude):
    selected_tag_name = None
    result = api.query(f"""
            [out:json][timeout:25];
            (
                way["name"](around:{OVERPASS_RADIUS},{latitude},{longitude}); 
            );
            out center;
            out tags;
            """)
    if len(result.ways) == 1:
        selected_tag_name = result.ways[0].tags['name']

    elif len(result.ways) >= 1:
        last_distance = None
        for way in result.ways:
            distance = compute_distance.distance((latitude, longitude), (way.center_lat, way.center_lon)).km
            if last_distance is None or distance < last_distance:
                last_distance = distance
                selected_tag_name = way.tags['name']

    return selected_tag_name


@_none_not_allowed
def _get_datetime_iso8601(date_time_info: str):
    date_time_split = date_time_info.split(' ')
    return f"{date_time_split[0].replace(':', '-')}T{date_time_split[1].replace(':', '-')}"


@_none_not_allowed
def _get_location(gps_exif_information: Dict):
    try:
        latitude = _get_latitude(gps_exif_information)
        longitude = _get_longitude(gps_exif_information)
        poi = _get_overpass_poi(latitude, longitude)
        if poi is not None:
            return poi
        else:
            location = re.sub('[^A-Za-z0-9,]+', '',
                              unidecode.unidecode(
                                  NOMINATIM_GEO_LOCATOR.reverse(f"{latitude}, {longitude}",
                                                                zoom=NOMINATIM_ZOOM).address)).split(',')
            return f"{location[0]} {location[1]}"
    except Exception:
        logging.error(f"Exception during coordinate parsing")
        raise ValueError


def get_location_and_datetime(photo_absolute_path: str) -> Dict[str, str]:
    """Returns a dictionary that can contain the location, date and time the photo was taken

    :param: photo_absolute_path: The absolute path of the photo of which informations is needed
    :type: photo_absolute_path: str
    :return: a dictionary that can contain location and datetime (under location and datetime keys)
    :rtype: Dict
    :raises ValueError: the given file is not supported
    """
    with Image.open(photo_absolute_path) as photo:
        exif_data = photo._getexif()
        location_datetime = {}
        if exif_data:
            gps_exif_information = exif_data.get(GPS_DECIMAL_IFD_TAG)
            date_time_exif_information = exif_data.get(
                DATETIME_DECIMAL_IFD_TAG) if DATETIME_DECIMAL_IFD_TAG in exif_data else exif_data.get(
                DATETIME_DECIMAL_TIFF_TAG)
            try:
                location = _get_location(gps_exif_information)
                location_datetime['location'] = location
            except ValueError:
                logging.warning("GPS exif data unavailable or not formatted correctly")
                pass
            try:
                date_time = _get_datetime_iso8601(date_time_exif_information)
                location_datetime['datetime'] = date_time
            except ValueError:
                logging.warning("Original date and time exif data unavailable")
                pass
        return location_datetime
