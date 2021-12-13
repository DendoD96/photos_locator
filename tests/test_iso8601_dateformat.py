import unittest

from sample.photo_utils import _validate_iso8601


class DateFormatTest(unittest.TestCase):

	def test_string_start_with_iso8601_date(self):
		self.assertTrue(_validate_iso8601("2003-12-14T12-01-44-name"))

	def test_string_without_iso8601_date(self):
		self.assertFalse(_validate_iso8601("2003-12-1412-01-44"))


if __name__ == '__main__':
	unittest.main()
