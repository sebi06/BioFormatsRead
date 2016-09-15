# -*- coding: utf-8 -*-
"""
@author: Sebi

File: test_get_image6d.py
Date: 14.09.2016
Version. 1.1
"""

import numpy as np
import os
import bfimage as bf
import sys

#filename = r'testdata/Beads_63X_NA1.35_xy=0.042_z=0.1.czi'
#filename = r'testdata/T=5_Z=3_CH=2_CZT_All_CH_per_Slice.czi'
filename = r'testdata/B4_B5_S=8_4Pos_perWell_T=2_Z=1_CH=1.czi'

# use for BioFormtas <= 5.1.10
urlnamespace = 'http://www.openmicroscopy.org/Schemas/OME/2015-01'
# use for BioFormtas > 5.2.0
#urlnamespace = 'http://www.openmicroscopy.org/Schemas/OME/2016-06'

redirect = False

if redirect:
    # redirect output
    orig_stdout = sys.stdout
    filepath_output = os.path.join(os.getcwd(), 'test_get_image6d_output.txt')
    f = file(filepath_output, 'w')
    sys.stdout = f

# specify bioformats_package.jar to use if required
bfpackage = r'BioFormats/5.1.10/bioformats_package.jar'
bf.set_bfpath(bfpackage)

# get image meta-information
MetaInfo = bf.bftools.get_relevant_metainfo_wrapper(filename, namespace=urlnamespace)
img6d = bf.bftools.get_image6d(filename, MetaInfo['Sizes'])

# show relevant image Meta-Information
print '\n'
print 'Testscript used      :  test_get_image6d.py'
print 'OME NameSpace used   : ', urlnamespace
print 'BF Version used      : ', bfpackage
print '-------------------------------------------------------------'
print 'Image Directory      : ', MetaInfo['Directory']
print 'Image Filename       : ', MetaInfo['Filename']
print 'Images Dim Sizes     : ', MetaInfo['Sizes']
print 'Dimension Order BF   : ', MetaInfo['DimOrder BF']
print 'Dimension Order CZI  : ', MetaInfo['OrderCZI']
print 'Shape CZI            : ', MetaInfo['ShapeCZI']
print 'Total Series Number  : ', MetaInfo['TotalSeries']
print 'Image Dimensions     : ', MetaInfo['TotalSeries'], MetaInfo['SizeT'], MetaInfo['SizeZ'], MetaInfo['SizeC'],\
                                    MetaInfo['SizeY'], MetaInfo['SizeX']
print 'Scaling XYZ [micron] : ', MetaInfo['XScale'], MetaInfo['YScale'], MetaInfo['ZScale']
print 'Objective M-NA-Imm   : ', MetaInfo['ObjMag'], MetaInfo['NA'], MetaInfo['Immersion']
print 'Objective Name       : ', MetaInfo['ObjModel']
print 'Ex. Wavelengths [nm] : ', MetaInfo['WLEx']
print 'Em. Wavelengths [nm] : ', MetaInfo['WLEm']
print 'Dyes                 : ', MetaInfo['Dyes']
print 'Detector Model       : ', MetaInfo['Detector Model']
print 'Detector Name        : ', MetaInfo['Detector Name']
print 'Detector ID          : ', MetaInfo['DetectorID']
print 'Channels             : ', MetaInfo['Channels']
print 'Channel Description  : ', MetaInfo['ChDesc']
print 'ImageIDs             : ', MetaInfo['ImageIDs']
print 'Array Shape 6D       : ', np.shape(img6d)

if redirect:
    sys.stdout = orig_stdout
    f.close()
    sys.__stdout__
    print 'Output written to : ', filepath_output
