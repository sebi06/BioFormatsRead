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

    for frame in range(SizeT):
        if verbose:
            print('[' + str(frame + 1) + ']'),
            sys.stdout.flush()

        index = frame
        pixel_buffer = bioformats.formatwriter.convert_pixels_to_buffer(img_XYCZT[:, :, :, :, frame], type)

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



# filename = r'testdata\T=30_Z=23_C=2_x=217_Y=94.czi'
# urlnamespace = 'http://www.openmicroscopy.org/Schemas/OME/2016-06'
# bfpackage = r'c:\Users\m1srh\Documents\Software\Bioformats\5.9.2\bioformats_package.jar'
# bf.set_bfpath(bfpackage)
#
# output_order = 'XYCZTS'
# #output_order = 'STZCYX'
#
# # get image meta-information
# MetaInfo = bf.get_relevant_metainfo_wrapper(filename,
#                                             namespace=urlnamespace,
#                                             bfpath=bfpackage,
#                                             showinfo=False,
#                                             xyorder='YX')
#
# img6d, readstate = bf.get_image6d(filename, MetaInfo['Sizes'], output_order=output_order)
#
#
# # show relevant image Meta-Information
# bf.showtypicalmetadata(MetaInfo, namespace=urlnamespace, bfpath=bfpackage)
# print('Array Shape          : ', img6d.shape)
#
# T = 16
# C = 1
# Z = 10
# S = 1
#
# if output_order == 'STZCYX':
#     img2show = img6d[S-1, T-1, Z-1, C-1, :, :]
# if output_order == 'XYCZTS':
#     img2show = img6d[:, :, C-1, Z-1, T-1, S-1]
#
# fig = plt.figure(figsize=(10, 8), dpi=100)
# ax = fig.add_subplot(111)
# cax = ax.imshow(img2show, interpolation='nearest', cmap=cm.hot)
# ax.set_title('S=' +str(S) + 'T=' + str(T) + ' Z=' + str(Z) + ' CH=' + str(C), fontsize=12)
# ax.set_xlabel('X-dimension [pixel]', fontsize=10)
# ax.set_ylabel('Y-dimension [pixel]', fontsize=10)
# cbar = fig.colorbar(cax)
# ax.format_coord = dsv.Formatter(cax)


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