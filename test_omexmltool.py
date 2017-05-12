# -*- coding: utf-8 -*-
"""
@author: Sebi

File: test_omexmltool.py
Date: 17.04.2017
Version. 1.2
"""

from __future__ import print_function
import bftools as bf

# use for BioFormtas <= 5.1.10
#urlnamespace = 'http://www.openmicroscopy.org/Schemas/OME/2015-01'
# use for BioFormtas > 5.2.0
urlnamespace = 'http://www.openmicroscopy.org/Schemas/OME/2016-06'

# specify bioformats_package.jar to use if required
bfpackage = r'bfpackage/5.4.1/bioformats_package.jar'
bf.set_bfpath(bfpackage)

testfile = r'testdata/B4_B5_S=8_4Pos_perWell_T=2_Z=1_CH=1.czi'

# try to create an OME-XML file
#bf.writeomexml(testfile, method=1, writeczi_metadata=True)
bf.writeomexml(testfile, method=2, writeczi_metadata=False)

# get the complete metadatastore and the XML string itself
metadata = bf.get_metadata_store(testfile)
xmlstring = bf.get_XMLStringfromMetaData(metadata)

# get OME-XML
omexml = bf.get_OMEXML(testfile)

jmd, totalseries, ids, dim, multires = bf.get_java_metadata_store(testfile)

print('Done.')
