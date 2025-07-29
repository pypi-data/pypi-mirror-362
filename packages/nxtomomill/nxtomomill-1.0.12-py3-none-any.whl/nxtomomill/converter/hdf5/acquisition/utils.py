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
Utils related to bliss-HDF5
"""

from __future__ import annotations

import typing
from typing import Iterable

import h5py
import numpy
from silx.io.url import DataUrl
from silx.io.utils import h5py_read_dataset
from silx.io.utils import open as open_hdf5

from nxtomo.nxobject.nxdetector import ImageKey
from nxtomomill.io.acquisitionstep import AcquisitionStep
from nxtomomill.io.config import TomoHDF5Config

try:
    import hdf5plugin  # noqa F401
except ImportError:
    pass
import logging

_logger = logging.getLogger(__name__)


def has_valid_detector(node, detectors_names):
    """
    :return True if the node looks like a valid nx detector
    """
    for key in node.keys():
        if (
            "NX_class" in node[key].attrs
            and node[key].attrs["NX_class"] == "NXdetector"
        ):
            if detectors_names is None or key in detectors_names:
                return True
    return False


def get_entry_type(
    url: DataUrl, configuration: TomoHDF5Config
) -> typing.Optional[AcquisitionStep]:
    """
    :param DataUrl url: bliss scan url to type
    :return: return the step of the acquisition or None if cannot find it.
    """
    if not isinstance(url, DataUrl):
        raise TypeError(f"DataUrl is expected. Not {type(url)}")
    if url.data_slice() is not None:
        raise ValueError(
            "url expect to provide a link to bliss scan. Slice " "are not handled"
        )

    def _get_entry_type_from_title(entry: h5py.Group):
        """
        try to determine the entry type from the title
        """
        try:
            title = h5py_read_dataset(entry["title"])
        except Exception:
            _logger.error(f"fail to find title for {entry.name}, skip this group")
            return None
        else:
            init_titles = list(configuration.init_titles)
            init_titles.extend(configuration.zserie_init_titles)
            init_titles.extend(configuration.pcotomo_init_titles)

            step_titles = {
                AcquisitionStep.INITIALIZATION: init_titles,
                AcquisitionStep.DARK: configuration.dark_titles,
                AcquisitionStep.FLAT: configuration.flat_titles,
                AcquisitionStep.PROJECTION: configuration.projections_titles,
                AcquisitionStep.ALIGNMENT: configuration.alignment_titles,
            }

            for step, titles in step_titles.items():
                for title_start in titles:
                    if title.startswith(title_start):
                        return step
            return None

    def _get_entry_type_from_technique(entry: h5py.Group):
        """
        try to determine entry type from the scan/technique sub groups.
        If this is a flat then we expect to have a "flat" group. If this is a set of projection we expect to have a "proj" group.
        For now alignment / return are unfiled
        """
        group_technique = entry.get("technique", dict())
        if "image_key" not in group_technique:
            return None

        image_key = h5py_read_dataset(group_technique["image_key"])
        if image_key is None:
            return None
        else:
            try:
                image_key = ImageKey.from_value(image_key)
            except ValueError:
                _logger.error(f"unrecognized image key: '{image_key}'")
                return None
            else:
                connections = {
                    ImageKey.DARK_FIELD: AcquisitionStep.DARK,
                    ImageKey.FLAT_FIELD: AcquisitionStep.FLAT,
                    ImageKey.PROJECTION: AcquisitionStep.PROJECTION,
                    ImageKey.ALIGNMENT: AcquisitionStep.ALIGNMENT,
                }
                return connections.get(image_key, None)

    with open_hdf5(url.file_path()) as h5f:
        if url.data_path() not in h5f:
            raise ValueError(f"Provided path does not exists: {url}")
        entry = h5f[url.data_path()]
        if not isinstance(entry, h5py.Group):
            raise ValueError(
                f"Expected path is not related to a h5py.Group ({entry}) when expect to target a bliss entry."
            )
        return _get_entry_type_from_technique(entry) or _get_entry_type_from_title(
            entry
        )


def get_nx_detectors(node: h5py.Group) -> tuple:
    """

    :param h5py.Group node: node to inspect
    :return: tuple of NXdetector (h5py.Group) contained in `node`
             (expected to be the `instrument` group)
    :rtype: tuple
    """
    if not isinstance(node, h5py.Group):
        raise TypeError("node should be an instance of h5py.Group")
    nx_detectors = []
    for _, subnode in node.items():
        if isinstance(subnode, h5py.Group) and "NX_class" in subnode.attrs:
            if subnode.attrs["NX_class"] == "NXdetector":
                if "data" in subnode and hasattr(subnode["data"], "ndim"):
                    if subnode["data"].ndim == 3:
                        nx_detectors.append(subnode)
    nx_detectors = sorted(nx_detectors, key=lambda det: det.name)
    return tuple(nx_detectors)


def guess_nx_detector(node: h5py.Group) -> tuple:
    """
    Try to guess what can be an nx_detector without using the "NXdetector"
    NX_class attribute. Expect to find a 3D dataset named 'data' under
    a subnode
    """
    if not isinstance(node, h5py.Group):
        raise TypeError("node should be an instance of h5py.Group")
    nx_detectors = []
    for _, subnode in node.items():
        if isinstance(subnode, h5py.Group) and "data" in subnode:
            if isinstance(subnode["data"], h5py.Dataset) and subnode["data"].ndim == 3:
                nx_detectors.append(subnode)

    nx_detectors = sorted(nx_detectors, key=lambda det: det.name)
    return tuple(nx_detectors)


def deduce_machine_electric_current(
    timestamps: tuple, known_machine_electric_current: dict
) -> dict:
    """
    :param dict knowned_machine_electric_current: keys are electric timestamp. Value is electric current
    :param tuple timestamp: keys are frame index. timestamp. Value is electric current
    """
    if not isinstance(known_machine_electric_current, dict):
        raise TypeError("knowned_machine_electric_current is expected to be a dict")
    for elmt in timestamps:
        if not isinstance(elmt, numpy.datetime64):
            raise TypeError(
                f"elmts of timestamps are expected to be {numpy.datetime64} and not {type(elmt)}"
            )
    if len(known_machine_electric_current) == 0:
        raise ValueError(
            "knowned_machine_electric_current should at least contains one element"
        )
    for key, value in known_machine_electric_current.items():
        if not isinstance(key, numpy.datetime64):
            raise TypeError(
                f"knowned_machine_electric_current keys are expected to be instances of {numpy.datetime64} and not {type(key)}"
            )
        if not isinstance(value, (float, numpy.number)):
            raise TypeError(
                "knowned_machine_electric_current values are expected to be instances of float"
            )

    # 1. order **knowned** electric current by time stamps (key)
    known_machine_electric_current = dict(
        sorted(known_machine_electric_current.items())
    )
    known_timestamps = tuple(known_machine_electric_current.keys())
    known_electric_currents = tuple(known_machine_electric_current.values())

    # 3. order input timestamps
    timestamp_input_ordering = numpy.argsort(numpy.array(timestamps))
    ordered_timestamps = numpy.take_along_axis(
        numpy.array(timestamps), indices=timestamp_input_ordering, axis=0
    )
    left_indexes = numpy.searchsorted(
        known_timestamps,  # input array
        ordered_timestamps,
        side="left",
    )

    def compute(timestamp, left_know_index):
        if left_know_index == 0:
            return known_electric_currents[0]
        elif left_know_index > len(known_timestamps) - 1:
            return known_electric_currents[-1]
        else:
            ec1 = known_electric_currents[left_know_index - 1]
            ec2 = known_electric_currents[left_know_index]
            left_timestamp = known_timestamps[left_know_index - 1]
            right_timestamp = known_timestamps[left_know_index]
            delta = right_timestamp - left_timestamp
            assert right_timestamp >= left_timestamp
            w1 = 1 - (timestamp - left_timestamp) / delta
            w2 = 1 - (right_timestamp - timestamp) / delta
            return ec1 * w1 + ec2 * w2

    res = tuple(
        [
            compute(timestamp, left_know_index)
            for timestamp, left_know_index in zip(ordered_timestamps, left_indexes)
        ]
    )
    assert len(res) == len(
        timestamp_input_ordering
    ), f"incoherent number of computed electric current ({len(res)}) vs input time stamp({len(timestamp_input_ordering)})"
    assert len(res) == len(timestamp_input_ordering)
    # 4. reorder resulting electrical current to fit the order of provided timestamp
    original_order_res = [None] * len(res)
    for i, o_pos in enumerate(timestamp_input_ordering):
        original_order_res[o_pos] = res[i]
    return tuple(original_order_res)


def split_timestamps(my_array: Iterable, n_part: int):
    """
    split given array into n_part (as equal as possible)
    :param Iterable my_array:
    """
    array_size = len(my_array)
    if array_size < n_part:
        yield my_array
    else:
        start = 0
        for _ in range(n_part):
            end = max(start + int(array_size / n_part) + 1, array_size)
            yield my_array[start:end]
            start = end


def group_series(acquisition, list_of_series: list) -> list:
    """
    :param ZSeriesBaseAcquisition acquisition:
    z-series version 2 and 3 are all defined in a separate sequence.
    So we need to aggregate for post processing based on there names.
    post-processing can be dark / flat copy to others NXtomo
    """
    for series in list_of_series:
        if series[0].is_part_of_same_series(acquisition):
            series.append(acquisition)
            return list_of_series
    list_of_series.append(
        [
            acquisition,
        ]
    )
    return list_of_series
