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
#
# ###########################################################################*/

"""
utils functions for io
"""


__authors__ = [
    "H. Payno",
]
__license__ = "MIT"
__date__ = "10/03/2021"


import logging
import re
from typing import Union

from silx.utils.enum import Enum as _Enum

from nxtomomill.io.framegroup import FrameGroup

_logger = logging.getLogger(__name__)


def remove_parenthesis_or_brackets(input_str):
    if (
        input_str.startswith("(")
        and input_str.endswith(")")
        or input_str.startswith("[")
        and input_str.endswith("]")
    ):
        input_str = input_str[1:-1]
    return input_str


def filter_str_def(elmt):
    if elmt is None:
        return None
    assert isinstance(elmt, str)
    elmt = elmt.lstrip(" ").rstrip(" ")
    for character in ("'", '"'):
        if elmt.startswith(character) and elmt.endswith(character):
            elmt = elmt[1:-1]
    return elmt


def convert_str_to_tuple(
    input_str: str, none_if_empty: bool = False
) -> Union[None, tuple]:
    """
    :param str input_str: string to convert
    :param bool none_if_empty: if true and the conversion is an empty tuple
                               return None instead of an empty tuple
    """
    if isinstance(input_str, (list, set)):
        input_str = tuple(input_str)
    if isinstance(input_str, tuple):
        return input_str
    if not isinstance(input_str, str):
        raise TypeError(
            f"input_str should be a string not {type(input_str)}, {input_str}"
        )
    input_str = input_str.lstrip(" ").rstrip(" ")
    input_str = remove_parenthesis_or_brackets(input_str)

    elmts = input_str.split(",")
    elmts = [filter_str_def(elmt) for elmt in elmts]
    rm_empty_str = lambda a: a != ""
    elmts = list(filter(rm_empty_str, elmts))
    if none_if_empty and len(elmts) == 0:
        return None
    else:
        return tuple(elmts)


def convert_str_to_bool(value: Union[str, bool]):
    if isinstance(value, bool):
        return value
    elif isinstance(value, str):
        if value not in ("False", "True", "1", "0"):
            raise ValueError("value should be 'True' or 'False'")
        return value in ("True", "1")
    else:
        raise TypeError("value should be a string")


def is_url_path(url_str: str) -> bool:
    """
    :return: True if the provided string fit DataUrl pattern
    [scheme]:://[file_path]?[data_path]
    """
    pattern_str_seq = "[a-zA-Z0-9]*"
    url_path_pattern = rf"{pattern_str_seq}\:\/\/{pattern_str_seq}"
    pattern = re.compile(url_path_pattern)
    return bool(re.match(pattern, url_str))


def convert_str_to_frame_grp(input_str: str) -> tuple:
    """
    Convert a list such as:

    .. code-block:: text

        urls = (
            (frame_type=dark, entry="silx:///file.h5?data_path=/dark", copy=True),
            (frame_type=flat, entry="silx:///file.h5?data_path=/flat"),
            (frame_type=projection, entry="silx:///file.h5?data_path=/flat"),
            (frame_type=projection, entry="silx:///file.h5?data_path=/flat"),
        )

    to a list of InputUrl
    """
    result = []
    if not isinstance(input_str, str):
        raise TypeError("input_str should be an instance of str")
    # remove spaces at the beginning and at the end
    input_str = input_str.replace("\n", "")
    input_str = input_str.lstrip(" ").rstrip(" ")
    input_str = remove_parenthesis_or_brackets(input_str)
    # special case when the ")" is given in a line and ignored by configparser
    input_str = input_str.replace("((", "(")
    # split sub entries
    re_expr = r"\([^\)]*\)"
    frame_grp_str_list = re.findall(re_expr, input_str)
    for frame_grp_str in frame_grp_str_list:
        try:
            frame_grp = FrameGroup.frm_str(frame_grp_str)
        except Exception as e:
            _logger.error(
                f"Unable to create a valid entry from {frame_grp_str}. Error is {e}"
            )
        else:
            result.append(frame_grp)

    return tuple(result)


class PathType(_Enum):
    ABSOLUTE = "absolute"
    RELATIVE = "relative"
