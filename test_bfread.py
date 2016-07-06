# -*- coding: utf-8 -*-
"""
@author: Sebi

File: test_bfread.py
Date: 08.04.2016
Version. 0.6
"""

import numpy as np
import os
import bfimage as bf
import pytest
import datetime
import zencom as zc


def setbfpath():

    # specify bioformats_package.jar to use if required
    bfpath = r'bioformats_package.jar'
    bf.set_bfpath(bfpath)

def get_filename():
    filename = r'c:\Users\M1SRH\Documents\Python_Projects\BioFormatsRead\20160425_BF_CZI.czi'
    return filename

def get_dims():
    #return [16, 3, 5, 2, 640, 640]
    return [16, 1, 1, 2, 640, 640]

def get_chwlex():
    return [493, 553]

def get_chwlem():
    return [517, 568]

def get_dyes():
    return ['None', 'None']

def get_chnames():
    return ['AF488', 'AF555']


def create_testCZI():

    # Define the experiment to be executed
    zenexperiment = r'e:\Data\BioFormats_CZI_Test\BioFormats_CZI_Test.czexp'

    # get current data and create filename from it
    today = datetime.datetime.today()
    currentCZI = today.strftime('%Y%m%d') + '_BF_CZI.czi'

    # Define place to store the CZI file
    savefolder = 'e:\\Data\BioFormats_CZI_Test\\' + today.strftime('%Y%m%d') + '\\'

    # check if the folder already exists
    try:
        os.makedirs(savefolder)
    except OSError:
        if not os.path.isdir(savefolder):
            raise

    czifilename_complete = zc.runZenExperiment(zenexperiment, savefolder, currentCZI, showCZI=False)

    # create the xml information - expects list of filenames as input
    bf.create_omexml([czifilename_complete], method=1, writeczi_metadata=True)

    # create plane info table and write into dataframe
    df = bf.get_planetable(czifilename_complete, writecsv=True, separator='\t')

    # show the dataframe
    print df[:5]
    print df.shape[0]

    return czifilename_complete



def test_metainfo():

    # run the test experiment to create the CZI test data set
    czifilename_complete = create_testCZI()

    # set the correct path to the bioformats_package.jar
    setbfpath()

    # get image meta-information
    MetaInfo = bf.get_relevant_metainfo_wrapper(czifilename_complete)
    img6d = bf.get_image6d(czifilename_complete, MetaInfo['Sizes'])

    fulldims = get_dims()
    print MetaInfo['Sizes']

    # check Sizes
    assert MetaInfo['Sizes'] == fulldims
    # check Dimension Order
    assert MetaInfo['DimOrder BF'] == 'XYCZT'
    # check Dimesnion Order CZI Style
    assert MetaInfo['OrderCZI'] == 'BSTCZYX0'
    # check Image Dimensions
    assert MetaInfo['TotalSeries'] == fulldims[0]
    assert MetaInfo['SizeT'] == fulldims[1]
    assert MetaInfo['SizeZ'] == fulldims[2]
    assert MetaInfo['SizeC'] == fulldims[3]
    assert MetaInfo['SizeY'] == fulldims[4]
    assert MetaInfo['SizeX'] == fulldims[5]
    # check Scaling
    assert MetaInfo['XScale'] == 0.2
    assert MetaInfo['YScale'] == 0.2
    assert MetaInfo['ZScale'] == 0.5
    # check Objective Data
    assert MetaInfo['ObjMag'] == 5.0
    assert MetaInfo['NA'] == 0.35
    assert MetaInfo['Immersion'] == 'Air'
    # check objective Name
    assert MetaInfo['ObjModel'] == 'Plan-Apochromat 5x/0.35'

    # check properties of all channels
    for ch in range(0, MetaInfo['SizeC']):
        # check Excitation and Emission Wavelengths
        assert MetaInfo['WLEx'][ch] == get_chwlex()[ch]
        assert MetaInfo['WLEm'][ch] == get_chwlem()[ch]
        # check Dye Names
        assert MetaInfo['Dyes'][ch] == get_dyes()[ch]
        assert MetaInfo['Channels'][ch] == get_chnames()[ch]
    # check Channel Description
    assert MetaInfo['ChDesc'] == []
    # check Numpy Array Shape
    for i in range(0, len(fulldims)):
        assert np.shape(img6d)[i] == fulldims[i]


    # test timeseries

    seriesID = 0
    zplane = 2
    dims = [3, 2, 640, 640]
    # get the actual time series from the data set
    tseries, dimorder_out = bf.bftools.get_timeseries(czifilename_complete, MetaInfo['Sizes'], seriesID, zplane=zplane)

    for i in range(0, len(dims)):
        assert np.shape(tseries)[i] == dims[i]

    # check resulting dimension order
    assert dimorder_out == 'TCXY'


    # test zstack

    seriesID = 0
    timepoint = 0
    dims = [5, 2, 640, 640]
    # get the actual z-stack from the data set
    zstack, dimorder_out = bf.bftools.get_zstack(czifilename_complete, MetaInfo['Sizes'], seriesID, timepoint=timepoint)
    print zstack.shape

    # get plane with the brightest pixel
    zplane = (zstack == zstack.max()).nonzero()[0][0]
    # check found zplane
    assert zplane+1 == 1

    for i in range(0, len(dims)):
        assert np.shape(zstack)[i] == dims[i]


    # test getdimonly:

    sizes_czi = bf.czitools.read_dimensions_czi(czifilename_complete)

    dims = [1, 4, 3, 2, 5, 1216, 136216, 1]
    dimorder = 'BSTCZYX0'

    for i in range(0, len(dims)):
        assert sizes_czi[0][i] == dims[i]

    assert sizes_czi[1] == dimorder


if __name__ == '__main__':
    pytest.main()
