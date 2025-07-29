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
module to convert from (bliss) .h5 to (nexus tomo compliant) .nx
"""

__authors__ = ["H. Payno"]
__license__ = "MIT"
__date__ = "13/05/2020"


class Tomo:
    class H5:
        """HDF5 settings for tomography"""

        VALID_CAMERA_NAMES = None
        # now camera names are deduce using converter `get_nx_detectors`
        # and `guess_nx_detector` functions. But you can provide A LIST of
        # detector name (unix shell-style wildcards are managed) like
        # ("pcolinux*", "basler", "frelon*", ...)

        ROT_ANGLE_KEYS = (
            "rotm",
            "mhsrot",
            "hsrot",
            "mrsrot",
            "hrsrot",
            "srot",
            "srot_eh2",
            "diffrz",
            "hrrz_trig",
            "rot",
        )

        X_TRANS_KEYS = ("sx", "d3tx", "tfx", "px", "fake_sx")
        """Keys used to find the x translation"""

        Y_TRANS_KEYS = ("sy", "d3ty", "hry", "py", "fake_sy")
        """Keys used by bliss to store y translation"""

        Z_TRANS_KEYS = ("sz", "d3tz", "hrz", "pz", "mrsz", "fake_sz")
        """Keys used by bliss to store translation"""

        Y_ROT_KEY = "instrument/positioners/yrot"
        """Key used by bliss to store the estimated center of rotation for half
        acquisition"""

        DIODE_KEYS = ("fpico3",)
        """keys used by bliss to store diode dataset"""

        ACQ_EXPO_TIME_KEYS = ("acq_expo_time",)

        INIT_TITLES = (
            # "pcotomo:basic",  seems to not be used anymore
            "tomo:basic",
            "tomo:fullturn",
            "sequence_of_scans",
            "tomo:halfturn",
            "tomo:multiturn",
            "tomo:helical",
        )
        """if a scan starts by one of those string then is considered as
        initialization scan"""

        ZSERIE_INIT_TITLES = ("tomo:zseries",)
        """specific titles for zserie. Will extend DEFAULT_SCAN_TITLES"""

        PCOTOMO_INIT_TITLES = ("tomo:pcotomo", "pcotomo:")
        """specific titles for pcotomo. Will extend DEFAULT_SCAN_TITLES"""

        DARK_TITLES = ("dark images", "dark")
        """if a scan starts by one of those string then is considered as
        dark scan"""
        FLAT_TITLES = ("flat", "reference images", "ref", "refend")
        """if a scan starts by one of those string then is considered as
        reference scan"""
        PROJ_TITLES = ("projections", "ascan rot 0 ", "ascan diffrz 0 180 1600 0.1")
        """if a scan starts by one of those string then is considered as
        projection scan"""
        ALIGNMENT_TITLES = ("static images", "ascan diffrz 180 0 4 0.1")
        """if a scan starts by one of those string then is considered as
        alignment scan"""

        X_PIXEL_SIZE = (  # aka "sample" pixel size
            "technique/optic/sample_pixel_size",
            "technique/detector/pixel_size",
        )
        """Possible path to th pixel size."""

        Y_PIXEL_SIZE = (  # aka "sample" pixel size
            "technique/optic/sample_pixel_size",
            "technique/detector/pixel_size",
        )

        DISTANCE_KEYS = ("technique/scan/sample_detector_distance",)
        """keys used by bliss to store the sample to detector distance"""

        MACHINE_ELECTRIC_CURRENT_KEYS = ("current",)
        """keys used by bliss to store the electric current"""

    class EDF:
        """EDF settings for tomography"""

        MOTOR_POS = ("motor_pos",)

        MOTOR_MNE = ("motor_mne",)

        ROT_ANGLE = (
            "srot",
            "somega",
        )

        X_TRANS = ("sx",)

        Y_TRANS = ("sy",)

        Z_TRANS = ("sz",)

        MACHINE_ELECTRIC_CURRENT = ("srcur", "srcurrent")

        # EDF_TO_IGNORE = ['HST', '_slice_']
        TO_IGNORE = ("_slice_",)

        DARK_NAMES = ("darkend", "dark")

        REFS_NAMES = ("ref", "refHST")


class XRD3D(Tomo):
    class H5(Tomo.H5):
        positioners_path = "instrument/positioners/"

        ROT_ANGLE_KEYS = (positioners_path + "diffrz", positioners_path + "rot")

        ROCKING_KEYS = (
            positioners_path + "diffty",
            positioners_path + "instrument/positioners/dty",
        )
