class Base:

    def __init__(self, data):
        self._data = data

    @property
    def data(self):
        return self._data
