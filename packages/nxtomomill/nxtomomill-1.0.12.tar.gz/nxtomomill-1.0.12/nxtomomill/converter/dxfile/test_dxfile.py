# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2016-2017 European Synchrotron Radiation Facility
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
__date__ = "02/06/2021"


import os
import shutil
import tempfile
import unittest

import numpy

from nxtomomill import converter
from nxtomomill.test.utils.dxfile import MockDxFile

from tomoscan.esrf.scan.nxtomoscan import NXtomoScan
from tomoscan.validator import is_valid_for_reconstruction

from silx.io.utils import get_data


class TestDxToNxConverter(unittest.TestCase):
    """
    Test the DXtoNxConverter and the 'from_dx_to_nx' function
    """

    def setUp(self) -> None:
        self.folder = tempfile.mkdtemp()
        self.dxfile_path = os.path.join(self.folder, "dxfile.h5")

        self.n_projections = 50
        self.n_darks = 2
        self.n_flats = 4
        self.mock = MockDxFile(
            file_path=self.dxfile_path,
            n_projection=self.n_projections,
            n_darks=self.n_darks,
            n_flats=self.n_flats,
        )

    def tearDown(self) -> None:
        shutil.rmtree(self.folder)

    def test_simple_converter(self):
        """
        Test a simple conversion when NX_class is defined
        """
        for duplicate_data in (True, False):
            with self.subTest(duplicate_data=duplicate_data):
                output_file = os.path.join(self.folder, "dxfile.nx")

                results = converter.from_dx_to_nx(
                    input_file=self.dxfile_path,
                    output_file=output_file,
                    duplicate_data=duplicate_data,
                )
                self.assertEqual(len(results), 1)
                self.assertTrue(os.path.exists(output_file))
                _, entry = results[0]
                scan = NXtomoScan(output_file, entry)
                self.assertEqual(len(scan.projections), self.n_projections)
                self.assertEqual(len(scan.darks), self.n_darks)
                self.assertEqual(len(scan.flats), self.n_flats)
                self.assertEqual(numpy.array(scan.rotation_angle).min(), 0)
                self.assertEqual(numpy.array(scan.rotation_angle).max(), 180)
                assert is_valid_for_reconstruction(scan)

                # check arrays are correctly copied from mock
                numpy.testing.assert_array_equal(
                    self.mock.data_dark[0], get_data(scan.darks[0])
                )
                numpy.testing.assert_array_equal(
                    self.mock.data_flat[1], get_data(scan.flats[3])
                )
                idx_last_proj = self.n_projections + self.n_flats + self.n_darks - 1
                numpy.testing.assert_array_equal(
                    self.mock.data_proj[-1], get_data(scan.projections[idx_last_proj])
                )
                self.assertEqual(scan.rotation_angle[0], 0)  # pylint: disable=E1136
                self.assertEqual(scan.rotation_angle[5], 0)  # pylint: disable=E1136
                self.assertEqual(scan.rotation_angle[6], 0)  # pylint: disable=E1136
                self.assertEqual(scan.rotation_angle[-1], 180)  # pylint: disable=E1136

                # if overwrite not requested should fail on reprocessing
                with self.assertRaises(OSError):
                    converter.from_dx_to_nx(
                        input_file=self.dxfile_path,
                        output_file=output_file,
                        duplicate_data=duplicate_data,
                        overwrite=False,
                    )

                # if overwrite requested should succeed
                converter.from_dx_to_nx(
                    input_file=self.dxfile_path,
                    output_file=output_file,
                    overwrite=True,
                    duplicate_data=duplicate_data,
                )
