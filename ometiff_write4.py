import bioformats.omexml as ome
import javabridge as jv
import bioformats
import os
import sys
import numpy as np
import bftools as bf
from matplotlib import pyplot as plt, cm
import dispvalues as dsv

# Write file to disk
def writeOMETIFF(img_XYCZT, path, type='uint16', verbose=True):

    if verbose:
        print('Dimensions XYCZT: ' + str(np.shape(img_XYCZT)))
        sys.stdout.flush()

    # Get the new dimensions
    SizeX = np.shape(img_XYCZT)[0]
    SizeY = np.shape(img_XYCZT)[1]
    SizeC = np.shape(img_XYCZT)[2]
    SizeZ = np.shape(img_XYCZT)[3]
    SizeT = np.shape(img_XYCZT)[4]

    # Start JVM for bioformats
    bfpackage = r'c:\Users\m1srh\Documents\Software\Bioformats\5.9.2\bioformats_package.jar'
    jars = jv.JARS + [bfpackage]
    jv.start_vm(class_path=jars, run_headless=True, max_heap_size='4G')

    # Getting metadata info
    omexml = ome.OMEXML()
    omexml.image(0).Name = os.path.split(path)[1]
    p = omexml.image(0).Pixels
    assert isinstance(p, ome.OMEXML.Pixels)
    p.SizeX = SizeX
    p.SizeY = SizeY
    p.SizeC = SizeC
    p.SizeT = SizeT
    p.SizeZ = SizeZ
    p.PhysicalSizeX = np.float(0.1)
    p.PhysicalSizeY = np.float(0.1)
    p.PhysicalSizeZ = np.float(0.5)
    p.DimensionOrder = ome.DO_XYCZT
    p.PixelType = type
    p.channel_count = SizeC
    p.plane_count = SizeZ
    p.Channel(0).SamplesPerPixel = SizeC
    omexml.structured_annotations.add_original_metadata(ome.OM_SAMPLES_PER_PIXEL, str(SizeC))

    # Converting to omexml
    xml = omexml.to_xml()

    # Write file using Bioformats
    if verbose:
        print ('Writing frames:'),
        sys.stdout.flush()

    #for t in range(SizeT):
    #    for z in range(SizeZ):
    #s        for c in range(SizeC):

    for t in range(SizeT):
                if verbose:
                    print('[' + str(t + 1) + ']'),
                    sys.stdout.flush()

                index = t

                pixel_buffer = bioformats.formatwriter.convert_pixels_to_buffer(img_XYCZT[:, :, :, :, t], type)
                #pixel_buffer = bioformats.formatwriter.convert_pixels_to_buffer(img_XYCZT[:, :, c, z, t], type)

                script = """
                importClass(Packages.loci.formats.services.OMEXMLService,
                            Packages.loci.common.services.ServiceFactory,
                            Packages.loci.formats.out.TiffWriter);
            
                var service = new ServiceFactory().getInstance(OMEXMLService);
                var metadata = service.createOMEXMLMetadata(xml);
                var writer = new TiffWriter();
                writer.setBigTiff(true);
                writer.setMetadataRetrieve(metadata);
                writer.setId(path);
                writer.setInterleaved(true);
                writer.saveBytes(index, buffer);
                writer.close();
                """
                jv.run_script(script, dict(path=path, xml=xml, index=index, buffer=pixel_buffer))

    if verbose:
        print ('[Done]')
        sys.stdout.flush()

    if verbose:
        print('File saved on ' + str(path))
        sys.stdout.flush()

    jv.kill_vm()

#######################################


# Dimension TZCXY
SizeT = 30
SizeZ = 23
SizeC = 2
SizeX = 217
SizeY = 94

output_file = r'stack.ome.tiff'
#img5d = np.squeeze(img6d)
#img5d = np.random.randn(SizeT, SizeZ, SizeC, SizeY, SizeX).astype(np.uint8)
img5d = np.random.randn(SizeX, SizeY, SizeC, SizeZ, SizeT).astype(np.uint16)
writeOMETIFF(img5d, output_file, type='uint16', verbose=True)

# show plots
#plt.show()