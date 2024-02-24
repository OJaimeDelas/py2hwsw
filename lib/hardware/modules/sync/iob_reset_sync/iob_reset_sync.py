import os

from iob_module import iob_module
from iob_r import iob_r


class iob_reset_sync(iob_module):
    def __init__(self):
        self.name = "iob_reset_sync"
        self.version = "V0.10"
        self.setup_dir = os.path.dirname(__file__)
        self.submodules_list = [
            iob_r,
        ]
