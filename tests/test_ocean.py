import os, shutil

from ekea import E3smKea

here = os.path.dirname(os.path.abspath(__file__))
is_summit = len([k for k in os.environ.keys() if k.startswith("OLCF_")]) > 3

prj = E3smKea()

def get_test_configuration():

    cfg = {}

    if is_summit:
        cfg["scratchdir"] = "/gpfs/alpine/cli115/scratch/grnydawn"
        cfg["createcase"] = "ne4_ne4"

    else:
        print("Not supported system")
        assert False

    cfg["workdir"] = os.path.join(cfg["scratchdir"], "ekea_tests", "mpasocn")
    cfg["outdir"] = os.path.join(cfg["workdir"], "output")
    cfg["e3smdir"] = os.path.join(cfg["workdir"], "E3SM")
    cfg["cimedir"] = os.path.join(cfg["e3smdir"], "cime")
    cfg["scriptdir"] = os.path.join(cfg["cimedir"], "scripts")

    cfg["casedir"] = os.path.join(cfg["workdir"], "TESTCASE")
    
    cfg["gitclone"] = ("git clone -b maint-1.2 --recursive "
                        "https://github.com/E3SM-Project/E3SM.git")

    cfg["compset"] = "FC5AV1C-L"
    cfg["res"] = "ne4_ne4"
    cfg["callsitefile"] = "mpas_ocn_diagnostics.F"
    cfg["callsitepath"] = os.path.join(cfg["e3smdir"], "components",
                        "mpas-source", "src", "core_ocean", "shared",
                        cfg["callsitefile"])

    if not os.path.isdir(cfg["workdir"]):
        os.makedirs(cfg["workdir"])

    return cfg


def download_e3sm(cfg):

    if os.path.isdir(cfg["e3smdir"]):
        # check if valid
        if not os.path.isfile(cfg["callsitepath"]):
            prj.run_command("-- shell git reset --hard", workdir=cfg["e3smdir"])
            
    else:
        prj.run_command("-- shell %s" % cfg["gitclone"], workdir=cfg["workdir"])

    import pdb; pdb.set_trace()


def create_e3smocn_case(cfg):

    script = "{scriptdir}/create_newcase"
    opt = "--case {casedir} --compset {compset} --res {res}"
    cmd = "-- shell %s %s" % (script, opt)

    prj.run_command(cmd.format(**cfg) , workdir=cfg["workdir"])


def extract_kernel(cfg):

    opts = "-o '{outdir}' --replace '{orgfile}:{newfile}'"
    cmd = "-- mpasocn '{casedir}' '{callsitepath}' " + opts

    ret, fwds = prj.run_command(cmd.format(**cfg), workdir=cfg["workdir"])

    assert ret == 0


def check_kernel(cfg):

    assert os.path.isfile(os.path.join(cfg["kerneldir"], "ocn_diagnostic_solve_part1.0.0.1"))

    cmd = "-- shell make --workdir '{kerneldir}'"
    ret, fwds = prj.run_command(cmd.format(**cfg), workdir=cfg["workdir"])

    assert ret == 0
    if fwds["stderr"]:
        print("STDERR")
        print(fwds["stderr"])

    cmd = "-- shell ./kernel.exe --workdir '{kerneldir}'"
    ret, fwds = prj.run_command(cmd.format(**cfg), workdir=cfg["workdir"])

    assert ret == 0
    assert not fwds["stderr"]
    assert b"PASSED verification" in fwds["stdout"]

    shutil.rmtree(cfg["workdir"])


def test_ocean(capsys):

    # check system
    cfg = get_test_configuration()

    # download e3sm
    download_e3sm(cfg)

    # create a case
    create_e3smocn_case(cfg)

    # extract a kernel
    extract_kernel(cfg)

    # check a kernel
    check_kernel(cfg)
