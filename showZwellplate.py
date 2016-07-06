# -*- coding: utf-8 -*-
"""
@author: Sebi

File: showZwellplate.py
Date: 21.03.2016
Version. 0.1
"""

import bfimage as bf
import dispZsurface as dsp
import pandas as pd
import matplotlib.pyplot as plt

#filename = r'c:\Users\M1SRH\Documents\Python_Projects_Testdata\CZI\Wellchamber_384_Comb.csv'
#filename = r'c:\Users\M1SRH\Documents\Python_Projects_Testdata\CZI\96Wells_S=96_9proWell.csv'
#filename = r'c:\Users\M1SRH\Documents\Python_Projects_Testdata\CZI\fixed endpoint 3C 2_5 384well_planetable.csv'
filename = r'c:\Users\M1SRH\Documents\Testdata_Zeiss\Castor\EMBL\testwell96_planetable.csv'

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