import os
import unittest

from sample.exif_data_utility import get_location_and_datetime


class MyTestCase(unittest.TestCase):

	def test_gps_and_datetime_data(self):
		expected_result = {'location': 'VilledAnaunia_ComunitadellaValdiNon', 'datetime': '2021-09-05T16:09:10'}
		photo_absolute_path = os.path.join(os.path.dirname(__file__), 'images/exif_gps.jpg')
		location_datetime = get_location_and_datetime(photo_absolute_path=photo_absolute_path)
		self.assertEqual(location_datetime, expected_result,
		                 f"location and datetime of {photo_absolute_path} does not match with {expected_result}")

	def test_datetime_data(self):
		expected_result = {'datetime': '2003-12-14T12:01:44'}
		photo_absolute_path = os.path.join(os.path.dirname(__file__), 'images/datetime_only.jpg')
		datetime = get_location_and_datetime(photo_absolute_path=photo_absolute_path)
		self.assertEqual(datetime, expected_result,
		                 f"datetime of {photo_absolute_path} does not match with {expected_result}")

	def test_no_gps_and_datetime_data(self):
		expected_result = {}
		photo_absolute_path = os.path.join(os.path.dirname(__file__), 'images/no_exif_data.jpg')
		no_data = get_location_and_datetime(photo_absolute_path=photo_absolute_path)
		self.assertEqual(no_data, expected_result,
		                 f"Empty dictionary expected")

	def test_no_exif_data(self):
		expected_result = {}
		photo_absolute_path = os.path.join(os.path.dirname(__file__), 'images/square.png')
		no_data = get_location_and_datetime(photo_absolute_path=photo_absolute_path)
		self.assertEqual(no_data, expected_result,
		                 f"Empty dictionary expected")

	def test_invalid_gps_data_format(self):
		expected_result = {'datetime': '2099-09-29T10:10:10'}
		photo_absolute_path = os.path.join(os.path.dirname(__file__), 'images/invalid_gps_data_format.jpg')
		datetime = get_location_and_datetime(photo_absolute_path=photo_absolute_path)
		self.assertEqual(datetime, expected_result,
		                 f"datetime of {photo_absolute_path} does not match with {expected_result}")

	def test_gps_error_and_tiff_datetime(self):
		expected_result = {'datetime': '2010-08-15T13:58:09'}
		photo_absolute_path = os.path.join(os.path.dirname(__file__), 'images/exif_gps_typeerror_and_tiff_data.jpg')
		datetime = get_location_and_datetime(photo_absolute_path=photo_absolute_path)
		self.assertEqual(datetime, expected_result,
		                 f"datetime of {photo_absolute_path} does not match with {expected_result}")




if __name__ == '__main__':
	unittest.main()
