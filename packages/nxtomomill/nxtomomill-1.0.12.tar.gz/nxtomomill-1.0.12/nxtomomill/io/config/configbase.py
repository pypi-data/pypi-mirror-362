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
# ###########################################################################


__authors__ = [
    "H. Payno",
]
__license__ = "MIT"
__date__ = "21/04/2022"


import configparser
import logging
from typing import Iterable, Union

from nxtomo.nxobject.nxdetector import FieldOfView
from nxtomomill.utils import FileExtension


class ConfigBase:
    __isfrozen = False
    # to ease API and avoid setting wrong attributes we 'freeze' the attributes
    # see https://stackoverflow.com/questions/3603502/prevent-creating-new-attributes-outside-init

    def __init__(self) -> None:
        self._output_file = None
        self._overwrite = False
        self._file_extension = FileExtension.NX
        self._log_level = logging.WARNING
        self._field_of_view = None
        self._machine_electric_current_keys = None

    def __setattr__(self, __name, __value):
        if self.__isfrozen and not hasattr(self, __name):
            raise AttributeError("can't set attribute", __name)
        else:
            super().__setattr__(__name, __value)

    @property
    def output_file(self) -> Union[None, str]:
        return self._output_file

    @output_file.setter
    def output_file(self, output_file: Union[None, str]):
        if not isinstance(output_file, (str, type(None))):
            raise TypeError("'input_file' should be None or an instance of Iterable")
        elif output_file == "":
            self._output_file = None
        else:
            self._output_file = output_file

    @property
    def overwrite(self) -> bool:
        return self._overwrite

    @overwrite.setter
    def overwrite(self, overwrite: bool) -> None:
        if not isinstance(overwrite, bool):
            raise TypeError("'overwrite' should be a boolean")
        else:
            self._overwrite = overwrite

    @property
    def file_extension(self) -> FileExtension:
        return self._file_extension

    @file_extension.setter
    def file_extension(self, file_extension: str):
        self._file_extension = FileExtension.from_value(file_extension)

    @property
    def log_level(self):
        return self._log_level

    @log_level.setter
    def log_level(self, level: str):
        self._log_level = getattr(logging, level.upper())

    def _set_freeze(self, freeze=True):
        self.__isfrozen = freeze

    @property
    def field_of_view(self) -> Union[None, FieldOfView]:
        return self._field_of_view

    @field_of_view.setter
    def field_of_view(self, fov: Union[None, FieldOfView, str]):
        if fov is None:
            self._field_of_view = fov
        elif isinstance(fov, str):
            self._field_of_view = FieldOfView.from_value(fov.title())
        elif isinstance(fov, FieldOfView):
            self._field_of_view = fov
        else:
            raise TypeError(
                f"fov is expected to be None, a string or FieldOfView. Not {type(fov)}"
            )

    @property
    def rotation_angle_keys(self) -> Iterable:
        return self._rot_angle_keys

    @rotation_angle_keys.setter
    def rotation_angle_keys(self, keys: Iterable):
        if not isinstance(keys, Iterable) or isinstance(keys, str):
            raise TypeError("'keys' should be an Iterable")
        else:
            for elmt in keys:
                if not isinstance(elmt, str):
                    raise TypeError("keys elmts are expected to be str")
            self._rot_angle_keys = keys

    @property
    def x_trans_keys(self) -> Iterable:
        return self._x_trans_keys

    @x_trans_keys.setter
    def x_trans_keys(self, keys) -> None:
        if not isinstance(keys, Iterable) or isinstance(keys, str):
            raise TypeError("'keys' should be an Iterable")
        else:
            for elmt in keys:
                if not isinstance(elmt, str):
                    raise TypeError("keys elmts are expected to be str")
            self._x_trans_keys = keys

    @property
    def y_trans_keys(self) -> Iterable:
        return self._y_trans_keys

    @y_trans_keys.setter
    def y_trans_keys(self, keys) -> None:
        if not isinstance(keys, Iterable) or isinstance(keys, str):
            raise TypeError("'keys' should be an Iterable")
        else:
            for elmt in keys:
                if not isinstance(elmt, str):
                    raise TypeError("keys elmts are expected to be str")
            self._y_trans_keys = keys

    @property
    def z_trans_keys(self) -> Iterable:
        return self._z_trans_keys

    @z_trans_keys.setter
    def z_trans_keys(self, keys) -> None:
        if not isinstance(keys, Iterable) or isinstance(keys, str):
            raise TypeError("'keys' should be an Iterable")
        else:
            for elmt in keys:
                if not isinstance(elmt, str):
                    raise TypeError("keys elmts are expected to be str")
            self._z_trans_keys = keys

    @property
    def machine_electric_current_keys(self) -> Iterable:
        return self._machine_electric_current_keys

    @machine_electric_current_keys.setter
    def machine_electric_current_keys(self, keys: Iterable) -> None:
        self._machine_electric_current_keys = keys

    def to_dict(self) -> dict:
        """convert the configuration to a dictionary"""
        raise NotImplementedError("Base class")

    def load_from_dict(self, dict_: dict) -> None:
        """Load the configuration from a dictionary"""
        raise NotImplementedError("Base class")

    @staticmethod
    def from_dict(dict_: dict):
        raise NotImplementedError("Base class")

    def to_cfg_file(self, file_path: str):
        # TODO: add some generic information like:provided order of the tuple
        # will be the effective one. You can provide a key from it names if
        # it is contained in the positioners group
        # maybe split in sub section ?
        self.dict_to_cfg(file_path=file_path, dict_=self.to_dict())

    @staticmethod
    def dict_to_cfg(file_path, dict_):
        """ """
        raise NotImplementedError("Base class")

    @staticmethod
    def _dict_to_cfg(file_path, dict_, comments_fct, logger):
        """ """
        if not file_path.lower().endswith((".cfg", ".config", ".conf")):
            logger.warning("add a valid extension to the output file")
            file_path += ".cfg"
        config = configparser.ConfigParser(allow_no_value=True)
        config.optionxform = str
        for section_name, values in dict_.items():
            config.add_section(section_name)
            config.set(section_name, "# " + comments_fct(section_name), None)
            for key, value in values.items():
                # adopt nabu design: comments are set prior to the key
                config.set(section_name, "# " + comments_fct(key), None)
                config.set(section_name, key, str(value))

        with open(file_path, "w") as config_file:
            config.write(config_file)

    @staticmethod
    def from_cfg_file(file_path: str, encoding=None):
        raise NotImplementedError("Base class")

    @staticmethod
    def get_comments(key):
        raise NotImplementedError("Base class")

    def __str__(self):
        return str(self.to_dict())
