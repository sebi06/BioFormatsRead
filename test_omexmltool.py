# -*- coding: utf-8 -*-
"""
@author: Sebi

File: test_omexmltool.py
Date: 03.02.2016
Version. 1.0
"""

import bfimage as bf

# specify bioformats_package.jar to use if required
#bf.set_bfpath(insert path to bioformats_packe.jar here)

# INSERT THE FILES INSIDE THE LIST BELOW

testfiles = [r'testdata/2x2_SNAP_CH=2_Z=5_T=2.czi']

bf.create_omexml(testfiles, method=1, writeczi_metadata=True)
