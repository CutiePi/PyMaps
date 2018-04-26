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

    def get_parent(self):
        return self._parent_node

    def __repr__(self):
        return f"[{self._key}:{self._value}]"


LEFT = True
RIGHT = False


class BinarySearchTree:
    __slots__ = ["_item_count", "_root", "_min_node", "_max_node"]

    def __init__(self):
        self._item_count = 0
        self._root = None
        self._min_node = None
        self._max_node = None

    def _inserted_hook(self, inserted_node):
        pass

    def _accessed_hook(self, accessed_node):
        pass

    def _deleted_hook(self, parent_node):
        pass

    def _search(self, key):
        last = None
        walk = self._root

        while walk is not None and walk.get_key() != key:
            last = walk
            walk = walk.get_child(key < walk.get_key())

        return walk if walk is not None else last

    def __setitem__(self, key, value):
        self._insert(key, value)

    def _insert(self, key, value):
        """
        Insert a node inside the tree. It will perform a search and then insert the node
        inside the tree.
        :performance: O(h), where the h is the height of the tree
        :param key: the key of the mapping
        :param value: the value of the mapping
        :return: void
        """

        insertion_spot = self._search(key)

        if self._root is None:
            self._root = self._make_node(key, value, None)
            node = self._root
        elif insertion_spot.get_key() == key:
            insertion_spot.set_value(value)
            self._accessed_hook(insertion_spot)
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
            if self._max_node is None or key > self._max_node.get_key():
                self._max_node = node
            self._inserted_hook(node)

    def _remove(self, key, value):
        pass  # TODO

    def _inorder_traversal(self, node=None):

        if node is None:
            node = self._root

        yield from self._inorder_traversal(node.get_child(LEFT))
        yield node
        yield from self._inorder_traversal(node.get_child(RIGHT))

    # noinspection PyMethodMayBeStatic
    def _inorder_predecessor(self, node):
        """
        Find the inorder predecessor than of the node. That is, the node with the largest smallest key than
        the node's itself
        :param node: the node from where we start
        :return: the predecessor
        """
        # TODO write test, and check algorithm
        if node.has_child(left=True):
            walk = node.get_child()
            while walk.has_child(RIGHT):
                walk = walk.get_child(RIGHT)
            return walk
        else:
            walk = node.get_parent()
            while walk is not None and walk.get_key() > node.get_key():
                walk = walk.get_parent()
            return walk

    def _inorder_successor(self, node):
        pass

    def __len__(self):
        return self._item_count

    def _make_node(self, key, value, parent):
        """
        Make a node in the tree. Can be overriden by subclasses
        :param key: the key
        :param value: the value
        :param parent: the parent node, can be None if root
        :return:
        """
        return TreeNode(key, value, parent)

    def get_max(self):
        """
        Get the key and the value associated with the largest key
        :performance O(1)
        :return: tuple (key, value)
        """
        if self._item_count == 0:
            raise ValueError("Empty Binary Search tree")
        else:
            return self._max_node.get_key(), self._max_node.get_value()

    def get_min(self):
        """
        Get the key and the value associated with the smallest key
        :performance O(1)
        :return: tuple (key, value)
        """
        if self._item_count == 0:
            raise ValueError("Empty Binary Search tree")
        else:
            return self._min_node.get_key(), self._min_node.get_value()
