# -*- coding: utf-8 -*-
"""
@author: Sebi

File: bftools.py
Date: 18.05.2015
Version. 1.4

The code is partially based on the project lesion by Juan Nunez-Iglesias:

https://github.com/jni/lesion
"""


import javabridge as jv
import bioformats
import numpy as np
import czitools as czt
import os

VM_STARTED = False
VM_KILLED = False

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


def start_jvm(max_heap_size='4G'):

    """
    Start the Java Virtual Machine, enabling BioFormats IO.

    Parameters
    ----------
    max_heap_size : string, optional
        The maximum memory usage by the virtual machine. Valid strings
        include '256M', '64k', and '2G'. Expect to need a lot.
    """
    #path = r'C:\Users\Sebastian\Dropbox\BioFormats\5.1.1\bioformats_package.jar'
    path = r'C:\Users\M1SRH\Documents\Software\BioFormats_Package\5.1.1\bioformats_package.jar'
    jars = jv.JARS + [path]
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

    return metadatastore


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

    rdr.close()

    return jmd, totalseries


def get_metainfo_dimension(jmd, MetaInfo):
    """
    Read the actual size for every dimension from the metadata
    and convert them into numbers.
    dimension order is returned as a string.
    """

    MetaInfo['SizeC'] = np.int(jmd.getPixelsSizeC(0).getValue().floatValue())
    MetaInfo['SizeT'] = np.int(jmd.getPixelsSizeT(0).getValue().floatValue())
    MetaInfo['SizeZ'] = np.int(jmd.getPixelsSizeZ(0).getValue().floatValue())
    MetaInfo['SizeX'] = np.int(jmd.getPixelsSizeX(0).getValue().floatValue())
    MetaInfo['SizeY'] = np.int(jmd.getPixelsSizeY(0).getValue().floatValue())
    # get dimension order string from BioFormats library
    MetaInfo['DimOrder BF'] = jmd.getPixelsDimensionOrder(0).getValue()

    print 'T: ', MetaInfo['SizeT'],  'Z: ', MetaInfo['SizeZ'],  'C: ', MetaInfo['SizeC'],  'X: ',\
        MetaInfo['SizeX'],  'Y: ', MetaInfo['SizeY']

    return MetaInfo


def get_metainfo_scaling(jmd):

    # get scaling for XYZ in micron
    xscale = np.round(jmd.getPixelsPhysicalSizeX(0).value().floatValue(), 3)
    yscale = np.round(jmd.getPixelsPhysicalSizeY(0).value().floatValue(), 3)

    # check if there is only one z-plane
    SizeZ = jmd.getPixelsSizeZ(0).getValue().floatValue()
    if SizeZ > 1:
        zscale = np.round(jmd.getPixelsPhysicalSizeZ(0).value().floatValue(), 3)
    else:
        # set z spacing equal to xy, if there is only one z-plane existing
        zscale = xscale

    return xscale, yscale, zscale


def get_metainfo_objective(jmd, filename):

    # try to get immersion type -  # get the first objective record in the first Instrument record
    try:
        objimm = jmd.getObjectiveImmersion(0, 0).getValue()
    except:
        objimm = 'n.a'

    # try to get objective Lens NA
    try:
        objna = np.round(jmd.getObjectiveLensNA(0, 0).floatValue(), 2)
    except:
        objna = 'n.a.'

    # try to get objective magnification
    try:
        objmag = np.round(jmd.getObjectiveNominalMagnification(0, 0).floatValue(), 0)
    except:
        objmag = 'n.a.'

    # try to get objective model
    try:
        objmodel = jmd.getObjectiveModel(0, 0).getValue()
    except:
        # this is a fallback option --> use cziread.py to get the information
        objmodel = czt.get_objective_name_cziread(filename)


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

    SizeC = np.int(jmd.getPixelsSizeC(0).getValue().floatValue())

    # initialize arrays for excitation and emission wavelength
    wl_excitation = np.zeros(SizeC)
    wl_emission = np.zeros(SizeC)

    for i in range(0, SizeC):

        try:
            # new from bioformats_package.jar >= 5.1.1
            wl_excitation[i] = jmd.getChannelExcitationWavelength(0, i).value().floatValue()
            wl_emission[i] = jmd.getChannelEmissionWavelength(0, i).value().floatValue()
        except:
            wl_excitation[i] = 0
            wl_emission[i] = 0

    return wl_excitation, wl_emission


def get_objective_model(jmd):

    # try to get the objective model
    try:
        objmodel = jmd.getObjectiveModel(0, 0).getValue()
    except:
        objmodel = 'n.a.'

    return objmodel


def get_dimension_only(imagefile):

    # get OME-XML and change the encoding to UTF-8
    omexml = bioformats.get_omexml_metadata(imagefile)
    new_omexml = omexml.encode('utf-8')

    rdr = bioformats.get_image_reader(None, path=imagefile)
    # read total number of image series
    totalseries = rdr.rdr.getSeriesCount()

    # get dimensions for CTZXY
    md = bioformats.OMEXML(new_omexml)
    pixels = md.image(0).Pixels
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


def get_image6d(imagefile, sizes):
    """
    This function will read the image data and store them into a 6D numpy array.
    The 6D array has the following dimension order: [Series, T, Z, C, X, X].
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


def get_relevant_metainfo_wrapper(filename):
    """
    A Python dictionary will be created to hold the relevant Metadata.
    """

    MetaInfo = {'Directory': os.path.dirname(filename),
                'Filename': os.path.basename(filename),
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
                'TotalMag': 0,
                'ObjModel': 'n.a.',
                'ShapeCZI': 0,
                'OrderCZI': 0,
                'DetName': 'n.a',
                'XScale': 0,
                'YScale': 0,
                'ZScale': 0,
                'WLEx': 0,
                'WLEm': 0,
                'ChDesc': 'n.a.',
                'Sizes': 0}

    # get JavaMetaDataStore and SeriesCount
    jmd, MetaInfo['TotalSeries'] = get_java_metadata_store(filename)

    # get dimension information and MetaInfo
    MetaInfo = get_metainfo_dimension(jmd, MetaInfo)

    # get objective information
    MetaInfo['NA'], MetaInfo['ObjMag'], MetaInfo['ObjModel'],MetaInfo['Immersion'],\
        MetaInfo['DetName'], MetaInfo['TotalMag'], MetaInfo['ShapeCZI'], MetaInfo['OrderCZI'] = czt.get_metainfo_cziread(
        filename)

    # get scaling information
    MetaInfo['XScale'], MetaInfo['YScale'], MetaInfo['ZScale'] = get_metainfo_scaling(jmd)

    # get wavelengths information
    MetaInfo['WLEx'], MetaInfo['WLEm'] = get_metainfo_wavelengths(jmd)

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
