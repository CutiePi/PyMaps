from pymaps.adapters.SortedList import SortedList
from pymaps.trees.AVLTree import AVLTree, HeightAwareNode

# TODO we need to take in account that we can insert multiple times an item. We need to keep track of how many time
# it is in the array
from pymaps.trees.BinarySearchTree import RIGHT_CHILD, LEFT_CHILD


class SortedListNode(HeightAwareNode):

    def __init__(self, item, value, parent):
        super().__init__(item, value, parent)

    def get_element(self):
        return self._key

    def get_count(self):
        return self._value


class AVLSortedList(SortedList, AVLTree):
    __slots__ = ["_node_count"]

    def __init__(self):
        super().__init__()
        self._item_count = 0

    def __len__(self):
        return self._item_count

    def __getitem__(self, item):
        if isinstance(item, slice):
            return self._get_slice(item)
        else:
            return self.at_index(item)

    def __setitem__(self, key, value):
        if isinstance(key, slice):
            pass  # TODO set slice
        else:
            self._set_at_index(key, value)

    def __delitem__(self, key):
        pass

    def __iter__(self):
        for item, count in super(AVLTree, self).__iter__():
            for _ in range(count):
                yield item

    def _set_at_index(self, index, value):
        node = super(AVLTree, self)._at_index(index)
        self._remove_node(node)
        self._item_count -= 1  # since append will manage the rest
        self.append(value)

    def append(self, element):

        current_node = self._search(element)

        if current_node is not None and current_node.get_key() == element:
            current_node.set_value(current_node.get_value() + 1)
            current_node.increment_subtree_size()
            super(AVLTree, self)._increment_subtree_size(current_node)
        else:
            super(AVLTree, self)._insert(element, 1)

        self._item_count += 1

    def pop(self):

        if self._max_node is not None:
            self._max_node.set_value(self._max_node.get_value() - 1)
            super(AVLTree, self)._decrement_subtree_size(self._max_node)
            if self._max_node.get_count() < 1:
                self._remove_node(self._max_node)
            self._item_count -= 1
            self._max_node.decrement_subtree_size()
        else:
            raise ValueError("The tree is currently empty")

    def clear(self):
        super(AVLTree, self).clear()
        self._item_count = 0

    def slice(self, start, stop, step=1, inclusive=False):
        pass

    def islice(self, start, stop, stpe=1, inclusive=False):
        pass

    def get_min(self):
        return super(AVLTree, self).get_min()[0]

    def get_max(self):
        return super(AVLTree, self).get_max()[0]

    def find_gt(self, item):
        return super(AVLTree, self).find_gt(item)[0]

    def find_gte(self, item):
        return super(AVLTree, self).find_gte(item)[0]

    def find_st(self, item):
        return super(AVLTree, self).find_st(item)[0]

    def find_ste(self, item):
        return super(AVLTree, self).find_ste(item)[0]

    def _make_node(self, key, value, parent):
        return SortedListNode(key, value, parent)

    def at_index(self, index):
        return super(AVLTree, self).at_index(index)[0]

    def index_of(self, key):
        """
        Return the index of the item with the key.
        It will return the index if the list was a sorted list.
        For instance, if you have a tree with the keys 0,1,2,3, their respective
        indices would be 0,1,2,3. It also matches the inorder traversal index of the tree.
        :performance: O(log(n))
        :param key: the key to search for
        :return: the index, or None if the key is not in the tree
        """

        if not self._enable_index:
            raise RuntimeError("The binary search tree has been instantiated without support for index methods.")

        node = self._search(key)

        if node.get_key() != key:
            return None

        ancestor = node.get_parent()

        smaller_than_count = 0

        if node.has_child(RIGHT_CHILD):
            smaller_than_count += node.get_child(RIGHT_CHILD).get_subtree_size()

        walk = node

        while ancestor is not None:
            if walk == ancestor.get_child(LEFT_CHILD):
                smaller_than_count += ancestor.get_count()
                if ancestor.get_child(RIGHT_CHILD) is not None:
                    smaller_than_count += ancestor.get_child(RIGHT_CHILD).get_subtree_size()
            walk = ancestor
            ancestor = ancestor.get_parent()

        return (len(self) - smaller_than_count) - node.get_count()

    def _get_slice(self, query, inclusive=False):
        result = [x.get_element() for x in self._gen_slice(query, inclusive)]
        return result

    def _gen_slice(self, query, inclusive=False):

        start = query.start if query.start is not None else 0
        stop = query.stop if query.stop is not None else (len(self) + 1)
        step = query.step if query.step is not None else 1

        walk = self._at_index(start)
        current_idx = start

        first_index_of_key = self.index_of(walk.get_element())

        step_walker = (start - first_index_of_key) % step

        while walk is not None and current_idx < stop + (1 if inclusive else 0):
            for _ in range(walk.get_count()):
                if step_walker == 0:
                    yield walk

                step_walker = (step_walker - 1) % step

                current_idx += 1

            walk = self._inorder_successor(walk)
