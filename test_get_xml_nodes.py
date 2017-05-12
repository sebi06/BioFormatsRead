# -*- coding: utf-8 -*-
"""
@author: Sebi

File: test_get_XML_nodes.py
Date: 02.05.2017
Version. 0.1
"""

import czitools as czt

filename = r'testdata/B4_B5_S=8_4Pos_perWell_T=2_Z=1_CH=1.czi'

path = 'Metadata/Information/Application/Name'
tag, attribute, text = czt.getXMLnodes(filename, path)
print(tag)
print(attribute)
print(text)

path = 'Metadata/Information/Application/Version'
tag, attribute, text = czt.getXMLnodes(filename, path)
print(tag)
print(attribute)
print(text)
