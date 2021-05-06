
import os, shutil, platform

from ekea import E3SMKea

here = os.path.dirname(os.path.abspath(__file__))
is_summit = len([k for k in os.environ.keys() if k.startswith("OLCF_")]) > 3

def test_summit(capsys):

    if not is_summit:
        return

    prj = E3SMKea()

    #mpidir = os.environ["MPI_ROOT"]

    e3smdir = "/ccs/home/grnydawn/repos/github/E3SM"
    #casedir = "/home/groups/coegroup/e3sm/scratch/coe0165/SMS_P12x2.ne4_oQU240.A_WCYCL1850.tulip_gnu.20200918_134511_d1oute"
    #casedir = "/ccs/home/grnydawn/prjdir/e3sm_scratch/ERS_Ld5.T62_oQU120.CMPASO-NYF.summit_pgi.20201112_170629_a0e7o3"
    casedir = "/gpfs/alpine/cli115/proj-shared/grnydawn/e3sm_scratch/ERS_Ld5.T62_oQU120.CMPASO-NYF.summit_pgi.20210125_094617_kmwz7r"

    #outdir = "/ccs/home/grnydawn/prjdir/kernels/ekeatest/ocn2_kmwz7r"
    outdir = "/gpfs/alpine/cli115/proj-shared/grnydawn/e3sm_scratch/ocn3_kmwz7r"

    #modeljson = os.path.join(outdir, "model.json")
    
    callsitefile = os.path.join(e3smdir, "components/mpas-source/src/core_ocean/shared/mpas_ocn_diagnostics.F")
    #callsitefile2 = os.path.join(casedir, "bld/cmake-bld/core_ocean/shared/mpas_ocn_gm.f90")
    patchfile = os.path.join(here, "res", "mpas_ocn_gm.F")
    #patchfile2 = os.path.join(here, "res", "mpas_ocn_gm.f90")
    patchpath = os.path.join(e3smdir, "components/mpas-source/src/core_ocean/shared")
    #patchpath2 = os.path.join(casedir, "bld/cmake-bld/core_ocean/shared")
    #compjson = os.path.join(outdir, "compile.json")
    #analysisjson = os.path.join(outdir, "analysis.json")
    #excludefile = "/ccs/home/grnydawn/bin/exclude_e3sm_mpas.ini"

    # copy patch file to workaround fparser bug of parsing array constructor using "[", "]"
    shutil.copy(patchfile, patchpath)
    #shutil.copy(patchfile2, patchpath2)

    if not os.path.exists(outdir):
        os.makedirs(outdir)


    cmd = "-- mpasocn '%s' '%s' -o '%s'" % (casedir, callsitefile, outdir)
    ret, fwds = prj.run_command(cmd)

    assert ret == 0

    #assert os.path.isfile(modeljson) is True
    assert os.path.isfile(os.path.join(outdir, "kernel", "gm_bolus_velocity.0.0.1"))

    ret, fwds = prj.run_command("shell 'make' --workdir '%s'" % os.path.join(outdir, "kernel"))

    assert ret == 0
    if fwds["stderr"]:
        print("STDERR")
        print(fwds["stderr"])

    ret, fwds = prj.run_command("shell './kernel.exe' --workdir '%s'" % os.path.join(outdir, "kernel"))

    assert ret == 0
    assert not fwds["stderr"]
    assert b"PASSED verification" in fwds["stdout"]

    shutil.rmtree(outdir)
