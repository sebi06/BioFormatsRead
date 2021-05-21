import javabridge
import bioformats as bf
import numpy as np
from matplotlib import pyplot as plt, cm

javabridge.start_vm(class_path=bf.JARS, run_headless=True)

NT = 10
NC = 2
NZ = 4
NX = 217
NY = 94

output_path = 'outome.tif'

frames = []

for t in range(NT):
    for z in range(NZ):
        for c in range(NC):
            frame = np.random.randn(NY, NX, 1, 1, 1).astype(np.uint16)
            frames.append(np.squeeze(frame))
            print(frame.shape)
            bf.write_image(output_path, pixels=frame, pixel_type=bf.PT_UINT16, c=c, t=t, z=z, size_c=NC, size_t=NT, size_z=NZ)


"""
xml_metadata = bf.get_omexml_metadata(path=output_path)
metadata = bf.OMEXML(xml_metadata)


NXp = metadata.image().Pixels.SizeX
NYp = metadata.image().Pixels.SizeY
NZp = metadata.image().Pixels.SizeZ
NCp = metadata.image().Pixels.SizeC
NTp = metadata.image().Pixels.SizeT

print(NXp, NYp, NZp, NCp, NTp)

assert(NXp == NX)
assert(NYp == NY)
assert(NZp == NZ)
assert(NCp == NC)
assert(NTp == NT)
"""

javabridge.kill_vm()


fig = plt.figure(figsize=(10, 8), dpi=100)
ax = fig.add_subplot(111)
cax = ax.imshow(frames[0], interpolation='nearest', cmap=cm.hot)
ax.set_xlabel('X-dimension [pixel]', fontsize=10)
ax.set_ylabel('Y-dimension [pixel]', fontsize=10)
cbar = fig.colorbar(cax)
# show plots
plt.show()