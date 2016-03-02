# -*- coding: utf-8 -*-
"""
@author: Sebi

File: test_omexmltool.py
Date: 03.02.2016
Version. 1.0
"""

import bfimage as bf

# INSERT THE FILES INSIDE THE LIST BELOW
testfiles = [r'testdata\Beads_63X_NA1.35_xy=0.042_z=0.1.czi',
             r'testdata\2x2_SNAP_CH=2_Z=5_T=2.czi']

bf.create_omexml(testfiles, method=1, writeczi_metadata=False)

