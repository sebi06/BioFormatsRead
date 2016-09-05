import bfimage as bf

filename = r'testdata/B4_B5_S=8_4Pos_perWell_T=2_Z=1_CH=1.czi'

# specify bioformats_package.jar to use if required
#bf.set_bfpath(insert path to bioformats_package.jar here)

planes, pixels = bf.getPlanesAndPixelsFromCZI(filename)

print "=== Planes ==="
print planes
print "==== Pixels ==="
print pixels