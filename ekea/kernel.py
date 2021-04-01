"""EKea Kernel"""

from microapp import App

class E3smKernel(App):
    """Base E3sm Kernel"""

    def __new__(cls, *vargs, **kwargs):

        obj = super(E3smKernel, cls).__new__(cls, *vargs, **kwargs)

        obj.add_argument("casedir", metavar="casedir", help="E3SM case directory")
        obj.add_argument("callsite", metavar="callsite", help="KGen callsite Fortran source file")
        obj.add_argument("-o", "--outdir", type=str, help="output directory")

        obj.register_forward("data", help="json object")

        return obj

    def perform(self, args):


        fwds = self.extract(args)

