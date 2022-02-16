import os, subprocess, json, shutil
from microapp import App, appdict
from ekea.utils import xmlquery

here = os.path.dirname(os.path.abspath(__file__))

class MixedPrec(App):
    _name_ = "mixedprec"
    _version_ = "0.1.0"

    def __init__(self, mgr):

        self.add_argument("analysis", metavar="casedir", help="E3SM Abstract Syntax Tree")
        self.add_argument("-o", "--outdir", type=str, help="output directory")

        self.register_forward("data", help="json object")

    def perform(self, args):
        pass

