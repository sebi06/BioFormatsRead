# -*- coding: utf-8 -*-
"""
@author: Sebi

File: test_get_image6d_multires.py
Date: 02.05.2017
Version. 0.1
"""

from __future__ import print_function
import numpy as np
import os
import bftools as bf

#filename = r'testdata/Beads_63X_NA1.35_xy=0.042_z=0.1.czi'
#filename = r'testdata/T=5_Z=3_CH=2_CZT_All_CH_per_Slice.czi'
filename = r'testdata/B4_B5_S=8_4Pos_perWell_T=2_Z=1_CH=1.czi'

# use for BioFormtas <= 5.1.10
#urlnamespace = 'http://www.openmicroscopy.org/Schemas/OME/2015-01'
# use for BioFormtas > 5.2.0
urlnamespace = 'http://www.openmicroscopy.org/Schemas/OME/2016-06'

# specify bioformats_package.jar to use if required
bfpackage = r'bioformats_package/5.4.1/bioformats_package.jar'
bf.set_bfpath(bfpackage)

# get image meta-information
MetaInfo = bf.get_relevant_metainfo_wrapper(filename, namespace=urlnamespace, bfpath=bfpackage, showinfo=False)

try:
    series_list, readstate = bf.get_image6d_multires(filename, MetaInfo)
except:
    print('Could not read image data into NumPy array.')

# show relevant image Meta-Information
bf.showtypicalmetadata(MetaInfo, namespace=urlnamespace, bfpath=bfpackage)
# show dimensions of individual series
print('Image Directory      : ', MetaInfo['Directory'])
print('-----  Individal Series Dimensions  -----')
for s in range(0, MetaInfo['TotalSeries']):
    print('SeriesID:', s, series_list[s].shape)
