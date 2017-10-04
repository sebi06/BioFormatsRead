# -*- coding: utf-8 -*-
"""
@author: Sebi

File: convert_czi2tiff.py
Date: 11.08.2017
Version. 0.1
"""

import os
from czifile import czi2tif
import numpy as np
print(np.__version__)
print(np.__path__)

rootdir = r'c:\Users\M1SRH\Documents\Testdata_Zeiss\Atomic\Trainingsdaten_Spine_Detection\CZI'
extensions = ('.czi')
#extensions = ('.czi', '.lsm')

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        ext = os.path.splitext(file)[-1].lower()
        if ext in extensions:
            czi2process = os.path.join(subdir, file)
            # Save processed image
            tiff2save = os.path.splitext(czi2process)[0] + '.tiff'
            print('Converting to TIFF --> ', tiff2save)
            czi2tif(czi2process, tiffile=tiff2save, bigtiff=True, truncate=True)

print('Done.')
