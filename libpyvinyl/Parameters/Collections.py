import json
from .Parameter import Parameter


class Parameters:
    """
    Collection of parameters related to a single calculator

    Parameters are stored in a dict using their name as key
    """
    def __init__(self, parameters=None):
        """
        Creates a Parameters object, optionally with list of parameter objects
        """
        self.parameters = {}
        if parameters is not None:
            self.add(parameters)

    def check_type(self, parameter):
        """
        Checks given parameter is of type Parameter
        """
        if not isinstance(parameter, Parameter):
            raise RuntimeError(
                "A non-Parameter object was given to Parameters class.")

    def check_list_type(self, parameter_list):
        """
        Checks given list of parameters is a list and contains only parameter objects
        """
        if not isinstance(parameter_list, list):
            raise RuntimeError("Parameters class takes list as input.")

        for par in parameter_list:
            self.check_type(par)

    def add(self, parameter):
        """
        Adds parameters to this parameters object, either single or list
        """
        # handle case where list of parameters given
        if isinstance(parameter, list):
            self.check_list_type(parameter)
            for par in parameter:
                if par.name in self.parameters:
                    raise RuntimeError(
                        "Duplicate parameter name in parameters!")

                self.parameters[par.name] = par
            return

        # handle case where single parameter is given
        self.check_type(parameter)
        if parameter in self.parameters:
            raise RuntimeError("Duplicate parameter name in parameters!")

        self.parameters[parameter.name] = parameter

    def new_parameter(self, *args, **kwargs):
        """
        Creates a new parameter with given arguments and adds to this Parameters object
        """
        new_parameter = Parameter(*args, **kwargs)
        self.add(new_parameter)

    def __getitem__(self, key):
        """
        Gets parameter with given name from internal dict
        """
        return self.parameters[key]

    def __setitem__(self, key, value):
        """
        Sets value of parameter with given key to given value
        """
        self.parameters[key].set_value(value)

    def __delitem__(self, key):
        """
        Deletes parameter with given key
        """
        del self.parameters[key]

    def print_indented(self, indents):
        """
        returns string describing this object, can optionally be indented
        """
        string = indents * " " + " - Parameters object -\n"
        for key in self.parameters:
            string += indents * " " + self.parameters[key].print_line() + "\n"

        return string

    def __repr__(self):
        return self.print_indented(0)

    @classmethod
    def from_json(cls, fname: str):
        """
        Initialize an instance from a json file.

        :param fname: The filename (path) of the json file.
        :type  fname: str

        """
        with open(fname, 'r') as fp:
            instance = cls.from_dict(json.load(fp))

        return instance

    @classmethod
    def from_dict(cls, params_dict: dict):
        """
        Initialize an instance from a dict.

        :param fname: The filename (path) of the json file.
        :type  fname: str

        """
        parameters = cls()
        for key in params_dict:
            parameters.add(Parameter.from_dict(params_dict[key]))

        return parameters

    def to_dict(self):
        params = {}
        for key in self.parameters:
            params[key] = self.parameters[key].__dict__
        return params

    def to_json(self, fname: str):
        """
        Save this parameters class to a human readable json file.

        :param fname: Write to this file.
        :type  fname: str

        """
        with open(fname, 'w') as fp:
            json.dump(self.to_dict(), fp, indent=4)


class MasterParameter(Parameter):
    """
    The master parameters need to affect multiple Parameters objects, and for
    this reason it is expanded on the basis of the Parameter class. A link
    system is added that contains information on which Parameters objects this
    master parameter should control parameters from.
    """
    def __init__(self, *args, **kwargs):
        """
        Create MasterParameter with uninitialized links
        """
        self.links = None
        super().__init__(*args, **kwargs)

    def add_links(self, links):
        """
        Links is a dict with key being reference to calculator and name of parameter to overwrite
        """
        self.links = links


class MasterParameters(Parameters):
    """
    Master Parameters object that contain all master parameters with the
    additional ability to set values for the other parameters this master
    should control.
    """
    def __init__(self, parameters_dict, *args, **kwargs):
        """
        Create MasterParameters object with given parameters dict

        The parameters_dict contains all the Parameters objects in the
        ParametersCollection, and provides the access for the master parameters
        so they can control the other Parameters objects of which they are
        responsible.
        """
        self.parameters_dict = parameters_dict
        super().__init__(*args, **kwargs)

    def __setitem__(self, key, value):
        """
        Set item that propagates change throughout all links
        """
        master_parameter = self.parameters[key]

        if master_parameter.links is not None:
            for calculator in master_parameter.links:
                calculator_par_name = master_parameter.links[calculator]
                self.parameters_dict[calculator][calculator_par_name] = value

        self.parameters[key].set_value(value)


class ParametersCollection:
    """
    Object intended for use as instrument parameters

    This object holds Parameters objects for a number of calculators and can
    have master parameters which control parameters for a number of
    calculators at once.
    """
    def __init__(self):
        """
        Create an empty ParametersCollection instance
        """
        self.parameters_dict = {}
        self.master = MasterParameters(self.parameters_dict)

    def to_dict(self):
        params_collect = {}
        for key in self.parameters_dict:
            params_collect[key] = self.parameters_dict[key].to_dict()
        return params_collect

    def to_json(self, fname: str):
        """
        Save this parameters class to a human readable json file.

        :param fname: Write to this file.
        :type  fname: str

        """
        with open(fname, 'w') as fp:
            json.dump(self.to_dict(), fp, indent=4)

    def add(self, key, parameters):
        """
        Here key could be a calculator object or a reference to such an object, like its name
        """
        if not isinstance(parameters, Parameters):
            raise RuntimeError(
                "ParametersCollection holds objects of type Parameters,"
                + " was provided with something else.")

        self.parameters_dict[key] = parameters

    def add_master_parameter(self, name, links, **kwargs):
        """
        link: dict with keys and parameters for which this parameter should override
        """
        master_parameter = MasterParameter(name, **kwargs)
        # Check the link keys correspond to keys in parameters_dict
        if not isinstance(links, dict):
            raise RuntimeError("links should be a dict")

        for link_key in links:
            if link_key not in self.parameters_dict:
                raise RuntimeError(
                    "A link had a key which was not recognized.")

        master_parameter.add_links(links)
        self.master.add(master_parameter)

    def __getitem__(self, key):
        """
        Provides access to parameters of calculator with given name
        """
        return self.parameters_dict[key]

    def __delitem__(self, key):
        """
        Allows deletion of parameters of calculator with given name
        """
        del self.parameters_dict[key]

    def __repr__(self):
        """
        Prints overview of state of this ParametersCollection object
        """
        string = "- ParametersCollection object -\n"

        if len(self.master.parameters) > 0:
            string += "  Master Parameters\n"
        for key in self.master.parameters:
            string += "  " + self.master.parameters[key].print_line() + "\n"

        string += "\n"
        for key in self.parameters_dict:
            string += 3 * " " + str(key) + "\n"
            string += self.parameters_dict[key].print_indented(3)
            string += "\n"

        return string
