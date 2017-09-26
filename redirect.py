# -*- coding: utf-8 -*-
"""
@author: Sebi

File: redirect.py
Date: 01.09.2016
Version. 0.1
"""

import bftools as bf
import os

script2test = 'test_get_image6d.py'

of = bf.output2file(scriptname=script2test, output_name=script2test[:-3] + '_results.txt', targetdir=os.getcwd())

