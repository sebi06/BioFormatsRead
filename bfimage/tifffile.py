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
Specifically, reading JPEG and CCITT compressed image data or EXIF, IPTC, GPS,
and XMP metadata is not implemented. Only primary info records are read for
STK, FluoView, MicroManager, and NIH Image formats.

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

:Version: 2015.08.17

Requirements
------------
* `CPython 2.7 or 3.4 <http://www.python.org>`_ (64 bit recommended)
* `Numpy 1.9.2 <http://www.numpy.org>`_
* `Matplotlib 1.4.3 <http://www.matplotlib.org>`_ (optional for plotting)
* `Tifffile.c 2015.08.17 <http://www.lfd.uci.edu/~gohlke/>`_
  (recommended for faster decoding of PackBits and LZW encoded strings)

Revisions
---------
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


__version__ = '2015.08.17'
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
        'compression': 259, 'photometric': 262, 'fill_order': 266,
        'document_name': 269, 'image_description': 270, 'strip_offsets': 273,
        'orientation': 274, 'samples_per_pixel': 277, 'rows_per_strip': 278,
        'strip_byte_counts': 279, 'x_resolution': 282, 'y_resolution': 283,
        'planar_configuration': 284, 'page_name': 285, 'resolution_unit': 296,
        'software': 305, 'datetime': 306, 'predictor': 317, 'color_map': 320,
        'tile_width': 322, 'tile_length': 323, 'tile_offsets': 324,
        'tile_byte_counts': 325, 'extra_samples': 338, 'sample_format': 339,
        'image_depth': 32997, 'tile_depth': 32998}

    def __init__(self, filename, bigtiff=False, byteorder=None,
                 software='tifffile.py', imagej=False):
        """Create a new TIFF file for writing.

        Use bigtiff=True when creating files greater than 2 GB.

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
            ImageJ doesn't support BigTIFF format or LZMA compression.
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
                raise ValueError("ImageJ can't handle LZMA compression")
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
                count *= int(dtype[:-1])
                dtype = dtype[-1]
            ifdentry = [pack('HH', code, tifftype),
                        pack(offset_format, rawcount)]
            ifdvalue = None
            if count == 1:
                if isinstance(value, (tuple, list, numpy.ndarray)):
                    value = value[0]
                ifdentry.append(pack(value_format, pack(dtype, value)))
            elif struct.calcsize(dtype) * count <= offset_size:
                ifdentry.append(pack(value_format,
                                     pack(str(count)+dtype, *value)))
            else:
                ifdentry.append(pack(offset_format, 0))
                if isinstance(value, numpy.ndarray):
                    assert value.size == count
                    assert value.dtype.char == dtype
                    ifdvalue = value.tobytes()
                else:
                    ifdvalue = pack(str(count)+dtype, *value)
            tags.append((code, b''.join(ifdentry), ifdvalue, writeonce))

        def rational(arg, max_denominator=1000000):
            # return nominator and denominator from float or two integers
            try:
                f = Fraction.from_float(arg)
            except TypeError:
                f = Fraction(arg[0], arg[1])
            f = f.limit_denominator(max_denominator)
            return f.numerator, f.denominator

        if description:
            # user provided description
            addtag('image_description', 's', 0, description, writeonce=True)

        # always write shape and metadata to image_description
        self._metadata = {} if metadata is None else metadata
        if self._imagej:
            description = imagej_description(
                data_shape, shape[-1] in (3, 4), self._colormap is not None,
                **self._metadata)
        else:
            description = image_description(
                data_shape, self._colormap is not None, **self._metadata)
        if description:
            # add 32 bytes buffer
            # the image description might be updated later with the final shape
            description += b'\0'*32
            self._description_len = len(description)
            addtag('image_description', 's', 0, description, writeonce=True)

        if self._software:
            addtag('software', 's', 0, self._software, writeonce=True)
            self._software = None  # only save to first page in file
        if datetime is None:
            datetime = self._now()
        addtag('datetime', 's', 0, datetime.strftime("%Y:%m:%d %H:%M:%S"),
               writeonce=True)
        addtag('compression', 'H', 1, compress_tag)
        addtag('image_width', 'I', 1, shape[-2])
        addtag('image_length', 'I', 1, shape[-3])
        if tile:
            addtag('tile_width', 'I', 1, tile[-1])
            addtag('tile_length', 'I', 1, tile[-2])
            if tile[0] > 1:
                addtag('image_depth', 'I', 1, shape[-4])
                addtag('tile_depth', 'I', 1, tile[0])
        addtag('new_subfile_type', 'I', 1, 0)
        addtag('sample_format', 'H', 1,
               {'u': 1, 'i': 2, 'f': 3, 'c': 6}[data.dtype.kind])
        addtag('photometric', 'H', 1, {'miniswhite': 0, 'minisblack': 1,
                                       'rgb': 2, 'palette': 3}[photometric])
        if colormap is not None:
            addtag('color_map', 'H', colormap.size, colormap)
        addtag('samples_per_pixel', 'H', 1, samplesperpixel)
        if planarconfig and samplesperpixel > 1:
            addtag('planar_configuration', 'H', 1, 1
                   if planarconfig == 'contig' else 2)
            addtag('bits_per_sample', 'H', samplesperpixel,
                   (data.dtype.itemsize * 8,) * samplesperpixel)
        else:
            addtag('bits_per_sample', 'H', 1, data.dtype.itemsize * 8)
        if extrasamples:
            if photometric == 'rgb' and extrasamples == 1:
                addtag('extra_samples', 'H', 1, 1)  # associated alpha channel
            else:
                addtag('extra_samples', 'H', extrasamples, (0,) * extrasamples)
        if resolution:
            addtag('x_resolution', '2I', 1, rational(resolution[0]))
            addtag('y_resolution', '2I', 1, rational(resolution[1]))
            addtag('resolution_unit', 'H', 1, 2)
        if not tile:
            addtag('rows_per_strip', 'I', 1, shape[-3])  # * shape[-4]

        if tile:
            # use one chunk per tile per plane
            tiles = ((shape[2] + tile[0] - 1) // tile[0],
                     (shape[3] + tile[1] - 1) // tile[1],
                     (shape[4] + tile[2] - 1) // tile[2])
            numtiles = product(tiles) * shape[1]
            strip_byte_counts = [
                product(tile) * shape[-1] * data.dtype.itemsize] * numtiles
            addtag(tag_byte_counts, offset_format, numtiles, strip_byte_counts)
            addtag(tag_offsets, offset_format, numtiles, [0] * numtiles)
            # allocate tile buffer
            chunk = numpy.empty(tile + (shape[-1],), dtype=data.dtype)
        else:
            # use one strip per plane
            strip_byte_counts = [
                data[0, 0].size * data.dtype.itemsize] * shape[1]
            addtag(tag_byte_counts, offset_format, shape[1], strip_byte_counts)
            addtag(tag_offsets, offset_format, shape[1], [0] * shape[1])

        # add extra tags from user
        for t in extratags:
            addtag(*t)

        # TODO: check TIFFReadDirectoryCheckOrder warning in files containing
        #   multiple tags of same code
        # the entries in an IFD must be sorted in ascending order by tag code
        tags = sorted(tags, key=lambda x: x[0])

        if not (self._bigtiff or self._imagej) and (
                fh.tell() + data.size*data.dtype.itemsize > 2**31-1):
            raise ValueError("data too large for standard TIFF file")

        # if not compressed or tiled, write the first ifd and then all data
        # contiguously; else, write all ifds and data interleaved
        for pageindex in range(shape[0] if (compress or tile) else 1):
            # update pointer at ifd_offset
            pos = fh.tell()
            fh.seek(self._ifd_offset)
            fh.write(pack(offset_format, pos))
            fh.seek(pos)

            # write ifdentries
            fh.write(pack(numtag_format, len(tags)))
            tag_offset = fh.tell()
            fh.write(b''.join(t[1] for t in tags))
            self._ifd_offset = fh.tell()
            fh.write(pack(offset_format, 0))  # offset to next IFD

            # write tag values and patch offsets in ifdentries, if necessary
            for tagindex, tag in enumerate(tags):
                if tag[2]:
                    pos = fh.tell()
                    fh.seek(tag_offset + tagindex*tag_size + offset_size + 4)
                    fh.write(pack(offset_format, pos))
                    fh.seek(pos)
                    if tag[0] == tag_offsets:
                        strip_offsets_offset = pos
                    elif tag[0] == tag_byte_counts:
                        strip_byte_counts_offset = pos
                    elif tag[0] == 270 and tag[2].endswith(b'\0\0\0\0'):
                        # image description buffer
                        self._description_offset = pos
                        self._description_len_offset = (
                            tag_offset + tagindex * tag_size + 4)
                    fh.write(tag[2])

            # write image data
            data_offset = fh.tell()
            if compress:
                strip_byte_counts = []
            if tile:
                for plane in data[pageindex]:
                    for tz in range(tiles[0]):
                        for ty in range(tiles[1]):
                            for tx in range(tiles[2]):
                                c0 = min(tile[0], shape[2] - tz*tile[0])
                                c1 = min(tile[1], shape[3] - ty*tile[1])
                                c2 = min(tile[2], shape[4] - tx*tile[2])
                                chunk[c0:, c1:, c2:] = 0
                                chunk[:c0, :c1, :c2] = plane[
                                    tz*tile[0]:tz*tile[0]+c0,
                                    ty*tile[1]:ty*tile[1]+c1,
                                    tx*tile[2]:tx*tile[2]+c2]
                                if compress:
                                    t = compress(chunk)
                                    strip_byte_counts.append(len(t))
                                    fh.write(t)
                                else:
                                    chunk.tofile(fh)
                                    fh.flush()
            elif compress:
                for plane in data[pageindex]:
                    plane = compress(plane)
                    strip_byte_counts.append(len(plane))
                    fh.write(plane)
            else:
                data.tofile(fh)  # if this fails try update Python and numpy

            # update strip/tile offsets and byte_counts if necessary
            pos = fh.tell()
            for tagindex, tag in enumerate(tags):
                if tag[0] == tag_offsets:  # strip/tile offsets
                    if tag[2]:
                        fh.seek(strip_offsets_offset)
                        strip_offset = data_offset
                        for size in strip_byte_counts:
                            fh.write(pack(offset_format, strip_offset))
                            strip_offset += size
                    else:
                        fh.seek(tag_offset + tagindex*tag_size +
                                offset_size + 4)
                        fh.write(pack(offset_format, data_offset))
                elif tag[0] == tag_byte_counts:  # strip/tile byte_counts
                    if compress:
                        if tag[2]:
                            fh.seek(strip_byte_counts_offset)
                            for size in strip_byte_counts:
                                fh.write(pack(offset_format, size))
                        else:
                            fh.seek(tag_offset + tagindex*tag_size +
                                    offset_size + 4)
                            fh.write(pack(offset_format, strip_byte_counts[0]))
                    break
            fh.seek(pos)
            fh.flush()

            # remove tags that should be written only once
            if pageindex == 0:
                tags = [tag for tag in tags if not tag[-1]]

        # if uncompressed, write remaining ifds/tags later
        if not (compress or tile):
            self._tags = tags

        self._shape = shape
        self._data_shape = (1,) + data_shape
        self._data_dtype = data.dtype
        self._data_offset = data_offset
        self._data_byte_counts = strip_byte_counts

    def _write_remaining_pages(self):
        """Write outstanding IFDs and tags to file."""
        if not self._tags:
            return

        fh = self._fh
        byteorder = self._byteorder
        numtag_format = self._numtag_format
        offset_format = self._offset_format
        offset_size = self._offset_size
        tag_size = self._tag_size
        data_offset = self._data_offset
        page_data_size = sum(self._data_byte_counts)
        tag_bytes = b''.join(t[1] for t in self._tags)
        numpages = self._shape[0] * self._data_shape[0] - 1

        pos = fh.tell()
        if not self._bigtiff and pos + len(tag_bytes) * numpages > 2**32 - 256:
            if self._imagej:
                warnings.warn("truncating ImageJ file")
                return
            raise ValueError("data too large for non-bigtiff file")

        def pack(fmt, *val):
            return struct.pack(byteorder+fmt, *val)

        for _ in range(numpages):
            # update pointer at ifd_offset
            pos = fh.tell()
            fh.seek(self._ifd_offset)
            fh.write(pack(offset_format, pos))
            fh.seek(pos)

            # write ifd entries
            fh.write(pack(numtag_format, len(self._tags)))
            tag_offset = fh.tell()
            fh.write(tag_bytes)
            self._ifd_offset = fh.tell()
            fh.write(pack(offset_format, 0))  # offset to next IFD

            # offset to image data
            data_offset += page_data_size

            # write tag values and patch offsets in ifdentries, if necessary
            for tagindex, tag in enumerate(self._tags):
                if tag[2]:
                    pos = fh.tell()
                    fh.seek(tag_offset + tagindex*tag_size + offset_size + 4)
                    fh.write(pack(offset_format, pos))
                    fh.seek(pos)
                    if tag[0] == self._tag_offsets:
                        strip_offsets_offset = pos
                    fh.write(tag[2])

            # update strip/tile offsets if necessary
            pos = fh.tell()
            for tagindex, tag in enumerate(self._tags):
                if tag[0] == self._tag_offsets:  # strip/tile offsets
                    if tag[2]:
                        fh.seek(strip_offsets_offset)
                        strip_offset = data_offset
                        for size in self._data_byte_counts:
                            fh.write(pack(offset_format, strip_offset))
                            strip_offset += size
                    else:
                        fh.seek(tag_offset + tagindex*tag_size +
                                offset_size + 4)
                        fh.write(pack(offset_format, data_offset))
                    break
            fh.seek(pos)

        self._tags = None
        self._data_dtype = None
        self._data_offset = None
        self._data_byte_counts = None
        # do not reset _shape or _data_shape

    def _write_image_description(self):
        """Write meta data to image_description tag."""
        if (not self._data_shape or self._data_shape[0] == 1 or
                self._description_offset <= 0):
            return

        colormapped = self._colormap is not None
        if self._imagej:
            isrgb = self._shape[-1] in (3, 4)
            description = imagej_description(
                self._data_shape, isrgb, colormapped, **self._metadata)
        else:
            description = image_description(
                self._data_shape, colormapped, **self._metadata)

        # rewrite description and its length to file
        description = description[:self._description_len-1]
        pos = self._fh.tell()
        self._fh.seek(self._description_offset)
        self._fh.write(description)
        self._fh.seek(self._description_len_offset)
        self._fh.write(struct.pack(self._byteorder+self._offset_format,
                                   len(description)+1))
        self._fh.seek(pos)

        self._description_offset = 0
        self._description_len_offset = 0
        self._description_len = 0

    def _now(self):
        """Return current date and time."""
        return datetime.datetime.now()

    def close(self, truncate=False):
        """Write remaining pages (if not truncate) and close file handle."""
        if not truncate:
            self._write_remaining_pages()
        self._write_image_description()
        self._fh.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()


def imread(files, **kwargs):
    """Return image data from TIFF file(s) as numpy array.

    The first image series is returned if no arguments are provided.

    Parameters
    ----------
    files : str or list
        File name, glob pattern, or list of file names.
    key : int, slice, or sequence of page indices
        Defines which pages to return as array.
    series : int
        Defines which series of pages in file to return as array.
    multifile : bool
        If True (default), OME-TIFF data may include pages from multiple files.
    pattern : str
        Regular expression pattern that matches axes names and indices in
        file names.
    kwargs : dict
        Additional parameters passed to the TiffFile or TiffSequence asarray
        function.

    Examples
    --------
    >>> imsave('temp.tif', numpy.random.rand(3, 4, 301, 219))
    >>> im = imread('temp.tif', key=0)
    >>> im.shape
    (4, 301, 219)
    >>> ims = imread(['temp.tif', 'temp.tif'])
    >>> ims.shape
    (2, 3, 4, 301, 219)

    """
    kwargs_file = {}
    if 'multifile' in kwargs:
        kwargs_file['multifile'] = kwargs['multifile']
        del kwargs['multifile']
    else:
        kwargs_file['multifile'] = True
    kwargs_seq = {}
    if 'pattern' in kwargs:
        kwargs_seq['pattern'] = kwargs['pattern']
        del kwargs['pattern']

    if isinstance(files, basestring) and any(i in files for i in '?*'):
        files = glob.glob(files)
    if not files:
        raise ValueError('no files found')
    if len(files) == 1:
        files = files[0]

    if isinstance(files, basestring):
        with TiffFile(files, **kwargs_file) as tif:
            return tif.asarray(**kwargs)
    else:
        with TiffSequence(files, **kwargs_seq) as imseq:
            return imseq.asarray(**kwargs)


class lazyattr(object):
    """Lazy object attribute whose value is computed on first access."""
    __slots__ = ('func',)

    def __init__(self, func):
        self.func = func

    def __get__(self, instance, owner):
        if instance is None:
            return self
        value = self.func(instance)
        if value is NotImplemented:
            return getattr(super(owner, instance), self.func.__name__)
        setattr(instance, self.func.__name__, value)
        return value


class TiffFile(object):
    """Read image and metadata from TIFF, STK, LSM, and FluoView files.

    TiffFile instances must be closed using the 'close' method, which is
    automatically called when using the 'with' statement.

    Attributes
    ----------
    pages : list of TiffPage
        All TIFF pages in file.
    series : list of TiffPageSeries
        TIFF pages with compatible shapes and types.
    micromanager_metadata: dict
        Extra MicroManager non-TIFF metadata in the file, if exists.

    All attributes are read-only.

    Examples
    --------
    >>> with TiffFile('temp.tif') as tif:
    ...     data = tif.asarray()
    ...     data.shape
    (5, 301, 219)

    """
    def __init__(self, arg, name=None, offset=None, size=None,
                 multifile=True, multifile_close=True, maxpages=None,
                 fastij=True):
        """Initialize instance from file.

        Parameters
        ----------
        arg : str or open file
            Name of file or open file object.
            The file objects are closed in TiffFile.close().
        name : str
            Optional name of file in case 'arg' is a file handle.
        offset : int
            Optional start position of embedded file. By default this is
            the current file position.
        size : int
            Optional size of embedded file. By default this is the number
            of bytes from the 'offset' to the end of the file.
        multifile : bool
            If True (default), series may include pages from multiple files.
            Currently applies to OME-TIFF only.
        multifile_close : bool
            If True (default), keep the handles of other files in multifile
            series closed. This is inefficient when few files refer to
            many pages. If False, the C runtime may run out of resources.
        maxpages : int
            Number of pages to read (default: no limit).
        fastij : bool
            If True (default), try to use only the metadata from the first page
            of ImageJ files. Significantly speeds up loading movies with
            thousands of pages.

        """
        self._fh = FileHandle(arg, name=name, offset=offset, size=size)
        self.offset_size = None
        self.pages = []
        self._multifile = bool(multifile)
        self._multifile_close = bool(multifile_close)
        self._files = {self._fh.name: self}  # cache of TiffFiles
        try:
            self._fromfile(maxpages, fastij)
        except Exception:
            self._fh.close()
            raise

    @property
    def filehandle(self):
        """Return file handle."""
        return self._fh

    @property
    def filename(self):
        """Return name of file handle."""
        return self._fh.name

    def close(self):
        """Close open file handle(s)."""
        for tif in self._files.values():
            tif._fh.close()
        self._files = {}

    def _fromfile(self, maxpages=None, fastij=True):
        """Read TIFF header and all page records from file."""
        self._fh.seek(0)
        try:
            self.byteorder = {b'II': '<', b'MM': '>'}[self._fh.read(2)]
        except KeyError:
            raise ValueError("not a valid TIFF file")
        self._is_native = self.byteorder == {'big': '>',
                                             'little': '<'}[sys.byteorder]
        version = struct.unpack(self.byteorder+'H', self._fh.read(2))[0]
        if version == 43:
            # BigTiff
            self.offset_size, zero = struct.unpack(self.byteorder+'HH',
                                                   self._fh.read(4))
            if zero or self.offset_size != 8:
                raise ValueError("not a valid BigTIFF file")
        elif version == 42:
            self.offset_size = 4
        else:
            raise ValueError("not a TIFF file")
        self.pages = []
        while True:
            try:
                page = TiffPage(self)
                self.pages.append(page)
            except StopIteration:
                break
            if maxpages and len(self.pages) > maxpages:
                break
            if fastij and page.is_imagej:
                if page._patch_imagej():
                    break  # only read the first page of ImageJ files
                fastij = False

        if not self.pages:
            raise ValueError("empty TIFF file")

        # TODO? sort pages by page_number value

        if self.is_micromanager:
            # MicroManager files contain metadata not stored in TIFF tags.
            self.micromanager_metadata = read_micromanager_metadata(self._fh)

        if self.is_lsm:
            self._fix_lsm_strip_offsets()
            self._fix_lsm_strip_byte_counts()

    def _fix_lsm_strip_offsets(self):
        """Unwrap strip offsets for LSM files greater than 4 GB."""
        for series in self.series:
            wrap = 0
            previous_offset = 0
            for page in series.pages:
                strip_offsets = []
                for current_offset in page.strip_offsets:
                    if current_offset < previous_offset:
                        wrap += 2**32
                    strip_offsets.append(current_offset + wrap)
                    previous_offset = current_offset
                page.strip_offsets = tuple(strip_offsets)

    def _fix_lsm_strip_byte_counts(self):
        """Set strip_byte_counts to size of compressed data.

        The strip_byte_counts tag in LSM files contains the number of bytes
        for the uncompressed data.

        """
        if not self.pages:
            return
        strips = {}
        for page in self.pages:
            assert len(page.strip_offsets) == len(page.strip_byte_counts)
            for offset, bytecount in zip(page.strip_offsets,
                                         page.strip_byte_counts):
                strips[offset] = bytecount
        offsets = sorted(strips.keys())
        offsets.append(min(offsets[-1] + strips[offsets[-1]], self._fh.size))
        for i, offset in enumerate(offsets[:-1]):
            strips[offset] = min(strips[offset], offsets[i+1] - offset)
        for page in self.pages:
            if page.compression:
                page.strip_byte_counts = tuple(
                    strips[offset] for offset in page.strip_offsets)

    def asarray(self, key=None, series=None, memmap=False):
        """Return image data from multiple TIFF pages as numpy array.

        By default the first image series is returned.

        Parameters
        ----------
        key : int, slice, or sequence of page indices
            Defines which pages to return as array.
        series : int or TiffPageSeries
            Defines which series of pages to return as array.
        memmap : bool
            If True, return an array stored in a binary file on disk
            if possible.

        """
        if key is None and series is None:
            series = 0
        if series is not None:
            try:
                series = self.series[series]
            except (KeyError, TypeError):
                pass
            pages = series.pages
        else:
            pages = self.pages

        if key is None:
            pass
        elif isinstance(key, int):
            pages = [pages[key]]
        elif isinstance(key, slice):
            pages = pages[key]
        elif isinstance(key, collections.Iterable):
            pages = [pages[k] for k in key]
        else:
            raise TypeError("key must be an int, slice, or sequence")

        if not len(pages):
            raise ValueError("no pages selected")

        if self.is_nih:
            if pages[0].is_palette:
                result = stack_pages(pages, colormapped=False, squeeze=False)
                result = numpy.take(pages[0].color_map, result, axis=1)
                result = numpy.swapaxes(result, 0, 1)
            else:
                result = stack_pages(pages, memmap=memmap,
                                     colormapped=False, squeeze=False)
        elif len(pages) == 1:
            result = pages[0].asarray(memmap=memmap)
        elif self.is_ome:
            assert not self.is_palette, "color mapping disabled for ome-tiff"
            if any(p is None for p in pages):
                # zero out missing pages
                firstpage = next(p for p in pages if p)
                nopage = numpy.zeros_like(
                    firstpage.asarray(memmap=False))
            if memmap:
                with tempfile.NamedTemporaryFile() as fh:
                    result = numpy.memmap(fh, series.dtype, shape=series.shape)
                    result = result.reshape(-1)
            else:
                result = numpy.empty(series.shape, series.dtype).reshape(-1)
            index = 0

            class KeepOpen:
                # keep Tiff files open between consecutive pages
                def __init__(self, parent, close):
                    self.master = parent
                    self.parent = parent
                    self._close = close

                def open(self, page):
                    if self._close and page and page.parent != self.parent:
                        if self.parent != self.master:
                            self.parent.filehandle.close()
                        self.parent = page.parent
                        self.parent.filehandle.open()

                def close(self):
                    if self._close and self.parent != self.master:
                        self.parent.filehandle.close()

            keep = KeepOpen(self, self._multifile_close)
            for page in pages:
                keep.open(page)
                if page:
                    a = page.asarray(memmap=False, colormapped=False,
                                     reopen=False)
                else:
                    a = nopage
                try:
                    result[index:index + a.size] = a.reshape(-1)
                except ValueError as e:
                    warnings.warn("ome-tiff: %s" % e)
                    break
                index += a.size
            keep.close()
        else:
            result = stack_pages(pages, memmap=memmap)

        if key is None:
            try:
                result.shape = series.shape
            except ValueError:
                try:
                    warnings.warn("failed to reshape %s to %s" % (
                        result.shape, series.shape))
                    # try series of expected shapes
                    result.shape = (-1,) + series.shape
                except ValueError:
                    # revert to generic shape
                    result.shape = (-1,) + pages[0].shape
        elif len(pages) == 1:
            result.shape = pages[0].shape
        else:
            result.shape = (-1,) + pages[0].shape
        return result

    @lazyattr
    def series(self):
        """Return series of TiffPage with compatible shape and properties."""
        if not self.pages:
            return []

        series = []
        if self.is_ome:
            series = self._ome_series()
        elif self.is_fluoview:
            series = self._fluoview_series()
        elif self.is_lsm:
            series = self._lsm_series()
        elif self.is_imagej:
            series = self._imagej_series()
        elif self.is_nih:
            series = self._nih_series()

        if not series:
            # generic detection of series
            shapes = []
            pages = {}
            index = 0
            for page in self.pages:
                if not page.shape:
                    continue
                if page.is_shaped:
                    index += 1  # shape starts a new series
                shape = page.shape + (index, page.axes,
                                      page.compression in TIFF_DECOMPESSORS)
                if shape in pages:
                    pages[shape].append(page)
                else:
                    shapes.append(shape)
                    pages[shape] = [page]
            series = []
            for s in shapes:
                shape = ((len(pages[s]),) + s[:-3] if len(pages[s]) > 1
                         else s[:-3])
                axes = (('I' + s[-2]) if len(pages[s]) > 1 else s[-2])
                page0 = pages[s][0]
                if page0.is_shaped:
                    description = page0.is_shaped
                    metadata = image_description_dict(description)
                    if product(metadata.get('shape', shape)) == product(shape):
                        shape = metadata.get('shape', shape)
                    else:
                        warnings.warn(
                            "metadata shape doesn't match data shape")
                    if 'axes' in metadata:
                        axes = metadata['axes']
                        if len(axes) != len(shape):
                            warnings.warn("axes don't match shape")
                    axes = 'Q'*(len(shape)-len(axes)) + axes[-len(shape):]
                series.append(
                    TiffPageSeries(pages[s], shape, page0.dtype, axes))

        # remove empty series, e.g. in MD Gel files
        series = [s for s in series if sum(s.shape) > 0]
        return series

    def _fluoview_series(self):
        """Return image series in FluoView file."""
        page0 = self.pages[0]
        dims = {
            b'X': 'X', b'Y': 'Y', b'Z': 'Z', b'T': 'T',
            b'WAVELENGTH': 'C', b'TIME': 'T', b'XY': 'R',
            b'EVENT': 'V', b'EXPOSURE': 'L'}
        mmhd = list(reversed(page0.mm_header.dimensions))
        axes = ''.join(dims.get(i[0].strip().upper(), 'Q')
                       for i in mmhd if i[1] > 1)
        shape = tuple(int(i[1]) for i in mmhd if i[1] > 1)
        return [TiffPageSeries(self.pages, shape, page0.dtype, axes)]

    def _lsm_series(self):
        """Return image series in LSM file."""
        page0 = self.pages[0]
        lsmi = page0.cz_lsm_info
        axes = CZ_SCAN_TYPES[lsmi.scan_type]
        if page0.is_rgb:
            axes = axes.replace('C', '').replace('XY', 'XYC')
        axes = axes[::-1]
        shape = tuple(getattr(lsmi, CZ_DIMENSIONS[i]) for i in axes)
        pages = [p for p in self.pages if not p.is_reduced]
        dtype = pages[0].dtype
        series = [TiffPageSeries(pages, shape, dtype, axes)]
        if len(pages) != len(self.pages):  # reduced RGB pages
            pages = [p for p in self.pages if p.is_reduced]
            cp = 1
            i = 0
            while cp < len(pages) and i < len(shape)-2:
                cp *= shape[i]
                i += 1
            shape = shape[:i] + pages[0].shape
            axes = axes[:i] + 'CYX'
            dtype = pages[0].dtype
            series.append(TiffPageSeries(pages, shape, dtype, axes))
        return series

    def _imagej_series(self):
        """Return image series in ImageJ file."""
        # ImageJ's dimension order is always TZCYXS
        # TODO: fix loading of color, composite or palette images
        shape = []
        axes = []
        page0 = self.pages[0]
        ij = page0.imagej_tags
        if 'frames' in ij:
            shape.append(ij['frames'])
            axes.append('T')
        if 'slices' in ij:
            shape.append(ij['slices'])
            axes.append('Z')
        if 'channels' in ij and not (self.is_rgb and not
                                     ij.get('hyperstack', False)):
            shape.append(ij['channels'])
            axes.append('C')
        remain = ij.get('images', len(self.pages)) // (product(shape)
                                                       if shape else 1)
        if remain > 1:
            shape.append(remain)
            axes.append('I')
        if page0.axes[0] == 'I':
            # contiguous multiple images
            shape.extend(page0.shape[1:])
            axes.extend(page0.axes[1:])
        elif page0.axes[:2] == 'SI':
            # color-mapped contiguous multiple images
            shape = page0.shape[0:1] + tuple(shape) + page0.shape[2:]
            axes = list(page0.axes[0]) + axes + list(page0.axes[2:])
        else:
            shape.extend(page0.shape)
            axes.extend(page0.axes)
        return [TiffPageSeries(self.pages, shape, page0.dtype, axes)]

    def _nih_series(self):
        """Return image series in NIH file."""
        page0 = self.pages[0]
        if len(self.pages) == 1:
            shape = page0.shape
            axes = page0.axes
        else:
            shape = (len(self.pages),) + page0.shape
            axes = 'I' + page0.axes
        return [TiffPageSeries(self.pages, shape, page0.dtype, axes)]

    def _ome_series(self):
        """Return image series in OME-TIFF file(s)."""
        omexml = self.pages[0].tags['image_description'].value
        omexml = omexml.decode('UTF-8', 'ignore')
        root = etree.fromstring(omexml)
        uuid = root.attrib.get('UUID', None)
        self._files = {uuid: self}
        dirname = self._fh.dirname
        modulo = {}
        series = []
        for element in root:
            if element.tag.endswith('BinaryOnly'):
                warnings.warn("ome-xml: not an ome-tiff master file")
                break
            if element.tag.endswith('StructuredAnnotations'):
                for annot in element:
                    if not annot.attrib.get('Namespace',
                                            '').endswith('modulo'):
                        continue
                    for value in annot:
                        for modul in value:
                            for along in modul:
                                if not along.tag[:-1].endswith('Along'):
                                    continue
                                axis = along.tag[-1]
                                newaxis = along.attrib.get('Type', 'other')
                                newaxis = AXES_LABELS[newaxis]
                                if 'Start' in along.attrib:
                                    labels = range(
                                        int(along.attrib['Start']),
                                        int(along.attrib['End']) + 1,
                                        int(along.attrib.get('Step', 1)))
                                else:
                                    labels = [label.text for label in along
                                              if label.tag.endswith('Label')]
                                modulo[axis] = (newaxis, labels)
            if not element.tag.endswith('Image'):
                continue
            for pixels in element:
                if not pixels.tag.endswith('Pixels'):
                    continue
                atr = pixels.attrib
                dtype = atr.get('Type', None)
                axes = ''.join(reversed(atr['DimensionOrder']))
                shape = list(int(atr['Size'+ax]) for ax in axes)
                size = product(shape[:-2])
                ifds = [None] * size
                for data in pixels:
                    if not data.tag.endswith('TiffData'):
                        continue
                    atr = data.attrib
                    ifd = int(atr.get('IFD', 0))
                    num = int(atr.get('NumPlanes', 1 if 'IFD' in atr else 0))
                    num = int(atr.get('PlaneCount', num))
                    idx = [int(atr.get('First'+ax, 0)) for ax in axes[:-2]]
                    try:
                        idx = numpy.ravel_multi_index(idx, shape[:-2])
                    except ValueError:
                        # ImageJ produces invalid ome-xml when cropping
                        warnings.warn("ome-xml: invalid TiffData index")
                        continue
                    for uuid in data:
                        if not uuid.tag.endswith('UUID'):
                            continue
                        if uuid.text not in self._files:
                            if not self._multifile:
                                # abort reading multifile OME series
                                # and fall back to generic series
                                return []
                            fname = uuid.attrib['FileName']
                            try:
                                tif = TiffFile(os.path.join(dirname, fname))
                            except (IOError, ValueError):
                                tif.close()
                                warnings.warn(
                                    "ome-xml: failed to read '%s'" % fname)
                                break
                            self._files[uuid.text] = tif
                            if self._multifile_close:
                                tif.close()
                        pages = self._files[uuid.text].pages
                        try:
                            for i in range(num if num else len(pages)):
                                ifds[idx + i] = pages[ifd + i]
                        except IndexError:
                            warnings.warn("ome-xml: index out of range")
                        # only process first uuid
                        break
                    else:
                        pages = self.pages
                        try:
                            for i in range(num if num else len(pages)):
                                ifds[idx + i] = pages[ifd + i]
                        except IndexError:
                            warnings.warn
