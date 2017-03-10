# -*- coding: utf-8 -*-
"""
@author: Sebi

File: test_get_image6d.py
Date: 31.01.2017
Version. 1.0
"""

import numpy as np
import os
import bfimage as bf
import sys

# define testdata base directory and filename of the image dataset to be read
#filename = r'testdata/Beads_63X_NA1.35_xy=0.042_z=0.1.czi'
#filename = r'testdata/T=5_Z=3_CH=2_CZT_All_CH_per_Slice.czi'
filename = r'testdata/B4_B5_S=8_4Pos_perWell_T=2_Z=1_CH=1.czi'

# specify bioformats_package.jar to use if required
bfpackage = r'BioFormats/5.1.10/bioformats_package.jar'
bf.set_bfpath(bfpackage)

# use for BioFormtas <= 5.1.10
urlnamespace = 'http://www.openmicroscopy.org/Schemas/OME/2015-01'
# use for BioFormtas > 5.2.0
#urlnamespace = 'http://www.openmicroscopy.org/Schemas/OME/2016-06'

redirect = True

if redirect:
    # redirect output
    orig_stdout = sys.stdout
    filepath_output = os.path.join(os.getcwd(), filename[:-4]+'_output.txt')
    f = open(filepath_output, 'w')
    sys.stdout = f

# get image meta-information
MetaInfo = bf.showtypicalmetadata(filename, urlnamespace=urlnamespace, bfpackage=bfpackage, showinfo=True)

if redirect:
    sys.stdout = orig_stdout
    f.close()
    sys.__stdout__
    print('Output written to : ', filepath_output)
