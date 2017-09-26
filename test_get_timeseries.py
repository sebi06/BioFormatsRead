# -*- coding: utf-8 -*-
"""
@author: Sebi

File: test_get_timeseries.py
Date: 17.04.2017
Version. 0.3
"""

from __future__ import print_function
import bftools as bf
from matplotlib import pyplot as plt, cm
import os
import numpy as np

filename = r'testdata/T=5_Z=3_CH=2_CZT_All_CH_per_Slice.czi'

# use for BioFormtas <= 5.1.10
#urlnamespace = 'http://www.openmicroscopy.org/Schemas/OME/2015-01'
# use for BioFormtas > 5.2.0
urlnamespace = 'http://www.openmicroscopy.org/Schemas/OME/2016-06'

# specify bioformats_package.jar to use if required
bfpackage = r'bfpackage/5.4.1/bioformats_package.jar'
bf.set_bfpath(bfpackage)

# get image meta-information
MetaInfo = bf.get_relevant_metainfo_wrapper(filename, namespace=urlnamespace, bfpath=bfpackage, showinfo=False)

seriesID = 0
timepoint = 2
channel = 1
zplane = 2

# get the actual time series from the data set
tseries, dimorder_out = bf.get_timeseries(filename, MetaInfo['Sizes'], seriesID, zplane=zplane)

img2show = tseries[timepoint, channel, :, :]
fig1 = plt.figure(figsize=(10, 8), dpi=100)
ax1 = fig1.add_subplot(111)
cax = ax1.imshow(img2show, interpolation='nearest', cmap=cm.gray, aspect='equal')
ax1.set_title('T=' + str(timepoint+1) + ' Z=' + str(zplane+1) + ' CH=' + str(channel+1), fontsize=12)
ax1.set_xlabel('X-dimension [pixel]', fontsize=10)
ax1.set_ylabel('Y-dimension [pixel]', fontsize=10)
cbar = fig1.colorbar(cax)
# show plots
plt.show()

# show relevant image Meta-Information
script = os.path.basename(__file__)
bf.showtypicalmetadata(MetaInfo, namespace=urlnamespace, bfpath=bfpackage, testscript=script)

