# -*- coding: utf-8 -*-
"""
@author: Sebi

File: dispvalues.py
Date: 13.07.2015
Version. 0.1

This file just holds a class used to display the pixel values under the cursor.
I found this somewhere on the internet.
"""


class Formatter(object):

    def __init__(self, im):
        self.im = im

    def __call__(self, x, y):
        intensity = self.im.get_array()[int(y), int(x)]
        #return 'x={:.01f},  y={:.01f},  Int={:.01f}'.format(x, y, intensity)
        return 'X={:.0f}  Y={:.0f}  Int={:.0f}'.format(x, y, intensity)
