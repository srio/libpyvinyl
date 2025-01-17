"""
:module BaseCalculator: Module hosting the BaseCalculator and Parameters classes.

"""

####################################################################################
#                                                                                  #
# This file is part of libpyvinyl - The APIs for Virtual Neutron and x-raY            #
# Laboratory.                                                                      #
#                                                                                  #
# Copyright (C) 2020  Carsten Fortmann-Grote                                       #
#                                                                                  #
# This program is free software: you can redistribute it and/or modify it under    #
# the terms of the GNU Lesser General Public License as published by the Free      #
# Software Foundation, either version 3 of the License, or (at your option) any    #
# later version.                                                                   #
#                                                                                  #
# This program is distributed in the hope that it will be useful, but WITHOUT ANY  #
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A  #
# PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details. #
#                                                                                  #
# You should have received a copy of the GNU Lesser General Public License along   #
# with this program.  If not, see <https://www.gnu.org/licenses/                   #
#                                                                                  #
####################################################################################

from abc import abstractmethod
from libpyvinyl.AbstractBaseClass import AbstractBaseClass
from libpyvinyl.Parameters import CalculatorParameters
from tempfile import mkstemp
import copy
import dill
import h5py
import sys
import logging
import numpy
import os

logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s',
                    level=logging.WARNING)


class BaseCalculator(AbstractBaseClass):
    """

    :class BaseCalculator: Base class of all calculators.

    This class is provides the libpyvinyl API. It defines all methods
    through which a user interacts with the simulation backengines.

    This class is to be used as a base class for all calculators that implement
    a special simulation module, such as a photon diffraction calculator. Such a
    specialized Calculator than has the same interface to the simulation
    backengine as all other ViNyL Calculators.

    """
    @abstractmethod
    def __init__(self, name: str, parameters=None, dumpfile=None, **kwargs):
        """

        :param name: The name for this calculator.
        :type  name: str

        :param parameters: The parameters for this calculator.
        :type  parameters: Parameters

        :param dumpfile: If given, load a previously dumped (aka pickled) calculator.

        :param kwargs: (key, value) pairs of further arguments to the calculator, e.g input_path, output_path.

        If both 'parameters' and 'dumpfile' are given, the dumpfile is loaded
        first. Passing a parameters object may be used to update some
        parameters.

        Example:
        ```
        # Define a specialized calculator.
        class MyCalculator(BaseCalculator):

            def __init__(self, parameters=None, dumpfile=None, **kwargs):
                super()__init__(parameters, dumpfile, **kwargs)

            def backengine(self):
                os.system("my_simulation_backengine_call")

            def saveH5(self):
                # Format output into openpmd hdf5 format.

        class MyParameters(Parameters):
            pass

        my_calculator = MyCalculator(my_parameters)

        my_calculator.backengine()

        my_calculator.saveH5("my_sim_output.h5")
        my_calculater.dump("my_calculator.dill")
        ```

        """

        if isinstance(name, str):
            self.name = name
        else:
            raise TypeError("name should be in str type.")
        # Set data
        self.__data = None

        if isinstance(parameters, (type(None), CalculatorParameters)):
            self.parameters = parameters
        else:
            raise TypeError(
                "parameters should be in CalculatorParameters type.")

        # Must load after setting paramters to avoid being overrode by empty parameters.
        if dumpfile is not None:
            self.__load_from_dump(dumpfile)

        if "output_path" in kwargs:
            self.output_path = kwargs["output_path"]

    def __call__(self, parameters=None, **kwargs):
        """ The copy constructor

        :param parameters: The parameters for the new calculator.
        :type  parameters: CalculatorParameters

        :param kwargs: key-value pairs of parameters to change in the new instance.

        :return: A new parameters instance with optionally changed parameters.

        """

        new = copy.deepcopy(self)

        new.__dict__.update(kwargs)

        if parameters is not None:
            new.parameters = parameters

        return new

    def __load_from_dump(self, dumpfile):
        """ """
        """
        Load a dill dump and initialize self's internals.

        """

        with open(dumpfile, 'rb') as fhandle:
            try:
                tmp = dill.load(fhandle)
            except:
                raise IOError(
                    "Cannot load calculator from {}.".format(dumpfile))

        self.__dict__ = copy.deepcopy(tmp.__dict__)

        del tmp

    @property
    def parameters(self):
        """ The parameters of this calculator. """

        return self.__parameters

    @parameters.setter
    def parameters(self, val):

        if not isinstance(val, (type(None), CalculatorParameters)):
            raise TypeError(
                """Passed argument 'parameters' has wrong type. Expected CalculatorParameters, found {}."""
                .format(type(val)))

        self.__parameters = val

    def dump(self, fname=None):
        """
        Dump class instance to file.

        :param fname: Filename (path) of the file to write.

        """

        if fname is None:
            _, fname = mkstemp(
                suffix="_dump.dill",
                prefix=self.__class__.__name__[-1],
                dir=os.getcwd(),
            )
        try:
            with open(fname, "wb") as file_handle:
                dill.dump(self, file_handle)
        except:
            raise

        return fname

    @abstractmethod
    def saveH5(self, fname: str, openpmd: bool = True):
        """ Save the simulation data to hdf5 file.

        :param fname: The filename (path) of the file to write the data to.
        :type  fname: str

        :param openpmd: Flag that controls whether the data is to be written in according to the openpmd metadata standard. Default is True.

        """

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, val):
        raise AttributeError("Attribute 'data' is read-only.")

    @abstractmethod
    def backengine(self):
        pass

    @classmethod
    def run_from_cli(cls):
        """
        Method to start calculator computations from command line.

        :return: exit with status code

        """
        if len(sys.argv) == 2:
            fname = sys.argv[1]
            calculator = cls(fname)
            status = calculator._run()
            sys.exit(status)

    def _run(self):
        """
        Method to do computations. By default starts backengine.

        :return: status code.

        """
        result = self.backengine()

        if result is None:
            result = 0

        return result

    def _set_data(self, data):
        """ """
        """ Private method to store the data on the object.

        :param data: The data to store.

        """

        self.__data = data


# Mocks for testing. Have to be here to work around bug in dill that does not
# like classes to be defined outside of __main__.
class SpecializedCalculator(BaseCalculator):
    def __init__(self, name, parameters=None, dumpfile=None, **kwargs):

        super().__init__(name, parameters, dumpfile, **kwargs)

    def setParams(self, photon_energy: float = 10, pulse_energy: float = 1e-3):
        if not isinstance(self.parameters, CalculatorParameters):
            self.parameters = CalculatorParameters()
        self.parameters.new_parameter("photon_energy",
                                      unit="eV",
                                      comment="Photon energy")
        self.parameters['photon_energy'].set_value(photon_energy)

        self.parameters.new_parameter("pulse_energy",
                                      unit="joule",
                                      comment="Pulse energy")
        self.parameters['pulse_energy'].set_value(pulse_energy)

    def backengine(self):
        self._BaseCalculator__data = numpy.random.normal(
            loc=self.parameters['photon_energy'].value,
            scale=0.001 * self.parameters['photon_energy'].value,
            size=(100, ))

        return 0

    def saveH5(self, openpmd=False):
        with h5py.File(self.output_path, "w") as h5:
            ds = h5.create_dataset("/data", data=self.data)

            h5.close()


# This project has received funding from the European Union's Horizon 2020 research and innovation programme under grant agreement No. 823852.
