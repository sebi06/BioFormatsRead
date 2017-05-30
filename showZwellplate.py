# -*- coding: utf-8 -*-
"""
@author: Sebi

File: showZwellplate.py
Date: 30.05.2017
Version. 1.3
"""

from __future__ import print_function
import bftools as bf
import dispZsurface as dsp
import matplotlib.pyplot as plt
import os

saveformat = '.png'

#filenamecsv = r'testdata/Wellchamber_384_Comb.csv'
#filenamecsv = r'testdata/fixed endpoint 3C 2_5 384well_planetable.csv'
#filenameczi = r'testdata/B4_B5_S=8_4Pos_perWell_T=2_Z=1_CH=1.czi'
filenameczi = r'testdata/testwell96.czi'
#filenamecsv = r'testdata/testwell96_planetable.csv'

# use for BioFormtas <= 5.1.10
#urlnamespace = 'http://www.openmicroscopy.org/Schemas/OME/2015-01'
# use for BioFormtas > 5.2.0
urlnamespace = 'http://www.openmicroscopy.org/Schemas/OME/2016-06'

# specify bioformats_package.jar to use if required
bfpackage = r'bfpackage/5.5.0/bioformats_package.jar'
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

# define name for figure to be saved
figuresavename = os.path.splitext(filenamecsv)[0] + '_XYZ-Pos' + saveformat

# display the XYZ positions
fig1, fig2 = dsp.scatterplot(planetable, ImageID=0, T=0, CH=0, Z=0, size=250,
                savefigure=True, figsavename=figuresavename, showsurface=True)

# show the plot
plt.show()
