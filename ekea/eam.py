"""Ekea for EAM model"""

import os, subprocess, json, shutil

from ekea.e3smapp import E3SMKernel, here
from ekea.utils import xmlquery

# EAM app
class EAMKernel(E3SMKernel):

    _name_ = "eam"
    _version_ = "1.0.0"

    # main entry
    def perform(self, args):

        self.generate(args, "exclude_e3sm_eam.ini")
