import numpy as np
import bioformats.omexml as ome
import tifffile
import sys
import bftools as bf


# Dimension TZCXY
filepath = r'stack.ome.tiff'

fp = bf.write_ometiff(filepath,
                      dimensions={'Series': 1, 'SizeT': 3, 'SizeZ': 4, 'SizeC': 2, 'SizeX': 217, 'SizeY': 94},
                      scalex=0.1,
                      scaley=0.1,
                      scalez=1.0,
                      dimorder='TZCYX',
                      pixeltype='uint16')

