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
__date__ = "03/02/2022"


import sys
import typing


class Progress:
    """Simple interface for defining advancement on a 100 percentage base"""

    def __init__(self, name: str):
        self._name = name
        self._progress = 0
        self.set_name(name)

    def set_name(self, name):
        self._name = name
        self.reset()

    def reset(self, max_: typing.Union[None, int] = None) -> None:
        """
        reset the advancement to n and max advancement to max_
        :param int max_:
        """
        self._n_processed = 0
        self._max_processed = max_

    def start_process(self) -> None:
        self.set_advancement(0)

    @property
    def progress(self):
        return self._progress

    @progress.setter
    def progress(self, progress):
        progress = max(0, progress)
        progress = min(100, progress)
        self._progress = progress
        length = 20  # modify this to change the length
        block = int(round(length * progress / 100))
        blocks_str = "#" * block + "-" * (length - block)
        msg = f"\r{self._name}: [{blocks_str}] {round(progress, 2)}%"
        if progress >= 100:
            msg += " DONE\r\n"
        sys.stdout.write(msg)
        sys.stdout.flush()

    def set_advancement(self, value: int) -> None:
        """

        :param int value: set advancement to value
        """
        self.progress = value

    def end_process(self) -> None:
        """Set advancement to 100 %"""
        self.set_advancement(100)

    def set_max_advancement(self, n: int) -> None:
        """

        :param int n: number of steps contained by the advancement. When
        advancement reach this value, advancement will be 100 %
        """
        self._max_processed = n

    def increase_advancement(self, i: int = 1) -> None:
        """

        :param int i: increase the advancement of n step
        """
        self._n_processed += i
        advancement = int(float(self._n_processed / self._max_processed) * 100)
        self.set_advancement(advancement)
