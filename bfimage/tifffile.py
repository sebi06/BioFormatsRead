

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# tifffile.py

# Copyright (c) 2008-2015, Christoph Gohlke
# Copyright (c) 2008-2015, The Regents of the University of California
# Produced at the Laboratory for Fluorescence Dynamics
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright
#   notice, this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in the
#   documentation and/or other materials provided with the distribution.
# * Neither the name of the copyright holders nor the names of any
#   contributors may be used to endorse or promote products derived
#   from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

"""Read image and meta data from (bio)TIFF files. Save numpy arrays as TIFF.

Image and metadata can be read from TIFF, BigTIFF, OME-TIFF, STK, LSM, NIH,
SGI, ImageJ, MicroManager, FluoView, SEQ and GEL files.
Only a subset of the TIFF specification is supported, mainly uncompressed
and losslessly compressed 2**(0 to 6) bit integer, 16, 32 and 64-bit float,
grayscale and RGB(A) images, which are commonly used in bio-scientific imaging.
Specifically, reading JPEG and CCITT compressed image data, chroma subsampling,
or EXIF, IPTC, GPS, and XMP metadata is not implemented. Only primary info
records are read for STK, FluoView, MicroManager, and NIH Image formats.

TIFF, the Tagged Image File Format, is under the control of Adobe Systems.
BigTIFF allows for files greater than 4 GB. STK, LSM, FluoView, SGI, SEQ, GEL,
and OME-TIFF, are custom extensions defined by Molecular Devices (Universal
Imaging Corporation), Carl Zeiss MicroImaging, Olympus, Silicon Graphics
International, Media Cybernetics, Molecular Dynamics, and the Open Microscopy
Environment consortium respectively.

For command line usage run `python tifffile.py --help`

:Author:
  `Christoph Gohlke <http://www.lfd.uci.edu/~gohlke/>`_

:Organization:
  Laboratory for Fluorescence Dynamics, University of California, Irvine

:Version: 2015.09.25

Requirements
------------
* `CPython 2.7 or 3.5 <http://www.python.org>`_ (64 bit recommended)
* `Numpy 1.9.3 <http://www.numpy.org>`_
* `Matplotlib 1.4.3 <http://www.matplotlib.org>`_ (optional for plotting)
* `Tifffile.c 2015.08.17 <http://www.lfd.uci.edu/~gohlke/>`_
  (recommended for faster decoding of PackBits and LZW encoded strings)

Revisions
---------
2015.09.25
    Read images with reversed bit order (fill_order is lsb2msb).
2015.09.21
    Read RGB OME-TIFF.
    Warn about malformed OME-XML.
2015.09.16
    Detect some corrupted ImageJ metadata.
    Better axes labels for 'shaped' files.
    Do not create TiffTags for default values.
    Chroma subsampling is not supported.
    Memory-map data in TiffPageSeries if possible (optional).
2015.08.17
    Pass 1906 tests.
    Write ImageJ hyperstacks (optional).
    Read and write LZMA compressed data.
    Specify datetime when saving (optional).
    Save tiled and color-mapped images (optional).
    Ignore void byte_counts and offsets if possible.
    Ignore bogus image_depth tag created by ISS Vista software.
    Decode floating point horizontal differencing (not tiled).
    Save image data contiguously if possible.
    Only read first IFD from ImageJ files if possible.
    Read ImageJ 'raw' format (files larger than 4 GB).
    TiffPageSeries class for pages with compatible shape and data type.
    Try to read incomplete tiles.
    Open file dialog if no filename is passed on command line.
    Ignore errors when decoding OME-XML.
    Rename decoder functions (backwards incompatible)
2014.08.24
    TiffWriter class for incremental writing images.
    Simplified examples.
2014.08.19
    Add memmap function to FileHandle.
    Add function to determine if image data in TiffPage is memory-mappable.
    Do not close files if multifile_close parameter is False.
2014.08.10
    Pass 1730 tests.
    Return all extrasamples by default (backwards incompatible).
    Read data from series of pages into memory-mapped array (optional).
    Squeeze OME dimensions (backwards incompatible).
    Workaround missing EOI code in strips.
    Support image and tile depth tags (SGI extension).
    Better handling of STK/UIC tags (backwards incompatible).
    Disable color mapping for STK.
    Julian to datetime converter.
    TIFF ASCII type may be NULL separated.
    Unwrap strip offsets for LSM files greater than 4 GB.
    Correct strip byte counts in compressed LSM files.
    Skip missing files in OME series.
    Read embedded TIFF files.
2014.02.05
    Save rational numbers as type 5 (bug fix).
2013.12.20
    Keep other files in OME multi-file series closed.
    FileHandle class to abstract binary file handle.
    Disable color mapping for bad OME-TIFF produced by bio-formats.
    Read bad OME-XML produced by ImageJ when cropping.
2013.11.03
    Allow zlib compress data in imsave function (optional).
    Memory-map contiguous image data (optional).
2013.10.28
    Read MicroManager metadata and little endian ImageJ tag.
    Save extra tags in imsave function.
    Save tags in ascending order by code (bug fix).
2012.10.18
    Accept file like objects (read from OIB files).
2012.08.21
    Rename TIFFfile to TiffFile and TIFFpage to TiffPage.
    TiffSequence class for reading sequence of TIFF files.
    Read UltraQuant tags.
    Allow float numbers as resolution in imsave function.
2012.08.03
    Read MD GEL tags and NIH Image header.
2012.07.25
    Read ImageJ tags.
    ...

Notes
-----
The API is not stable yet and might change between revisions.

Tested on little-endian platforms only.

Other Python packages and modules for reading bio-scientific TIFF files:

*  `Imread <http://luispedro.org/software/imread>`_
*  `PyLibTiff <http://code.google.com/p/pylibtiff>`_
*  `SimpleITK <http://www.simpleitk.org>`_
*  `PyLSM <https://launchpad.net/pylsm>`_
*  `PyMca.TiffIO.py <http://pymca.sourceforge.net/>`_ (same as fabio.TiffIO)
*  `BioImageXD.Readers <http://www.bioimagexd.net/>`_
*  `Cellcognition.io <http://cellcognition.org/>`_
*  `CellProfiler.bioformats
   <https://github.com/CellProfiler/python-bioformats>`_

Acknowledgements
----------------
*   Egor Zindy, University of Manchester, for cz_lsm_scan_info specifics.
*   Wim Lewis for a bug fix and some read_cz_lsm functions.
*   Hadrien Mary for help on reading MicroManager files.
*   Christian Kliche for help writing tiled and color-mapped files.

References
----------
(1) TIFF 6.0 Specification and Supplements. Adobe Systems Incorporated.
    http://partners.adobe.com/public/developer/tiff/
(2) TIFF File Format FAQ. http://www.awaresystems.be/imaging/tiff/faq.html
(3) MetaMorph Stack (STK) Image File Format.
    http://support.meta.moleculardevices.com/docs/t10243.pdf
(4) Image File Format Description LSM 5/7 Release 6.0 (ZEN 2010).
    Carl Zeiss MicroImaging GmbH. BioSciences. May 10, 2011
(5) File Format Description - LSM 5xx Release 2.0.
    http://ibb.gsf.de/homepage/karsten.rodenacker/IDL/Lsmfile.doc
(6) The OME-TIFF format.
    http://www.openmicroscopy.org/site/support/file-formats/ome-tiff
(7) UltraQuant(r) Version 6.0 for Windows Start-Up Guide.
    http://www.ultralum.com/images%20ultralum/pdf/UQStart%20Up%20Guide.pdf
(8) Micro-Manager File Formats.
    http://www.micro-manager.org/wiki/Micro-Manager_File_Formats
(9) Tags for TIFF and Related Specifications. Digital Preservation.
    http://www.digitalpreservation.gov/formats/content/tiff_tags.shtml

Examples
--------
>>> data = numpy.random.rand(5, 301, 219)
>>> imsave('temp.tif', data)

>>> image = imread('temp.tif')
>>> numpy.testing.assert_array_equal(image, data)

>>> with TiffFile('temp.tif') as tif:
...     images = tif.asarray()
...     for page in tif:
...         for tag in page.tags.values():
...             t = tag.name, tag.value
...         image = page.asarray()

"""

