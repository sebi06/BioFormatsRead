import bfimage as bf

filename = r'c:\Users\M1SRH\Documents\Spyder_Projects_Testdata\CZI_Read\2x2_SNAP_CH=2_Z=5_T=2.czi'

df = bf.get_planetable(filename, writecsv=True, separator=',')

print df


