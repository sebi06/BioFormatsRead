# -*- coding: utf-8 -*-
"""
@author: Sebi

File: bftools.py
Date: 13.07.2015
Version. 1.7
"""


import javabridge as jv
import bioformats
import numpy as np
import czitools as czt
import os
import pandas as pd
from lxml import etree as etl
import sys

VM_STARTED = False
VM_KILLED = False

# define default path to bioformats_package.jar globally
BFPATH = 'bioformats_package.jar'

BF2NP_DTYPE = {
    0: np.int8,
    1: np.uint8,
    2: np.int16,
    3: np.uint16,
    4: np.int32,
    5: np.uint32,
    6: np.float32,
    7: np.double
}

# global default imageID
IMAGEID = 0

def set_bfpath(bfpackage_path=BFPATH):
    # this function can be used to set the path to the package individually
    global BFPATH
    BFPATH = bfpackage_path

    return BFPATH


def start_jvm(max_heap_size='4G'):

    """
    Start the Java Virtual Machine, enabling BioFormats IO.
    Optional: Specify the path to the bioformats_package.jar to your needs by calling.
    set_bfpath before staring to read the image data

    Parameters
    ----------
    max_heap_size : string, optional
    The maximum memory usage by the virtual machine. Valid strings
    include '256M', '64k', and '2G'. Expect to need a lot.
    """

    # TODO - include check for the OS, so that the file paths are always working

    jars = jv.JARS + [BFPATH]
    #jars = jv.JARS
    jv.start_vm(class_path=jars, max_heap_size=max_heap_size)
    VM_STARTED = True


def kill_jvm():
    """
    Kill the JVM. Once killed, it cannot be restarted.
    See the python-javabridge documentation for more information.
    """
    jv.kill_vm()
    VM_KILLED = True


def jvm_error():

    raise RuntimeError("The Java Virtual Machine has already been "
                       "killed, and cannot be restarted. See the "
                       "python-javabridge documentation for more "
                       "information. You must restart your program "
                       "and try again.")


def get_metadata_store(imagefile):

    if not VM_STARTED:
        start_jvm()
    if VM_KILLED:
        jvm_error()

    omexml = bioformats.get_omexml_metadata(imagefile)
    new_omexml = omexml.encode('utf-8')
    metadatastore = bioformats.OMEXML(new_omexml)
    xmlout = metadatastore.to_xml()

    return metadatastore, xmlout


def createOMEXML(imagefile):

    if not VM_STARTED:
        start_jvm()
    if VM_KILLED:
        jvm_error()

    omexml = bioformats.get_omexml_metadata(imagefile)
    new_omexml = omexml.encode('utf-8')

    return new_omexml


def get_java_metadata_store(imagefile):

    if not VM_STARTED:
        start_jvm()
    if VM_KILLED:
        jvm_error()

    rdr = bioformats.get_image_reader(None, path=imagefile)

    # for "whatever" reason the number of total series can only be accessed here ...
    try:
        totalseries = np.int(rdr.rdr.getSeriesCount())
    except:
        totalseries = 1  # in case there is only ONE series

    # rdr.rdr is the actual BioFormats reader. rdr handles its lifetime
    jmd = jv.JWrapper(rdr.rdr.getMetadataStore())

    imagecount = jmd.getImageCount()
    IMAGEID = imagecount - 1

    rdr.close()

    return jmd, totalseries, IMAGEID


