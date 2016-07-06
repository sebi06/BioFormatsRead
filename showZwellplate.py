# -*- coding: utf-8 -*-
"""
@author: Sebi

File: showZwellplate.py
Date: 06.07.2016
Version. 1.0
"""

import bfimage as bf
import dispZsurface as dsp
import pandas as pd
import matplotlib.pyplot as plt

#filename = r'testdata/\Wellchamber_384_Comb.csv'
#filename = r'testdata/\fixed endpoint 3C 2_5 384well_planetable.csv'
filename = r'testdata/\testwell96_planetable.csv'

# create plane info from CZI image file and write CSV file (optional)
#planetable = bf.get_planetable(filename, writecsv=True, separator=',')

# or use the CSV file directly once it was created
planetable = pd.read_csv(filename, sep='\t')

# show the dataframe
print planetable[:10]
print planetable.shape[0]

# display the XYZ positions
dsp.scatterplot(planetable, ImageID=0, T=0, CH=0, Z=0, size=250, savefigure=True, filename=filename, showsurface=False)

# show the plot
plt.show()
