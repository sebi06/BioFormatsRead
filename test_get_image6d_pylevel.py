# -*- coding: utf-8 -*-
"""
@author: Sebi

File: test_get_image6d_pylevel.py
Date: 16.12.2018
Version. 0.1
"""

import numpy as np
import bftools as bf
from matplotlib import pyplot as plt, cm
import dispvalues as dsv

showimage = True

filename = r'c:\Users\m1srh\OneDrive - Carl Zeiss AG\Projects\Apeer\ZenCore_Workflows\ParticleAnalysis\Filtertest1_POLsm.czi'

# use for BioFormtas <= 5.1.10
#urlnamespace = 'http://www.openmicroscopy.org/Schemas/OME/2015-01'
# use for BioFormtas > 5.2.0
urlnamespace = 'http://www.openmicroscopy.org/Schemas/OME/2016-06'

# specify bioformats_package.jar to use if required
#bfpackage = r'bfpackage/5.1.10/bioformats_package.jar'
bfpackage = r'bfpackage/5.9.2/bioformats_package.jar'
# set path the bioformats_package.jar
bf.set_bfpath(bfpackage)

# get image meta-information
MetaInfo = bf.get_relevant_metainfo_wrapper(filename,
                                            namespace=urlnamespace,
                                            bfpath=bfpackage,
                                            showinfo=False,
                                            xyorder='YX')

try:
    img6d, readstate = bf.get_image6d_pylevel(filename, MetaInfo, pylevel=0,)
    arrayshape = np.shape(img6d)
except:
    arrayshape = []
    print('Could not read image data into NumPy array.')

# show relevant image Meta-Information
bf.showtypicalmetadata(MetaInfo, namespace=urlnamespace, bfpath=bfpackage)
print('Array Shape          : ', arrayshape)

if showimage:

    T = 1
    C = 1
    Z = 1
    S = 1

    img2show = img6d[S - 1, T - 1, Z - 1, C - 1, :, :]

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