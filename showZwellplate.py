# -*- coding: utf-8 -*-
"""
@author: Sebi

File: showZwellplate.py
Date: 17.04.2017
Version. 1.2
"""

from __future__ import print_function
import bftools as bf
import dispZsurface as dsp
#import pandas as pd
import matplotlib.pyplot as plt

#filenamecsv = r'testdata/Wellchamber_384_Comb.csv'
#filenamecsv = r'testdata/fixed endpoint 3C 2_5 384well_planetable.csv'
filenameczi = r'testdata/B4_B5_S=8_4Pos_perWell_T=2_Z=1_CH=1.czi'
#filenamecsv = r'testdata/testwell96_planetable.csv'

# use for BioFormtas <= 5.1.10
#urlnamespace = 'http://www.openmicroscopy.org/Schemas/OME/2015-01'
# use for BioFormtas > 5.2.0
urlnamespace = 'http://www.openmicroscopy.org/Schemas/OME/2016-06'

# specify bioformats_package.jar to use if required
bfpackage = r'bfpackage/5.4.1/bioformats_package.jar'
bf.set_bfpath(bfpackage)

# define separator
separator = '\t'

# create plane info from CZI image file and write CSV file (optional)
planetable, filenamecsv = bf.get_planetable(filenameczi, writecsv=True, separator=separator)

# or use the CSV file directly once it was created
#planetable = pd.read_csv(filenamecsv, sep=separator)

# show the dataframe
print(planetable[:10])
print(planetable.shape[0])

# display the XYZ positions
dsp.scatterplot(planetable, ImageID=0, T=0, CH=0, Z=0, size=250,
                savefigure=False, figsavename=filenamecsv, showsurface=True)

# show the plot
plt.show()
