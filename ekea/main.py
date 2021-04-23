from fortlab import Fortlab

from ekea.mpasocn import MPASOcnKernel
from ekea.cam import CamKernel
from ekea.eam import EAMKernel

class E3smKea(Fortlab):

    _name_ = "ekea"
    _version_ = "0.2.1"
    _description_ = "E3SM Fortran Kernel Extractor and Analyzer"
    _long_description_ = "E3SM Fortran Kernel Extractor and Analyzer"
    _author_ = "Youngsung Kim"
    _author_email_ = "youngsung.kim.act2@gmail.com"
    _url_ = "https://github.com/grnydawn/ekea"
    _builtin_apps_ = [MPASOcnKernel, EAMKernel, CamKernel]

    def __init__(self):
        pass
