import os

from iob_module import iob_module


class alt_iobuf(iob_module):
    def __init__(self):
        self.name = "alt_iobuf"
        self.version = "V0.10"
        self.setup_dir = os.path.dirname(__file__)
