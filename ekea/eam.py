"""Ekea for EAM model"""

from ekea.e3smapp import E3SMKernel

# EAM app
class EAMKernel(E3SMKGen):

    _name_ = "eam"
    _version_ = "1.0.0"

    # main entry
    def perform(self, args):

        self.generate(args, "exclude_e3sm_eam.ini")
