import bfimage as bf
from matplotlib import pyplot as plt, cm
import os
import numpy as np

filename = r'testdata/T=5_Z=3_CH=2_CZT_All_CH_per_Slice.czi'

imgbase = os.path.basename(filename)
imgdir = os.path.dirname(filename)

# specify bioformats_package.jar to use if required
#bf.set_bfpath(insert path to bioformats_packe.jar here)

# get image meta-information
MetaInfo = bf.bftools.get_relevant_metainfo_wrapper(filename)

seriesID = 0
timepoint = 2
channel = 1
zplane = 2

#get the actual time series from the data set
tseries = bf.bftools.get_timeseries(filename, MetaInfo['Sizes'], seriesID, zplane)

## show relevant image Meta-Information
print '\n'
print 'Image Directory      : ', imgdir
print 'Image Filename       : ', imgbase
print 'Images Dim Sizes     : ', MetaInfo['Sizes']
print 'Dimension Order BF   : ', MetaInfo['DimOrder BF']
print 'Dimension Order CZI  : ', MetaInfo['OrderCZI']
print 'Total Series Number  : ', MetaInfo['TotalSeries']
print 'Image Dimensions     : ', MetaInfo['TotalSeries'], MetaInfo['SizeT'], MetaInfo['SizeZ'], MetaInfo['SizeC'],\
                                    MetaInfo['SizeY'], MetaInfo['SizeX']
print 'Scaling XYZ [micron] : ', MetaInfo['XScale'], MetaInfo['YScale'], MetaInfo['ZScale']
print 'Objective M-NA-Imm   : ', MetaInfo['ObjMag'], MetaInfo['NA'], MetaInfo['Immersion']
print 'Objective Name       : ', MetaInfo['ObjModel']
print 'Detector Name        : ', MetaInfo['DetName']
print 'Ex. Wavelengths [nm] : ', MetaInfo['WLEx']
print 'Em. Wavelengths [nm] : ', MetaInfo['WLEm']
print 'Channel Description  : ', MetaInfo['ChDesc']
print '============================================================='
print 'Shape Time Series    : ', np.shape(tseries)

img2show = tseries[timepoint, channel, :, :]
fig1 = plt.figure(figsize=(10, 8), dpi=100)
ax1 = fig1.add_subplot(111)
cax = ax1.imshow(img2show, interpolation='nearest', cmap=cm.gray, aspect='equal')
ax1.set_title('T=' + str(timepoint+1) + ' Z=' + str(zplane+1) + ' CH=' + str(channel+1), fontsize=12)
ax1.set_xlabel('X-dimension [pixel]', fontsize=10)
ax1.set_ylabel('Y-dimension [pixel]', fontsize=10)
cbar = fig1.colorbar(cax)
# show plots
plt.show()

