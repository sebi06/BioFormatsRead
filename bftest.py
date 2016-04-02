# -*- coding: utf-8 -*-
"""
@author: Sebi

File: test_get_image6d.py
Date: 03.02.2016
Version. 1.0
"""

import numpy as np
import os
import bfimage as bf


def func(filename):

    imgdir = os.path.dirname(filename)
    imgbase = os.path.basename(filename)

    return imgbase, imgdir

def test_basic_filenames():

    filename = r'testdata/Beads_63X_NA1.35_xy=0.042_z=0.1.czi'

    ib, id = func(filename)
    print '!!!'
    assert ib == os.path.basename(filename)
    assert id == os.path.dirname(filename)


def test_metainfo():

    filename = r'testdata/Beads_63X_NA1.35_xy=0.042_z=0.1.czi'

    # get image meta-information
    MetaInfo = bf.get_relevant_metainfo_wrapper(filename)
    img6d = bf.get_image6d(filename, MetaInfo['Sizes'])

    # check Sizes
    assert MetaInfo['Sizes'] == [1, 1, 100, 1, 346, 580]
    # check Dimension Order
    assert MetaInfo['DimOrder BF'] == 'XYCZT'
    # check Dimesnion Order CZI Style
    assert MetaInfo['OrderCZI'] == 'BCZYX0'
    # check Image Dimensions
    assert MetaInfo['TotalSeries'] == 1
    assert MetaInfo['SizeT'] == 1
    assert MetaInfo['SizeZ'] == 100
    assert MetaInfo['SizeC'] == 1
    assert MetaInfo['SizeY'] == 346
    assert MetaInfo['SizeX'] == 580
    # check Scaling
    assert MetaInfo['XScale'] == 0.042
    assert MetaInfo['YScale'] == 0.042
    assert MetaInfo['ZScale'] == 0.1
    # check Objective Data
    assert MetaInfo['ObjMag'] == 63.0
    assert MetaInfo['NA'] == 1.4
    assert MetaInfo['Immersion'] == 'Oil'
    # check objective Name
    assert MetaInfo['ObjModel'] == 'na'
    # check Excitation and Emission Wavelengths
    assert MetaInfo['WLEx'] == 493
    assert MetaInfo['WLEm'] == 517
    # check Dye Names
    assert MetaInfo['Dyes'] == ['Dye1']
    # check Channels
    assert MetaInfo['Channels'] == ['Alexa Fluor 488']
    # check Channel Description
    assert MetaInfo['ChDesc'] == []
    # check Numpy Array Shape
    dims = [1, 1, 100, 1, 346, 580]
    for i in range(0, len(dims)):
        assert np.shape(img6d)[i] == dims[i]


#test_metainfo()