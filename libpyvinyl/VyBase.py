
class VyBaseParameters(dict): # I inheritate from dict, I find this can useful but it can be changed...

    def __init__(self):
        pass

    def to_json(self, **kwargs):
        raise NotImplementedError()

    def from_json(self, **kwargs):
        raise NotImplementedError()

    def to_h5(self, **kwargs):
        raise NotImplementedError()

    def from_h5(self, **kwargs):
        raise NotImplementedError()

    def is_valid(self):
        raise NotImplementedError()


class VyBaseData(object):

    def __init__(self):
        pass

    def to_h5(self, **kwargs):
        raise NotImplementedError()

    def from_h5(self, **kwargs):
        raise NotImplementedError()

    def is_valid(self):
        raise NotImplementedError()


class VyBaseCalculator(object):

    def __init__(self, parameters, data):
        self._parameters = parameters
        self._data = data

    def dump(self, **kwargs):
        raise NotImplementedError()

    def load_dump(self, **kwargs):
        raise NotImplementedError()

    def backengine(self, **kwargs):  # better run() ?
        raise NotImplementedError()

    def is_valid(self):
        if isinstance(self._parameters, VyBaseParameters) and isinstance(self._data,VyBaseData):
            return True
        else:
            return False

    def get_parameters(self):
        return self._parameters

    def set_parameters(self, parameters):
            self._parameters = parameters

    def get_data(self):
        return self._data

    def set_data(self, data):
        self._data = data
