import bfimage as cz
from matplotlib import pyplot as plt, cm
import os
import numpy as np

#filename = r'C:\Python_ZEN_Output\XYZCT_Z=15_C=2_T=20.czi'

imgbase = os.path.basename(filename)
imgdir = os.path.dirname(filename)
## get image meta-information
MetaInfo = cz.bftools.get_relevant_metainfo_wrapper(filename)


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

seriesID = 0
timepoint = 10
channel = 0
zplane = 6

zstack = cz.bftools.get_zstack(filename, MetaInfo['Sizes'], seriesID, timepoint)
print 'Shape Z-Stack        : ', np.shape(zstack)
img2show = zstack[zplane, channel, :, :]
fig1 = plt.figure(figsize=(10, 8), dpi=100)
ax1 = fig1.add_subplot(111)
cax = ax1.imshow(img2show, interpolation='nearest', cmap=cm.hot)
ax1.set_title('T=' + str(timepoint+1) + ' Z=' + str(zplane+1) + ' CH=' + str(channel+1), fontsize=12)
ax1.set_xlabel('X-dimension [pixel]', fontsize=10)
ax1.set_ylabel('Y-dimension [pixel]', fontsize=10)
cbar = fig1.colorbar(cax)
# show plots
plt.show()