def get_metainfo_dimension(jmd, MetaInfo):
    """
    Read the actual size for every dimension from the metadata
    and convert them into numbers.
    dimension order is returned as a string.
    """

    MetaInfo['SizeC'] = np.int(jmd.getPixelsSizeC(IMAGEID).getValue().floatValue())
    MetaInfo['SizeT'] = np.int(jmd.getPixelsSizeT(IMAGEID).getValue().floatValue())
    MetaInfo['SizeZ'] = np.int(jmd.getPixelsSizeZ(IMAGEID).getValue().floatValue())
    MetaInfo['SizeX'] = np.int(jmd.getPixelsSizeX(IMAGEID).getValue().floatValue())
    MetaInfo['SizeY'] = np.int(jmd.getPixelsSizeY(IMAGEID).getValue().floatValue())
    # get dimension order string from BioFormats library
    MetaInfo['DimOrder BF'] = jmd.getPixelsDimensionOrder(IMAGEID).getValue()

    print 'T: ', MetaInfo['SizeT'],  'Z: ', MetaInfo['SizeZ'],  'C: ', MetaInfo['SizeC'],  'X: ',\
        MetaInfo['SizeX'],  'Y: ', MetaInfo['SizeY']

    return MetaInfo


def get_metainfo_scaling(jmd):

    # get scaling for XYZ in micron
    xscale = np.round(jmd.getPixelsPhysicalSizeX(IMAGEID).value().floatValue(), 3)
    yscale = np.round(jmd.getPixelsPhysicalSizeY(IMAGEID).value().floatValue(), 3)

    # check if there is only one z-plane
    SizeZ = jmd.getPixelsSizeZ(IMAGEID).getValue().floatValue()
    if SizeZ > 1:
        zscale = np.round(jmd.getPixelsPhysicalSizeZ(IMAGEID).value().floatValue(), 3)
    else:
        # set z spacing equal to xy, if there is only one z-plane existing
        zscale = xscale

    return xscale, yscale, zscale


def get_metainfo_objective(jmd, filename):

    try:
        # get the correct objective ID (the objective that was used to acquire the image)
        instrumentID = np.int(jmd.getInstrumentID(IMAGEID)[-1])
        objID = np.int(jmd.getObjectiveSettingsID(instrumentID)[-1])
        # error handling --> sometime only one objective is there with ID > 0
        numobj = jmd.getObjectiveCount(instrumentID)
        if numobj == 1:
            objID = 0
    except:
        print 'No suitable instrument and objective ID found.'

    # try to get immersion type -  # get the first objective record in the first Instrument record
    try:
        objimm = jmd.getObjectiveImmersion(instrumentID, objID).getValue()
        #objimm = jmd.getObjectiveImmersion(instrumentID, objID)
    except:
        objimm = 'n.a'

    # try to get objective Lens NA
    try:
        objna = np.round(jmd.getObjectiveLensNA(instrumentID, objID).floatValue(), 3)
    except:
        objna = 'n.a.'

    # try to get objective magnification
    try:
        objmag = np.round(jmd.getObjectiveNominalMagnification(instrumentID, objID).floatValue(), 0)
    except:
        objmag = 'n.a.'

    # try to get objective model
    try:
        objmodel = jmd.getObjectiveModel(instrumentID, objID)
        if len(objmodel) == 0:
            objmodel = 'n.a'
            print 'No objective model name found in metadata.'
    except:
        print 'Try to read objective name via czifile.py'
        # this is a fallback option --> use cziread.py to get the information
        if filename[-4:] == '.czi':
            objmodel = czt.get_objective_name_cziread(filename)
            if objmodel == None:
                objmodel = 'n.a.'
        else:
            objmodel = 'n.a.'

    return objimm, objna, objmag, objmodel


def get_metainfo_pixeltype(jmd):

    pixtype = jmd.getPixelsType(0).getValue()

    return pixtype


def get_metainfo_numscenes(filename):
    """
    Currently the number of scenes cannot be read directly using BioFormats so
    czifile.py is used to determine the number of scenes.
    """
    czidim, cziorder = czt.readdimensions(filename)
    numscenes = czidim[1]

    return numscenes


