import os, subprocess, json, shutil
from microapp import App, appdict
from ekea.utils import xmlquery

from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource

here = os.path.dirname(os.path.abspath(__file__))

class KernelTimeViewer(App):
    _name_ = "ktimeview"
    _version_ = "0.1.0"

    def __init__(self, mgr):

        self.add_argument("model", metavar="model", help="Timing model file")

    def perform(self, args):

        etimes = {}
        min_start = 1.E10
        min_etime = 1.E10
        max_etime = 0.
 
        # read model file
        with open(args.model["_"]) as f:
            model = json.load(f)
            for mpi, d1 in model["etime"].items():
                if not mpi.isnumeric():
                    continue

                for omp, d2 in d1.items():
                    ylabel = mpi+"."+omp
                    if ylabel not in etimes:
                        etimes[ylabel] = {}
                    for invoke in sorted(d2.keys()):
                        start, stop = [float(v) for v in d2[invoke]]

                        if start < min_etime:
                            min_etime = start

                        etime = stop - start
                        if etime < min_etime:
                            min_etime = etime

                        elif etime > max_etime:
                            max_etime = etime

                        etimes[ylabel][start] = etime

        source = ColumnDataSource()

        p = figure(title="etime test", x_axis_label="time", y_axis_label="item")

        # TODO: Y : MPI + OpenMP selections
        #       X : Time, merge invervals per abs time, invocations, ...

        #for ylabel in sorted(etimes)[:5]:
        for ylabel in sorted(etimes):
            x, y = [], []
            points = etimes[ylabel]
            min_y = 1.E10
            max_y = 0.
            #for k in sorted(points)[:20]:
            for k in sorted(points):
                yval = points[k]
                x.append(k)
                #y.append((ylabel, yval))
                y.append(yval)
                
                if yval < min_y:
                    min_y = yval 

                elif yval > max_y:
                    max_y = yval 

            x.insert(0, x[0]); x.append(x[-1])
            #y.insert(0, (ylabel, min_y)); y.append((ylabel, min_y))
            y.insert(0, min_y); y.append(min_y)

            xlabel = ylabel + "_x"
            source.add(x, xlabel)
            source.add(y, ylabel)
            p.line(x, y, alpha=0.2, legend_label="Etime", line_width=2)
            #p.vbar(x=x, top=y, legend_label="Etime", line_width=2)
            #p.patch(x=x, ylabel, alpha=0.6, line_color="black", source=source)
            #import pdb; pdb.set_trace()
            #p.patch(xlabel, ylabel, alpha=0.6, line_color="black", source=source)

        p.toolbar_location = "below"

        show(p)


class KernelTimeGenerator(App):
    _name_ = "ktimegen"
    _version_ = "0.1.0"

    def __init__(self, mgr):

        self.add_argument("casedir", metavar="casedir", help="E3SM case directory")
        self.add_argument("callsitefile", metavar="callsitefile", help="ekea callsite Fortran source file")
        self.add_argument("-o", "--outdir", type=str, help="output directory")

        self.register_forward("data", help="json object")

    def perform(self, args):

        casedir = os.path.abspath(os.path.realpath(args.casedir["_"]))
        callsitefile = os.path.abspath(os.path.realpath(args.callsitefile["_"]))
        csdir, csfile = os.path.split(callsitefile)
        csname, csext = os.path.splitext(csfile)
        outdir = os.path.abspath(os.path.realpath(args.outdir["_"])) if args.outdir else os.getcwd()

        cleancmd = "cd %s; ./case.build --clean-all" % casedir
        buildcmd = "cd %s; ./case.build" % casedir
        runcmd = "cd %s; ./case.submit" % casedir

        # TODO: move this batch support to common area

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
        outfile = os.path.join(outdir, "model.json")
        srcbackup = os.path.join(outdir, "backup", "src")

        # get mpi and git info here(branch, commit, ...)
        srcroot = os.path.abspath(os.path.realpath(xmlquery(casedir, "SRCROOT", "--value")))
        reldir = os.path.relpath(csdir, start=os.path.join(srcroot, "components", "mpas-source", "src"))

        callsitefile2 = os.path.join(casedir, "bld", "cmake-bld", reldir, "%s.f90" % csname)

        # get mpi: mpilib from xmlread , env ldlibrary path with the mpilib
        mpidir = os.environ["MPI_ROOT"]
        excludefile = os.path.join(here, "exclude_e3sm_mpas.ini")

        blddir = xmlquery(casedir, "OBJROOT", "--value")
        if not os.path.isfile(compjson) and os.path.isdir(blddir):
            shutil.rmtree(blddir)

        cmd = " -- buildscan '%s' --savejson '%s' --reuse '%s' --backupdir '%s'" % (
                buildcmd, compjson, compjson, srcbackup)
        ret, fwds = self.manager.run_command(cmd)

        # save compjson with case directory map
        # handle mpas converted file for callsitefile2
        # TODO: replace ekea contaminated file with original files
        # TODO: recover removed e3sm converted files in cmake-bld, ... folders

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
                
        # TODO: actually scan source files if they should be recovered

        statedir = os.path.join(outdir, "state")
        etimedir = os.path.join(outdir, "etime")

        if os.path.isdir(statedir) and os.path.isfile(os.path.join(statedir, "Makefile")):
            stdout = subprocess.check_output("make recover", cwd=statedir, shell=True)

        elif os.path.isdir(etimedir) and os.path.isfile(os.path.join(etimedir, "Makefile")):
            stdout = subprocess.check_output("make recover", cwd=etimedir, shell=True)

        #cmd = " -- resolve --compile-info '@data' '%s'" % callsitefile
        rescmd = (" -- resolve --mpi header='%s/include/mpif.h' --openmp enable"
                 " --compile-info '%s' --exclude-ini '%s' '%s'" % (
                mpidir, compjson, excludefile, callsitefile2))
        #ret, fwds = prj.run_command(cmd)
        #assert ret == 0

        # TODO wait??
        #cmd = rescmd + " -- runscan '@analysis' -s 'timing' --outdir '%s' --cleancmd '%s' --buildcmd '%s' --runcmd '%s' --output '%s'" % (
                    #outdir, cleancmd, buildcmd, runcmd, outfile)
        cmd = rescmd + " -- runscan '@analysis' -s 'timing' --outdir '%s' --buildcmd '%s' --runcmd '%s' --output '%s'" % (
                    outdir, buildcmd, runcmd, outfile)

        ret, fwds = self.manager.run_command(cmd)

        if os.path.isfile(outfile):
            with open(outfile) as f:
                mfile = json.load(f)
                if "etime" in mfile:
                    print("Kernel timing file is generated at '%s'." % outfile)

                else:
                    print("ERROR: wrong rkKernel timing file is generated at '%s'." % outfile)
        else: 
            print("No kernel timing file is generated.")
