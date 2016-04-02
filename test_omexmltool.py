# -*- coding: utf-8 -*-
"""
@author: Sebi

File: test_omexmltool.py
Date: 03.02.2016
Version. 1.0
"""

import bfimage as bf

# INSERT THE FILES INSIDE THE LIST BELOW

# testfiles = [r'c:\Users\M1SRH\Documents\Testdata_Zeiss\OME-TIFF_Metadatatest\Tile=4_T=3_CH=2_Z=3.czi',
#             r'c:\Users\M1SRH\Documents\Testdata_Zeiss\OME-TIFF_Metadatatest\Tile=4_T=3_CH=2_Z=3_s1_Use_Tile=OFF.ome.tiff',
#             r'c:\Users\M1SRH\Documents\Testdata_Zeiss\OME-TIFF_Metadatatest\Tile=4_T=3_CH=2_Z=3_s1_UseTiles=ON.ome.tiff',
#             r'c:\Users\M1SRH\Documents\Testdata_Zeiss\OME-TIFF_Metadatatest\Tile=4_T=3_CH=2_Z=3.czi_Fiji_Export.ome.tiff',
#             r'c:\Users\M1SRH\Documents\Testdata_Zeiss\OME-TIFF_Metadatatest\Tile=4_T=3_CH=2_Z=3.czi_Fiji_Export_allTiles.ome.tiff']

# testfiles = [r'c:\Users\M1SRH\Documents\Spyder_Projects\BioFormatsRead\testdata\2x2_SNAP_CH=2_Z=5.czi']
testfiles = [r'c:\Users\M1SRH\Documents\Testdata_Zeiss\Python_bfimage_Testdata\20160331_C=2_Z=5_T=3_A488_A555_CD7.czi',
             r'c:\Users\M1SRH\Documents\Testdata_Zeiss\Python_bfimage_Testdata\20160331_C=2_Z=5_T=3_488_561_LSM800.czi']

bf.create_omexml(testfiles, method=1, writeczi_metadata=True)
