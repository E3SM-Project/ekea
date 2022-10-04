"""E3SM Kernel generation module"""

import os, subprocess, json, shutil, re

import xml.etree.ElementTree as ET

from microapp import App
from ekea.utils import xmlquery

here = os.path.dirname(os.path.abspath(__file__))

#match_namepath = re.compile(r'\s*\[\s*namepath\s*\]')

# E3SM app
class E3SMKernel(App):
    """Generate E3SM kernel

    Command-line arguments
    -----------------------
    casedir : str
        E3SM case directory
    callsitefile : str
        E3SM source file containing ekea kernel extraction directives
    outdir: str, optional
        E3SM kernel output directory
"""

    def __init__(self, mgr):

        self.add_argument("casedir", metavar="casedir", help="E3SM case directory")
        self.add_argument("callsitefile", metavar="callsitefile", help="ekea callsite Fortran source file")
        self.add_argument("-o", "--outdir", type=str, help="output directory")
        self.add_argument("-m", "--mpidir", type=str, help="MPI root directory")
        self.add_argument("-e", "--exclude-ini", dest="exclude_ini", action='store',
                            type=str, help="information to be excluded for analysis")
        self.add_argument("-i", "--include-ini", dest="include_ini", action='store',
                            type=str, help="information to be included for analysis")
        self.add_argument("--no-batch", action="store_true", help="Do not submit jobs to batch system, run locally")

        # placeholder for providing next application with analysis object. Not used yet.
        self.register_forward("data", help="json object")

    
    def ini_merge(self, userini, excludefile, outdir):

        sections = {}
        section = None

        for inifile in [userini, excludefile]:
            with open(inifile) as f:
                for line in f:
                    line2 = line.strip()
                    if len(line2) >=2 and line2[0] == "[" and line2[-1] == "]":
                        secname = line2[1:-1].strip()
                        if secname not in sections:
                            sections[secname] = []

                        section = sections[secname]

                    elif section:
                        section.append(line)

                    else:
                        raise("Exclude ini file syntax error: %s" % line)

        outini = os.path.join(outdir, "excludes.ini")

        with open(outini, "w") as f:
            for secname, secbody in sections.items():
                f.write("[%s]\n" % secname)
                for line in secbody:
                    f.write(line)
        
        return outini

    # main entry
    def generate(self, args, excludefile):
        """Generate E3SM kernel

        Parameters 
        -----------------------
        args : ArgParser
            MicroApp command-line parser object
        excludefile : str
            INI-format file that contains list of identifies that will be skipped during source code analysis.
"""

        print("==== Kernel extraction is started. (%s) ====" % self._name_)

        # generate several absolute paths
        casedir = os.path.abspath(os.path.realpath(args.casedir["_"]))
        callsitefile = os.path.abspath(os.path.realpath(args.callsitefile["_"]))
        outdir = os.path.abspath(os.path.realpath(args.outdir["_"])) if args.outdir else os.getcwd()

        print("[Case directory] = %s" % casedir)
        print("[Callsite file] = %s" % callsitefile)
        print("[Output directory] = %s" % outdir)

        # create E3SM commands to clean/build/submit a E3SM case
        cleancmd = "cd %s; ./case.build --clean-all" % casedir
        buildcmd = "cd %s; ./case.build" % casedir
        runcmd = "cd %s; ./case.submit" % casedir

        if args.exclude_ini and os.path.isfile(args.exclude_ini["_"]):
            excludefile = self.ini_merge(args.exclude_ini["_"], excludefile, outdir)

        includeopt = ""
        if args.include_ini and os.path.isfile(args.include_ini["_"]):
            includeopt = "--include-ini '%s'" % args.include_ini["_"]

        if args.no_batch:
            runcmd += " --no-batch"

        batchspec = xmlquery(casedir, "BATCH_SPEC_FILE", "--value")
        mach = xmlquery(casedir, "MACH", "--value")
        nthreads = xmlquery(casedir, "NTHRDS", "--value")

        nthrds = re.findall(r'\w\w\w:(?P<t>\d)', nthreads)
        ompflag = ""
        if any([int(t)>1 for t in nthrds]):
            ompflag = "--openmp enable"

        root = ET.parse(batchspec).getroot()

        for node in root.findall("./batch_system"):
            if "MACH" in node.attrib and node.attrib["MACH"] == mach:
                batch = node.attrib["type"]

                print("[Batch system] = %s" % batch)

                if batch == "lsf":
                    runcmd += " --batch-args='-K'"

                elif "slurm" in batch:
                    runcmd += " --batch-args='-W'"

                elif batch == "pbs": # SGE PBS
                    runcmd += " --batch-args='-sync yes'"
                    #runcmd += " --batch-args='-Wblock=true'" # PBS

                elif batch == "moab":
                    runcmd += " --batch-args='-K'"

                break

        # create some output names
        compjson = os.path.join(outdir, "compile.json")
        outfile = os.path.join(outdir, "model.json")
        srcbackup = os.path.join(outdir, "backup", "src")

        # get mpi root directory
        mpidir = None

        if args.mpidir:
            mpidir = os.path.abspath(os.path.realpath(args.mpidir["_"]))

        else:
            for val in os.environ.values():
                if (os.path.isdir(val) and os.path.isdir(os.path.join(val, "include")) and
                    os.path.isfile(os.path.join(val, "include", "mpif.h"))):
                    mpidir = val
                    break

        if mpidir is None:
            raise Exception("Unknown MPI directory")

        
        print("[MPI directory] = %s" % mpidir)

        blddir = xmlquery(casedir, "OBJROOT", "--value")
        if not os.path.isfile(compjson) and os.path.isdir(blddir):
            shutil.rmtree(blddir)

        # run a fortlab command to compile e3sm and collect compiler options
        cmd = " -- buildscan '%s' --savejson '%s' --reuse '%s' --backupdir '%s'" % (
                buildcmd, compjson, compjson, srcbackup)
        ret, fwds = self.manager.run_command(cmd)

        # copy source file back to original locations if deleted
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
            try:
                stdout = subprocess.check_output("make recover", cwd=statedir, shell=True)
            except:
                shutil.rmtree(statedir)

        elif os.path.isdir(etimedir) and os.path.isfile(os.path.join(etimedir, "Makefile")):
            try:
                stdout = subprocess.check_output("make recover", cwd=etimedir, shell=True)
            except:
                shutil.rmtree(etimedir)

        # fortlab command to analyse source files
        rescmd = (" -- resolve --mpi header='%s/include/mpif.h' %s"
                 " --compile-info '%s' --exclude-ini '%s' %s '%s' --outdir '%s'" % (
                mpidir, ompflag, compjson, excludefile, includeopt, callsitefile, outdir))

        # fortlab command to generate raw timing data
        cmd = rescmd + " -- runscan '@analysis' -s 'timing' --outdir '%s' --buildcmd '%s' --runcmd '%s' --output '%s'" % (
                    outdir, buildcmd, runcmd, outfile)

        # fortlab command to generate kernel and input/output data
        cmd = cmd + " -- kernelgen '@analysis' --model '@model' --repr-etime 'ndata=40,nbins=10'  --outdir '%s'" % outdir

        # run microapp command
        ret, fwds = self.manager.run_command(cmd)

        print("==== Kernel extraction is finished. (%s) ====" % self._name_)
