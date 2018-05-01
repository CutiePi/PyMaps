from pymaps.trees.AVLTree import AVLTree


class SortedList:

    def __init__(self):
        self._backing_tree = AVLTree(enable_index=True)

    def __len__(self):
        return len(self._backing_tree)

    def append(self, element):
        """
        Append a value to the list
        :performance: O(log(n))
        :param element: the element to add to the list
        :return: void
        """
        self._backing_tree[element] = None

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

        # we do this trickery to avoid having confusing result. When we do SortedList[x:], we expect all the array.
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
