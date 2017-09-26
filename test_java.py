# -*- coding: utf-8 -*-
"""
@author: Sebi

File: test_java.py
Date: 17.04.2017
Version. 0.2
"""

from __future__ import print_function
import os
import javabridge as jv

# modify path to your needs
bfpackage = r'bfpackage/5.4.1/bioformats_package.jar'
jars = jv.JARS + [bfpackage]
jv.start_vm(class_path=jars, max_heap_size='2G')

# get all the places
paths = jv.JClassWrapper('java.lang.System').getProperty('java.class.path').split(";")

for path in paths:
    print("%s: %s" %("exists" if os.path.isfile(path) else "missing", path))