from __future__ import division, print_function

import sys
import os
import re
import glob
import math
import zlib
import time
import json
import struct
import warnings
import tempfile
import datetime
import collections
from fractions import Fraction
from xml.etree import cElementTree as etree

import numpy

try:
    import lzma
except ImportError:
    try:
        import backports.lzma as lzma
    except ImportError:
        lzma = None

try:
    if __package__:
        from . import _tifffile
    else:
        import _tifffile
except ImportError:
    warnings.warn(
        "failed to import the optional _tifffile C extension module.\n"
        "Loading of some compressed images will be very slow.\n"
        "Tifffile.c can be obtained at http://www.lfd.uci.edu/~gohlke/")


__version__ = '2015.09.25'
__docformat__ = 'restructuredtext en'
__all__ = (
    'imsave', 'imread', 'imshow', 'TiffFile', 'TiffWriter', 'TiffSequence',
    # utility functions used in oiffile and czifile
    'FileHandle', 'lazyattr', 'natural_sorted', 'decode_lzw', 'stripnull')


def imsave(filename, data, **kwargs):
    """Write image data to TIFF file.

    Refer to the TiffWriter class and member functions for documentation.

    Parameters
    ----------
    filename : str
        Name of file to write.
    data : array_like
        Input image. The last dimensions are assumed to be image depth,
        height, width, and samples.
    kwargs : dict
        Parameters 'byteorder', 'bigtiff', 'software', and 'imagej', are passed
        to the TiffWriter class.
        Parameters 'photometric', 'planarconfig', 'resolution', 'compress',
        'colormap', 'tile', 'description', 'datetime', 'metadata', 'contiguous'
        and 'extratags' are passed to the TiffWriter.save function.

    Examples
    --------
    >>> data = numpy.random.rand(2, 5, 3, 301, 219)
    >>> metadata = {'axes': 'TZCYX'}
    >>> imsave('temp.tif', data, compress=6, metadata={'axes': 'TZCYX'})

    """
    tifargs = {}
    for key in ('byteorder', 'bigtiff', 'software', 'imagej'):
        if key in kwargs:
            tifargs[key] = kwargs[key]
            del kwargs[key]

    if 'bigtiff' not in tifargs and 'imagej' not in tifargs and (
            data.size*data.dtype.itemsize > 2000*2**20):
        tifargs['bigtiff'] = True

    with TiffWriter(filename, **tifargs) as tif:
        tif.save(data, **kwargs)


