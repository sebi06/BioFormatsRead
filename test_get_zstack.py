import bfimage as bf
from matplotlib import pyplot as plt, cm
import os
import numpy as np

filename = r'testdata/Beads_63X_NA1.35_xy=0.042_z=0.1.czi'

imgbase = os.path.basename(filename)
imgdir = os.path.dirname(filename)

# specify bioformats_package.jar to use if required
#bf.set_bfpath(insert path to bioformats_packe.jar here)

## get image meta-information
MetaInfo = bf.bftools.get_relevant_metainfo_wrapper(filename)

seriesID = 0
timepoint = 0
channel = 0

# get the actual z-stack from the data set
zstack, dimorder_out = bf.bftools.get_zstack(filename, MetaInfo['Sizes'], seriesID, timepoint=timepoint)

# get plane with the brightest pixel
zplane = (zstack == zstack.max()).nonzero()[0][0]
print 'Brightest Z-Plane: ', zplane+1

# show relevant image Meta-Information
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
print 'Detector Model       : ', MetaInfo['Detector Model']
print 'Detector Name        : ', MetaInfo['Detector Name']
print 'Ex. Wavelengths [nm] : ', MetaInfo['WLEx']
print 'Em. Wavelengths [nm] : ', MetaInfo['WLEm']
print 'Dyes                 : ', MetaInfo['Dyes']
print 'Channel Description  : ', MetaInfo['ChDesc']
print '============================================================='
print 'Shape Z-Stack        : ', np.shape(zstack)

img2show = zstack[zplane, channel, :, :]
fig1 = plt.figure(figsize=(10, 8), dpi=100)
ax1 = fig1.add_subplot(111)
cax = ax1.imshow(img2show, interpolation='nearest', cmap=cm.hot)
ax1.set_title('T=' + str(timepoint+1) + ' Z=' + str(zplane+1) + ' CH=' + str(channel+1), fontsize=12)
ax1.set_xlabel('X-dimension [pixel]', fontsize=10)
ax1.set_ylabel('Y-dimension [pixel]', fontsize=10)
cbar = fig1.colorbar(cax)
ax1.format_coord = bf.Formatter(cax)
# show plots
plt.show()
