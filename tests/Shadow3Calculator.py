from libpyvinyl.BaseCalculator import BaseCalculator, CalculatorParameters
import Shadow
import inspect

class Shadow3Calculator(BaseCalculator):
    def __init__(self,
                 name,
                 parameters=None,
                 dumpfile=None,
                 input_path=None,
                 output_path=None):

        super().__init__(name,
                         parameters=parameters,
                         dumpfile=dumpfile,
                         output_path=output_path)

        self.number_of_optical_elements = 0

    def setParams(self,
            source=None,
            beamline=[],
            number_of_optical_elements = 0,
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
            self.parameters.new_parameter("oe0."+key)
            if isinstance(oe0_dict[key], bytes):
                self.parameters["oe0."+key].set_value(oe0_dict[key].decode("utf-8"))
            else:
                self.parameters["oe0."+key].set_value(oe0_dict[key])

        # beamline
        if len(beamline) == 0 and number_of_optical_elements > 0:
            beamline = [Shadow.OE()] * number_of_optical_elements

        for i in range(len(beamline)):
            if isinstance(beamline[i], Shadow.OE):
                oe_i = beamline[i]
            else:
                oe_i = Shadow.OE()

            oe_i_dict = oe_i.to_dictionary()

            if not isinstance(self.parameters, CalculatorParameters):
                self.parameters = CalculatorParameters()

            for key in oe_i_dict.keys():
                self.parameters.new_parameter("oe%d.%s" % (i+1, key))
                if isinstance(oe_i_dict[key], bytes):
                    self.parameters["oe%d.%s" % (i+1, key)].set_value(oe_i_dict[key].decode("utf-8"))
                else:
                    self.parameters["oe%d.%s" % (i+1, key)].set_value(oe_i_dict[key])

        self.number_of_optical_elements = number_of_optical_elements

    def __get_valiable_list(self, object1):
        """
        returns a list of the Shadow.Source or Shadow.OE variables
        """
        mem = inspect.getmembers(object1)
        mylist = []
        for i,var in enumerate(mem):
            if var[0].isupper():
                mylist.append(var[0])
        return(mylist)

    def backengine(self):
        beam = Shadow.Beam()
        oe0 = Shadow.Source()


        oe0_list = self.__get_valiable_list(oe0)

        for name in oe0_list:
            try:
                value = self.parameters["oe0."+name].value
                if isinstance(value, str):
                    value = bytes(value, 'UTF-8')
                setattr(oe0, name, value)
            except:
                raise Exception("Error setting parameters name %s" % name)


        beam.genSource(oe0)

        if self.number_of_optical_elements > 0:
            oei_list = self.__get_valiable_list(Shadow.OE())
            for i in range(self.number_of_optical_elements):
                oe_i = Shadow.OE()
                for name in oei_list:
                    try:
                        value = self.parameters["oe%d.%s" % (i+1, name)].value
                        if isinstance(value, str):
                            value = bytes(value, 'UTF-8')
                        setattr(oe_i, name, value)
                    except:
                        raise Exception("Error setting parameters name %s" % name)

                beam.traceOE(oe_i, i+1)

        self._set_data(beam)
        return 0


    def dump(self,filename="star.01"): # overwritten method
        self.data.write(filename)

    def saveH5(self, filename="tmp.h5", openpmd=False):
        from orangecontrib.panosc.shadow.util.openPMD import saveShadowToHDF
        saveShadowToHDF(self.data, filename=filename)

