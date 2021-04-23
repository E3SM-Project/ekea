import os, shutil

from ekea import E3smKea

here = os.path.dirname(os.path.abspath(__file__))
is_summit = len([k for k in os.environ.keys() if k.startswith("OLCF_")]) > 3

prj = E3smKea()

def get_test_configuration():

    cfg = {}

    cfg["e3sm_commit"] = "c5671da3cf54d99a5fa5e1d022263fbb913b25e1"

    if is_summit:
        #cfg["testcase"] = "SMS.f09_g16.X"
        #cfg["testcase"] = "ERS.f19_g16_rx1.A"
        cfg["testcase"] = "ERS_Ld5.T62_oQU120.CMPASO-NYF"
        cfg["testid"] = "ekeatest"
        cfg["scratchdir"] = "/gpfs/alpine/cli115/scratch/grnydawn"
        cfg["workdir"] = os.path.join(cfg["scratchdir"], "ekea_tests", "eam")
        cfg["casedir"] = os.path.join(cfg["workdir"],
            "{testcase}.summit_ibm.{testid}".format(**cfg))

    else:
        print("Not supported system")
        assert False

    cfg["outdir"] = os.path.join(cfg["workdir"], "output")
    cfg["e3smdir"] = os.path.join(cfg["workdir"], "E3SM")
    cfg["cimedir"] = os.path.join(cfg["e3smdir"], "cime")
    cfg["scriptdir"] = os.path.join(cfg["cimedir"], "scripts")

    #cfg["casedir"] = os.path.join(cfg["workdir"], "TESTCASE")
    
    #cfg["gitclone"] = ("git clone -b maint-1.2 --recursive "
    cfg["gitclone"] = ("git clone --recursive "
                        "https://github.com/E3SM-Project/E3SM.git")

    cfg["compset"] = "FC5AV1C-L"
    cfg["res"] = "ne4_ne4"

    cfg["callsitefile"] = "micro_mg_cam.F90"
    cfg["callsiteorgdir"] = os.path.join(cfg["e3smdir"], "components",
                        "eam", "src", "physics", "cam")
    #cfg["srcmodpath"] = os.path.join(here, "res", cfg["callsitefile"])
    cfg["callsiteorgpath"] = os.path.join(cfg["callsiteorgdir"], cfg["callsitefile"])
    #cfg["callsitemoddir"] = os.path.join(cfg["casedir"], "SourceMods", "src.eam")
    #cfg["callsitemodpath"] = os.path.join(cfg["callsitemoddir"], cfg["callsitefile"])
    cfg["callsitenewpath"] = os.path.join(here, "res", cfg["callsitefile"])

    cfg["kerneldir"] = os.path.join(cfg["outdir"], "kernel")
    cfg["testdatapath"] = os.path.join(cfg["kerneldir"], "mg20.0.0.1")

    if not os.path.isdir(cfg["workdir"]):
        os.makedirs(cfg["workdir"])

    print("Testing is configured.")

    return cfg


def download_e3sm(cfg):

    if os.path.isdir(cfg["e3smdir"]):
        # check if valid
        if not os.path.isfile(cfg["callsiteorgpath"]):
            ret, fwds = prj.run_command("-- shell 'git reset --hard'", workdir=cfg["e3smdir"])
            assert ret == 0
    else:
        ret, fwds = prj.run_command("-- shell '%s'" % cfg["gitclone"], workdir=cfg["workdir"])
        assert ret == 0

    ret, fwds = prj.run_command("-- shell 'git checkout %s'" % cfg["e3sm_commit"], workdir=cfg["e3smdir"])
    assert ret == 0

    # to workaround parser bug to sqaure bracket array constructor
    for patch in ["micro_mg_utils.F90"]:
        shutil.copy(os.path.join(here, "res", patch), cfg["callsiteorgdir"])

    print("E3SM code is ready.")


def create_e3smeam_case(cfg):

#./create_test SMS.f09_g16.X
#--test-root TEST_ROOT
#--wait
#--no-setup

    script = "{scriptdir}/create_test"
    opt = "{testcase} --test-root {workdir} --no-setup --test-id {testid} --project cli115"
#    script = "{scriptdir}/create_newcase"
#    opt = "--case {casedir} --compset {compset} --res {res}"
    cmd = "-- shell '%s %s'" % (script, opt)

    if not os.path.isdir(cfg["casedir"]):
        ret, fwds = prj.run_command(cmd.format(**cfg) , workdir=cfg["workdir"])
        assert ret == 0

    cmd = "-- shell './case.setup'"
    ret, fwds = prj.run_command(cmd.format(**cfg) , workdir=cfg["casedir"])
    assert ret == 0

    #shutil.copy(cfg["callsitenewpath"], cfg["callsitemodpath"])
    shutil.copy(cfg["callsitenewpath"], cfg["callsiteorgpath"])

    print("A E3SM case is created.")


def extract_kernel(cfg):

    #opts = "-o '{outdir}' --srcmod '{callsitemodpath}'"
    opts = "-o '{outdir}'"
    #cmd = "-- eam '{casedir}' '{callsitemodpath}' " + opts
    cmd = "-- eam '{casedir}' '{callsiteorgpath}' " + opts

    if (not os.path.isdir(cfg["kerneldir"]) or
        not os.path.isfile(cfg["testdatapath"])):
        ret, fwds = prj.run_command(cmd.format(**cfg), workdir=cfg["workdir"])
        assert ret == 0

    #os.remove(cfg["callsitemodpath"])

    print("A kernel is extracted.")


def check_kernel(cfg):

    assert os.path.isfile(cfg["testdatapath"])

    cmd = "-- shell 'make''"
    ret, fwds = prj.run_command(cmd.format(**cfg), workdir=cfg["kerneldir"])

    assert ret == 0
    if fwds["stderr"]:
        print("STDERR")
        print(fwds["stderr"])

    cmd = "-- shell './kernel.exe'"
    ret, fwds = prj.run_command(cmd.format(**cfg), workdir=cfg["kerneldir"])

    assert ret == 0
    assert not fwds["stderr"]
    assert b"PASSED verification" in fwds["stdout"]

    shutil.rmtree(cfg["workdir"])

    print("A kernel is verified.")


def test_eam(capsys):

    # check system
    cfg = get_test_configuration()

    # download e3sm
    download_e3sm(cfg)

    # create a case
    create_e3smeam_case(cfg)

    # extract a kernel
    extract_kernel(cfg)

    # check a kernel
    check_kernel(cfg)
