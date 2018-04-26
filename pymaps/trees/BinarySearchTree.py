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

    def set_key(self, key):
        old_key = self._key
        self._key = key
        return old_key

    def get_parent(self):
        return self._parent_node

    def set_parent(self, new_parent):
        old_parent = self._parent_node
        self._parent_node = new_parent
        return old_parent

    def __repr__(self):
        return "[%s:%s]" % (self._key, self._value)


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

    def __getitem__(self, key):
        return self._get(key)

    def _get(self, key):
        node = self._search(key)

        if node is not None and node.get_key() == key:
            return node.get_value()
        else:
            return None

    def __contains__(self, key):
        node = self._search(key)
        return node is not None and node.get_key() == key

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

    def __delitem__(self, key):
        self._remove(key)

    def _remove(self, key):
        node = self._search(key)

        if node is None or node.get_key() != key:
            return

        one_child = node.has_child(LEFT) != node.has_child(RIGHT)
        no_child = node.has_child(LEFT) == node.has_child(RIGHT) == False

        if one_child or no_child:
            self._single_child_delete(node)
        else:
            # we find the predecessor and actually delete that node
            predecessor = self._inorder_predecessor(node)

            if predecessor == self._min_node:
                self._min_node = node
            if predecessor == self._max_node:
                self._max_node = node

            p_key = predecessor.get_key()
            p_value = predecessor.get_value()

            self._single_child_delete(predecessor)

            node.set_key(p_key)
            node.set_value(p_value)

    def _single_child_delete(self, node):

        ancestor = node.get_parent()
        side = LEFT if (ancestor is None or ancestor.get_child(LEFT) == node) else RIGHT
        child = node.get_child(LEFT) if node.has_child(LEFT) else node.get_child(RIGHT)

        if node is self._min_node:
            self._min_node = child

        if node is self._max_node:
            self._max_node = child

        if ancestor is None:
            self._root = child
            if child is not None:
                child.set_parent(None)
        elif child is not None:
            self._attach(ancestor, child, side)
        else:
            ancestor.set_child(None, side)

        node.set_parent(None)
        self._item_count -= 1

    def __iter__(self):
        for node in self._inorder_traversal(self._root):
            yield node.get_key(), node.get_value()

    def _inorder_traversal(self, node):

        if node is None:
            return

        yield from self._inorder_traversal(node.get_child(LEFT))
        yield node
        yield from self._inorder_traversal(node.get_child(RIGHT))

    def _preorder_traversal(self, node):

        if node is None:
            return

        yield node
        yield from self._preorder_traversal(node.get_child(LEFT))
        yield from self._preorder_traversal(node.get_child(RIGHT))

    def _postorder_traversal(self, node):

        if node is None:
            return

        yield from self._postorder_traversal(node.get_child(LEFT))
        yield from self._postorder_traversal(node.get_child(RIGHT))
        yield node

    # noinspection PyMethodMayBeStatic
    def _inorder_predecessor(self, node):
        """
        Find the inorder predecessor than of the node. That is, the node with the largest smallest key than
        the node's itself
        :param node: the node from where we start
        :return: the predecessor
        """
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

        if node.has_child(RIGHT):
            walk = node.get_child(RIGHT)
            while walk.has_child(LEFT):
                walk = walk.get_child(LEFT)
            return walk
        else:
            walk = node.get_parent()
            while walk is not None and walk.get_key() < node.get_key():
                walk = walk.get_parent()
            return walk

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

    def _attach(self, parent, new_child, side=LEFT):
        """
        Attach and node to a parent node, and perform the two way bindings
        :param parent: the parent node
        :param new_child: the child node
        :param side: the side where the child will be
        :return: void
        """
        parent.set_child(new_child, side)
        new_child.set_parent(parent)
