# -*- coding: utf-8 -*-
"""
@author: Sebi

File: test_omexmltool.py
Date: 03.02.2016
Version. 1.0
"""

import bfimage as bf

# specify bioformats_package.jar to use if required
bfpath = r'c:\Users\M1SRH\Documents\Software\BioFormats_Package\5.1.10\bioformats_package.jar'
bf.set_bfpath(bfpath)

# INSERT THE FILES INSIDE THE LIST BELOW

#testfiles = [r'c:\Users\M1SRH\Documents\Testdata_Zeiss\Pyramid_Test\PyTest_int_fromZEN.czi',
#             r'c:\Users\M1SRH\Documents\Testdata_Zeiss\Pyramid_Test\PyTest_int_viaOAD-COM.czi']

testfiles = [r'c:\Users\M1SRH\Documents\Python_Projects_Testdata\CZI_XML_Test\B4_B5_S=8_4Pos_perWell_T=2_Z=1_CH=1.czi']

#bf.create_omexml(testfiles, method=1, writeczi_metadata=True)
bf.create_omexml(testfiles, method=2, writeczi_metadata=False)
