import javabridge as jv
import bioformats as bf
import numpy as np
from matplotlib import pyplot as plt, cm
import json
import tifffile

bfpackage = r'c:\Users\m1srh\Documents\Software\Bioformats\5.9.2\bioformats_package.jar'
#jars = jv.JARS + [bfpackage]

jv.start_vm(class_path=bf.JARS, run_headless=True)

# Dimension TZCXY
SizeT = 10
SizeZ = 23
SizeC = 2
SizeX = 217
SizeY = 94

output_file = r'stackome.tiff'
img5d = np.random.randn(SizeT, SizeZ, SizeC, SizeY, SizeX).astype(np.uint16)

frames = []

for t in range(SizeT):
    for z in range(SizeZ):
        for c in range(SizeC):

            img2write = img5d[t, z, c, :, :]
            frame = np.uint16(img2write[:, :, np.newaxis, np.newaxis, np.newaxis])
            print(frame.shape)
            bf.write_image(output_file,
                           pixels=frame,
                           pixel_type=bf.PT_UINT16,
                           t=t,
                           z=z,
                           c=c,
                           size_t=SizeT,
                           size_z=SizeZ,
                           size_c=SizeC)

jv.kill_vm()

# fig = plt.figure(figsize=(10, 8), dpi=100)
# ax = fig.add_subplot(111)
# cax = ax.imshow(frames[0], interpolation='nearest', cmap=cm.hot)
# ax.set_xlabel('X-dimension [pixel]', fontsize=10)
# ax.set_ylabel('Y-dimension [pixel]', fontsize=10)
# cbar = fig.colorbar(cax)
# # show plots
# plt.show()