def get_metainfo_wavelengths(jmd):

    SizeC = np.int(jmd.getPixelsSizeC(IMAGEID).getValue().floatValue())

    # initialize arrays for excitation and emission wavelength
    wl_excitation = np.zeros(SizeC)
    wl_emission = np.zeros(SizeC)
    dyes = []
    channels = []

    for i in range(0, SizeC):

        try:
            # new from bioformats_package.jar >= 5.1.1
            wl_excitation[i] = np.round(jmd.getChannelExcitationWavelength(IMAGEID, i).value().floatValue(), 0)
            wl_emission[i] = np.round(jmd.getChannelEmissionWavelength(IMAGEID, i).value().floatValue() ,0)
            dyes.append(str(jmd.getChannelFluor(IMAGEID, i)))
            channels.append(str(jmd.getChannelName(IMAGEID, i)))
        except:
            wl_excitation[i] = 0
            wl_emission[i] = 0
            dyes.append('n.a')
            channels.append('n.a.')

    return wl_excitation, wl_emission, dyes, channels


def get_dimension_only(imagefile):

    # get OME-XML and change the encoding to UTF-8
    omexml = bioformats.get_omexml_metadata(imagefile)
    new_omexml = omexml.encode('utf-8')

    rdr = bioformats.get_image_reader(None, path=imagefile)
    # read total number of image series
    totalseries = rdr.rdr.getSeriesCount()

    # get dimensions for CTZXY
    md = bioformats.OMEXML(new_omexml)
    pixels = md.image(IMAGEID).Pixels
    SizeC = pixels.SizeC
    SizeT = pixels.SizeT
    SizeZ = pixels.SizeZ
    SizeX = pixels.SizeX
    SizeY = pixels.SizeY

    print 'Series: ', totalseries, 'T: ', SizeT,  'Z: ', SizeZ,  'C: ', SizeC,  'X: ', SizeX,  'Y: ', SizeY

    # usually the x-axis of an image is from left --> right and y from top --> bottom
    # in order to be compatible with numpy arrays XY are switched
    # for numpy arrays the 2st axis are columns (top --> down) = Y-Axis for an image

    sizes = [totalseries, SizeT, SizeZ, SizeC, SizeY, SizeX]

    return sizes


def get_planetable(imagefile, writecsv=False, separator=','):

    MetaInfo = create_metainfo_dict()

    # get image meta-information
    #sz = get_dimension_only(imagefile)

    # get JavaMetaDataStore and SeriesCount
    jmd, MetaInfo['TotalSeries'], IMAGEID = get_java_metadata_store(imagefile)

    # get dimension information and MetaInfo
    MetaInfo = get_metainfo_dimension(jmd, MetaInfo)

    id = []
    plane = []
    xpos = []
    ypos = []
    zpos = []
    dt = []
    theC = []
    theZ = []
    theT = []

    print 'Start reading the plane data ',

    for imageIndex in range(0, IMAGEID):
        for planeIndex in range(0, MetaInfo['SizeZ'] * MetaInfo['SizeC'] * MetaInfo['SizeT']):

            id.append(imageIndex)
            plane.append(planeIndex)
            theC.append(jmd.getPlaneTheC(imageIndex, planeIndex).getValue().intValue())
            theZ.append(jmd.getPlaneTheZ(imageIndex, planeIndex).getValue().intValue())
            theT.append(jmd.getPlaneTheT(imageIndex, planeIndex).getValue().intValue())
            xpos.append(jmd.getPlanePositionX(imageIndex, planeIndex).value().doubleValue())
            ypos.append(jmd.getPlanePositionY(imageIndex, planeIndex).value().doubleValue())
            zpos.append(jmd.getPlanePositionZ(imageIndex, planeIndex).value().doubleValue())
            dt.append(jmd.getPlaneDeltaT(imageIndex, planeIndex).value().doubleValue())
            
            # optional detailed output
            #print id[-1], plane[-1], planeIndex, theT[-1], theZ[-1], theC[-1], xpos[-1], ypos[-1], zpos[-1], dt[-1]
            
        # create some kind of progress bar
        print '\b.',
        sys.stdout.flush()
        if np.mod(imageIndex, 50) == 0:
            print '\n'

    # just print an empty line
    print 'Done.\n'

    # round the data
    xpos = np.round(xpos, 1)
    ypos = np.round(ypos, 1)
    zpos = np.round(zpos, 1)
    dt = np.round(dt, 3)
    # normalize plane timings to 0 for the 1st acquired plane
    dt = dt - dt.min()

    # create Pandas dataframe to hold the plane data
    df = pd.DataFrame([np.asarray(id), np.asarray(plane), np.asarray(theT), np.asarray(theZ), np.asarray(theC), xpos, ypos, zpos, dt])
    df = df.transpose()
    # give the columns the correct names
    df.columns = ['IMAGEID', 'Plane', 'TheC', 'TheZ', 'TheC', 'XPos', 'YPos', 'ZPos', 'DeltaT']

    if writecsv:
        csvfile = imagefile[:-4] + '.csv'
        # use tab as separator and do not write the index to the CSV data table
        df.to_csv(csvfile, sep=separator, index=False)
        print 'Writing CSV file: ', csvfile

    return df


