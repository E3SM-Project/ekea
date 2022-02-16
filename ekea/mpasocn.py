import os, subprocess, json, shutil

from microapp import appdict

from ekea.e3smapp import E3SMKGen, here
from ekea.utils import xmlquery

# MPAS Ocean app
class MPASOcnKernel(E3SMKGen):

    _name_ = "mpasocn"
    _version_ = "0.1.0"

    def perform(self, args):
#
#        casedir = os.path.abspath(os.path.realpath(args.casedir["_"]))
#        callsitefile = os.path.abspath(os.path.realpath(args.callsitefile["_"]))
#        csdir, csfile = os.path.split(callsitefile)
#        csname, csext = os.path.splitext(csfile)
#
#        srcroot = os.path.abspath(os.path.realpath(xmlquery(casedir, "SRCROOT", "--value")))
#
#        import pdb; pdb.set_trace()
#        reldir = os.path.relpath(csdir, start=os.path.join(srcroot, "components", "mpas-ocean", "src"))
#        callsitefile2 = os.path.join(casedir, "bld", "cmake-bld", reldir, "%s.f90" % csname)
#
#        args.callsitefile["_"] = callsitefile2

        self.generate(args, "exclude_e3sm_mpas.ini")

