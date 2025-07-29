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
Application to convert a tomo dataset written in edf into and hdf5/nexus file.

.. code-block:: bash

    usage: nxtomomill edf2nx [-h] [--dataset-basename DATASET_BASENAME] [--info-file INFO_FILE] [--config CONFIG] [scan_path] [output_file]

    convert data acquired as edf to hdf5 - nexus compliant file format.

    positional arguments:
    scan_path             folder containing the edf files
    output_file           foutput .h5 file

    optional arguments:
    -h, --help            show this help message and exit
    --dataset-basename DATASET_BASENAME, --file-prefix DATASET_BASENAME
                            file prefix to be used to deduce projections
    --info-file INFO_FILE
                            .info file containing acquisition information (ScanRange, Energy, TOMO_N...)
    --config CONFIG, --configuration-file CONFIG, --configuration CONFIG
                            file containing the full configuration to convert from SPEC-EDF to bliss to nexus. Default configuration file can be created from `nxtomomill edf-config` command

For a complete tutorial you can have a look at :ref:`edf2nxtutorial`
"""

__authors__ = ["C. Nemoz", "H. Payno", "A.Sole"]
__license__ = "MIT"
__date__ = "16/01/2020"


import argparse
import logging

from nxtomomill import converter
from nxtomomill.io.utils import convert_str_to_tuple
from nxtomomill.io.config.edfconfig import TomoEDFConfig
from nxtomomill.settings import Tomo
from nxtomomill.utils import Progress

logging.basicConfig(level=logging.INFO)


def main(argv):
    """ """
    parser = argparse.ArgumentParser(
        description="convert data acquired as "
        "edf to hdf5 - nexus "
        "compliant file format."
    )
    parser.add_argument("scan_path", help="folder containing the edf files", nargs="?")
    parser.add_argument("output_file", help="foutput .h5 file", nargs="?")
    parser.add_argument(
        "--dataset-basename",
        "--file-prefix",
        default=None,
        help="file prefix to be used to deduce projections",
    )
    parser.add_argument(
        "--info-file",
        default=None,
        help=".info file containing acquisition information (ScanRange, Energy, TOMO_N...)",
    )
    parser.add_argument(
        "--config",
        "--configuration-file",
        "--configuration",
        default=None,
        help="file containing the full configuration to convert from SPEC-EDF to bliss to nexus. "
        "Default configuration file can be created from `nxtomomill edf-config` command",
    )
    parser.add_argument(
        "--delete-edf",
        "--delete-edf-source",
        "--delete-edf-source-files",
        default=False,
        action="store_true",
        help="if you are duplicating data (default behavior) you can ask to delete used edf files to free space",
    )
    parser.add_argument(
        "--output-checks",
        default=tuple(),
        help="Define list of check to be run once the conversion is finished (raise an error if check fails). This is done before removing edf if asked. So if check fails source edf files won't be removed",
    )
    parser.add_argument(
        "--use-existing-angles",
        "--no-angle-recalculcation",
        default=None,
        action="store_true",
        help=f"By default the angle will be recomputed to have equally spaced angles from the min and the max angles. If this option is set then angles defined in edf headers ({','.join(Tomo.EDF.ROT_ANGLE)}) will be used.",
    )
    options = parser.parse_args(argv[1:])
    config = TomoEDFConfig()
    if options.config is not None:
        config = config.from_cfg_file(options.config)

    check_input = {
        "dataset basename": (options.dataset_basename, config.dataset_basename),
        "scan path": (options.scan_path, config.input_folder),
        "output file": (options.output_file, config.output_file),
        "info file": (options.info_file, config.dataset_info_file),
    }
    for input_name, (opt_value, config_value) in check_input.items():
        if (
            opt_value is not None
            and config_value is not None
            and opt_value != config_value
        ):
            raise ValueError(
                f"two values for {input_name} are provided from arguments and configuration file ({opt_value, config_value})"
            )

    if options.dataset_basename is not None:
        config.dataset_basename = options.dataset_basename
    if options.info_file is not None:
        config.dataset_info_file = options.info_file
    if options.scan_path is not None:
        config.input_folder = options.scan_path
    if options.output_file is not None:
        config.output_file = options.output_file
    config.delete_edf_source_files = options.delete_edf
    if options.use_existing_angles is not None:
        config.force_angle_calculation = not options.use_existing_angles
    config.output_checks = convert_str_to_tuple(options.output_checks)

    assert isinstance(
        config.output_checks, tuple
    ), f"config.output_checks is expected to be a tuple. Gets {type(config.output_checks)}"
    converter.from_edf_to_nx(
        configuration=config,
        progress=Progress(""),
    )