def get_image6d(imagefile, sizes):
    """
    This function will read the image data and store them into a 6D numpy array.
    The 6D array has the following dimension order: [Series, T, Z, C, X, Y].
    """
    if not VM_STARTED:
        start_jvm()
    if VM_KILLED:
        jvm_error()

    rdr = bioformats.ImageReader(imagefile, perform_init=True)

    #img6d = np.empty(sizes, dtype=BF2NP_DTYPE[rdr.rdr.getPixelType()])
    img6d = np.zeros(sizes, dtype=BF2NP_DTYPE[rdr.rdr.getPixelType()])

    # main loop to read the images from the data file
    for seriesID in range(0, sizes[0]):
        for timepoint in range(0, sizes[1]):
            for zplane in range(0, sizes[2]):
                for channel in range(0, sizes[3]):
                    img6d[seriesID, timepoint, zplane, channel, :, :] =\
                        rdr.read(series=seriesID, c=channel, z=zplane, t=timepoint, rescale=False)

    rdr.close()

    return img6d


def get_image2d(imagefile, sizes, seriesindex, channel, zplane, timepoint):
    """
    This will just read a single plane from an image data set.
    """
    if not VM_STARTED:
        start_jvm()
    if VM_KILLED:
        jvm_error()

    rdr = bioformats.ImageReader(imagefile, perform_init=True)
    img2d = rdr.read(series=seriesindex, c=channel, z=zplane, t=timepoint, rescale=False)

    rdr.close()

    return img2d


def get_zstack(imagefile, sizes, seriesID, timepoint):
    """
    This will read a single Z-Stack from an image data set.
    """
    if not VM_STARTED:
        start_jvm()
    if VM_KILLED:
        jvm_error()

    rdr = bioformats.ImageReader(imagefile, perform_init=True)

    # initialize array for specific series and time point that only contains a mutichannel z-Stack
    #imgZStack = np.empty([sizes[2], sizes[3], sizes[4], sizes[5]], dtype=BF2NP_DTYPE[rdr.rdr.getPixelType()])
    imgZStack = np.zeros([sizes[2], sizes[3], sizes[4], sizes[5]], dtype=BF2NP_DTYPE[rdr.rdr.getPixelType()])

    for zplane in range(0, sizes[2]):
        for channel in range(0, sizes[3]):
            imgZStack[zplane, channel, :, :] = rdr.read(series=seriesID, c=channel, z=zplane, t=timepoint, rescale=False)

    rdr.close()

    return imgZStack


