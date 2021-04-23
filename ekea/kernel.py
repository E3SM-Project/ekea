"""EKea Kernel"""

import os, shutil, json, subprocess

from microapp import App
from ekea.utils import xmlquery

here = os.path.dirname(os.path.abspath(__file__))

class E3smKernel(App):
    """Base E3sm Kernel"""

    def __new__(cls, *vargs, **kwargs):

        obj = super(E3smKernel, cls).__new__(cls, *vargs, **kwargs)

        obj.add_argument("casedir", metavar="casedir",
                    help="E3SM case directory")
        obj.add_argument("callsite", metavar="callsite",
                    help="KGen callsite Fortran source file")
        obj.add_argument("-o", "--outdir", type=str,
                    help="output directory")

        obj.add_argument("--srcmod", type=str, nargs="*",
                    help="temporary source modification([eam|cam|ocn:]path)")

        obj.register_forward("data", help="json object")

        obj._namemap = {
            "srcmodname": {
                "eam": "src.eam"
            }
        }

        return obj

    def perform(self, args):

        srcmods = {}

        casedir = os.path.abspath(os.path.realpath(args.casedir["_"]))
        callsite= os.path.abspath(os.path.realpath(args.callsite["_"]))
        csdir, csfile = os.path.split(callsite)
        csname, csext = os.path.splitext(csfile)

        if args.outdir:
            outdir = os.path.abspath(os.path.realpath(args.outdir["_"]))
        else:
            outdir = os.getcwd()

        cleancmd = "cd %s; ./case.build --clean-all" % casedir
        buildcmd = "cd %s; ./case.build" % casedir
        runcmd = "cd %s; ./case.submit" % casedir

        if args.srcmod:
            for smod in args.srcmod:
                pair = smod["_"].split(":") 
                if len(pair)==2:
                    srcmods[pair[1].strip()] = os.path.join(casedir,
                                    "SourceMods", "src."+pair[0].strip())
                else:
                    srcmods[pair[0].strip()] = os.path.join(casedir,
                                    "SourceMods", self._namemap["srcmodname"][self.__name__])

        try:

            # copy source files into sourcemod directory
            for src, modpath in srcmods.items():
                assert os.path.isfile(src)
                shutil.copy(src, modpath)

            batch = xmlquery(casedir, "BATCH_SYSTEM", "--value")

            if batch == "lsf":
                runcmd += " --batch-args='-K'"

            elif "slurm" in batch:
                runcmd += " --batch-args='-W'"

            elif batch == "pbs": # SGE PBS
                runcmd += " --batch-args='-sync yes'"
                #runcmd += " --batch-args='-Wblock=true'" # PBS

            elif batch == "moab":
                runcmd += " --batch-args='-K'"

            else:
                raise Exception("Unknown batch system: %s" % batch)


            compjson = os.path.join(outdir, "compile.json")
            analysisjson = os.path.join(outdir, "analysis.json")
            modeljson = os.path.join(outdir, "model.json")
            srcbackup = os.path.join(outdir, "backup", "src")

            # get mpi and git info here(branch, commit, ...)
            srcroot = os.path.abspath(os.path.realpath(xmlquery(casedir, "SRCROOT", "--value")))
            reldir = os.path.relpath(csdir, start=os.path.join(srcroot, "components", "mpas-source", "src"))

            #callsitefile2 = os.path.join(casedir, "bld", "cmake-bld", reldir, "%s.f90" % csname)

            # get mpi: mpilib from xmlread , env ldlibrary path with the mpilib
            mpidir = os.environ["MPI_ROOT"]
            excludefile = os.path.join(here, "exclude_e3sm_eam.ini")

            # remove e3sm build directory
            blddir = xmlquery(casedir, "OBJROOT", "--value")
            if not os.path.isfile(compjson) and os.path.isdir(blddir):
                shutil.rmtree(blddir)

            # create compile.json
            cmd = " -- buildscan '%s' --savejson '%s' --reuse '%s' --backupdir '%s'" % (
                    buildcmd, compjson, compjson, srcbackup)
            ret, fwds = self.manager.run_command(cmd)

            # recover removed source files
            with open(compjson) as f:
                jcomp = json.load(f)

                for srcpath, compdata in jcomp.items():
                    srcbackup = compdata["srcbackup"]

                    if not srcbackup:
                        continue

                    if not os.path.isfile(srcpath) and srcbackup[0] and os.path.isfile(srcbackup[0]):
                        orgdir = os.path.dirname(srcpath)

                        if not os.path.isdir(orgdir):
                            os.makedirs(orgdir)

                        shutil.copy(srcbackup[0], srcpath)

                    for incsrc, incbackup in srcbackup[1:]:
                        if not os.path.isfile(incsrc) and incbackup and os.path.isfile(incbackup):
                            orgdir = os.path.dirname(incsrc)

                            if not os.path.isdir(orgdir):
                                os.makedirs(orgdir)

                            shutil.copy(incbackup, incsrc)

            statedir = os.path.join(outdir, "state")
            etimedir = os.path.join(outdir, "etime")

            if os.path.isdir(statedir) and os.path.isfile(os.path.join(statedir, "Makefile")):
                stdout = subprocess.check_output("make recover", cwd=statedir, shell=True)

            elif os.path.isdir(etimedir) and os.path.isfile(os.path.join(etimedir, "Makefile")):
                stdout = subprocess.check_output("make recover", cwd=etimedir, shell=True)

            #cmd = " -- resolve --compile-info '@data' '%s'" % callsitefile
            rescmd = (" -- resolve --mpi header='%s/include/mpif.h' --openmp enable"
                     " --compile-info '%s' --keep '%s' --exclude-ini '%s' '%s'" % (
                    mpidir, compjson, analysisjson, excludefile, callsite))

            #ret, fwds = prj.run_command(cmd)
            #assert ret == 0

            # TODO wait??
            #cmd = rescmd + " -- runscan '@analysis' -s 'timing' --outdir '%s' --cleancmd '%s' --buildcmd '%s' --runcmd '%s' --output '%s'" % (
                        #outdir, cleancmd, buildcmd, runcmd, outfile)
            cmd = rescmd + " -- runscan '@analysis' -s 'timing' --outdir '%s' --buildcmd '%s' --runcmd '%s' --output '%s'" % (
                        outdir, buildcmd, runcmd, modeljson)
            #ret, fwds = prj.run_command(cmd)
            # add model config to analysis

            cmd = cmd + " -- kernelgen '@analysis' --model '@model' --repr-etime 'ndata=40,nbins=10'  --outdir '%s'" % outdir

            ret, fwds = self.manager.run_command(cmd)
                                                     
            fwds = self.extract(args)

        except Exception as e:
            print("Uncaught error: %s" % e)
            raise

        finally:
            for org, moddir in srcmods.items():
                os.remove(os.path.join(moddir, os.path.basename(org)))
