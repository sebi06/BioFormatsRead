# -*- coding: utf-8 -*-
"""
@author: Sebi

File: test_get_XML_nodes.py
Date: 28.05.2017
Version. 0.2
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

path = 'Metadata/Information/Image/Dimensions/Channels/Channel'
tag, attribute, text = czt.getXMLnodes(filename, path)
print(tag)
print(attribute)

path = 'Metadata/Information/Image/Dimensions/S/Scenes/Scene'
tag, attribute, text = czt.getXMLnodes(filename, path)
print(tag)
print(attribute)

path = 'Metadata/Information/Image/Dimensions/S/Scenes/Scene/ArrayName'
tag, attribute, text = czt.getXMLnodes(filename, path)
print(tag)
print(attribute)
print(text)

path = 'Metadata/Information/Image/Dimensions/S/Scenes/Scene/Shape'
tag, attribute, text = czt.getXMLnodes(filename, path)
print(tag)
print(attribute)
print(attribute[0]['Name'])

path = 'Metadata/Scaling/AutoScaling/ObjectiveName'
tag, attribute, text = czt.getXMLnodes(filename, path)
print(tag)
print(text)

obj = {'LensNA': 1.0,
        'NominalMagnification': 1,
        'WorkingDistance': 0,
        'Immersion': 'Air',
        'TubeLensMagnification': 1,
        'TotalMagnification': 1}

for k, v in obj.items():

    path = 'Metadata/Information/Instrument/Objectives/Objective/' + k
    tag, attribute, text = czt.getXMLnodes(filename, path)
    obj[k] = text

path = 'Metadata/Information/Instrument/TubeLenses/TubeLens/Magnification'
tag, attribute, text = czt.getXMLnodes(filename, path)
obj['TubeLensMagnification'] = text

print(obj)

dims = {'SizeX': 0,
            'SizeY': 0,
            'SizeS': 0,
            'SizeB': 0,
            'SizeC': 0,
            'SizeT': 0,
            'SizeZ': 0}

for k, v in dims.items():

    path = 'Metadata/Information/Image/' + k
    tag, attribute, text = czt.getXMLnodes(filename, path)
    #print(tag)
    #print(attribute)
    #print(text)
    dims[k] = text
    # check for empty entries
    if dims[k] == []:
        dims[k] = 1

print(dims)
