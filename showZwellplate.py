# -*- coding: utf-8 -*-
"""
@author: Sebi

File: showZwellplate.py
Date: 03.02.2016
Version. 1.0
"""

import bfimage as bf
import dispZsurface as dsp
import pandas as pd

filename = r's:\Spyder_Projects_Testdata\CZI\WP_96_Positions.csv'

# create plane info from CZI image file and write CSV file (optional)
planetable = bf.get_planetable(filename, writecsv=True, separator='\t')

# or use the CSV file directly once it was created
planetable = pd.read_csv(filename, sep='\t')

# show the dataframe
print planetable[:5]
print planetable.shape[0]

# display the Z-surface
dsp.dispXYZfromTable(planetable, planetable.shape[0])
