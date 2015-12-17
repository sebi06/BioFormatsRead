# -*- coding: utf-8 -*-
"""
@author: Sebi

File: write_OME-XML_from_file.py
Date: 17.12.2015
Version. 1.0
"""

import bfimage as bf
from lxml import etree as etl


def create_omexml(testdata, method=1, writeczi_metadata=True):

    # creates readable xml files from image data files. Default method should be = 1.
    if method == 1:
        # method 1
        for i in range(0, len(testdata)):

            # Change File name and write XML file to same folder
            xmlfile1 = testdata[i] + '_MetaData1.xml'

            try:
                # get the actual OME-XML
                omexml = bf.createOMEXML(testdata[i])
                # create root and tree from XML string and write "pretty" to disk
                root = etl.fromstring(omexml)
                tree = etl.ElementTree(root)
                tree.write(xmlfile1, pretty_print=True, encoding='utf-8', method='xml')
                print 'Created OME-XML file for testdata: ', testdata[i]
            except:
                print 'Creating OME-XML failed for testdata: ', testdata[i]

    if method == 2:
        # method 2
        for i in range(0, len(testdata)):

            # Change File name and write XML file to same folder
            xmlfile2 = testdata[i] + '_MetaData2.xml'

            try:
                # get the actual OME-XML
                md, omexml = bf.get_metadata_store(testdata[i])
                # create root and tree from XML string and write "pretty" to disk
                root = etl.fromstring(omexml)
                tree = etl.ElementTree(root)
                tree.write(xmlfile2, pretty_print=True, encoding='utf-8', method='xml')
                print 'Created OME-XML file for testdata: ', testdata[i]
            except:
                print 'Creating OME-XML failed for testdata: ', testdata[i]

    if writeczi_metadata:

        # this writes the special CZI xml metadata to disk, when a CZI file was found.
        for i in range(0, len(testdata)):

            if testdata[i][-4:] == '.czi':
                try:
                    bf.czt.writexml_czi(testdata[i])
                except:
                    print 'Could not write special CZI metadata for: ', testdata[i]


# INSERT THE FILES INSIDE THE LIST BELOW

testfiles = [r'c:\Users\Testuser\OME-TIFF_Metadatatest\test1.czi',
            r'c:\Users\Testuser\Documents\Testdata_Zeiss\OME-TIFF_Metadatatest\Tile=4_T=3_CH=2_Z=3.czi_Fiji_Export_allTiles.ome.tiff']

create_omexml(testfiles, method=1, writeczi_metadata=True)

