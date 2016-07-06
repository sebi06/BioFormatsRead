# -*- coding: utf-8 -*-
"""
@author: Sebi

File: test_get_image6d.py
Date: 03.02.2016
Version. 1.0
"""

import numpy as np
from lxml import etree as etl
import os
import bfimage as bf

filename = r'c:\Users\M1SRH\Documents\Testdata_Zeiss\Python_bfimage_Testdata\20160331_C=2_Z=5_T=3_A488_A555_CD7.czi'

omexml = bf.createOMEXML(filename)
# create root and tree from XML string and write "pretty" to disk
root = etl.fromstring(omexml)
tree = etl.ElementTree(root)

for child in root:
    print child.tag, child.attrib


from StringIO import StringIO

def parseXML(xmlFile):
    """
    Parse the xml
    """
    f = open(xmlFile)
    xml = f.read()
    f.close()

    tree = etl.parse(StringIO(xml))
    context = etl.iterparse(StringIO(xml))
    for action, elem in context:
        if not elem.text:
            text = "None"
        else:
            text = elem.text
        print elem.tag + " => " + text

parseXML(r'c:\Users\M1SRH\Documents\Testdata_Zeiss\Python_bfimage_Testdata\20160331_C=2_Z=5_T=3_A488_A555_CD7.czi_MetaData1.xml')