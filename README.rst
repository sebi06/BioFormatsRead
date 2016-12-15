===============================
bfimage
===============================

This package can be used to read image data using BioFormats into numpy arrays.
It was initially created to simplify reading CZI image files, but should work with many more
image data files thanks to BioFormats.

:Author: Sebastian Rhode

:Version: 2016.12.14

Requirements
------------
* `CPython 2.7 <http://www.python.org>`_
* `Numpy 1.8.2 <http://www.numpy.org>`_
* `python-bioformats <https://github.com/CellProfiler/python-bioformats>`_
* `BioFormats package <http://downloads.openmicroscopy.org/bio-formats/>`_
* `javabridge <https://pypi.python.org/pypi/javabridge>`_
* `czifile <http://www.lfd.uci.edu/~gohlke/code/czifile.py.html>`_
* `tifffile <http://www.lfd.uci.edu/~gohlke/code/tifffile.py.html>`_

Notes
-----
The package is still under development and was mainly tested with CZI files.

The python-bioformats package includes loci_tool.jar but it is also possible to use the latest bioformats_package.jar.
Currently the 5.1.10 version of bioformats_package.jar is used.

The new 5.3.0 version of the BioFormats library offers various new features for reading especially CZI images, which are currently not fully supoorted by python-bioformats.

Some more infos can be found at: `python-and-bioformats <http://slides.com/sebastianrhode/python-and-bioformats/fullscreen>`_

Acknowledgements
----------------
*   Christoph Gohlke from providing the czifile.py and tifffile.py.
*   The Cellprofiler team for providing python-bioformats.
*   The OME people for creating BioFormats.

References
----------
(1)  CZI - Image format for microscopes
     http://www.zeiss.com/czi
(2)  The OME-TIFF format.
     http://www.openmicroscopy.org/site/support/file-formats/ome-tiff
(3)  Read microscopy images to numpy array with python-bioformats.
     http://ilovesymposia.com/2014/08/10/read-microscopy-images-to-numpy-arrays-with-python-bioformats/

Additional Tools
----------------
*   Read image series, z-stacks, time series or single planes.
*   Retrieve all important meta-information.
*   Write OME-XML Metadata to XML file.
*   Create and write plane info table.
*   Create PlaneTable with containing als XYZ Positions.
*   Display XYZ data from PlaneTable.
*   Extract Well Information form Scenes (CZI only).

Screenshots
-----------

.. figure:: images/BFRead_Test.png
   :align: center
   :alt:

.. figure:: images/OME-XML_output.png
   :align: center
   :alt:

.. figure:: images/testwell96_planetable_XYZ-Pos.png
   :align: center
   :alt:

Disclaimer
----------
*   Remark: Please use at your own risk.
