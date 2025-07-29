# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2016-2022 European Synchrotron Radiation Facility
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# ###########################################################################*/

__authors__ = ["H. Payno"]
__license__ = "MIT"
__date__ = "23/02/2022"


import contextlib

import h5py

try:
    import hdf5plugin  # noqa F401
except ImportError:
    pass
from silx.io.url import DataUrl
from silx.io.utils import open as open_hdf5


class _BaseReader(contextlib.AbstractContextManager):
    def __init__(self, url: DataUrl):
        if not isinstance(url, DataUrl):
            raise TypeError(f"url should be an instance of DataUrl. Not {type(url)}")
        if url.scheme() not in ("silx", "h5py"):
            raise ValueError("Valid scheme are silx and h5py")
        if url.data_slice() is not None:
            raise ValueError(
                "Data slices are not managed. Data path should "
                "point to a bliss node (h5py.Group)"
            )
        self._url = url
        self._file_handler = None

    def __exit__(self, *exc):
        return self._file_handler.close()


class EntryReader(_BaseReader):
    """Context manager used to read a bliss node"""

    def __enter__(self):
        self._file_handler = open_hdf5(filename=self._url.file_path())
        if self._url.data_path() == "":
            entry = self._file_handler
        elif self._url.data_path() not in self._file_handler:
            raise KeyError(
                f"data path '{self._url.data_path()}' doesn't exists from '{self._url.file_path()}'"
            )
        else:
            entry = self._file_handler[self._url.data_path()]
        if not isinstance(entry, h5py.Group):
            raise ValueError("Data path should point to a bliss node (h5py.Group)")
        return entry


class DatasetReader(_BaseReader):
    """Context manager used to read a bliss node"""

    def __enter__(self):
        self._file_handler = open_hdf5(filename=self._url.file_path())
        entry = self._file_handler[self._url.data_path()]
        if not isinstance(entry, h5py.Dataset):
            raise ValueError(
                f"Data path ({self._url.path()}) should point to a dataset (h5py.Dataset)"
            )
        return entry
