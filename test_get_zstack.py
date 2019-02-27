# -*- coding: utf-8 -*-
"""
@author: Sebi

File: test_get_zstack.py
Date: 06.02.2019
Version. 0.4
"""

from __future__ import print_function
import bftools as bf
from matplotlib import pyplot as plt, cm
import os
import dispvalues as dsv

filename = r'testdata/Beads_63X_NA1.35_xy=0.042_z=0.1.czi'
imgbase = os.path.basename(filename)
imgdir = os.path.dirname(filename)

# use for BioFormtas <= 5.1.10
#urlnamespace = 'http://www.openmicroscopy.org/Schemas/OME/2015-01'
# use for BioFormtas > 5.2.0
urlnamespace = 'http://www.openmicroscopy.org/Schemas/OME/2016-06'

# specify bioformats_package.jar to use if required
bfpackage = r'bfpackage/5.9.2/bioformats_package.jar'
bf.set_bfpath(bfpackage)

# get image meta-information
MetaInfo = bf.get_relevant_metainfo_wrapper(filename, namespace=urlnamespace, bfpath=bfpackage, showinfo=False)

seriesID = 0
timepoint = 0
channel = 0

# get the actual z-stack from the data set
zstack, dimorder_out = bf.get_zstack(filename, MetaInfo['Sizes'], seriesID, timepoints='single', tindex=0)

# get plane with the brightest pixel
zplane = (zstack == zstack.max()).nonzero()[0][0]
print('Brightest Z-Plane: ', zplane+1)


img2show = zstack[zplane, channel, :, :]
fig1 = plt.figure(figsize=(10, 8), dpi=100)
ax1 = fig1.add_subplot(111)
cax = ax1.imshow(img2show, interpolation='nearest', cmap=cm.hot)
ax1.set_title('T=' + str(timepoint+1) + ' Z=' + str(zplane+1) + ' CH=' + str(channel+1), fontsize=12)
ax1.set_xlabel('X-dimension [pixel]', fontsize=10)
ax1.set_ylabel('Y-dimension [pixel]', fontsize=10)
cbar = fig1.colorbar(cax)
ax1.format_coord = dsv.Formatter(cax)
# show plots
plt.show()