def get_timeseries(imagefile, sizes, seriesID, zplane):
    """
    This will read a single Time Lapse from an image data set.
    """
    if not VM_STARTED:
        start_jvm()
    if VM_KILLED:
        jvm_error()

    rdr = bioformats.ImageReader(imagefile, perform_init=True)

    # initialize array for specific series and zplane that only contains a mutichannel time series
    #imgTimeSeries = np.empty([sizes[1], sizes[3], sizes[4], sizes[5]], dtype=BF2NP_DTYPE[rdr.rdr.getPixelType()])
    imgTimeSeries = np.zeros([sizes[1], sizes[3], sizes[4], sizes[5]], dtype=BF2NP_DTYPE[rdr.rdr.getPixelType()])

    for timepoint in range(0, sizes[2]):
        for channel in range(0, sizes[3]):
            imgTimeSeries[timepoint, channel, :, :] = rdr.read(series=seriesID, c=channel, z=zplane, t=timepoint, rescale=False)

    rdr.close()

    return imgTimeSeries


def get_imageseries(imagefile, sizes, seriesID=0):

    if not VM_STARTED:
        start_jvm()
    if VM_KILLED:
        jvm_error()

    rdr = bioformats.ImageReader(imagefile, perform_init=True)

    # initialize an array with the correct dimensions of one series only
    #imgseries = np.empty(sizes[1:], dtype=BF2NP_DTYPE[rdr.rdr.getPixelType()])
    imgseries = np.zeros(sizes[1:], dtype=BF2NP_DTYPE[rdr.rdr.getPixelType()])

    for timepoint in range(0, sizes[1]):
        for zplane in range(0, sizes[2]):
            for channel in range(0, sizes[3]):
                imgseries[seriesID, timepoint, zplane, channel, :, :] = rdr.read(series=seriesID, c=channel, z=zplane, t=timepoint, rescale=False)

    rdr.close()

    return imgseries


def get_series_from_well(imagefile, sizes, seriesseq):
    """
    Reads all scenes from a single well and stores them in a array.
    """
    if not VM_STARTED:
        start_jvm()
    if VM_KILLED:
        jvm_error()

    rdr = bioformats.ImageReader(imagefile, perform_init=True)
    sizes[0] = len(seriesseq)

    #img6dwell = np.empty(sizes, dtype=BF2NP_DTYPE[rdr.rdr.getPixelType()])
    img6dwell = np.zeros(sizes, dtype=BF2NP_DTYPE[rdr.rdr.getPixelType()])

    for seriesID in range(0, len(seriesseq)):
        for timepoint in range(0, sizes[1]):
            for zplane in range(0, sizes[2]):
                for channel in range(0, sizes[3]):
                    img6dwell[seriesID, timepoint, zplane, channel, :, :] =\
                        rdr.read(series=seriesID, c=channel,z=zplane, t=timepoint, rescale=False)

    rdr.close()

    return img6dwell


def create_metainfo_dict():

    """
    A Python dictionary will be created to hold the relevant Metadata.
    """

    MetaInfo = {'Directory': '',
                'Filename': '',
                'TotalSeries': 0,
                'SizeX': 0,
                'SizeY': 0,
                'SizeZ': 0,
                'SizeC': 0,
                'SizeT': 0,
                'DimOrder BF': 'n.a',
                'Immersion': 'n.a.',
                'NA': 0,
                'ObjMag': 0,
                'ObjModel': 'n.a.',
                'ShapeCZI': 0,
                'OrderCZI': 0,
                'DetName': 'n.a',
                'XScale': 0,
                'YScale': 0,
                'ZScale': 0,
                'WLEx': 0,
                'WLEm': 0,
                'Dyes': [],
                'Channels': [],
                'ChDesc': 'n.a.',
                'Sizes': 0}

    return MetaInfo


