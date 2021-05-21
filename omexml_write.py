import numpy as np
import bioformats
import bioformats.omexml as ome
import javabridge as jv
import bioformats.omexml as ome

filename = r'testdata\T=30_Z=23_C=2_x=217_Y=94.czi'
urlnamespace = 'http://www.openmicroscopy.org/Schemas/OME/2016-06'

# Start JVM for bioformats
bfpackage = r'c:\Users\m1srh\Documents\Software\Bioformats\5.9.2\bioformats_package.jar'
jars = jv.JARS + [bfpackage]
jv.start_vm(class_path=jars, run_headless=True, max_heap_size='4G')

xml_metadata = bioformats.get_omexml_metadata(path=filename)
metadata = bioformats.OMEXML(xml_metadata)

omexml = ome.OMEXML()

jv.kill_vm()

