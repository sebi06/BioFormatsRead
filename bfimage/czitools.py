# -*- coding: utf-8 -*-
"""
@author: Sebi

File: czitools.py
Date: 09.06.2015
Version. 0.8
"""

import misctools as misc
from czifile import *
import numpy as np


def get_metainfo_channel_description(filename):

    try:
        czi = CziFile(filename)
        namelst = []
        valuelst = []
        # get root tree of CZI metadata (uses ElementTree)

        for elem in czi.metadata.getiterator():

            namelst.append(elem.tag)
            valuelst.append(elem.text)

        # get the channel descriptions
        ids = misc.find_index_byname(namelst, 'Description')
        chdescript = misc.get_entries(valuelst, ids)

        czi.close()

    except:
        chdescript = 'n.a.'

    return chdescript


def writexml_czi(filename):

    # write xml file to disk
    czi = CziFile(filename)

    # Change File name and write XML file to same folder
    xmlfile = filename.replace('.bfimage', '_MetaData.xml')
    tree = czi.metadata.getroottree()
    tree.write(xmlfile, encoding='utf-8', method='xml')
    print 'XML metadata : ', xmlfile

    czi.close()


def get_objective_name_cziread(filename):

    czi = CziFile(filename)
    namelst = []
    valuelst = []
    # get root tree of CZI metadata (uses ElementTree)

    for elem in czi.metadata.getiterator():

        namelst.append(elem.tag)
        valuelst.append(elem.text)

    # get the channel descriptions
    try:
        ids = misc.find_index_byname(namelst, 'ObjectiveName')
        objname = misc.get_entries(valuelst, ids)
    except:
        objname = 'n.a.'

    czi.close()


def read_dimensions_czi(filename):

    # Read the dimensions of the image stack and their order
    czi = CziFile(filename)
    czishape = czi.shape
    cziorder = czi.axes
    czi.close()

    return czishape, cziorder


def get_shapeinfo_cziread(filename):
    # get CZI shape and dimension order using czifile.py

    try:
        czi = CziFile(filename)
        czishape = czi.shape
        cziorder = czi.axes

        czi.close()

    except:

        print 'czifile.py did not detect an CZI file.'
        czishape = 'unknown'
        cziorder = 'unknown'

    return czishape, cziorder


def get_metainfo_cziread(filename):

    # define default values in case something is missing inside the metadata
    objNA = np.NaN
    objMag = np.NaN
    objName = 'n.a.'
    objImm = 'n.a.'
    CamName = 'n.a.'
    totalMag = np.NaN

    try:
        czi = CziFile(filename)

        # Iterate over the metadata
        for elem in czi.metadata.getiterator():

            if elem.tag == 'LensNA':
                objNA = np.float(elem.text)

            if elem.tag == 'NominalMagnification':
                objMag = elem.text

            if elem.tag == 'ObjectiveName':
                objName = elem.text

            if elem.tag == 'Immersion':
                objImm = elem.text

            if elem.tag == 'CameraName':
                CamName = elem.text

            if elem.tag == 'TotalMagnification':
                totalMag = np.float(elem.text)
                if totalMag == 0:
                    totalMag == 'n.a.'

        czi.close()

    except:

        print 'czifile.py did not detect an CZI file.'
        czishape = 'unknown'
        cziorder = 'unknown'

    return objNA, objMag, objName, objImm, CamName, totalMag


def get_metainfo_cziread_camera(filename):

    czi = CziFile(filename)

    # Iterate over the metadata
    for elem in czi.metadata.getiterator():

        if elem.tag == 'CameraName':
            CamName = elem.text

    czi.close()

    return CamName


def convert_dimension_string(cziorder):
    """

    EXPERIMENTAL !!!

    Read the actual dimension order from the CZI file via czifile.py, NOT BioFormats.
    The order will be converted to the standard ordering scheme of Bioformats, e.g. XYCZT or XYZCT etc.
    """

    # TODO - Experimental - Can this be removed?

    # get number of dimensions of CZI file and create empty list
    numdimczi = len(cziorder)
    dimorder = [None] * 5
    # first two dimension strings are always XY
    dimorder[0] = 'X'
    dimorder[1] = 'Y'
    # read next 3 dimension strings from the back after XY and store them into the list
    dimorder[2] = str(cziorder[numdimczi - 3 - 1])
    dimorder[3] = str(cziorder[numdimczi - 4 - 1])
    dimorder[4] = str(cziorder[numdimczi - 5 - 1])
    if dimorder[3] != 'Z' or dimorder[3] != 'T':
        dimorder[3] = 'Z'
    if dimorder[4] != 'Z' or dimorder[4] != 'T':
        dimorder[4] = 'T'

    # concatenate the complete dimension string from list elements
    dims = dimorder[0]+dimorder[1]+dimorder[2]+dimorder[3]+dimorder[4]

    return dims


