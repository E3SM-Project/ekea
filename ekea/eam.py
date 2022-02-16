"""Ekea for EAM model"""

import os, subprocess, json, shutil

from ekea.e3smapp import E3SMKGen, here
from ekea.utils import xmlquery

# EAM app
class EAMKernel(E3SMKGen):

    _name_ = "eam"
    _version_ = "0.1.0"

    # main entry
    def perform(self, args):

        self.generate(args, "exclude_e3sm_eam.ini")
