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

zoomlevels = {
		  80: 2,
		 200: 5,
		 400: 10,
		 800: 20,
		1600: 40,
		3200: 80,
		}

outcache = StringIO.StringIO()
output = csv.writer(outcache, delimiter=',')

for folder in args.folders:
	for filename in os.listdir(folder):
		file, ext = os.path.splitext(filename)
		# skip files with no valid tiff file extension
		if ext.lower() not in ['.tif', '.tiff']: continue
		exif = GExiv2.Metadata(os.path.join(folder, filename))
		XRESOLUTION = float(exif['Exif.Image.XResolution'].split('/')[0]) / 25.4
		YRESOLUTION = float(exif['Exif.Image.YResolution'].split('/')[0]) / 25.4
		WIDTH  = float(exif['Exif.Image.ImageWidth']) / XRESOLUTION
		HEIGHT = float(exif['Exif.Image.ImageLength']) / YRESOLUTION
		ZOOM = 0
		for key, value in zoomlevels.iteritems():
			if XRESOLUTION > key and ZOOM < value: ZOOM = value
		output.writerow([
			exif['Exif.Image.ImageDescription'], exif['Exif.Image.DateTime'], '', # staining
			filename, ZOOM, '%0.2f' % WIDTH, '%0.2f' % HEIGHT, exif['Exif.Image.ImageWidth'],
			exif['Exif.Image.ImageLength'], '%0.2f' % XRESOLUTION, '%0.2f' % XRESOLUTION,
			'%s %s' % (exif['Exif.Image.Make'], exif['Exif.Image.Model'])
		])

print(outcache.getvalue())