class TiffWriter(object):
    """Write image data to TIFF file.

    TiffWriter instances must be closed using the 'close' method, which is
    automatically called when using the 'with' statement.

    Examples
    --------
    >>> data = numpy.random.rand(2, 5, 3, 301, 219)
    >>> with TiffWriter('temp.tif', bigtiff=True) as tif:
    ...     for i in range(data.shape[0]):
    ...         tif.save(data[i], compress=6)

    """
    TYPES = {'B': 1, 's': 2, 'H': 3, 'I': 4, '2I': 5, 'b': 6,
             'h': 8, 'i': 9, 'f': 11, 'd': 12, 'Q': 16, 'q': 17}
    TAGS = {
        'new_subfile_type': 254, 'subfile_type': 255,
        'image_width': 256, 'image_length': 257, 'bits_per_sample': 258,
        'compression': 259, 'photometric': 262, 'document_name': 269,
        'image_description': 270, 'strip_offsets': 273, 'orientation': 274,
        'samples_per_pixel': 277, 'rows_per_strip': 278,
        'strip_byte_counts': 279, 'x_resolution': 282, 'y_resolution': 283,
        'planar_configuration': 284, 'page_name': 285, 'resolution_unit': 296,
        'software': 305, 'datetime': 306, 'predictor': 317, 'color_map': 320,
        'tile_width': 322, 'tile_length': 323, 'tile_offsets': 324,
        'tile_byte_counts': 325, 'extra_samples': 338, 'sample_format': 339,
        'smin_sample_value': 340, 'smax_sample_value': 341,
        'image_depth': 32997, 'tile_depth': 32998}

    def __init__(self, filename, bigtiff=False, byteorder=None,
                 software='tifffile.py', imagej=False):
        """Create a new TIFF file for writing.

        Use bigtiff=True when creating files larger than 2 GB.

        Parameters
        ----------
        filename : str
            Name of file to write.
        bigtiff : bool
            If True, the BigTIFF format is used.
        byteorder : {'<', '>'}
            The endianness of the data in the file.
            By default this is the system's native byte order.
        software : str
            Name of the software used to create the file.
            Saved with the first page in the file only.
        imagej : bool
            If True, write an ImageJ hyperstack compatible file.
            This format can handle data types uint8, uint16, or float32 and
            data shapes up to 6 dimensions in TZCYXS order.
            RGB images (S=3 or S=4) must be uint8.
            ImageJ's default byte order is big endian but this implementation
            uses the system's native byte order by default.
            ImageJ does not support BigTIFF format or LZMA compression.
            The ImageJ file format is undocumented.

        """
        if byteorder not in (None, '<', '>'):
            raise ValueError("invalid byteorder %s" % byteorder)
        if byteorder is None:
            byteorder = '<' if sys.byteorder == 'little' else '>'
        if imagej and bigtiff:
            warnings.warn("writing incompatible bigtiff ImageJ")

        self._byteorder = byteorder
        self._software = software
        self._imagej = bool(imagej)
        self._metadata = None
        self._colormap = None

        self._description_offset = 0
        self._description_len_offset = 0
        self._description_len = 0

        self._tags = None
        self._shape = None  # normalized shape of data in consecutive pages
        self._data_shape = None  # shape of data in consecutive pages
        self._data_dtype = None  # data type
        self._data_offset = None  # offset to data
        self._data_byte_counts = None  # byte counts per plane
        self._tag_offsets = None  # strip or tile offset tag code

        self._fh = open(filename, 'wb')
        self._fh.write({'<': b'II', '>': b'MM'}[byteorder])

        if bigtiff:
            self._bigtiff = True
            self._offset_size = 8
            self._tag_size = 20
            self._numtag_format = 'Q'
            self._offset_format = 'Q'
            self._value_format = '8s'
            self._fh.write(struct.pack(byteorder+'HHH', 43, 8, 0))
        else:
            self._bigtiff = False
            self._offset_size = 4
            self._tag_size = 12
            self._numtag_format = 'H'
            self._offset_format = 'I'
            self._value_format = '4s'
            self._fh.write(struct.pack(byteorder+'H', 42))

        # first IFD
        self._ifd_offset = self._fh.tell()
        self._fh.write(struct.pack(byteorder+self._offset_format, 0))

    def save(self, data, photometric=None, planarconfig=None, resolution=None,
             compress=0, colormap=None, tile=None, datetime=None,
             description='', metadata=None, contiguous=True, extratags=()):
        """Write image data and tags to TIFF file.

        Image data are written in one stripe per plane by default.
        Dimensions larger than 2 to 4 (depending on photometric mode, planar
        configuration, and SGI mode) are flattened and saved as separate pages.
        The 'sample_format' and 'bits_per_sample' tags are derived from
        the data type.

        Parameters
        ----------
        data : numpy.ndarray
            Input image. The last dimensions are assumed to be image depth,
            height (length), width, and samples.
            If a colormap is provided, the dtype must be uint8 or uint16 and
            the data values are indices into the last dimension of the
            colormap.
        photometric : {'minisblack', 'miniswhite', 'rgb', 'palette'}
            The color space of the image data.
            By default this setting is inferred from the data shape and the
            value of colormap.
        planarconfig : {'contig', 'planar'}
            Specifies if samples are stored contiguous or in separate planes.
            By default this setting is inferred from the data shape.
            'contig': last dimension contains samples.
            'planar': third last dimension contains samples.
        resolution : (float, float) or ((int, int), (int, int))
            X and Y resolution in dots per inch as float or rational numbers.
        compress : int or 'lzma'
            Values from 0 to 9 controlling the level of zlib compression.
            If 0, data are written uncompressed (default).
            Compression cannot be used to write contiguous files.
            If 'lzma', LZMA compression is used, which is not available on
            all platforms.
        colormap : numpy.ndarray
            RGB color values for the corresponding data value.
            Must be of shape (3, 2**(data.itemsize*8)) and dtype uint16.
        tile : tuple of int
            The shape (depth, length, width) of image tiles to write.
            If None (default), image data are written in one stripe per plane.
            The tile length and width must be a multiple of 16.
            If the tile depth is provided, the SGI image_depth and tile_depth
            tags are used to save volume data. Few software can read the
            SGI format, e.g. MeVisLab.
        datetime : datetime
            Date and time of image creation. Saved with the first page only.
            If None (default), the current date and time is used.
        description : str
            The subject of the image. Saved with the first page only.
            Cannot be used with the ImageJ format. If None (default),
            the data shape and metadata are saved in JSON or ImageJ format.
        metadata : dict
            Additional meta data passed to the image description functions.
        contiguous : bool
            If True (default) and the data and parameters are compatible with
            previous ones, if any, the data are stored contiguously after
            the previous one. Parameters 'photometric' and 'planarconfig' are
            ignored.
        extratags : sequence of tuples
            Additional tags as [(code, dtype, count, value, writeonce)].

            code : int
                The TIFF tag Id.
            dtype : str
                Data type of items in 'value' in Python struct format.
                One of B, s, H, I, 2I, b, h, i, f, d, Q, or q.
            count : int
                Number of data values. Not used for string values.
            value : sequence
                'Count' values compatible with 'dtype'.
            writeonce : bool
                If True, the tag is written to the first page only.

        """
        # TODO: refactor this function
        fh = self._fh
        byteorder = self._byteorder
        numtag_format = self._numtag_format
        value_format = self._value_format
        offset_format = self._offset_format
        offset_size = self._offset_size
        tag_size = self._tag_size

        data = numpy.asarray(data, dtype=byteorder+data.dtype.char, order='C')

        # just append contiguous data if possible
        if self._data_shape:
            if (not contiguous or
                    self._data_shape[1:] != data.shape or
                    self._data_dtype != data.dtype or
                    (compress and self._tags) or
                    tile or
                    not numpy.array_equal(colormap, self._colormap)):
                # incompatible shape, dtype, compression mode, or colormap
                self._write_remaining_pages()
                self._write_image_description()
                self._description_offset = 0
                self._description_len_offset = 0
                self._data_shape = None
                self._colormap = None
                if self._imagej:
                    raise ValueError(
                        "ImageJ does not support non-contiguous data")
            else:
                # consecutive mode
                self._data_shape = (self._data_shape[0] + 1,) + data.shape
                if not compress:
                    # write contiguous data, write ifds/tags later
                    data.tofile(fh)
                    return

        if photometric not in (None, 'minisblack', 'miniswhite',
                               'rgb', 'palette'):
            raise ValueError("invalid photometric %s" % photometric)
        if planarconfig not in (None, 'contig', 'planar'):
            raise ValueError("invalid planarconfig %s" % planarconfig)

        # prepare compression
        if not compress:
            compress = False
            compress_tag = 1
        elif compress == 'lzma':
            compress = lzma.compress
            compress_tag = 34925
            if self._imagej:
                raise ValueError("ImageJ can not handle LZMA compression")
        elif not 0 <= compress <= 9:
            raise ValueError("invalid compression level %s" % compress)
        elif compress:
            def compress(data, level=compress):
                return zlib.compress(data, level)
            compress_tag = 32946

        # prepare ImageJ format
        if self._imagej:
            if description:
                warnings.warn("not writing description to ImageJ file")
                description = None
            volume = False
            if data.dtype.char not in 'BHhf':
                raise ValueError("ImageJ does not support data type '%s'"
                                 % data.dtype.char)
            ijrgb = photometric == 'rgb' if photometric else None
            if data.dtype.char not in 'B':
                ijrgb = False
            ijshape = imagej_shape(data.shape, ijrgb)
            if ijshape[-1] in (3, 4):
                photometric = 'rgb'
                if data.dtype.char not in 'B':
                    raise ValueError("ImageJ does not support data type '%s' "
                                     "for RGB" % data.dtype.char)
            elif photometric is None:
                photometric = 'minisblack'
                planarconfig = None
            if planarconfig == 'planar':
                raise ValueError("ImageJ does not support planar images")
            else:
                planarconfig = 'contig' if ijrgb else None

        # verify colormap and indices
        if colormap is not None:
            if data.dtype.char not in 'BH':
                raise ValueError("invalid data dtype for palette mode")
            colormap = numpy.asarray(colormap, dtype=byteorder+'H')
            if colormap.shape != (3, 2**(data.itemsize * 8)):
                raise ValueError("invalid color map shape")
            self._colormap = colormap

        # verify tile shape
        if tile:
            tile = tuple(int(i) for i in tile[:3])
            volume = len(tile) == 3
            if (len(tile) < 2 or tile[-1] % 16 or tile[-2] % 16 or
                    any(i < 1 for i in tile)):
                raise ValueError("invalid tile shape")
        else:
            tile = ()
            volume = False

        # normalize data shape to 5D or 6D, depending on volume:
        #   (pages, planar_samples, [depth,] height, width, contig_samples)
        data_shape = shape = data.shape
        data = numpy.atleast_2d(data)

        samplesperpixel = 1
        extrasamples = 0
        if volume and data.ndim < 3:
            volume = False
        if colormap is not None:
            photometric = 'palette'
            planarconfig = None
        if photometric is None:
            if planarconfig:
                photometric = 'rgb'
            elif data.ndim > 2 and shape[-1] in (3, 4):
                photometric = 'rgb'
            elif self._imagej:
                photometric = 'minisblack'
            elif volume and data.ndim > 3 and shape[-4] in (3, 4):
                photometric = 'rgb'
            elif data.ndim > 2 and shape[-3] in (3, 4):
                photometric = 'rgb'
            else:
                photometric = 'minisblack'
        if planarconfig and len(shape) <= (3 if volume else 2):
            planarconfig = None
            photometric = 'minisblack'
        if photometric == 'rgb':
            if len(shape) < 3:
                raise ValueError("not a RGB(A) image")
            if len(shape) < 4:
                volume = False
            if planarconfig is None:
                if shape[-1] in (3, 4):
                    planarconfig = 'contig'
                elif shape[-4 if volume else -3] in (3, 4):
                    planarconfig = 'planar'
                elif shape[-1] > shape[-4 if volume else -3]:
                    planarconfig = 'planar'
                else:
                    planarconfig = 'contig'
            if planarconfig == 'contig':
                data = data.reshape((-1, 1) + shape[(-4 if volume else -3):])
                samplesperpixel = data.shape[-1]
            else:
                data = data.reshape(
                    (-1,) + shape[(-4 if volume else -3):] + (1,))
                samplesperpixel = data.shape[1]
            if samplesperpixel > 3:
                extrasamples = samplesperpixel - 3
        elif planarconfig and len(shape) > (3 if volume else 2):
            if planarconfig == 'contig':
                data = data.reshape((-1, 1) + shape[(-4 if volume else -3):])
                samplesperpixel = data.shape[-1]
            else:
                data = data.reshape(
                    (-1,) + shape[(-4 if volume else -3):] + (1,))
                samplesperpixel = data.shape[1]
            extrasamples = samplesperpixel - 1
        else:
            planarconfig = None
            # remove trailing 1s
            while len(shape) > 2 and shape[-1] == 1:
                shape = shape[:-1]
            if len(shape) < 3:
                volume = False
            if False and (
                    photometric != 'palette' and
                    len(shape) > (3 if volume else 2) and shape[-1] < 5 and
                    all(shape[-1] < i
                        for i in shape[(-4 if volume else -3):-1])):
                # DISABLED: non-standard TIFF, e.g. (220, 320, 2)
                planarconfig = 'contig'
                samplesperpixel = shape[-1]
                data = data.reshape((-1, 1) + shape[(-4 if volume else -3):])
            else:
                data = data.reshape(
                    (-1, 1) + shape[(-3 if volume else -2):] + (1,))

        # normalize shape to 6D
        assert len(data.shape) in (5, 6)
        if len(data.shape) == 5:
            data = data.reshape(data.shape[:2] + (1,) + data.shape[2:])
        shape = data.shape

        if tile and not volume:
            tile = (1, tile[-2], tile[-1])

        if photometric == 'palette':
            if (samplesperpixel != 1 or extrasamples or
                    shape[1] != 1 or shape[-1] != 1):
                raise ValueError("invalid data shape for palette mode")

        if samplesperpixel == 2:
            warnings.warn("writing non-standard TIFF (samplesperpixel 2)")

        bytestr = bytes if sys.version[0] == '2' else (
            lambda x: bytes(x, 'utf-8') if isinstance(x, str) else x)
        tags = []  # list of (code, ifdentry, ifdvalue, writeonce)

        strip_or_tile = 'tile' if tile else 'strip'
        tag_byte_counts = TiffWriter.TAGS[strip_or_tile + '_byte_counts']
        tag_offsets = TiffWriter.TAGS[strip_or_tile + '_offsets']
        self._tag_offsets = tag_offsets

        def pack(fmt, *val):
            return struct.pack(byteorder+fmt, *val)

        def addtag(code, dtype, count, value, writeonce=False):
            # Compute ifdentry & ifdvalue bytes from code, dtype, count, value
            # Append (code, ifdentry, ifdvalue, writeonce) to tags list
            code = int(TiffWriter.TAGS.get(code, code))
            try:
                tifftype = TiffWriter.TYPES[dtype]
            except KeyError:
                raise ValueError("unknown dtype %s" % dtype)
            rawcount = count
            if dtype == 's':
                value = bytestr(value) + b'\0'
                count = rawcount = len(value)
                rawcount = value.find(b'\0\0')
                if rawcount < 0:
                    rawcount = count
                else:
                    rawcount += 1  # length of string without buffer
                value = (value,)
            if len(dtype) > 1:
                co