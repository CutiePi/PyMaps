from pymaps.SortedContainer import SortedContainer


class SortedList(SortedContainer):

    def __init__(self):
        super().__init__()

    def __getitem__(self, item):
        raise NotImplementedError()

    def __setitem__(self, key, value):
        raise NotImplementedError()

    def __delitem__(self, key):
        raise NotImplementedError()

    def append(self, element):
        raise NotImplementedError()

    def pop(self):
        raise NotImplementedError()

    def clear(self):
        raise NotImplementedError()

    def slice(self, start, stop, step=1, inclusive=False):
        raise NotImplementedError()

    def islice(self, start, stop, stpe=1, inclusive=False):
        raise NotImplementedError()

    def get_min(self):
        raise NotImplementedError()

    def get_max(self):
        raise NotImplementedError()

    def find_gt(self, item):
        raise NotImplementedError()

    def find_gte(self, item):
        raise NotImplementedError()

    def find_st(self, item):
        raise NotImplementedError()

    def find_ste(self, item):
        raise NotImplementedError()
