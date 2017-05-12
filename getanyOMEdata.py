# -*- coding: utf-8 -*-
"""
@author: Sebi

File: getanyOMEdata.py
Date: 11.05.2017
Version. 0.4
"""

from __future__ import print_function
from lxml import etree as etl
import bftools as bf


filename = r'testdata/T=5_Z=3_CH=2_CZT_All_CH_per_Slice.czi'

# use for BioFormtas <= 5.1.10
#urlnamespace = 'http://www.openmicroscopy.org/Schemas/OME/2015-01'
# use for BioFormtas > 5.2.0
urlnamespace = 'http://www.openmicroscopy.org/Schemas/OME/2016-06'

# specify bioformats_package.jar to use if required
bfpackage = r'bfpackage/5.4.1/bioformats_package.jar'
bf.set_bfpath(bfpackage)

omexml = bf.get_OMEXML(filename)
bf.parseXML(omexml, 'Image', 'Pixel')

print('-' * 80 + '\n')
bf.parseXML(omexml, 'Instrument', 'Filterset', highdetail=True)

print('-' * 80 + '\n')

result = bf.getinfofromOMEXML(omexml, ['Image', 'Pixels', 'Channel'], ns=urlnamespace)
print(result)
result = bf.getinfofromOMEXML(omexml, ['Instrument', 'Objective'], ns=urlnamespace)
print(result)
result = bf.getinfofromOMEXML(omexml, ['Instrument', 'Detector'])
print(result)
result = bf.getinfofromOMEXML(omexml, ['Image', 'Pixels', 'Channel'], ns=urlnamespace)
print(result[0])
print(result[1])

