# -*- coding: utf-8 -*-
"""
@author: Sebi

File: test_planeXYZ.py
Date: 21.03.2016
Version. 0.1
"""

import bfimage as bf

# define filename
#filename = r'testdata\2x2_SNAP_CH=2_Z=5_T=2.czi'
filename = r's:\Spyder_Projects_Testdata\CZI\WP_96_Positions.czi'

# create plane info and write into dataframe
df = bf.get_planetable(filename, writecsv=True, separator='\t')

# show the dataframe
print df[:5]
print df.shape[0]


