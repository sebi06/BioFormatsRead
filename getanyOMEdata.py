# -*- coding: utf-8 -*-
"""
@author: Sebi

File: getanyOMEdata.py
Date: 17.04.2017
Version. 0.3
"""

from __future__ import print_function
from lxml import etree as etl
import bftools as bf


def parseXML(omexml, topchild, subchild, highdetail=False):
    """
    Parse XML with ElementTree and print the output to the console.
    topchild = specific node to search for
    subchild = specfic subchild of the topchild to search for
    """
    root = etl.fromstring(omexml)
    tree = etl.ElementTree(root)

    for child in root:
        print('*   ', child.tag, '--> ', child.attrib)
        if topchild in child.tag:
        #if child.tag == "{http://www.openmicroscopy.org/Schemas/OME/2015-01}Instrument":
            for step_child in child:
                print('**  ', step_child.tag, '-->', step_child.attrib)

                if subchild in step_child.tag and highdetail:
                    print("*** ", step_child.tag)

                    testdict = {}
                    if highdetail:
                        for step_child2 in step_child:
                            print('****', step_child2.tag, step_child2.attrib)
                            testdict[step_child2.tag] = step_child2.attrib


def getinfofromOMEXML(omexml, nodenames, ns='http://www.openmicroscopy.org/Schemas/OME/2015-01'):
    """
    This function can be used to read the most useful OME-MetaInformation from the respective XML.
    Check for the correct namespace. More info can be found at: http://www.openmicroscopy.org/Schemas/

    The output is a list that can contain multiple elements.

    Usages:
    ------

    filename = myfile.czi'
    omexml = bf.createOMEXML(filename)
    parseXML(omexml, 'Image', 'Pixel')

    # case 1
    result = getinfofromOMEXML(omexml, ['Instrument', 'Objective'], ns='http://www.openmicroscopy.org/Schemas/OME/2015-01')
    print(result)

    # case 2
    result = getinfofromOMEXML(omexml, ['Instrument', 'Detector'])
    print(result)

    # case 3
    result = getinfofromOMEXML(omexml, ['Image', 'Pixels', 'Channel'])
    print(result[0])
    print(result[1])
    """

    # get the root tree
    root = etl.fromstring(omexml)

    # define the namespace in order to find the correct path later on
    NSMAP = {'mw': ns}
    # enclose namespace with {...} and check the length
    namespace = u'{%s}' % ns
    nsl = len(namespace)

    # construct the search string
    if len(nodenames) >= 1:
        search = './/mw:' + nodenames[0]
    if len(nodenames) >= 2:
        search = search + '/mw:' + nodenames[1]
    if len(nodenames) >= 3:
        search = search + '/mw:' + nodenames[2]

    # find all elements using the search string
    out = root.findall(search, namespaces=NSMAP)
    # create an empty list to store the dictionaries in
    dictlist = []
    for i in range(0, len(out)):
        # create the dictionary from key - values pairs of the element
        dict = {}
        for k in range(0, len(out[i].attrib)):
            dict[out[i].keys()[k]] = out[i].values()[k]
        # add dictionary to the list
        dictlist.append(dict)

    return dictlist


filename = r'testdata/T=5_Z=3_CH=2_CZT_All_CH_per_Slice.czi'

# use for BioFormtas <= 5.1.10
#urlnamespace = 'http://www.openmicroscopy.org/Schemas/OME/2015-01'
# use for BioFormtas > 5.2.0
urlnamespace = 'http://www.openmicroscopy.org/Schemas/OME/2016-06'

# specify bioformats_package.jar to use if required
bfpackage = r'bfpackage/5.4.1/bioformats_package.jar'
bf.set_bfpath(bfpackage)

omexml = bf.get_OMEXML(filename)
parseXML(omexml, 'Image', 'Pixel')

print('-' * 80 + '\n')
parseXML(omexml, 'Instrument', 'Filterset', highdetail=True)

print('-' * 80 + '\n')

result = getinfofromOMEXML(omexml, ['Image', 'Pixels', 'Channel'], ns=urlnamespace)
print(result)
result = getinfofromOMEXML(omexml, ['Instrument', 'Objective'], ns=urlnamespace)
print(result)
result = getinfofromOMEXML(omexml, ['Instrument', 'Detector'])
print(result)
result = getinfofromOMEXML(omexml, ['Image', 'Pixels', 'Channel'])
print(result[0])
print(result[1])

