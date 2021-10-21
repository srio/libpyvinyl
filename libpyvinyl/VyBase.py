class VyBaseParameters(dict):

    def __init__(self):
        pass

    def to_json(self, **kwargs):
        raise NotImplementedError()

    def to_h5(self, **kwargs):
        raise NotImplementedError()

    def is_valid(self):
        raise NotImplementedError()


class VyBaseData(dict):

    def __init__(self):
        pass

    def to_h5(self, **kwargs):
        raise NotImplementedError()

    def is_valid(self):
        raise NotImplementedError()


class VyBaseCalculator(object):

    def __init__(self, parameters=None, data=None):
        self._parameters = parameters
        self._data = data

    def is_valid(self):
        raise NotImplementedError()

    def dump(self, **kwargs):
        raise NotImplementedError()

    def backengine(self, **kwargs):
        raise NotImplementedError()
