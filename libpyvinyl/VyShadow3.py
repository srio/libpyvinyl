from VyBase import VyBaseData, VyBaseParameters, VyBaseCalculator
import Shadow

class VyS3Parameters(VyBaseParameters):

    def __init__(self, source=None, optical_elements=None):
        super().__init__()
        _source = source
        _optical_elements = optical_elements

    def to_json(self, **kwargs):
        raise NotImplementedError()

    def to_h5(self, **kwargs):
        raise NotImplementedError()

    def is_valid(self):
        if isinstance(self._source, Shadow.Source) and isinstance(self._optical_elements, list):
            return True
        else:
            return False


class VyS3Data(VyBaseData, Shadow.Beam):

    def __init__(self):
        VyBaseData.__init__()
        Shadow.Beam.__init__()

    def to_h5(self, **kwargs):
        raise NotImplementedError()

    def is_valid(self):
        raise NotImplementedError()


class VyS3Calculator(VyBaseCalculator):

    def __init__(self,
        parameters = None,
        data = None):

        super().__init__()

    def setParams(self,
                  source=None,
                  beamline=[],
                  native=None,
                  ):

        # native format from json
        if native is not None:
            self.parameters = native
            return

        # source
        if isinstance(source, Shadow.Source):
            oe0 = source
        else:
            oe0 = Shadow.Source()

        oe0_dict = oe0.to_dictionary()

        if not isinstance(self.parameters, CalculatorParameters):
            self.parameters = CalculatorParameters()

        for key in oe0_dict.keys():
            print(key, oe0_dict[key])
            self.parameters.new_parameter(key)
            if isinstance(oe0_dict[key], bytes):
                self.parameters[key].set_value(oe0_dict[key].decode("utf-8"))
            else:
                self.parameters[key].set_value(oe0_dict[key])

        # beamline TODO!

    def backengine(self):
        beam = Shadow.Beam()
        oe0 = Shadow.Source()

        oe0.FDISTR = self.parameters["FDISTR"].value
        oe0.FGRID = self.parameters["FGRID"].value
        oe0.FSOUR = self.parameters["FSOUR"].value
        oe0.FSOURCE_DEPTH = self.parameters["FSOURCE_DEPTH"].value
        oe0.F_COHER = self.parameters["F_COHER"].value
        oe0.F_COLOR = self.parameters["F_COLOR"].value
        oe0.F_PHOT = self.parameters["F_PHOT"].value
        oe0.F_POL = self.parameters["F_POL"].value
        oe0.F_POLAR = self.parameters["F_POLAR"].value
        oe0.F_OPD = self.parameters["F_OPD"].value
        oe0.F_WIGGLER = self.parameters["F_WIGGLER"].value
        oe0.F_BOUND_SOUR = self.parameters["F_BOUND_SOUR"].value
        oe0.F_SR_TYPE = self.parameters["F_SR_TYPE"].value
        oe0.ISTAR1 = self.parameters["ISTAR1"].value
        oe0.NPOINT = self.parameters["NPOINT"].value
        oe0.NCOL = self.parameters["NCOL"].value
        oe0.N_CIRCLE = self.parameters["N_CIRCLE"].value
        oe0.N_COLOR = self.parameters["N_COLOR"].value
        oe0.N_CONE = self.parameters["N_CONE"].value
        oe0.IDO_VX = self.parameters["IDO_VX"].value
        oe0.IDO_VZ = self.parameters["IDO_VZ"].value
        oe0.IDO_X_S = self.parameters["IDO_X_S"].value
        oe0.IDO_Y_S = self.parameters["IDO_Y_S"].value
        oe0.IDO_Z_S = self.parameters["IDO_Z_S"].value
        oe0.IDO_XL = self.parameters["IDO_XL"].value
        oe0.IDO_XN = self.parameters["IDO_XN"].value
        oe0.IDO_ZL = self.parameters["IDO_ZL"].value
        oe0.IDO_ZN = self.parameters["IDO_ZN"].value
        oe0.SIGXL1 = self.parameters["SIGXL1"].value
        oe0.SIGXL2 = self.parameters["SIGXL2"].value
        oe0.SIGXL3 = self.parameters["SIGXL3"].value
        oe0.SIGXL4 = self.parameters["SIGXL4"].value
        oe0.SIGXL5 = self.parameters["SIGXL5"].value
        oe0.SIGXL6 = self.parameters["SIGXL6"].value
        oe0.SIGXL7 = self.parameters["SIGXL7"].value
        oe0.SIGXL8 = self.parameters["SIGXL8"].value
        oe0.SIGXL9 = self.parameters["SIGXL9"].value
        oe0.SIGXL10 = self.parameters["SIGXL10"].value
        oe0.SIGZL1 = self.parameters["SIGZL1"].value
        oe0.SIGZL2 = self.parameters["SIGZL2"].value
        oe0.SIGZL3 = self.parameters["SIGZL3"].value
        oe0.SIGZL4 = self.parameters["SIGZL4"].value
        oe0.SIGZL5 = self.parameters["SIGZL5"].value
        oe0.SIGZL6 = self.parameters["SIGZL6"].value
        oe0.SIGZL7 = self.parameters["SIGZL7"].value
        oe0.SIGZL8 = self.parameters["SIGZL8"].value
        oe0.SIGZL9 = self.parameters["SIGZL9"].value
        oe0.SIGZL10 = self.parameters["SIGZL10"].value
        oe0.CONV_FACT = self.parameters["CONV_FACT"].value
        oe0.CONE_MAX = self.parameters["CONE_MAX"].value
        oe0.CONE_MIN = self.parameters["CONE_MIN"].value
        oe0.EPSI_DX = self.parameters["EPSI_DX"].value
        oe0.EPSI_DZ = self.parameters["EPSI_DZ"].value
        oe0.EPSI_X = self.parameters["EPSI_X"].value
        oe0.EPSI_Z = self.parameters["EPSI_Z"].value
        oe0.HDIV1 = self.parameters["HDIV1"].value
        oe0.HDIV2 = self.parameters["HDIV2"].value
        oe0.PH1 = self.parameters["PH1"].value
        oe0.PH2 = self.parameters["PH2"].value
        oe0.PH3 = self.parameters["PH3"].value
        oe0.PH4 = self.parameters["PH4"].value
        oe0.PH5 = self.parameters["PH5"].value
        oe0.PH6 = self.parameters["PH6"].value
        oe0.PH7 = self.parameters["PH7"].value
        oe0.PH8 = self.parameters["PH8"].value
        oe0.PH9 = self.parameters["PH9"].value
        oe0.PH10 = self.parameters["PH10"].value
        oe0.RL1 = self.parameters["RL1"].value
        oe0.RL2 = self.parameters["RL2"].value
        oe0.RL3 = self.parameters["RL3"].value
        oe0.RL4 = self.parameters["RL4"].value
        oe0.RL5 = self.parameters["RL5"].value
        oe0.RL6 = self.parameters["RL6"].value
        oe0.RL7 = self.parameters["RL7"].value
        oe0.RL8 = self.parameters["RL8"].value
        oe0.RL9 = self.parameters["RL9"].value
        oe0.RL10 = self.parameters["RL10"].value
        oe0.BENER = self.parameters["BENER"].value
        oe0.POL_ANGLE = self.parameters["POL_ANGLE"].value
        oe0.POL_DEG = self.parameters["POL_DEG"].value
        oe0.R_ALADDIN = self.parameters["R_ALADDIN"].value
        oe0.R_MAGNET = self.parameters["R_MAGNET"].value
        oe0.SIGDIX = self.parameters["SIGDIX"].value
        oe0.SIGDIZ = self.parameters["SIGDIZ"].value
        oe0.SIGMAX = self.parameters["SIGMAX"].value
        oe0.SIGMAY = self.parameters["SIGMAY"].value
        oe0.SIGMAZ = self.parameters["SIGMAZ"].value
        oe0.VDIV1 = self.parameters["VDIV1"].value
        oe0.VDIV2 = self.parameters["VDIV2"].value
        oe0.WXSOU = self.parameters["WXSOU"].value
        oe0.WYSOU = self.parameters["WYSOU"].value
        oe0.WZSOU = self.parameters["WZSOU"].value
        oe0.PLASMA_ANGLE = self.parameters["PLASMA_ANGLE"].value
        oe0.FILE_TRAJ = bytes(self.parameters["FILE_TRAJ"].value, 'UTF-8')
        oe0.FILE_SOURCE = bytes(self.parameters["FILE_SOURCE"].value, 'UTF-8')
        oe0.FILE_BOUND = bytes(self.parameters["FILE_BOUND"].value, 'UTF-8')
        oe0.OE_NUMBER = self.parameters["OE_NUMBER"].value
        oe0.NTOTALPOINT = self.parameters["NTOTALPOINT"].value
        oe0.IDUMMY = self.parameters["IDUMMY"].value
        oe0.DUMMY = self.parameters["DUMMY"].value
        oe0.F_NEW = self.parameters["F_NEW"].value

        beam.genSource(oe0)

        self._set_data(beam)
        return 0

    def dump(self):  # overwritten method
        self.data.write("begin.dat")

    def saveH5(self, filename="tmp.h5", openpmd=False):
        from orangecontrib.panosc.shadow.util.openPMD import saveShadowToHDF
        saveShadowToHDF(self.data, filename=filename)

    def is_valid(self):
        raise NotImplementedError()

    def dump(self, **kwargs):
        raise NotImplementedError()

    def backengine(self):
        raise NotImplementedError()




