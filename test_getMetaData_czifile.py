# -*- coding: utf-8 -*-
"""
@author: Sebi

File: testgetMetaData_czifile.py
Date: 07.04.2017
Version. 0.2
"""

from __future__ import print_function
from czifile import *
from lxml import etree as etl

filename = r'testdata\2x2_SNAP_CH=2_Z=5_T=2.czi'

czi = CziFile(filename, detectmosaic=True)
metadata = czi.metadata
header = czi.header

for child in metadata.getiterator():
    print(child.tag, child.attrib)

for child in metadata.findall('Objective'):
    print(child.tag, child.attrib)

print('Done.')
