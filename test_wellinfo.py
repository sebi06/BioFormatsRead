import bfimage as bf

filename = r'testdata/B4_B5_S=8_4Pos_perWell_T=2_Z=1_CH=1.czi'

# specify bioformats_package.jar to use if required
#bf.set_bfpath(insert path to bioformats_package.jar here)

wellstr = bf.getWelllNamesfromCZI(filename)
welllist, cols, rows, welldict, numdiffwells = bf.processWellStringfromCZI(wellstr)

print wellstr
print welllist
print cols
print rows
print welldict
print numdiffwells