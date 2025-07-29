# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2015-2020 European Synchrotron Radiation Facility
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

"""
module to define some converter utils function
"""

__authors__ = [
    "H. Payno",
]
__license__ = "MIT"
__date__ = "08/03/2022"


import h5py
import h5py._hl.selections as selection
from silx.io.url import DataUrl
from silx.io.utils import open as open_hdf5


def from_data_url_to_virtual_source(url: DataUrl) -> tuple:
    """
    :param DataUrl url: url to be converted to a virtual source. It must target a 2D detector
    :return: (h5py.VirtualSource, tuple(shape of the virtual source), numpy.drype: type of the dataset associated with the virtual source)
    :rtype: tuple
    """
    if not isinstance(url, DataUrl):
        raise TypeError(
            f"url is expected to be an instance of DataUrl and not {type(url)}"
        )

    with open_hdf5(url.file_path()) as o_h5s:
        original_data_shape = o_h5s[url.data_path()].shape
        data_type = o_h5s[url.data_path()].dtype
        if len(original_data_shape) == 2:
            original_data_shape = (
                1,
                original_data_shape[0],
                original_data_shape[1],
            )

        vs_shape = original_data_shape
        if url.data_slice() is not None:
            vs_shape = (
                url.data_slice().stop - url.data_slice().start,
                original_data_shape[-2],
                original_data_shape[-1],
            )

    vs = h5py.VirtualSource(
        url.file_path(), url.data_path(), shape=vs_shape, dtype=data_type
    )

    if url.data_slice() is not None:
        vs.sel = selection.select(original_data_shape, url.data_slice())
    return vs, vs_shape, data_type


def from_virtual_source_to_data_url(vs: h5py.VirtualSource) -> DataUrl:
    if not isinstance(vs, h5py.VirtualSource):
        raise TypeError(
            f"vs is expected to be an instance of h5py.VirtualSorce and not {type(vs)}"
        )
    url = DataUrl(file_path=vs.path, data_path=vs.name, scheme="silx")
    return url
