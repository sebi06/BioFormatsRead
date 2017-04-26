# -*- coding: utf-8 -*-
"""
@author: Sebi

File: test_getdimonly.py
Date: 17.04.2017
Version. 0.2
"""

from __future__ import print_function
import bftools as bf
import czitools as czt

# define testdata base directory and filename of the image dataset to be read
#filenames = [r'testdata/2x2_SNAP_CH=2_Z=5_T=2.czi']
filenames = [r'l:\Data\BioFormats_CZI_Test\20170419\20170419_BioFormats_CZI_Test_small_384chamber_5X_2X.czi']

# specify bioformats_package.jar to use if required
bfpackage = r'BioFormats/5.4.1/bioformats_package.jar'
bf.set_bfpath(bfpackage)

for currentfile in filenames:

    sizes = bf.get_dimension_only(currentfile)
    sizes_czi = czt.read_dimensions_czi(currentfile)
    print(sizes)
    print(sizes_czi)
