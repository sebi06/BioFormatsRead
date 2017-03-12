import bfimage as bf

# define testdata base directory and filename of the image dataset to be read
filenames = [r'testdata/2x2_SNAP_CH=2_Z=5_T=2.czi']

# specify bioformats_package.jar to use if required
bfpackage = r'BioFormats/5.3.1/bioformats_package.jar'
bf.set_bfpath(bfpackage)

for currentfile in filenames:

    sizes = bf.bftools.get_dimension_only(currentfile)
    sizes_czi = bf.czitools.read_dimensions_czi(currentfile)
    print sizes
    print sizes_czi
