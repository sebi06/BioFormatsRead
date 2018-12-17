# -*- coding: utf-8 -*-
"""
@author: Sebi
File: test_get_image6d.py
Date: 02.05.2017
Version. 1.7
"""

import numpy as np
import bftools as bf
from matplotlib import pyplot as plt, cm
import dispvalues as dsv

#filename = r'testdata/Beads_63X_NA1.35_xy=0.042_z=0.1.czi'
filename = r'c:\Users\m1srh\Documents\Testdata_Zeiss\BioFormats_DimOrder_Test\T=30_Z=23_C=2_x=217_Y=94.czi'
#filename = r'testdata/T=5_Z=3_CH=2_CZT_All_CH_per_Slice.czi'
#filename = r'testdata/B4_B5_S=8_4Pos_perWell_T=2_Z=1_CH=1.czi'
#filename = r'l:\Data\BioFormats_CZI_Test\20170419\20170419_BioFormats_CZI_Test_small_384chamber_5X_2X.czi'
#filename = r'l:\Data\BioFormats_CZI_Test\20160425_BF_CZI.czi'
#filename = r'c:\Users\M1SRH\Downloads\Raw-HR-NLM_segmented_C_PA_small.ome.tiff'

# use for BioFormtas <= 5.1.10
#urlnamespace = 'http://www.openmicroscopy.org/Schemas/OME/2015-01'
# use for BioFormtas > 5.2.0
urlnamespace = 'http://www.openmicroscopy.org/Schemas/OME/2016-06'

# specify bioformats_package.jar to use if required
#bfpackage = r'bfpackage/5.1.10/bioformats_package.jar'
bfpackage = r'bfpackage/5.9.2/bioformats_package.jar'
# set path the bioformats_package.jar
bf.set_bfpath(bfpackage)

# get image meta-information using bioformats
MetaInfo = bf.get_relevant_metainfo_wrapper(filename,
                                            namespace=urlnamespace,
                                            bfpath=bfpackage,
                                            showinfo=False,
                                            xyorder='YX')

try:
    img6d, readstate = bf.get_image6d(filename, MetaInfo['Sizes'])
    arrayshape = np.shape(img6d)
except:
    arrayshape = []
    print('Could not read image data into NumPy array.')

# show relevant image Meta-Information
bf.showtypicalmetadata(MetaInfo, namespace=urlnamespace, bfpath=bfpackage)
print('Array Shape          : ', arrayshape)

T = 15
C = 1
Z = 1
S = 1

img2show = img6d[S - 1, T - 1, Z - 1, C - 1, :, :]

# write OME-TIFF
filepath = r'stack.ome.tiff'
fp = bf.write_ometiff(filepath, img6d,
                      scalex=MetaInfo['XScale'],
                      scaley=MetaInfo['YScale'],
                      scalez=MetaInfo['ZScale'],
                      dimorder='STZCXY',
                      pixeltype='uint16')

# plot one image plane to check results
fig = plt.figure(figsize=(10, 8), dpi=100)
ax = fig.add_subplot(111)
cax = ax.imshow(img2show, interpolation='nearest', cmap=cm.hot)
ax.set_title('S=' + str(S) + 'T=' + str(T) + ' Z=' + str(Z) + ' CH=' + str(C), fontsize=12)
ax.set_xlabel('X-dimension [pixel]', fontsize=10)
ax.set_ylabel('Y-dimension [pixel]', fontsize=10)
cbar = fig.colorbar(cax)
ax.format_coord = dsv.Formatter(cax)
# show plots
plt.show()
