from libpyvinyl.BaseCalculator import CalculatorParameters as Parameters


import sys

sys.path.insert(0, '../tests/')
from Shadow3Calculator import Shadow3Calculator


calculator  = Shadow3Calculator("")

# ### Setup the parameters
calculator.setParams()

### Run the backengine

calculator.backengine()

### Look at the data and store as hdf5
# calculator.data
# calculator.saveH5(calculator.output_path)

### Save the parameters to a human readable json file.
calculator.parameters.to_json("my_parameters.json")

### Save calculator to binary dump.
# dumpfile = calculator.dump()

########################################################################################################################

### Load back parameters

new_parameters = Parameters.from_json("my_parameters.json")

new_parameters["NPOINT"] = 10000

print('NPOINT:', new_parameters['NPOINT'])

new_calculator  = Shadow3Calculator("", output_path="out.h5")

new_calculator.setParams(native=new_parameters)

new_calculator.backengine()

new_calculator.saveH5("tmp.h5")


