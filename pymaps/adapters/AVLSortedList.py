from pymaps.adapters.SortedList import SortedList
from pymaps.trees.AVLTree import AVLTree


# TODO we need to take in account that we can insert multiple times an item. We need to keep track of how many time it is in the array

class AVLSortedList(SortedList):

    def __init__(self):
        super().__init__()
        self._backing_tree = AVLTree(enable_index=True)

    def __len__(self):
        return len(self._backing_tree)

    def clear(self):
        self._backing_tree.clear()

    def append(self, element):
        """
        Append a value to the list
        :performance: O(log(n))
        :param element: the element to add to the list
        :return: void
        """

        if element in self._backing_tree:
            raise ValueError("The element is already in the list")

        self._backing_tree[element] = 1

    def __getitem__(self, query):
        if isinstance(query, slice):
            return self._get_slice(query)
        else:
            return self._get_at_index(query)

    def _get_at_index(self, index):
        """
        Get an element at the index passed in params
        :param index: the index
        :return: the item or None if nothing found
        """
        element, _ = self._backing_tree.at_index(index)
        return element

    def _gen_slice(self, query, inclusive=False):
        """
        Generator for a slice
        :param query: the slice object
        :param inclusive: if we include the stop index in the slice
        :return:
        """

        # we do this trickery to avoid having confusing result. When we do AVLSortedList[x:], we expect all the array.
        if inclusive:
            max_len = len(self) - 1
        else:
            max_len = len(self)

        start = query.start if query.start is not None else 0
        stop = query.stop if query.stop is not None else max_len
        step = query.step if query.step is not None else 1

        if stop is not None:
            if start > stop:
                raise ValueError("Cannot have a start index greater than a stop index")

        for index in range(start, stop + (1 if inclusive else 0), step):  # include stop if we want it
            yield self._get_at_index(index)

    def _get_slice(self, query, inclusive=False):
        """
        Build an array slice for the desired range
        :param query: the range wanted
        :param inclusive: if we want to include the last element
        :return: the array
        """
        result = [x for x in self._gen_slice(query, inclusive=inclusive)]
        return result

    def __delitem__(self, query):
        if isinstance(query, slice):
            return self._del_slice(query)
        else:
            return self._del_index(query)

    def _del_index(self, index):
        # noinspection PyProtectedMember
        node = self._backing_tree._at_index(index)
        if node is not None:
            # noinspection PyProtectedMember
            self._backing_tree._remove_node(node)
        else:
            raise RuntimeError("Supposed to have found a node or raised an index error, for key %i" % index)

    def __setitem__(self, query, value):
        if isinstance(query, slice):
            return self._set_slice(query, value)
        else:
            return self._set_at_index(query, value)

    def _set_slice(self, query, value):

        count = 0

        for key in self._gen_slice(query):
            del self._backing_tree[key]
            count += 1

        for i in range(count):
            self.append(value)

    def _find(self, item):
        # noinspection PyProtectedMember
        node = self._backing_tree._search(item)

        if node is None:
            return None
        elif node.get_key() != item:
            return None
        else:
            return node

    def __contains__(self, item):
        return self._find(item) is not None

    def __iter__(self):
        for item, _ in self._backing_tree:
            yield item

    def _set_at_index(self, index, value):
        # noinspection PyProtectedMember
        node = self._backing_tree._at_index(index)
        # since we change the key, we need to reinsert in the tree
        # noinspection PyProtectedMember
        self._backing_tree._remove_node(node)
        self.append(value)

    def get_min(self):
        return self._backing_tree.get_min()[0]

    def get_max(self):
        return self._backing_tree.get_max()[0]

    def pop(self):
        if len(self) == 0:
            raise ValueError("The sorted list is empty; cannot pop an element")
        # noinspection PyProtectedMember
        last_node = self._backing_tree._max_node
        # noinspection PyProtectedMember
        self._backing_tree._remove_node(last_node)

    def slice(self, start, stop, step=1, inclusive=False):
        query = slice(start, stop, step)
        return self._get_slice(query, inclusive=inclusive)

    def islice(self, start, stop, step=1, inclusive=False):
        pass

    def find_gt(self, item):
        return self._backing_tree.find_gt(item)[0]

    def find_gte(self, item):
        return self._backing_tree.find_ste(item)[0]

    def find_st(self, item):
        return self._backing_tree.find_st(item)[0]

    def find_ste(self, item):
        return self._backing_tree.find_ste(item)[0]
