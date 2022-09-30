"""MPAS Ocean kernel generation module."""

import os, subprocess, json, shutil

from ekea.e3smapp import E3SMKernel, here
from ekea.utils import xmlquery

# MPAS Ocean app
class MPASOcnKernel(E3SMKernel):
    """A wrapper class of E3SMKernel to place any customization for MPAS Ocean.
    """

    _name_ = "ocn"
    _version_ = "1.0.0"

    # The main entry to extract a MPAS Ocean kernel.
    def perform(self, args):
        """Extract a MPAS Ocean kernel."""

        here = os.path.dirname(os.path.realpath(__file__))

        # MPAS Ocean convert raw source files before the compilation
        # Following statements convert the path to the raw source file to
        # the path to the converted sourcefile.
        casedir = os.path.abspath(os.path.realpath(args.casedir["_"]))
        srcroot = os.path.abspath(os.path.realpath(xmlquery(casedir, "SRCROOT", "--value")))

        callsitefile = os.path.abspath(os.path.realpath(args.callsitefile["_"]))
        csdir, csfile = os.path.split(callsitefile)
        csname, csext = os.path.splitext(csfile)
        reldir = os.path.relpath(csdir, start=os.path.join(srcroot, "components", "mpas-ocean", "src"))
        callsitefile2 = os.path.join(casedir, "bld", "cmake-bld", "core_ocean", reldir, "%s.f90" % csname)

        args.callsitefile["_"] = callsitefile2

        self.generate(args, os.path.join(here, "exclude_e3sm_mpas.ini"))

