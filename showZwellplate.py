# -*- coding: utf-8 -*-
"""
@author: Sebi

File: showZwellplate.py
Date: 01.06.2017
Version. 1.4
"""

#from __future__ import print_function
import bftools as bf
import dispZsurface as dsp
import matplotlib.pyplot as plt
import os

saveformat = '.png'

#filenamecsv = r'testdata/Wellchamber_384_Comb.csv'
#filenamecsv = r'testdata/fixed endpoint 3C 2_5 384well_planetable.csv'
#filenameczi = r'testdata/B4_B5_S=8_4Pos_perWell_T=2_Z=1_CH=1.czi'
#filenameczi = r'c:\Users\m1srh\OneDrive - Carl Zeiss AG\Python_Projects\BioFormatsRead\testdata\B4_B5_S=8_4Pos_perWell_T=2_Z=1_CH=1.czi'
filenameczi = r'c:\Users\m1srh\OneDrive - Carl Zeiss AG\Python_Projects\BioFormatsRead\testdata\testwell96.czi'
#filenameczi = r'c:\Users\M1SRH\Documents\Testdata_Zeiss\RareEvent_Test_Wizard\OverViewScan_Test_raw.czi'
#filenamecsv = r'testdata/testwell96_planetable.csv'
#filenameczi = r'c:\Users\M1SRH\Downloads\Focus_map\Dan.czi'

# specify bioformats_package.jar to use if required
# Attention: for larger CZI tile images containing an image pyramid one must still use 5.1.10
# since the latest version is not fully supported by python-bioformats yet
bfpackage = r'c:\Users\m1srh\Documents\Software\Bioformats\5.1.10\bioformats_package.jar'
bf.set_bfpath(bfpackage)

# define separator
separator = '\t'

# create plane info from CZI image file and write CSV file (optional)
planetable, filenamecsv = bf.get_planetable(filenameczi, writecsv=True, separator=separator)

# or use the CSV file directly once it was created
#planetable = pd.read_csv(filenamecsv, sep=separator)

# show the dataframe
print(planetable[:10])
print(planetable.shape[0])

# define name for figure to be saved
figuresavename = os.path.splitext(filenamecsv)[0] + '_XYZ-Pos' + saveformat

# display the XYZ positions
fig1, fig2 = dsp.scatterplot(planetable, ImageID=0, T=0, CH=0, Z=0, size=250,
                savefigure=True, figsavename=figuresavename, showsurface=True)

# show the plot
plt.show()
