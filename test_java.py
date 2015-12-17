# -*- coding: utf-8 -*-
"""
@author: Sebi

File: test_java.py
Date: 17.12.2015
Version. 0.1
"""

import os
import javabridge as jv

# modify path to your needs
path = r'C:\Users\Testuser\Documents\Software\BioFormats_Package\5.1.7\bioformats_package.jar'
jars = jv.JARS + [path]
jv.start_vm(class_path=jars, max_heap_size='2G')

# get all the places
paths = jv.JClassWrapper('java.lang.System').getProperty('java.class.path').split(";")

for path in paths:
    print "%s: %s" %("exists" if os.path.isfile(path) else "missing", path)
    
