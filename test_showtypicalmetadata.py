# -*- coding: utf-8 -*-
"""
@author: Sebi

File: test_get_image6d.py
Date: 31.01.2017
Version. 1.0
"""

from __future__ import print_function
import numpy as np
import os
import bftools as bf
import sys

# define testdata base directory and filename of the image dataset to be read
#filename = r'testdata/Beads_63X_NA1.35_xy=0.042_z=0.1.czi'
#filename = r'testdata/T=5_Z=3_CH=2_CZT_All_CH_per_Slice.czi'
#filename = r'testdata/B4_B5_S=8_4Pos_perWell_T=2_Z=1_CH=1.czi'
filename = r'/home/sebi06/Dokumente/Image_Datasets/Hoechst_A488_A568_MitoDeep633-3.czi'

# specify bioformats_package.jar to use if required
bfpackage = r'bioformats_package/5.4.1/bioformats_package.jar'
bf.set_bfpath(bfpackage)

# use for BioFormtas <= 5.1.10
#urlnamespace = 'http://www.openmicroscopy.org/Schemas/OME/2015-01'
# use for BioFormtas > 5.2.0
urlnamespace = 'http://www.openmicroscopy.org/Schemas/OME/2016-06'

redirect = False

if redirect:
    # redirect output
    orig_stdout = sys.stdout
    filepath_output = os.path.join(os.getcwd(), filename[:-4]+'_output.txt')
    fo = open(filepath_output, 'wb+')
    sys.stdout = fo

# get image meta-information
MetaInfo = bf.get_relevant_metainfo_wrapper(filename, namespace=urlnamespace, bfpath=bfpackage, showinfo=False)
bf.showtypicalmetadata(MetaInfo, namespace=urlnamespace, bfpath=bfpackage)

if redirect:
    sys.stdout = orig_stdout
    fo.close()
    sys.__stdout__
    print('Output written to : ', filepath_output)
