# -*- coding: utf-8 -*-
"""
@author: Sebi

File: test_wellinfo.py
Date: 26.03.2017
Version. 0.3
"""

from __future__ import print_function
import bftools as bf

filename = r'testdata/B4_B5_S=8_4Pos_perWell_T=2_Z=1_CH=1.czi'

# use for BioFormtas <= 5.1.10
#urlnamespace = 'http://www.openmicroscopy.org/Schemas/OME/2015-01'
# use for BioFormtas > 5.2.0
ns='{http://www.openmicroscopy.org/Schemas/SA/2016-06}'

# specify bioformats_package.jar to use if required
bfpackage = r'bioformats_package/5.4.1/bioformats_package.jar'
bf.set_bfpath(bfpackage)

wellstr = bf.getWelllNamesfromCZI(filename, namespace=ns)
welllist, cols, rows, welldict, numdiffwells = bf.processWellStringfromCZI(wellstr)
well2check = 'B4'
isids = bf.getImageSeriesIDforWell(welllist, well2check)

print('WellString          : ', wellstr)
print('WellList            : ', welllist)
print('Well Column Indices : ', cols)
print('Well Row Indices    : ', rows)
print('WellCounter         : ', welldict)
print('Different Wells     : ', numdiffwells)
print('ImageSeries Ind. Well ', well2check, ' : ', isids)
