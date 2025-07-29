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
contains the FrameGroup
"""

__authors__ = [
    "H. Payno",
]
__license__ = "MIT"
__date__ = "17/03/2021"


from silx.utils.enum import Enum as _Enum
from nxtomo.nxobject.nxdetector import ImageKey


class AcquisitionStep(_Enum):
    # Warning: order of acquisition step should be same as H5ScanTitles
    INITIALIZATION = "initialization"
    DARK = "darks"
    FLAT = "flats"
    PROJECTION = "projections"
    ALIGNMENT = "alignment projections"

    @classmethod
    def from_value(cls, value):
        if isinstance(value, str):
            value = value.lower()
            if value in ("init", "initialization"):
                value = AcquisitionStep.INITIALIZATION
            elif value in ("dark", "darks"):
                value = AcquisitionStep.DARK
            elif value in ("reference", "flat", "flats", "ref", "refs", "references"):
                value = AcquisitionStep.FLAT
            elif value in ("proj", "projection", "projs", "projections"):
                value = AcquisitionStep.PROJECTION
            elif value in (
                "alignment",
                "alignments",
                "alignment projection",
                "alignment projections",
            ):
                value = AcquisitionStep.ALIGNMENT

        return super().from_value(value)

    def to_image_key(self):
        if self is AcquisitionStep.PROJECTION:
            return ImageKey.PROJECTION
        elif self is AcquisitionStep.ALIGNMENT:
            return ImageKey.PROJECTION
        elif self is AcquisitionStep.DARK:
            return ImageKey.DARK_FIELD
        elif self is AcquisitionStep.FLAT:
            return ImageKey.FLAT_FIELD
        else:
            raise ValueError(f"The step {self.value} does not fit any AcquisitionStep")

    def to_image_key_control(self):
        if self is AcquisitionStep.PROJECTION:
            return ImageKey.PROJECTION
        elif self is AcquisitionStep.ALIGNMENT:
            return ImageKey.ALIGNMENT
        elif self is AcquisitionStep.DARK:
            return ImageKey.DARK_FIELD
        elif self is AcquisitionStep.FLAT:
            return ImageKey.FLAT_FIELD
        else:
            raise ValueError(f"The step {self.value} does not fit any AcquisitionStep")
