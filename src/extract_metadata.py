#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import os, StringIO, csv
from argparse import ArgumentParser
from gi.repository import GExiv2

parser = ArgumentParser(description='Extract metadata from tiff images.')
parser.add_argument('folders', metavar='Folder', type=str, nargs='+',
                  help='folders containing tiff images to be processed')

args = parser.parse_args()

outcache = StringIO.StringIO()
output = csv.writer(outcache, delimiter=',')

for folder in args.folders:
	for filename in os.listdir(folder):
		file, ext = os.path.splitext(filename)
		# skip files with no valid tiff file extension
		if ext.lower() not in ['.tif', '.tiff']: continue
		exif = GExiv2.Metadata(os.path.join(folder, filename))
		ZOOM = ''
		WIDTH,HEIGHT = '', ''
		output.writerow([
			exif['Exif.Image.ImageDescription'], exif['Exif.Image.DateTime'], '', # staining
			filename, ZOOM, WIDTH, HEIGHT, exif['Exif.Image.ImageWidth'],
			exif['Exif.Image.ImageLength'], exif['Exif.Image.XResolution'].split('/')[0],
			exif['Exif.Image.YResolution'].split('/')[0],
			'%s %s' % (exif['Exif.Image.Make'], exif['Exif.Image.Model'])
		])

print(outcache.getvalue())
