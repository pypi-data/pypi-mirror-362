"""
module to define a xrd-ct acquisition (made by bliss)
"""

from silx.io.url import DataUrl

from nxtomomill.io.acquisitionstep import AcquisitionStep
from nxtomomill.io.config import TomoHDF5Config
from nxtomomill.converter.hdf5.acquisition.standardacquisition import (
    StandardAcquisition,
)


class XRDCTAcquisition(StandardAcquisition):
    def __init__(
        self,
        root_url: DataUrl,
        configuration: TomoHDF5Config,
        detector_sel_callback,
        start_index,
        copy_frames: bool = False,
    ):
        """
        Note: for now we are force to provide entry and entry path as both
        can be different. For example when we are browsing the sample
        file entry == entry_path == 1.1 for example.
        Bit for the sample file file entry == 1.1 != entry_path == acquisssXXX_1.1

        :param entry:
        :param file_keys:
        :param scan_titles:
        :param param_already_defined:
        :param raise_error_if_issue:
        :param detector_sel_callback:
        """
        super().__init__(
            root_url=root_url,
            configuration=configuration,
            detector_sel_callback=detector_sel_callback,
            start_index=start_index,
        )
        # for XRD-CT data is contained in the 'acquisition' sequence
        # and we only have projections
        self.register_step(url=root_url, entry_type=AcquisitionStep.PROJECTION)

    @property
    def is_xrd_ct(self):
        return True

    @property
    def require_x_translation(self):
        return False

    @property
    def require_z_translation(self):
        return True

    @property
    def has_diode(self):
        return True

    def is_different_sequence(self, url: DataUrl):
        if not isinstance(url, DataUrl):
            raise TypeError(
                "url is expected to be a DataUrl. This case is " "not managed"
            )

        def get_scan_name(my_str):
            return "".join(my_str.rstrip(".").split(".")[0:-1])

        return self.root_url.file_path() != url.file_path() and get_scan_name(
            self.root_url.data_path()
        ) != get_scan_name(url.data_path())

    def get_axis_scale_types(self):
        """
        Return axis display for the detector data to be used by silx view
        """
        return ["linear", "log"]

    def _write_beam(self, root_node, request_input, input_callback):
        instrument_node = root_node.require_group("instrument")
        instrument_node.require_group("beam")
