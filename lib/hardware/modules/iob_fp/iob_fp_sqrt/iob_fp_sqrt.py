import os

from iob_module import iob_module

from iob_int_sqrt import iob_int_sqrt


class iob_fp_sqrt(iob_module):
    def __init__(self):
        self.name = "iob_fp_sqrt"
        self.version = "V0.10"
        self.setup_dir = os.path.dirname(__file__)
        self.submodules_list = [
            iob_int_sqrt,
        ]
