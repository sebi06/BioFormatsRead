# -*- coding: utf-8 -*-
"""
@author: Sebi

File: zencom.py
Date: 18.04.2017
Version. 0.2
"""

from __future__ import print_function
import win32com.client
import numpy as np


def getZENScripting():

    # Import the ZEN OAD Scripting into Python
    try:
        Zen = win32com.client.GetActiveObject("Zeiss.Micro.Scripting.ZenWrapperLM")
        print('Successfully imported ZEN Scripting.')
    except:
        print('Could not import ZEN Scripting.')
        raise

    return Zen


def readXYZ(Zen):

    xyz = [np.NaN, np.NaN, np.NaN]

    # read actual XYZ positions
    try:
        xyz[0] = Zen.Devices.Stage.ActualPositionX
        xyz[1] = Zen.Devices.Stage.ActualPositionX
        xyz[2] = Zen.Devices.Focus.ActualPosition
        print('XYZ Position [micron]: ', xyz[0], xyz[1], xyz[2])
    except:
        print('Could not read current XYZ position.')

    return xyz


def runExperiment(ZEN_Experiment, savefolder, cziname, showCZI=False):

    # Import the ZEN OAD Scripting into Python
    Zen = getZENScripting()

    # read XYZ values
    readXYZ(Zen)

    # move focus to defined position
    Zen.Devices.Focus.MoveTo(500.0)

    # run the experiment in ZEN and save the data to the specified folder
    exp = Zen.Acquisition.Experiments.GetByName(ZEN_Experiment)
    img = Zen.Acquisition.Execute(exp)

    # close the experiment
    exp.Close()

    if showCZI == True:
        Zen.Application.Documents.Add(img)

    # Use the correct save method - it is polymorphic ... :)
    czifilename_complete = savefolder + cziname
    img.Save_2(czifilename_complete)

    if showCZI == False:
        # close the image
        img.Close()

    return czifilename_complete