def get_relevant_metainfo_wrapper(filename):

    MetaInfo = create_metainfo_dict()

    MetaInfo['Directory'] = os.path.dirname(filename)
    MetaInfo['Filename'] = os.path.basename(filename)

    # get JavaMetaDataStore and SeriesCount
    jmd, MetaInfo['TotalSeries'], IMAGEID = get_java_metadata_store(filename)

    # get dimension information and MetaInfo
    MetaInfo = get_metainfo_dimension(jmd, MetaInfo)

    if filename[-4:] == '.czi':
        # get objective information using cziread
        print 'Using czifile.py to get CZI Shape info.'

        MetaInfo['ShapeCZI'], MetaInfo['OrderCZI'] = czt.get_shapeinfo_cziread(filename)
        # currently not used any more --> trust BioFormtas instead
        #MetaInfo['NA'], MetaInfo['ObjMag'], MetaInfo['ObjModel'],MetaInfo['Immersion'],\
        #    MetaInfo['DetName'], MetaInfo['TotalMag'] = czt.get_metainfo_cziread(filename)

    # use bioformats to get the objective informations
    print 'Using BioFormats to get MetaInfo.'
    MetaInfo['Immersion'], MetaInfo['NA'], MetaInfo['ObjMag'], MetaInfo['ObjModel'] = get_metainfo_objective(jmd, filename)

    # get scaling information
    MetaInfo['XScale'], MetaInfo['YScale'], MetaInfo['ZScale'] = get_metainfo_scaling(jmd)

    # get wavelengths and dyes information
    MetaInfo['WLEx'], MetaInfo['WLEm'], MetaInfo['Dyes'], MetaInfo['Channels'] = get_metainfo_wavelengths(jmd)

    # get channel description
    MetaInfo['ChDesc'] = czt.get_metainfo_channel_description(filename)

    # summarize dimensions
    MetaInfo['Sizes'] = [MetaInfo['TotalSeries'], MetaInfo['SizeT'], MetaInfo['SizeZ'],
                         MetaInfo['SizeC'], MetaInfo['SizeY'], MetaInfo['SizeX']]

    return MetaInfo


def calc_series_range(total_series, scenes, sceneID):

    sps = total_series / scenes  # series_per_scence = sps
    series_seq = range(sceneID * sps - sps, sps * sceneID)

    return series_seq


def calc_series_range_well(wellnumber, imgperwell):
    """
    This function can be used when the number of positions or scenes
    per well is equal for every well
    The well numbers start with Zero and have nothing to do with the actual wellID, e.g. C2
    """
    seriesseq = range(wellnumber * imgperwell,  wellnumber * imgperwell + imgperwell, 1)

    return seriesseq


def create_omexml(testdata, method=1, writeczi_metadata=True):

    # creates readable xml files from image data files. Default method should be = 1.
    if method == 1:
        # method 1
        for i in range(0, len(testdata)):

            # Change File name and write XML file to same folder
            xmlfile1 = testdata[i] + '_MetaData1.xml'

            try:
                # get the actual OME-XML
                omexml = createOMEXML(testdata[i])
                # create root and tree from XML string and write "pretty" to disk
                root = etl.fromstring(omexml)
                tree = etl.ElementTree(root)
                tree.write(xmlfile1, pretty_print=True, encoding='utf-8', method='xml')
                print 'Created OME-XML file for testdata: ', testdata[i]
            except:
                print 'Creating OME-XML failed for testdata: ', testdata[i]

    if method == 2:

        # method 2
        for i in range(0, len(testdata)):

            # Change File name and write XML file to same folder
            xmlfile2 = testdata[i] + '_MetaData2.xml'

            try:
                # get the actual OME-XML
                md, omexml = get_metadata_store(testdata[i])
                # create root and tree from XML string and write "pretty" to disk
                root = etl.fromstring(omexml)
                tree = etl.ElementTree(root)
                tree.write(xmlfile2, pretty_print=True, encoding='utf-8', method='xml')
                print 'Created OME-XML file for testdata: ', testdata[i]
            except:
                print 'Creating OME-XML failed for testdata: ', testdata[i]

    if writeczi_metadata:

        # this writes the special CZI xml metadata to disk, when a CZI file was found.
        for i in range(0, len(testdata)):

            if testdata[i][-4:] == '.czi':
                try:
                    czt.writexml_czi(testdata[i])
                except:
                    print 'Could not write special CZI metadata for: ', testdata[i]
