import os

from iob_module import iob_module


class iob_div_pipe(iob_module):
    def __init__(self):
        self.name = "iob_div_pipe"
        self.version = "V0.10"
        self.setup_dir = os.path.dirname(__file__)
