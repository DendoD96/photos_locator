import logging
import os
import PIL
import re

from sample.exif_data_utility import get_location_and_datetime

iso8601_without_colon_regex = r'^(-?(?:[1-9][0-9]*)?[0-9]{4})-(1[0-2]|0[1-9])-(3[01]|0[1-9]|[12][0-9])T(2[0-3]|[01][' \
                              r'0-9])-([0-5][0-9])-([0-5][0-9])(\.[0-9]+)?(Z|[+-](?:2[0-3]|[01][0-9]):[0-5][0-9])?.*'
match_iso8601_without_colon = re.compile(iso8601_without_colon_regex).match


def _validate_iso8601(string_to_validate):
    try:
        if match_iso8601_without_colon(string_to_validate) is not None:
            return True
    except re.error:
        pass
    return False


def rename_photos(photos_folder: str):
    """Rename all photos in a folder.
    If the photo in question contains gps data and datetime it will be renamed to 'datetime-location'.
    If the photo contains only datetime and has not already been renamed by the software
    it will be renamed to 'datetime-original name'.
    Otherwise it will not be renamed.

    :param: photos_folder: The folder that contains the photos
    :type: photos_folder: str
    """

    for photo_name in os.listdir(photos_folder):
        photo_absolute_path = os.path.join(photos_folder, photo_name)
        photo_filename_and_extension = os.path.splitext(photo_name)
        original_file_name = photo_filename_and_extension[0]
        file_extension = photo_filename_and_extension[1]

        if os.path.isfile(photo_absolute_path) and not _validate_iso8601(original_file_name):
            try:
                location_datetime = get_location_and_datetime(photo_absolute_path=photo_absolute_path)
                new_name = ""

                try:
                    photo_datetime = location_datetime['datetime']
                    new_name += photo_datetime
                except KeyError:
                    logging.error(f"No datetime exif data for photo: {photo_absolute_path}. Leaving its original name")
                    break

                try:
                    location = location_datetime['location']
                    new_name += f"-{location}{file_extension}"
                except KeyError:
                    new_name += f"-{original_file_name}{file_extension}"

                os.rename(photo_absolute_path, os.path.join(photos_folder, new_name))

            except PIL.UnidentifiedImageError:
                logging.error(f"file extension of {photo_absolute_path} not supported!")
