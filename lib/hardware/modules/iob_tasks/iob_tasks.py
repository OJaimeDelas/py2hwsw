import os
import shutil

from iob_module import iob_module


class iob_tasks(iob_module):
    def __init__(self):
        self.name = "iob_tasks"
        self.version = "V0.10"
        self.setup_dir = os.path.dirname(__file__)
