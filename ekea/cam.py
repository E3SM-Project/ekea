"""EKea CAM Kernel"""

import os, subprocess, json, shutil
from microapp import App, appdict
from ekea.kernel import E3smKernel
from ekea.utils import xmlquery

here = os.path.dirname(os.path.abspath(__file__))

class CamKernel(E3smKernel):

    _name_ = "cam"
    _version_ = "0.1.0"

    def extract(self, args):

        fwds = {}


        return fwds
