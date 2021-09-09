import logging
import sys

from photo_utils import rename_photos


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
	logging.basicConfig(level=logging.INFO)
	if len(sys.argv) != 2:
		raise ValueError('Please provide the photos folder path.')
	rename_photos(sys.argv[1])