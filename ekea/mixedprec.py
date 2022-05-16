"""Ekea Mixed-precision experiment app"""

import os

# Mixed-precision app
class E3SMMixedPrec(App):

    _name_ = "mixedprec"
    _version_ = "0.1.0"

    def __init__(self, mgr):

        self.add_argument("casedir", metavar="casedir", help="E3SM case directory")
        self.add_argument("callsitefile", metavar="callsitefile", help="ekea callsite Fortran source file")
        self.add_argument("-o", "--outdir", type=str, help="output directory")

        self.register_forward("data", help="json object")

    # main entry
    def perform(self, args):

        # check if eam or mpas-ocean


        callsitefile = os.path.abspath(os.path.realpath(args.callsitefile["_"]))
        csdir, csfile = os.path.split(callsitefile)
        reldir = os.path.relpath(csdir, start=os.path.join(srcroot, "components", "mpas-source", "src"))
        callsitefile2 = os.path.join(casedir, "bld", "cmake-bld", reldir, "%s.f90" % csname)

        args.callsitefile["_"] = callsitefile2

        self.generate(args, "exclude_e3sm_mpas.ini")

        self.generate(args, "exclude_e3sm_eam.ini")

