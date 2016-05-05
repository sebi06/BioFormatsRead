# -*- coding: utf-8 -*-
"""
@author: Sebi

File: test_planeXYZ.py
Date: 21.03.2016
Version. 0.1
"""

import bfimage as bf

# define filename
filename = r'testdata/Beads_63X_NA1.35_xy=0.042_z=0.1.czi'

# specify bioformats_package.jar to use if required
#bf.set_bfpath(insert path to bioformats_package.jar here)

# create plane info and write into dataframe
df = bf.get_planetable(filename, writecsv=True, separator='\t')

# show the dataframe
print df[:5]
print df.shape[0]
