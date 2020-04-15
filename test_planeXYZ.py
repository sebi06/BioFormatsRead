
"""
@author: Sebi

File: test_planeXYZ.py
Date: 26.03.2017
Version. 0.3
"""

from __future__ import print_function
import bftools as bf

# define filename
#filename = r'testdata/Beads_63X_NA1.35_xy=0.042_z=0.1.czi'
filename = r"C:\Users\m1srh\OneDrive - Carl Zeiss AG\Testdata_Zeiss\BrainSlide\DTScan_ID2.czi"
#filename = r"C:\Users\m1srh\OneDrive - Carl Zeiss AG\Testdata_Zeiss\Castor\testwell96_woatt.czi"
#filename = r'c:\Output\Guided_Acquisition\OverViewScan.ome.tiff'

# use for BioFormats <= 5.1.10
#urlnamespace = 'http://www.openmicroscopy.org/Schemas/OME/2015-01'
# use for BioFormtas > 5.2.0
urlnamespace = 'http://www.openmicroscopy.org/Schemas/OME/2016-06'

# specify bioformats_package.jar to use if required
#bfpackage = r'bfpackage/5.1.10/bioformats_package.jar'
bfpackage = r'bfpackage/6.4.0/bioformats_package.jar'
bf.set_bfpath(bfpackage)

# create plane info and write into dataframe
df, csvfile, metainfo = bf.get_planetable(filename, writecsv=True, separator='\t')

# show the dataframe
# print(df[:5])
print(df)
