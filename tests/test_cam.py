import os, shutil

from ekea import E3smKea

here = os.path.dirname(os.path.abspath(__file__))
is_summit = len([k for k in os.environ.keys() if k.startswith("OLCF_")]) > 3

prj = E3smKea()

def get_test_configuration():

    cfg = {}

    if is_summit:
        cfg["scratchdir"] = "/gpfs/alpine/cli115/scratch/grnydawn"

    else:
        print("Not supported system")
        assert False

    cfg["workdir"] = os.path.join(cfg["scratchdir"], "ekea_tests", "cam")
    cfg["outdir"] = os.path.join(cfg["workdir"], "output")
    cfg["e3smdir"] = os.path.join(cfg["workdir"], "E3SM")
    cfg["cimedir"] = os.path.join(cfg["e3smdir"], "cime")
    cfg["scriptdir"] = os.path.join(cfg["cimedir"], "scripts")

    cfg["casedir"] = os.path.join(cfg["workdir"], "TESTCASE")
    
    #cfg["gitclone"] = ("git clone -b maint-1.2 --recursive "
    cfg["gitclone"] = ("git clone --recursive "
                        "https://github.com/E3SM-Project/E3SM.git")

    cfg["compset"] = "FC5AV1C-L"
    cfg["res"] = "ne4_ne4"

    cfg["callsitefile"] = "micro_mg_cam.F90"
    cfg["callsitedir"] = os.path.join(cfg["e3smdir"], "components",
                        "cam", "src", "physics", "cam")
    cfg["srcmodpath"] = os.path.join(here, "res", cfg["callsitefile"])
    cfg["callsitepath"] = os.path.join(cfg["callsitedir"], cfg["callsitefile"])

    cfg["kerneldir"] = os.path.join(cfg["outdir"], "kernel")
    cfg["testdatapath"] = os.path.join(cfg["kerneldir"], "mg20.0.0.1")

    if not os.path.isdir(cfg["workdir"]):
        os.makedirs(cfg["workdir"])

    return cfg


def download_e3sm(cfg):

    if os.path.isdir(cfg["e3smdir"]):
        # check if valid
        if not os.path.isfile(cfg["callsitepath"]):
            ret, fwds = prj.run_command("-- shell 'git reset --hard'", cwd=cfg["e3smdir"])
            assert ret == 0
    else:
        ret, fwds = prj.run_command("-- shell '%s'" % cfg["gitclone"], cwd=cfg["workdir"])
        assert ret == 0


def create_e3smcam_case(cfg):

    script = "{scriptdir}/create_newcase"
    opt = "--case {casedir} --compset {compset} --res {res}"
    cmd = "-- shell '%s %s'" % (script, opt)

    if not os.path.isdir(cfg["casedir"]):
        ret, fwds = prj.run_command(cmd.format(**cfg) , cwd=cfg["workdir"])
        assert ret == 0

    cmd = "-- shell './case.setup'"
    ret, fwds = prj.run_command(cmd.format(**cfg) , cwd=cfg["casedir"])
    assert ret == 0


def extract_kernel(cfg):

    opts = "-o '{outdir}' --srcmod '{srcmodpath}'"
    cmd = "-- cam '{casedir}' '{callsitepath}' " + opts

    if (not os.path.isdir(cfg["kerneldir"]) or
        not os.path.isfile(cfg["testdatapath"])):
        ret, fwds = prj.run_command(cmd.format(**cfg), cwd=cfg["workdir"])
        assert ret == 0


def check_kernel(cfg):

    assert os.path.isfile(cfg["testdatapath"])

    cmd = "-- shell 'make''"
    ret, fwds = prj.run_command(cmd.format(**cfg), cwd=cfg["kerneldir"])

    assert ret == 0
    if fwds["stderr"]:
        print("STDERR")
        print(fwds["stderr"])

    cmd = "-- shell './kernel.exe'"
    ret, fwds = prj.run_command(cmd.format(**cfg), cwd=cfg["kerneldir"])

    assert ret == 0
    assert not fwds["stderr"]
    assert b"PASSED verification" in fwds["stdout"]

    shutil.rmtree(cfg["workdir"])


def test_cam(capsys):

    # check system
    cfg = get_test_configuration()

    # download e3sm
    download_e3sm(cfg)

    # create a case
    create_e3smcam_case(cfg)

    # extract a kernel
    extract_kernel(cfg)

    # check a kernel
    check_kernel(cfg)
