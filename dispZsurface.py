# -*- coding: utf-8 -*-

from mpl_toolkits.mplot3d import axes3d
from matplotlib import cm
import matplotlib.pyplot as plt
import numpy as np


def ExtractLabels(nr, nc):

     # labeling schemes for plates up-to 384 wellplate
    labelX = ['1','2','3','4','5','6','7','8','9','10','11','12',
              '13','14','15','16','17','18','19','20','21','22','23','24',
              '25','26','27','28','29','30','31','32','33','34','35','36',
              '37','38','39','40','41','42','43','44','45','46','47','48',]

    labelY = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P',
              'Q','R','S','T','U','V','W','X','Y','Z','AA','AB','AC','AD','AE','AF']

    lx = labelX[0:nc]
    ly = labelY[0:nr]

    # determine an appropriate font size based on the plate type
    if nr <= 32 and nr > 16:
        fs = 7
    elif nr <= 16 and nr > 8:
        fs = 9
    elif nr <= 8:
        fs = 11

    return lx, ly, fs


def creategrid(nr, nc):

    x = np.arange(1, nc+1, 1)
    y = np.arange(1, nr+1, 1)
    x, y = np.meshgrid(x, y)

    return x, y


def dispXYZfromTable(table, well):

    if well == 96:
        nr = 8
        nc = 12
    elif well == 384:
        nr = 16
        nc = 24
    elif well == 1536:
        nr = 32
        nc = 48

    # read data from dataframe
    xpos = table['XPos']
    ypos = table['YPos']
    zpos = table['ZPos']
    # normalize z-data
    zpos_norm = zpos - zpos.max()
    z = zpos_norm.reshape(nr, nc)
    xpos2d = xpos.reshape(nr, nc)
    ypos2d = ypos.reshape(nr, nc)

    # create different views

    # show 2D plot
    ShowPlateDataZ(nr, nc, z, showlabels=True)
    # show 3D plot using the absolute XY positions
    ShowPlateDataZ3Dpos(xpos2d, ypos2d, z, showlabels=False)
    # show 3D plot using the XY position index (1-8 and 1-12 for a 96 well plate
    ShowPlateDataZ3Dwell(nr, nc, z, showlabels=True)
    # show 3D wireframe plot using the XY position index (1-8 and 1-12 for a 96 well plate
    ShowPlateDataZWireFrame(xpos2d, ypos2d, z, showlabels=True)

    plt.show()


def ShowPlateDataZ(nr, nc, data, showlabels=True):

    print np.shape(data), nr, nc
    # extract labels when needed
    if showlabels:
        labelx, labely, fs = ExtractLabels(nr, nc)

    # create figure
    fig = plt.figure(figsize=(10, 6), dpi=100)
    ax = fig.add_subplot(111)

    # set colormap
    cmap = cm.coolwarm

    # show the well plate as an image
    cax = ax.imshow(data, interpolation='nearest', cmap=cmap)
    ax.grid(True, 'minor', ls='solid', lw=4, color='black')

    #format the display
    ax.set_xticks(np.arange(0, nc, 1))
    ax.set_yticks(np.arange(0, nr, 1))
    if showlabels:
        ax.set_xticklabels(labelx, fontsize=fs)
        ax.set_yticklabels(labely, fontsize=fs)
    ax.set_title('Z-Offset [micron] per Well')
    cbar = fig.colorbar(cax)


def ShowPlateDataZ3Dwell(nr, nc, z, showlabels=True):

    # extract labels when needed
    if showlabels:
        labelx, labely, fs = ExtractLabels(nr, nc)

    fig = plt.figure(figsize=(10, 6), dpi=100)
    ax = fig.gca(projection='3d')
    x, y = creategrid(nr, nc)
    surf = ax.plot_surface(x, y, z, rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0, antialiased=False)
    fig.colorbar(surf, shrink=0.5, aspect=5)
    ax.auto_scale_xyz([0, nc], [0, nr], [z.min(), z.max()])
    ax.set_aspect('equal')

    #format the display
    ax.set_xticks(np.arange(0, nc, 1))
    ax.set_yticks(np.arange(0, nr, 1))
    if showlabels:
        ax.set_xticklabels(labelx, fontsize=fs)
        ax.set_yticklabels(labely, fontsize=fs)
    ax.set_title('Z-Offset [micron] per Well')


def ShowPlateDataZ3Dpos(x, y, data, showlabels=True):

    fig = plt.figure(figsize=(10, 6), dpi=100)
    ax = fig.gca(projection='3d')
    surf = ax.plot_surface(x, y, data, rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0, antialiased=False)
    fig.colorbar(surf, shrink=0.5, aspect=5)
    ax.set_aspect('equal')
    ax.set_title('Z-Offset [micron] per Well')


def ShowPlateDataZWireFrame(x, y, z, showlabels=True):


    fig = plt.figure(figsize=(10, 6), dpi=100)
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_wireframe(x, y, z, rstride=1, cstride=1)
