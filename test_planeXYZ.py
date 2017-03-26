# -*- coding: utf-8 -*-
"""
@author: Sebi

File: test_planeXYZ.py
Date: 26.03.2017
Version. 0.3
"""

from __future__ import print_function
import bfimage as bf

# define filename
filename = r'testdata/Beads_63X_NA1.35_xy=0.042_z=0.1.czi'

# use for BioFormtas <= 5.1.10
urlnamespace = 'http://www.openmicroscopy.org/Schemas/OME/2015-01'
# use for BioFormtas > 5.2.0
#urlnamespace = 'http://www.openmicroscopy.org/Schemas/OME/2016-06'

# specify bioformats_package.jar to use if required
bfpackage = r'bioformats_package/5.1.10/bioformats_package.jar'
bf.set_bfpath(bfpackage)

# create plane info and write into dataframe
df, csvfile = bf.get_planetable(filename, writecsv=True, separator='\t')

# show the dataframe
print(df[:5])
print(df.shape[0])
