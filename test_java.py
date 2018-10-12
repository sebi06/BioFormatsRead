# -*- coding: utf-8 -*-
"""
@author: Sebi

File: test_java.py
Date: 01.07.2018
Version. 0.3
"""

from __future__ import print_function
import os
import javabridge as jv

# modify path to your needs
bfpackage = r'bfpackage/5.8.2/bioformats_package.jar'
jars = jv.JARS + [bfpackage]
jv.start_vm(class_path=jars, max_heap_size='4G')

# get all the places
paths = jv.JClassWrapper('java.lang.System').getProperty('java.class.path').split(";")

for path in paths:
    print("%s: %s" % ("exists" if os.path.isfile(path) else "missing", path))
