import numpy as np
import bioformats.omexml as ome
import tifffile
import sys


def writeplanes(pixel, SizeT=1,
                SizeZ=1,
                SizeC=1,
                order='TZCYX',
                verbose=False):

    if order == 'TZCYX':

        pixel.DimensionOrder = ome.DO_XYCZT
        counter = 0
        for t in range(SizeT):
            for z in range(SizeZ):
                for c in range(SizeC):

                    if verbose:
                        print('Write PlaneTable: ', t, z, c),
                        sys.stdout.flush()

                    pixel.Plane(counter).TheT = t
                    pixel.Plane(counter).TheZ = z
                    pixel.Plane(counter).TheC = c
                    counter = counter + 1

    return pixel


# Dimension TZCXY
SizeT = 3
SizeZ = 4
SizeC = 2
SizeX = 217
SizeY = 94
Series = 0


scalex = 0.1
scaley = scalex
scalez = 0.5
pixeltype = 'uint16'
dimorder = 'TZCYX'
output_file = r'stack.ome.tiff'


# create numpy array with correct order
img5d = np.random.randn(SizeT, SizeZ, SizeC, SizeY, SizeX).astype(np.uint16)

# Getting metadata info
omexml = ome.OMEXML()
omexml.image(Series).Name = output_file
p = omexml.image(Series).Pixels
#p.ID = 0
p.SizeX = SizeX
p.SizeY = SizeY
p.SizeC = SizeC
p.SizeT = SizeT
p.SizeZ = SizeZ
p.PhysicalSizeX = np.float(scalex)
p.PhysicalSizeY = np.float(scaley)
p.PhysicalSizeZ = np.float(scalez)
p.PixelType = pixeltype
p.channel_count = SizeC
p.plane_count = SizeZ * SizeT * SizeC
p = writeplanes(p, SizeT=SizeT, SizeZ=SizeZ, SizeC=SizeC, order=dimorder)

for c in range(SizeC):
    if pixeltype == 'unit8':
        p.Channel(c).SamplesPerPixel = 1
    if pixeltype == 'unit16':
        p.Channel(c).SamplesPerPixel = 2


omexml.structured_annotations.add_original_metadata(ome.OM_SAMPLES_PER_PIXEL, str(SizeC))

# Converting to omexml
xml = omexml.to_xml()

# write file and save OME-XML as description
tifffile.imwrite(output_file, img5d, metadata={'axes': dimorder}, description=xml)
