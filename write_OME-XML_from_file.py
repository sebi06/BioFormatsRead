# -*- coding: utf-8 -*-
"""
@author: Sebi

File: write_OME-XML_from_file.py
Date: 11.05.2015
Version. 1.1
"""

from __future__ import print_function
import bftools as bf


# use for BioFormtas <= 5.1.10
#urlnamespace = 'http://www.openmicroscopy.org/Schemas/OME/2015-01'
# use for BioFormtas > 5.2.0
urlnamespace = 'http://www.openmicroscopy.org/Schemas/OME/2016-06'

# specify bioformats_package.jar to use if required
bfpackage = r'bioformats_package/5.4.1/bioformats_package.jar'
bf.set_bfpath(bfpackage)

# INSERT THE FILES INSIDE THE LIST BELOW

testfiles = [r'testdata/T=5_Z=3_CH=2_CZT_All_CH_per_Slice.czi']

bf.writeomexml(testfiles, method=1, writeczi_metadata=True)
