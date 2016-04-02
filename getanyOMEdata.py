from lxml import etree as etl
import bfimage as bf


def parseXML(omexml, ch1, ch2):
    """
    Parse XML with ElementTree
    """
    root = etl.fromstring(omexml)
    tree = etl.ElementTree(root)

    for child in root:
        print '*   ', child.tag, '--> ', child.attrib
        if ch1 in child.tag:
        #if child.tag == "{http://www.openmicroscopy.org/Schemas/OME/2015-01}Instrument":
            for step_child in child:
                print '**  ', step_child.tag, step_child.attrib

                if ch2 in step_child.tag:
                    print "*** ", step_child.tag

                    testdict = {}
                    for step_child2 in step_child:
                        print '****', step_child2.tag, step_child2.attrib
                        testdict[step_child2.tag] = step_child2.attrib


def getinfo(omexml, nodenames, ns='http://www.openmicroscopy.org/Schemas/OME/2015-01'):
    """
    This function can be used to read the most useful OME-MetaInformation from the respective XML.
    Check for the correct namespace. More info can be found at: http://www.openmicroscopy.org/Schemas/

    The output is a list that can contain multiple elements.

    Usages:
    ------

    filename = r'c:\Users\M1SRH\Documents\Testdata_Zeiss\Python_bfimage_Testdata\20160331_C=2_Z=5_T=3_488_561_LSM800.czi'
    omexml = bf.createOMEXML(filename)
    parseXML(omexml, 'Image', 'Pixel')

    # case 1
    result = getinfo(omexml, ['Instrument', 'Objective'], ns='http://www.openmicroscopy.org/Schemas/OME/2015-01')
    print result

    # case 2
    result = getinfo(omexml, ['Instrument', 'Detector'])
    print result

    # case 3
    result = getinfo(omexml, ['Image', 'Pixels', 'Channel'])
    print result[0]
    print result[1]

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


filename = r'c:\Users\M1SRH\Documents\Testdata_Zeiss\Python_bfimage_Testdata\20160331_C=2_Z=5_T=3_488_561_LSM800.czi'
omexml = bf.createOMEXML(filename)
#parseXML(omexml, 'Image', 'Pixel')

print '-' * 80 + '\n'

result = getinfo(omexml, ['Image', 'Pixels', 'Channel'], ns='http://www.openmicroscopy.org/Schemas/OME/2015-01')
print result
result = getinfo(omexml, ['Instrument', 'Objective'], ns='http://www.openmicroscopy.org/Schemas/OME/2015-01')
print result
result = getinfo(omexml, ['Instrument', 'Detector'])
print result
result = getinfo(omexml, ['Image', 'Pixels', 'Channel'])
print result[0]
print result[1]

