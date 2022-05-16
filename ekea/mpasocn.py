import os, subprocess, json, shutil

from microapp import appdict

from ekea.e3smapp import E3SMKGen, here
from ekea.utils import xmlquery

# MPAS Ocean app
class MPASOcnKernel(E3SMKGen):

    _name_ = "mpasocn"
    _version_ = "1.0.0"

    def perform(self, args):

        casedir = os.path.abspath(os.path.realpath(args.casedir["_"]))
        srcroot = os.path.abspath(os.path.realpath(xmlquery(casedir, "SRCROOT", "--value")))

        callsitefile = os.path.abspath(os.path.realpath(args.callsitefile["_"]))
        csdir, csfile = os.path.split(callsitefile)
        reldir = os.path.relpath(csdir, start=os.path.join(srcroot, "components", "mpas-source", "src"))
        callsitefile2 = os.path.join(casedir, "bld", "cmake-bld", reldir, "%s.f90" % csname)

        args.callsitefile["_"] = callsitefile2

        self.generate(args, "exclude_e3sm_mpas.ini")

