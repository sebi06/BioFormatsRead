import bfimage as bf

filename = r'c:\Users\M1SRH\Documents\Spyder_Projects_Testdata\CZI_Read\2x2_SNAP_CH=2_Z=5.czi'

#sizes = bf.bftools.get_dimension_only(filename)

sizes_czi = bf.czitools.read_dimensions_czi(filename)

#print sizes
print sizes_czi