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
Application to create a default configuration file to be used by edf2nx application.

.. code-block:: bash

    usage: nxtomomill edf-config [-h] output_file

    Create a default configuration file

    positional arguments:
      output_file         output .cfg file

For a complete tutorial you can have a look at :ref:`edf2nxtutorial`
"""

__authors__ = [
    "H. Payno",
]
__license__ = "MIT"
__date__ = "23/02/2021"


import argparse
import logging

from nxtomomill.io import TomoEDFConfig, generate_default_edf_config

logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger(__name__)


def main(argv):
    """ """
    parser = argparse.ArgumentParser(description="Create a default configuration file")
    parser.add_argument("output_file", help="output .cfg file")
    parser.add_argument(
        "--level",
        "--option-level",
        help="Level of options to embed in the configuration file. Can be 'required' or 'advanced'.",
        default="required",
    )

    options = parser.parse_args(argv[1:])

    configuration = generate_default_edf_config(level=options.level)
    TomoEDFConfig.dict_to_cfg(file_path=options.output_file, dict_=configuration)
