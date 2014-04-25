#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import os
from argparse import ArgumentParser
from PIL import Image

parser = ArgumentParser(description='Extract metadata from tiff images.')
parser.add_argument('folders', metavar='Folder', type=str, nargs='+',
                  help='folders containing tiff images to be processed')

args = parser.parse_args()

mapping = {
		256: 'XPIXEL',
		257: 'YPIXEL',
		270: 'NAME',
		271: 'MAKE',
		272: 'MODEL',
		282: 'XRESOLUTION',
		283: 'YRESOLUTION',
		306: 'DATE',
		}

zoomlevels = {
		  80: 2,
		 200: 5,
		 400: 10,
		 800: 20,
		1600: 40,
		3200: 80,
		}

for folder in args.folders:
	for filename in os.listdir(folder):
		file, ext = os.path.splitext(filename)
		# skip files with no valid tiff file extension
		if ext.lower() not in ['.tif', '.tiff']:
			continue
		e = dict()
		filepath = os.path.join(folder, filename)
		im = Image.open(filepath)
		# pillow does some crazy shit with the tag list
		# need to compile list of integers first and then iterate ...
		for tag in [tag for tag in im.tag]:
			if tag in mapping:
				e[mapping[tag]] = im.tag[tag]
		for item in ['XPIXEL', 'YPIXEL', 'XRESOLUTION', 'YRESOLUTION',
					 'XRESOLUTION', 'YRESOLUTION']:
			e[item] = e[item][0]
		e['SLIDESCANNER'] = '%s %s' % (e['MAKE'], e['MODEL'])
		e['XRESOLUTION'] = float(e['XRESOLUTION']) / 25.4
		e['YRESOLUTION'] = float(e['YRESOLUTION']) / 25.4
		WIDTH  = float(e['XPIXEL']) / e['XRESOLUTION']
		HEIGHT = float(e['YPIXEL']) / e['YRESOLUTION']
		ZOOM = 0
		for key, value in zoomlevels.iteritems():
			if float(e['XRESOLUTION']) > key and ZOOM < value: ZOOM = value
		print ('%s,%s,,%s,%i,%0.2f,%0.2f,%s,%s,%0.2f,%0.2f,%s' %
		(e['NAME'], e['DATE'], filename, ZOOM, WIDTH, HEIGHT,
		 e['XPIXEL'], e['YPIXEL'], e['XRESOLUTION'], e['YRESOLUTION'],
		 e['SLIDESCANNER']) )
