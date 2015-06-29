===============================
bfimage
===============================

This package can be used to read image data using BioFormats into numpy arrays.
It was initially created to simplify reading CZI image files, but should work with many more
image data files thanks to BioFormats.

:Author: Sebastian Rhode

:Version: 2015.06.18

Requirements
------------
* `CPython 2.7 <http://www.python.org>`_
* `Numpy 1.8.2 <http://www.numpy.org>`_
* `python-bioformats <https://github.com/CellProfiler/python-bioformats>`_
* `BioFormats package <http://downloads.openmicroscopy.org/bio-formats/>`_
* `javabridge <https://pypi.python.org/pypi/javabridge>`_
* `czifile <http://www.lfd.uci.edu/~gohlke/code/czifile.py.html>`_

Notes
-----
The package is still under development and was mainly tested with CZI files.

The python-bioformats package includes loci_tool.jar but it is also possible to use the latest bioformats_package.jar.
Currently the 5.1.2 version of bioformats_package.jar is used. Update it to your needs.

Acknowledgements
----------------
*   Christoph Gohlke from providing the czifily.py.
*   The Cellprofiler team for providing python-bioformats
*   The OME people for creating BioFormats                                                                                 

References
----------
(1)  CZI - Image format for microscopes
     http://www.zeiss.com/czi
(2)  The OME-TIFF format.
     http://www.openmicroscopy.org/site/support/file-formats/ome-tiff
(3)  Read microscopy images to numpy array with python-bioformats.
     http://ilovesymposia.com/2014/08/10/read-microscopy-images-to-numpy-arrays-with-python-bioformats/
