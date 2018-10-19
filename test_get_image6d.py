# -*- coding: utf-8 -*-
"""
@author: Sebi
File: test_get_image6d.py
Date: 02.05.2017
Version. 1.7
"""

from __future__ import print_function
import numpy as np
import bftools as bf

filename = r'testdata/Beads_63X_NA1.35_xy=0.042_z=0.1.czi'
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
<<<<<<< HEAD
bfpackage = r'bfpackage/5.8.2/bioformats_package.jar'
=======
#bfpackage = r'bfpackage/5.7.2/bioformats_package.jar'
#bfpackage = r'c:\Users\M1SRH\Documents\Software\BioFormats_Package\5.1.10\bioformats_package.jar'
bfpackage = r'c:\Users\m1srh\Documents\Software\Bioformats\5.9.2\bioformats_package.jar'
>>>>>>> e904a8d4351869e5dc6224d99865f66da1c81ccd
bf.set_bfpath(bfpackage)

# get image meta-information
MetaInfo = bf.get_relevant_metainfo_wrapper(filename, namespace=urlnamespace, bfpath=bfpackage, showinfo=False)

try:
    img6d, readstate = bf.get_image6d(filename, MetaInfo['Sizes'])
    arrayshape = np.shape(img6d)
except:
    arrayshape = []
    print('Could not read image data into NumPy array.')

# show relevant image Meta-Information
bf.showtypicalmetadata(MetaInfo, namespace=urlnamespace, bfpath=bfpackage)
print('Array Shape          : ', arrayshape)
