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
contains the HDF5ConfigHandler
"""

__authors__ = ["H. Payno"]
__license__ = "MIT"
__date__ = "08/03/2021"


import logging
import os
from typing import Union

from nxtomomill import utils
from nxtomomill.io.utils import filter_str_def
from nxtomomill.utils import Format
from nxtomomill.converter.hdf5.utils import get_default_output_file

from .hdf5config import TomoHDF5Config, XRD3DHDF5Config

_logger = logging.getLogger(__name__)

SETTABLE_PARAMETERS_UNITS = {
    "energy": "kev",
    "x_pixel_size": "m",
    "y_pixel_size": "m",
    "detector_sample_distance": "m",
}

SETTABLE_PARAMETERS_TYPE = {
    "energy": float,
    "x_pixel_size": float,
    "y_pixel_size": float,
    "detector_sample_distance": float,
}

SETTABLE_PARAMETERS = SETTABLE_PARAMETERS_UNITS.keys()


def _extract_param_value(key_values):
    """extract all the key / values elements from the str_list. Expected
    format is `param_1_name param_1_value param_2_name param_2_value ...`

    :param str str_list: raw input string as `param_1_name param_1_value
                         param_2_name param_2_value ...`
    :return: dict of tuple (param_name, param_value)
    :rtype: dict
    """
    if len(key_values) % 2 != 0:
        raise ValueError(
            "Expect a pair `param_name, param_value` for each " "parameters"
        )

    def pairwise(it):
        it = iter(it)
        while True:
            try:
                yield next(it), next(it)
            except StopIteration:
                # no more elements in the iterator
                return

    res = {}
    for name, value in pairwise(key_values):
        if name not in SETTABLE_PARAMETERS:
            raise ValueError(f"parameters {name} is not managed")
        if name in SETTABLE_PARAMETERS_TYPE:
            type_ = SETTABLE_PARAMETERS_TYPE[name]
            if type_ is not None:
                res[name] = type_(value)
                continue
        res[name] = value
    return res


class BaseHDF5ConfigHandler:
    """Class to handle inputs to HDF5Config.
    And insure there is no opposite Information
    """

    @staticmethod
    def get_tuple_of_keys_from_cmd(cmd_value):
        return utils.get_tuple_of_keys_from_cmd(cmd_value)

    @staticmethod
    def conv_str_to_bool(bstr):
        return bstr in ("True", True)

    @staticmethod
    def conv_log_level(bool_debug):
        if bool_debug is True:
            return "debug"
        else:
            return "warning"

    @staticmethod
    def conv_xrd_ct_to_format(str_bool):
        if str_bool in ("True", True):
            return Format.XRD_CT
        elif str_bool in ("False", False):
            return Format.STANDARD
        else:
            return None

    def __init__(self, argparse_options, raise_error=True):
        self._argparse_options = argparse_options
        self._config = None
        self.build_configuration(raise_error=raise_error)

    @property
    def configuration(self) -> Union[None, TomoHDF5Config]:
        return self._config

    @property
    def argparse_options(self):
        return self._argparse_options

    def _check_argparse_options(self, raise_error):
        raise NotImplementedError("BaseClass")

    def _create_HDF5_config(self):
        raise NotImplementedError("BAse class")

    def build_configuration(self, raise_error) -> bool:
        """
        :param bool raise_error: raise error if encounter some errors. Else
                                 display a log message
        :return: True if the settings are valid
        """
        self._check_argparse_options(raise_error=raise_error)
        options = self.argparse_options
        config = self._create_HDF5_config()

        # check input and output file
        if config.input_file is None:
            config.input_file = options.input_file
        elif options.input_file is not None and config.input_file != options.input_file:
            raise ValueError(
                "Two different input files provided from "
                "command line and from the configuration file"
            )
        if config.input_file is None:
            err = "No input file provided"
            if raise_error:
                raise ValueError(err)
            else:
                _logger.error(err)

        if config.output_file is None:
            config.output_file = options.output_file
        elif (
            options.output_file is not None
            and config.output_file != options.output_file
        ):
            raise ValueError(
                "Two different output files provided from "
                "command line and from the configuration file"
            )
        if config.output_file is None:
            if config.file_extension is None:
                err = "If no outputfile provided you should provide the extension"
                raise ValueError(err)

            config.output_file = get_default_output_file(
                input_file=config.input_file,
                output_file_extension=config.file_extension.value,
            )
        elif os.path.isdir(config.output_file):
            # if the output file is only a directory: consider we want the same file basename with default extension
            # in this directory
            input_file, _ = os.path.splitext(config.input_file)
            config.output_file = os.path.join(
                os.path.abspath(config.output_file),
                os.path.basename(input_file) + config.file_extension.value,
            )

        # set parameter from the arg parse options
        # key is the name of the argparse option.
        # value is a tuple: (name of the setter in the HDF5Config,
        # function to format the input)
        self._config = self._map_option_to_config_param(config, options)

    def _map_option_to_config_param(self, config, options):
        raise NotImplementedError("Base class")

    def __str__(self):
        raise NotImplementedError("")


class TomoHDF5ConfigHandler(BaseHDF5ConfigHandler):
    def _create_HDF5_config(self):
        if self.argparse_options.config:
            return TomoHDF5Config.from_cfg_file(self.argparse_options.config)
        else:
            return TomoHDF5Config()

    def _map_option_to_config_param(self, config, options):
        mapping = {
            "valid_camera_names": (
                "valid_camera_names",
                self.get_tuple_of_keys_from_cmd,
            ),
            "overwrite": ("overwrite", self.conv_str_to_bool),
            "file_extension": ("file_extension", filter_str_def),
            "single_file": ("single_file", self.conv_str_to_bool),
            "debug": ("log_level", self.conv_log_level),
            "entries": ("entries", self.get_tuple_of_keys_from_cmd),
            "ignore_sub_entries": (
                "sub_entries_to_ignore",
                self.get_tuple_of_keys_from_cmd,
            ),
            "duplicate_data": ("default_copy_behavior", self.conv_str_to_bool),
            "raises_error": ("raises_error", self.conv_str_to_bool),
            "field_of_view": ("field_of_view", filter_str_def),
            "request_input": ("request_input", self.conv_str_to_bool),
            "x_trans_keys": ("x_trans_keys", self.get_tuple_of_keys_from_cmd),
            "y_trans_keys": ("y_trans_keys", self.get_tuple_of_keys_from_cmd),
            "z_trans_keys": ("z_trans_keys", self.get_tuple_of_keys_from_cmd),
            "rot_angle_keys": ("rotation_angle_keys", self.get_tuple_of_keys_from_cmd),
            "sample_detector_distance_paths": (
                "sample_detector_distance_paths",
                self.get_tuple_of_keys_from_cmd,
            ),
            "acq_expo_time_keys": (
                "exposition_time_keys",
                self.get_tuple_of_keys_from_cmd,
            ),
            "x_pixel_size_key": ("x_pixel_size_paths", self.get_tuple_of_keys_from_cmd),
            "y_pixel_size_key": ("y_pixel_size_paths", self.get_tuple_of_keys_from_cmd),
            "init_titles": ("init_titles", self.get_tuple_of_keys_from_cmd),
            "init_zserie_titles": (
                "zserie_init_titles",
                self.get_tuple_of_keys_from_cmd,
            ),
            "init_pcotomo_titles": (
                "pcotomo_init_titles",
                self.get_tuple_of_keys_from_cmd,
            ),
            "dark_titles": ("dark_titles", self.get_tuple_of_keys_from_cmd),
            "flat_titles": ("flat_titles", self.get_tuple_of_keys_from_cmd),
            "proj_titles": ("projections_titles", self.get_tuple_of_keys_from_cmd),
            "align_titles": ("alignment_titles", self.get_tuple_of_keys_from_cmd),
            "set_params": ("param_already_defined", _extract_param_value),
        }
        for argparse_name, (config_name, format_fct) in mapping.items():
            argparse_value = getattr(options, argparse_name)
            if argparse_value is not None:
                value = format_fct(argparse_value)  # pylint: disable=E1102
                setattr(config, config_name, value)
        return config

    def _check_argparse_options(self, raise_error):
        if self.argparse_options is None:
            err = "No argparse options provided"
            if raise_error:
                raise ValueError(err)
            else:
                _logger.error(err)
            return False

        options = self.argparse_options
        if options.config is not None:
            # check no other option are provided
            duplicated_inputs = []
            for opt in (
                "set_params",
                "align_titles",
                "proj_titles",
                "flat_titles",
                "dark_titles",
                "init_zserie_titles",
                "init_titles",
                "init_pcotomo_titles",
                "x_pixel_size_key",
                "y_pixel_size_key",
                "acq_expo_time_keys",
                "rot_angle_keys",
                "valid_camera_names",
                "z_trans_keys",
                "y_trans_keys",
                "x_trans_keys",
                "request_input",
                "raises_error",
                "ignore_sub_entries",
                "entries",
                "debug",
                "overwrite",
                "single_file",
                "file_extension",
                "field_of_view",
                "duplicate_data",
            ):
                if getattr(options, opt):
                    duplicated_inputs.append(opt)
            if len(duplicated_inputs) > 0:
                err = f"You provided a configuration file and inputs for {duplicated_inputs}"
                if raise_error:
                    raise ValueError(err)
                else:
                    _logger.error(err)
                return False


class XRD3DHDF5ConfigHandler(TomoHDF5ConfigHandler):
    def _create_HDF5_config(self):
        if self.argparse_options.config:
            return XRD3DHDF5Config.from_cfg_file(self.argparse_options.config)
        else:
            return XRD3DHDF5Config()

    def _map_option_to_config_param(self, config, options):
        config = super()._map_option_to_config_param(config, options)

        mapping = {
            "rocking_keys": ("rocking_keys", self.get_tuple_of_keys_from_cmd),
        }
        for argparse_name, (config_name, format_fct) in mapping.items():
            argparse_value = getattr(options, argparse_name)
            if argparse_value is not None:
                value = format_fct(argparse_value)  # pylint: disable=E1102
                setattr(config, config_name, value)
        return config

    def _check_argparse_options(self, raise_error):
        super()._check_argparse_options(raise_error)
        options = self.argparse_options
        if options.config is not None:
            # check no other option are provided
            duplicated_inputs = []
            for opt in ("rocking_keys",):
                if getattr(options, opt):
                    duplicated_inputs.append(opt)
            if len(duplicated_inputs) > 0:
                err = f"You provided a configuration file and inputs for {duplicated_inputs}"
                if raise_error:
                    raise ValueError(err)
                else:
                    _logger.error(err)
                return False
