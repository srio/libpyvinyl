from libpyvinyl.BaseCalculator import CalculatorParameters as Parameters


import sys

sys.path.insert(0, '../tests/')
from Shadow3Calculator import Shadow3Calculator


calculator  = Shadow3Calculator("")

# ### Setup the parameters
calculator.setParams(number_of_optical_elements=1)

print(">>>>>DEFAULTS: ", calculator.parameters, "\n\n\n")

calculator.parameters["oe0.FDISTR"].value = 3
calculator.parameters["oe0.F_COLOR"].value = 3
calculator.parameters["oe0.F_PHOT"].value = 0
calculator.parameters["oe0.HDIV1"].value = 0.0
calculator.parameters["oe0.HDIV2"].value = 0.0
calculator.parameters["oe0.NPOINT"].value = 10000
calculator.parameters["oe0.PH1"].value = 8799.999
calculator.parameters["oe0.PH2"].value = 8799.999
calculator.parameters["oe0.SIGDIX"].value = 4.728541797631135e-06
calculator.parameters["oe0.SIGDIZ"].value = 4.095010077148124e-06
calculator.parameters["oe0.SIGMAX"].value = 0.0015810951361940363
calculator.parameters["oe0.SIGMAZ"].value = 0.0006681031579752021
calculator.parameters["oe0.VDIV1"].value = 0.0
calculator.parameters["oe0.VDIV2"].value = 0.0

calculator.parameters["oe1.DUMMY"].value = 1.0
calculator.parameters["oe1.FMIRR"].value = 3
calculator.parameters["oe1.FWRITE"].value = 1
calculator.parameters["oe1.T_IMAGE"].value = 1000.0
calculator.parameters["oe1.T_INCIDENCE"].value = 89.828
calculator.parameters["oe1.T_REFLECTION"].value = 89.828
calculator.parameters["oe1.T_SOURCE"].value = 4000.0


### Run the backengine

calculator.backengine()

import Shadow
Shadow.ShadowTools.plotxy(calculator.data, 1, 3, nbins=101, nolost=1, title="Real space")

### Look at the data and store as hdf5
print(calculator.data)
calculator.saveH5("tmp.h5")



if False: # errors here!!!!

    ### Save the parameters to a human readable json file.
    print(calculator.parameters["oe1.CCC"])
    calculator.parameters.to_json("my_parameters.json")

    ### Save calculator to binary dump.
    # dumpfile = calculator.dump()

    ########################################################################################################################

    ### Load back parameters

    new_parameters = Parameters.from_json("my_parameters.json")

    new_parameters["oe0.NPOINT"] = 10000

    print('oe0.NPOINT:', new_parameters['oe0.NPOINT'])

    new_calculator  = Shadow3Calculator("", output_path="out.h5")

    new_calculator.setParams(native=new_parameters)

    new_calculator.backengine()

    new_calculator.saveH5("tmp.h5")


