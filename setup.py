from setuptools import setup, find_packages

with open('README.md') as file:
	readme_file = file.read()

with open('LICENSE') as file:
	license_file = file.read()

setup(
	name='photos_locator',
	version='0.1.0',
	description='A simple tool to rename your photos using gps metadata',
	long_description=readme_file,
	author='Daniele Rossi',
	author_email='daniele.rossi27@unibo.it',
	url='https://github.com/DendoD96/photos_locator',
	keywords=['photography', 'gps-location'],
	license=license_file,
	packages=find_packages(exclude='tests'),
	install_requires=[
		'Pillow',
		'geopy',
		'Unidecode'
	],
	classifiers=[
		'Development Status :: 3 - Alpha',
		'Environment :: Console',
		'Intended Audience :: Hobbyist photographer',
		'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
		'Topic :: Utilities',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.6',
		'Programming Language :: Python :: 3.7',
		'Programming Language :: Python :: 3.8',
		'Programming Language :: Python :: 3.9',
	]
)
