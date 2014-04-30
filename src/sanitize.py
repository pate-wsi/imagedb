#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import os, StringIO, re, csv
from argparse import ArgumentParser
from subprocess import Popen


parser = ArgumentParser(description='Extract metadata from tiff images.')
parser.add_argument('folder', metavar='Folder', type=str,
                  help='folders containing tiff images to be processed')
parser.add_argument('-c', metavar='db.csv', help='specify csv file')

args = parser.parse_args()

outcache = StringIO.StringIO()
output = csv.writer(outcache, delimiter=',')
inputfile = open(args.c)
db = csv.reader(inputfile, delimiter=',')
for row in db:
	if len(row) < 4:
		output.writerow(row)
		continue
	sourcefn = row[3]
	targetfn = re.sub('[^A-Za-z0-9]+', '_', row[0]).lower() + '.tif'
	if sourcefn != targetfn and sourcefn in os.listdir(args.folder):
		print ('%s => %s' % (sourcefn, targetfn))
		os.rename(os.path.join(args.folder, sourcefn),
				  os.path.join(args.folder, targetfn))
		Popen(['tiffset', '-s', '270', row[0], os.path.join(args.folder, targetfn)])
		row[3] = targetfn
	output.writerow(row)
inputfile.close()

f = open(args.c, 'w')
f.write(outcache.getvalue())
