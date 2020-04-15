# -*- coding: utf-8 -*-
"""
@author: Sebi
File: test_get_image6d.py
Date: 01.03.2019
Version. 1.9
"""
import os
import numpy as np
import bftools as bf
from matplotlib import pyplot as plt, cm
import dispvalues as dsv

showimage = True
writeimage = False

imgdict = {
    1: r'C:\Users\m1srh\Documents\Testdata_Zeiss\Castor\Z-Stack_DCV\CellDivision_T=10_Z=15_CH=2_DCV_small.czi',
    2: r'C:\Users\m1srh\Documents\Testdata_Zeiss\Castor\Z-Stack_DCV\CellDivision_T=10_Z=15_CH=2_DCV_small.ome.tiff',
    3: r'C:\Users\m1srh\Documents\Testdata_Zeiss\Castor\Z-Stack_DCV\CellDivision_T=10_Z=15_CH=2_DCV_small_Fiji.ome.tiff',
    4: r'C:\Users\m1srh\Documents\Testdata_Zeiss\Castor\Z-Stack_DCV\CellDivision_T=15_Z=20_CH=2_DCV.czi',
    5: r'C:\Users\m1srh\Documents\Testdata_Zeiss\Castor\Z-Stack_DCV\NeuroSpheres_DCV_A635_A488_A405.czi',
    6: r'C:\Users\m1srh\Documents\Testdata_Zeiss\Castor\Z-Stack_DCV\NeuroSpheres_DCV_A635_A488_A405.ome.tiff',
    7: r'C:\Users\m1srh\Documents\Testdata_Zeiss\Castor\Z-Stack_DCV\NeuroSpheres_DCV_A635_A488_A405_fromFiji.ome.tiff',
    8: r'C:\Users\m1srh\Documents\Testdata_Zeiss\Castor\Z-Stack_DCV\CZI_DimorderTZC.czi'
}

filename = imgdict[7]

# filename = r'testdata/Beads_63X_NA1.35_xy=0.042_z=0.1.czi'
#filename = r'testdata/B4_B5_S=8_4Pos_perWell_T=2_Z=1_CH=1.czi'


# use for BioFormtas <= 5.1.10
# urlnamespace = 'http://www.openmicroscopy.org/Schemas/OME/2015-01'
# use for BioFormtas > 5.2.0
urlnamespace = 'http://www.openmicroscopy.org/Schemas/OME/2016-06'

# specify bioformats_package.jar to use if required
# bfpackage = r'bfpackage/5.1.10/bioformats_package.jar'
# bfpackage = r'bfpackage/5.9.2/bioformats_package.jar'
bfpackage = r'bfpackage/6.3.0/bioformats_package.jar'

# set path the bioformats_package.jar
bf.set_bfpath(bfpackage)

# get image meta-information using bioformats
MetaInfo = bf.get_relevant_metainfo_wrapper(filename,
                                            namespace=urlnamespace,
                                            bfpath=bfpackage,
                                            showinfo=False,
                                            xyorder='YX')

num_series = MetaInfo['Sizes'][0]
num_levels = MetaInfo['PyLevels']
num_scenes = MetaInfo['NumScenes']
pylevel2read = 0
xysizes_pylevel = MetaInfo['SeriesDimensions'][pylevel2read]

print('Total Series          : ', MetaInfo['Sizes'][0])
print('Resolution Levels     : ', MetaInfo['PyLevels'])
print('Number of Scenes      : ', MetaInfo['NumScenes'])
print('XY Dimensions PyLevel : ', xysizes_pylevel)


out = bf.calc_series_pylevel(num_series,
                             num_levels=num_levels,
                             num_scenes=num_scenes,
                             pylevel=pylevel2read)

print(' SeriesIDs for PyLevel : ', out)

try:
    img6d, readstate = bf.get_image6d(filename, MetaInfo,
                                      num_levels=MetaInfo['PyLevels'],
                                      num_scenes=MetaInfo['NumScenes'],
                                      pylevel2read=pylevel2read)

    arrayshape = np.shape(img6d)

except:

    arrayshape = []
    print('Could not read image data into NumPy array.')

# show relevant image Meta-Information
bf.showtypicalmetadata(MetaInfo)

print('----------------------------------------------------')
print('Array Shape          : ', arrayshape)

if showimage:
    S = 1
    T = 1
    C = 1
    Z = 40

    img2show = img6d[S - 1, T - 1, Z - 1, C - 1, :, :]

    # plot one image plane to check results
    fig = plt.figure(figsize=(8, 8), dpi=100)
    ax = fig.add_subplot(111)
    cax = ax.imshow(img2show, interpolation='nearest', cmap=cm.hot)
    ax.set_title('S=' + str(S) + 'T=' + str(T) + ' Z=' + str(Z) + ' CH=' + str(C), fontsize=12)
    ax.set_xlabel('X-dimension [pixel]', fontsize=10)
    ax.set_ylabel('Y-dimension [pixel]', fontsize=10)
    cbar = fig.colorbar(cax)
    ax.format_coord = dsv.Formatter(cax)
    # show plots
    plt.show()

if writeimage:

    # write OME-TIFF
    omefile = os.path.splitext(filename)[0] + '.ome.tiff'
    fp = bf.write_ometiff(omefile, img6d,
                          scalex=MetaInfo['XScale'],
                          scaley=MetaInfo['YScale'],
                          scalez=MetaInfo['ZScale'],
                          dimorder='STZCXY',
                          pixeltype='uint16')
