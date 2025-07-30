""" Defines the configuration values of the module.
    Values in the ProStore are saved and loaded during application startup/shutdown automatically
Copyright Nanosurf AG 2021
License - MIT
"""

import enum
import pathlib
import os
import nanosurf.lib.datatypes.sci_val as sci_val
import nanosurf.lib.datatypes.prop_val as prop_val

class SetupSettings(prop_val.PropStore):
    """ settings defined here as PropVal are stored persistently in a ini-file
        settings with a '_' as first char are not stored
    """
    def __init__(self) -> None:
        super().__init__()
        self._controller_sn = prop_val.PropVal("-")
        self._sample_holder_sn = prop_val.PropVal("-")
        self._cal_names = ""
        self._cal_0_values:list[float] = []
        self._cal_1_values:list[float] = []
        self._cal_2_values:list[float] = []
        # self.auto_field_start = prop_val.PropVal(sci_val.SciVal(0, "T"))
        # self.auto_field_step = prop_val.PropVal(sci_val.SciVal(0.01, "T"))
        # self.cal_steps = prop_val.PropVal(sci_val.SciVal(3, ""))
        # self.save_to_path = prop_val.PropVal(pathlib.Path(os.getenv(r"UserProfile"))  / "Desktop" / "VMF_Data")
        # self.data_file_mask = prop_val.PropVal(pathlib.Path(r'VMF_Image'))



