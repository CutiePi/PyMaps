class SortedContainer:

    def __init__(self):
        pass

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
