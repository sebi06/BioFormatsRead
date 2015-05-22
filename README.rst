===============================
bfimage
===============================

This package can be used to read image data using BioFormats into numpy arrays.
It was initially created to read CZI image files, but should work with many more
image data files thanks to BioFormats.

:Author: Sebastian Rhode

:Version: 2015.05.18

Requirements
------------
* `CPython 2.7 <http://www.python.org>`_
* `Numpy 1.8.2 <http://www.numpy.org>`_
* `CellProfiler.bioformats <https://github.com/CellProfiler/python-bioformats>`_
* `czifile <http://www.lfd.uci.edu/~gohlke/code/czifile.py.html>`_

Notes
-----
The package is still under development and was mainly tested with CZI files.

Acknowledgements
----------------
*   Christoph Gohlke from providing the czifily.py.
*   The Cellprofiler team for providing python-bioformats
*   The OME people for creating BioFormats and ist readers                                                                                 

References
----------
(1)  CZI - Image format for microscopes
     http://www.zeiss.com/czi
(2)  The OME-TIFF format.
     http://www.openmicroscopy.org/site/support/file-formats/ome-tiff
