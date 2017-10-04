# -*- coding: utf-8 -*-
"""

File: test_getPixelsPlanes.py
Date: 18.04.2017
Version. 0.2
"""

import bftools as bf

filename = r'testdata/B4_B5_S=8_4Pos_perWell_T=2_Z=1_CH=1.czi'

# use for BioFormtas <= 5.1.10
#urlnamespace = 'http://www.openmicroscopy.org/Schemas/OME/2015-01'
# use for BioFormtas > 5.2.0
urlnamespace = 'http://www.openmicroscopy.org/Schemas/OME/2016-06'

# specify bioformats_package.jar to use if required
bfpackage = r'bioformats_package/5.4.1/bioformats_package.jar'
bf.set_bfpath(bfpackage)

planes, pixels = bf.getPlanesAndPixelsFromCZI(filename)

print("=== Planes ===")
print(planes)
print("==== Pixels ===")
print(pixels)

