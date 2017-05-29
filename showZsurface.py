# -*- coding: utf-8 -*-
"""
@author: Sebi

File: showZsurface.py
Date: 29.05.2017
Version. 0.1
"""

import bftools as bf
import dispZsurface as dsp
import matplotlib.pyplot as plt
import argparse


# setup commandline parameters
parser = argparse.ArgumentParser(description='Read Filename and Parameters.')
parser.add_argument('-f', action="store", dest='filename')
parser.add_argument('-csv', action="store", dest='writecsv')
parser.add_argument('-sep', action="store", dest='separator')
# get the arguments
args = parser.parse_args()

# get the filename
filenameczi = args.filename
#filenameczi = r'testdata/testwell96.czi'

# get separator
#separator = '\t'
separator = args.separator
if args.separator == 'Tab':
    separator = '\t'
elif args.separator == 'Comma':
    separator = ','
elif args.sparator == 'semicolon':
    separator = ';'


# get CSV write option
#csv = True
if args.writecsv == 'True':
    wcsv = True
elif args.writecsv == 'False':
    wcsv = False

# use for BioFormtas <= 5.1.10
#urlnamespace = 'http://www.openmicroscopy.org/Schemas/OME/2015-01'
# use for BioFormtas > 5.2.0
urlnamespace = 'http://www.openmicroscopy.org/Schemas/OME/2016-06'

# specify bioformats_package.jar to use if required
bfpackage = r'bfpackage/5.5.0/bioformats_package.jar'
bf.set_bfpath(bfpackage)

# create plane info from CZI image file and write CSV file (optional)
planetable, filenamecsv = bf.get_planetable(filenameczi, writecsv=wcsv, separator=separator)

# show the dataframe
print(planetable[:10])
print(planetable.shape[0])

# display the XYZ positions
dsp.scatterplot(planetable, ImageID=0, T=0, CH=0, Z=0, size=250,
                savefigure=True, figsavename=filenamecsv, showsurface=True)

# show the plot
plt.show()
