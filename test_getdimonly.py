import bfimage as bf

filename = r'testdata/2x2_SNAP_CH=2_Z=5_T=2.czi'

#sizes = bf.bftools.get_dimension_only(filename)

sizes_czi = bf.czitools.read_dimensions_czi(filename)

#print sizes
print sizes_czi