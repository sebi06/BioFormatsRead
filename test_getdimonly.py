import bfimage as bf

# define testdata base directory and filename of the image dataset to be read
filenames = [r'testdata/2x2_SNAP_CH=2_Z=5_T=2.czi']

# specify bioformats_package.jar to use if required
#bf.set_bfpath(insert path to bioformats_package.jar here)

for currentfile in filenames:

    sizes = bf.bftools.get_dimension_only(currentfile)
    sizes_czi = bf.czitools.read_dimensions_czi(currentfile)
    print sizes
    print sizes_czi
