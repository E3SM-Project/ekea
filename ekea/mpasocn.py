import os, subprocess, json, shutil

from microapp import appdict

from ekea.e3smapp import E3SMKernel, here
from ekea.utils import xmlquery

# MPAS Ocean app
class MPASOcnKernel(E3SMKernel):

    _name_ = "mpasocn"
    _version_ = "0.1.0"

    def perform(self, args):

        callsitefile = os.path.abspath(os.path.realpath(args.callsitefile["_"]))
        csdir, csfile = os.path.split(callsitefile)
        reldir = os.path.relpath(csdir, start=os.path.join(srcroot, "components", "mpas-source", "src"))
        callsitefile2 = os.path.join(casedir, "bld", "cmake-bld", reldir, "%s.f90" % csname)

        args.callsitefile["_"] = callsitefile2

        self.generate(args, "exclude_e3sm_mpas.ini")

