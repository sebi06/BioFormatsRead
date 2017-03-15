# -*- coding: utf-8 -*-
"""
@author: Sebi

File: showZwellplate.py
Date: 06.07.2016
Version. 1.1
"""

import bfimage as bf
import dispZsurface as dsp
import pandas as pd
import matplotlib.pyplot as plt

#filenamecsv = r'testdata/Wellchamber_384_Comb.csv'
#filenamecsv = r'testdata/fixed endpoint 3C 2_5 384well_planetable.csv'
#filenameczi = r'testadata/yourCZIimage.czi'
filenamecsv = r'testdata/testwell96_planetable.csv'

# define separator
separator = '\t'

# create plane info from CZI image file and write CSV file (optional)
planetable, filenamecsv = bf.get_planetable(filenameczi, writecsv=True, sep=separator)

# or use the CSV file directly once it was created
#planetable = pd.read_csv(filenamecsv, sep=separator)

# show the dataframe
print planetable[:10]
print planetable.shape[0]

# display the XYZ positions
dsp.scatterplot(planetable, ImageID=0, T=0, CH=0, Z=0, size=250,
                savefigure=False, figsavename=filenamecsv, showsurface=True)

# show the plot
plt.show()
