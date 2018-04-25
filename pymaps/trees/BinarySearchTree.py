from abc import ABC


class TreeNode:
    __slots__ = ["_key", "_value", "_parent_node", "_left_child", "_right_child"]

    def __init__(self, key, value, parent_node):
        self._key = key
        self._value = value
        self._parent_node = parent_node
        self._left_child = None
        self._right_child = None

    def has_child(self, left=True):
        return (self._left_child is not None) if left else (self._right_child is not None)

    def get_child(self, left=True):
        return self._left_child if left else self._right_child

    def set_child(self, child, left=True):
        if left:
            self._left_child = child
        else:
            self._right_child = child

    def get_value(self):
        return self._value

    def get_key(self):
        return self._key

    def set_value(self, new_value):
        old_value = self._value
        self._value = new_value
        return old_value


LEFT = True
RIGHT = False


class BinarySearchTree:
    __slots__ = ["_item_count", "_root", "_min_node", "_max_node"]

    def __init__(self):
        self._item_count = 0
        self._root = None
        self._min_node = None
        self._max_node = None

    def _search(self, key):
        last = None
        walk = self._root

        while walk is not None and walk.get_key() != key:
            last = walk
            walk = walk.get_child(walk.get_key() < key)

        return walk if walk is not None else last

    def _insert(self, key, value):

        insertion_spot = self._search(key)

        if self._root is None:
            self._root = self._make_node(key, value, None)
            node = self._root
        elif insertion_spot.get_key() == key:
            insertion_spot.set_value(value)
            node = None
        elif insertion_spot.get_key() < key:
            right_child = self._make_node(key, value, insertion_spot)
            insertion_spot.set_child(right_child, RIGHT)
            node = right_child
        else:
            left_child = self._make_node(key, value, insertion_spot)
            insertion_spot.set_child(left_child, LEFT)
            node = left_child

        if node is not None:
            self._item_count += 1
            if self._min_node is None or key < self._min_node.get_key():
                self._min_node = node
            if self._min_node is None or key > self._max_node.get_key():
                self._max_node = node

    def _remove(self, key, value):
        pass

    def _inorder_predecessor(self, node):

        if node.has_child(left=True):
            walk = node.get_child()
            while walk.has_child(RIGHT):
                walk = walk.get_child(RIGHT)
            return walk
        else:
            pass  # TODO parent with lt key

    def _inorder_successor(self, node):
        pass

    def __len__(self):
        return self._item_count

    def _make_node(self, key, value, parent):
        return TreeNode(key, value, parent)
