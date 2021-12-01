# from libpyvinyl.BaseCalculator import CalculatorParameters as Parameters
# import numpy
#
# cal_par = Parameters()
#
# cal_par.new_parameter("tmp")
# cal_par["tmp"] = 0
#
# cal_par.new_parameter("tmp_array")
# cal_par["tmp_array"] = [0, 1., 2]
#
# cal_par.new_parameter("tmp_ndarray")
# cal_par["tmp_ndarray"] = numpy.array([0, 1., 2])
#
#
# print(cal_par)
# try:
#     cal_par.to_json("tmp.json")
# except:
#     from json_tricks import dump, load
#
#     with open("tmp.json", 'w') as fp:
#         dump(cal_par.to_dict(), fp, indent=4)
#
#
# a = load("tmp.json")
# print(a["tmp_array"]["value"])
# print(a["tmp_ndarray"]["value"])

from libpyvinyl.BaseCalculator import CalculatorParameters as Parameters
import numpy
from json_tricks import dump, load

try:

    cal_par = Parameters()

    cal_par.new_parameter("tmp_ndarray")
    cal_par["tmp_ndarray"] = numpy.array([0, 1., 2])

    cal_par.to_json("tmp.json")

except:
    cal_par = Parameters()

    cal_par.new_parameter("tmp_ndarray")
    cal_par["tmp_ndarray"] = numpy.array([0, 1., 2])

    # cal_par.to_json("tmp.json")
    with open("tmp.json", 'w') as fp:
        dump(cal_par.to_dict(), fp, indent=4)

    a = load("tmp.json")
    print(a["tmp_ndarray"]["value"])