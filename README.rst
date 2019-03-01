==================================
BioFormatsRead - Scripts and Tools
==================================

This collection of scripts can be used to read image data using BioFormats into numpy arrays.
It was initially created to simplify reading CZI image files, but should work with many more
image data files thanks to BioFormats.

The main scripts are:

*   bftools.py
*   czitools.py
*   misctools.py

:Author: Sebastian Rhode

:Version: 2019.03.01

Important Requirements
----------------------
* `Python 3 <http://www.python.org>`_
* `Numpy <http://www.numpy.org>`_
* `Matplotlib <http://www.matplotlib.org>`_
* `python-bioformats <https://github.com/CellProfiler/python-bioformats>`_
* `BioFormats package <http://downloads.openmicroscopy.org/bio-formats/>`_
* `zisraw <https://pypi.org/project/zisraw/>`_

Notes
-----
The package is still under development and was mainly tested with CZI files.

The newer versions of the BioFormats library offers various new features for reading especially CZI images,
which are currently not fully supported by python-bioformats. But most of the functionality should work without any problems.

More information can be found at: `python-and-bioformats <http://slides.com/sebastianrhode/python-and-bioformats/fullscreen>`_

Acknowledgements
----------------
*   Christoph Gohlke from providing the zisraw package.
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
