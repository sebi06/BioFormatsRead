import bfimage as bf

filename = r'c:\Users\M1SRH\Documents\Python_Projects_Testdata\CZI_XML_Test\B4_B5_S=8_4Pos_perWell_T=2_Z=1_CH=1.czi'

# specify bioformats_package.jar to use if required
bfpath = r'c:\Users\M1SRH\Documents\Software\BioFormats_Package\5.1.10\bioformats_package.jar'
bf.set_bfpath(bfpath)

wellstr = bf.getWelllNamesfromCZI(filename)
welllist, cols, rows, welldict, numwells = bf.getWellInfofromCZI(wellstr)

print wellstr
print welllist
print cols
print rows
print welldict
print numwells


