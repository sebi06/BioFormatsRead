# -*- coding: utf-8 -*-
"""
@author: Sebi

File: test_bfread.py
Date: 08.04.2016
Version. 0.5
"""

import numpy as np
import os
import bfimage as bf
import pytest


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


def test_timeseries():

    filename = r'testdata/T=5_Z=3_CH=2_CZT_All_CH_per_Slice.czi'
    # get image meta-information
    MetaInfo = bf.bftools.get_relevant_metainfo_wrapper(filename)
    seriesID = 0
    timepoint = 2
    channel = 1
    zplane = 2
    dims = [5, 2, 640, 640]
    # get the actual time series from the data set
    tseries = bf.bftools.get_timeseries(filename, MetaInfo['Sizes'], seriesID, zplane)

    for i in range(0, len(dims)):
        assert np.shape(tseries)[i] == dims[i]


def test_zstack():

    filename = r'testdata/Beads_63X_NA1.35_xy=0.042_z=0.1.czi'
    # get image meta-information
    MetaInfo = bf.bftools.get_relevant_metainfo_wrapper(filename)
    seriesID = 0
    timepoint = 0
    channel = 0
    dims = [100, 1, 346, 580]
    # get the actual z-stack from the data set
    zstack = bf.bftools.get_zstack(filename, MetaInfo['Sizes'], seriesID, timepoint)

    # get plane with the brightest pixel
    zplane = (zstack == zstack.max()).nonzero()[0][0]
    # check found zplane
    assert zplane == 46

    for i in range(0, len(dims)):
        assert np.shape(zstack)[i] == dims[i]

def test_getdimonly():

    filename = r'testdata/2x2_SNAP_CH=2_Z=5_T=2.czi'

    sizes_czi = bf.czitools.read_dimensions_czi(filename)

    dims = [1, 1, 2, 2, 5, 1216, 1216, 1]
    dimorder = 'BSTCZYX0'

    for i in range(0, len(dims)):
        assert sizes_czi[0][i] == dims[i]

    assert sizes_czi[1] == dimorder


if __name__ == '__main__':
    pytest.main()
