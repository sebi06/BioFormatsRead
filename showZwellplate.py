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

#filenameczi = r's:\Python_Projects_Testdata\CZI\testwell96.czi'
filenameczi = r'/home/sebi06/Dokumente/Python_Projects_Testdata/CZI/testwell96.czi'
#filenamecsv = r'testdata/Wellchamber_384_Comb.csv'
#filenamecsv = r'testdata/fixed endpoint 3C 2_5 384well_planetable.csv'
#filenamecsv = r'testdata/testwell96_planetable.csv'
filenamecsv = r'/home/sebi06/Dokumente/Python_Projects_Testdata/CZI/testwell96_planetable.csv'

# create plane info from CZI image file and write CSV file (optional)
#planetable1, filenamecsv = bf.get_planetable(filenameczi, writecsv=True, separator='\t')

# or use the CSV file directly once it was created
planetable2 = pd.read_csv(filenamecsv, sep='\t')

# show the dataframe
print planetable2[:10]
print planetable2.shape[0]

# display the XYZ positions
dsp.scatterplot(planetable2, ImageID=0, T=0, CH=0, Z=0, size=250,
                savefigure=False, figsavename=filenameczi, showsurface=True)

# show the plot
plt.show()
