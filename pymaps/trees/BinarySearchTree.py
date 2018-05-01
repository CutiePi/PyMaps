class TreeNode:
    __slots__ = ["_key", "_value", "_parent_node", "_left_child", "_right_child", "_subtree_size"]

    def __init__(self, key, value, parent_node):
        self._key = key
        self._value = value
        self._parent_node = parent_node
        self._left_child = None
        self._right_child = None
        self._subtree_size = 1

    def increment_subtree_size(self):
        self._subtree_size += 1

    def get_subtree_size(self):
        return self._subtree_size

    def set_subtree_size(self, new_size):
        old_size = self._subtree_size
        self._subtree_size = new_size
        return old_size

    def decrement_subtree_size(self):
        self._subtree_size -= 1

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


# noinspection PyMethodMayBeStatic
class BinarySearchTree:
    __slots__ = [
        "_item_count",
        "_root",
        "_min_node",
        "_max_node",
        "_enable_index"
    ]

    def __init__(self, enable_index=True):
        self._item_count = 0
        self._root = None
        self._min_node = None
        self._max_node = None
        self._enable_index = enable_index

    def clear(self):
        """
        Empty the tree
        :return: void
        """
        self._root = None
        self._item_count = 0
        self._min_node = None
        self._max_node = None

    def _inserted_hook(self, inserted_node):
        pass

    def _accessed_hook(self, accessed_node):
        pass

    def _deleted_hook(self, parent_node):
        pass

    def _rotate(self, node):
        """
        Perform a rotate on the given node. It will automatically perform left rotate or right rotate,
        depending where the node is.

        Rotate:
             Ancestor      Node
            /          < - >   \
           Node                 Ancestor

        :param node: the node being rotated
        :return: void
        """
        ancestor = node.get_parent()
        if ancestor is None:
            return

        side = (node == ancestor.get_child(LEFT))

        great_ancestor = ancestor.get_parent()  # maybe None
        ancestor_side = (ancestor == great_ancestor.get_child()) if great_ancestor is not None else None

        moved_child = node.get_child(not side)

        self._attach(node, ancestor, not side)
        ancestor.set_subtree_size(ancestor.get_subtree_size() - node.get_subtree_size())
        node.set_subtree_size(ancestor.get_subtree_size() + node.get_subtree_size())

        self._attach(ancestor, moved_child, side)

        if moved_child is not None:
            ancestor.set_subtree_size(ancestor.get_subtree_size() + moved_child.get_subtree_size())

        if great_ancestor is None:
            self._root = node
            node.set_parent(None)
        else:
            self._attach(great_ancestor, node, ancestor_side)

    def _trinode_restructure(self, node):
        """
        Restructure three nodes
        :param node: the node to restructure
        :return: the new root of the subtree made by the tri-node structure
        """
        ancestor = node.get_parent()

        if ancestor is None:
            return None  # TODO raise?

        great_ancestor = ancestor.get_parent()

        if great_ancestor is None:
            return None  # TODO raise?

        aligned = (node == ancestor.get_child()) == (ancestor == great_ancestor.get_child())

        if aligned:
            self._rotate(ancestor)
            return ancestor
        else:
            self._rotate(node)
            self._rotate(node)
            return node

    def _search(self, key):
        """
        Performs a binary search for a key in the tree.
        It returns the node with the key or the node where the key should be inserted.
        (The deepest node possible)
        :performance: O(h)
        :param key: the key to search for
        :return: the node where the key is or would be a child of
        """
        last = None
        walk = self._root

        while walk is not None and walk.get_key() != key:
            last = walk
            walk = walk.get_child(key < walk.get_key())

        return walk if walk is not None else last

    def __getitem__(self, query):
        if isinstance(query, slice):
            return self._get_slice(query)
        else:
            return self._get(query)

    def _gen_slice(self, query, inclusive=False):
        start_node = self._search(query.start) if query.start is not None else self._min_node
        stop_node = self._search(query.stop) if query.stop is not None else None
        step = query.step

        if start_node is not None and stop_node is not None:
            if start_node.get_key() > stop_node.get_key():
                raise ValueError("Cannot search for a slice with a start greater than a stop")

        walk = start_node

        while walk is not None:

            if not inclusive and walk == stop_node:
                break

            yield walk

            if walk == stop_node:
                break

            for i in range(1 if step is None else step):  # skip "step" many items
                walk = self._inorder_successor(walk)

    def _gen_islice(self, query, inclusive=False):
        start_node = self._search(query.start) if query.start is not None else self._min_node
        stop_node = self._search(query.stop) if query.stop is not None else None
        step = query.step

        walk = self._min_node

        while walk is not None:
            if not inclusive and walk == start_node:
                break

            yield walk

            if walk == start_node:
                break

            for i in range(1 if step is None else step):  # skip "step" many items
                walk = self._inorder_successor(walk)

        # skip the area between start and stop
        walk = stop_node

        while walk is not None:

            if not (not inclusive and walk == stop_node):
                yield walk

            for i in range(1 if step is None else step):  # skip "step" many items
                walk = self._inorder_successor(walk)

    def _get_slice(self, query, inclusive=False):
        result = [(node.get_key(), node.get_value()) for node in self._gen_slice(query, inclusive)]
        return result

    def _get_islice(self, query, inclusive=False):
        result = [(node.get_key(), node.get_value()) for node in self._gen_islice(query, inclusive)]
        return result

    def slice(self, start, stop, step=1, inclusive=False):
        """
        Return a slice of the tree
        :param start: the start key (None for min_key)
        :param stop: the stop key (None for until the end of the tree)
        :param step: the number of keys skipped in between each result
        :param inclusive: if the stop key is included or not
        :return: an array of (key,value) tuples
        """
        return self._get_slice(slice(start, stop, step), inclusive=inclusive)

    def islice(self, start, stop, step=1, inclusive=False):
        return self._get_islice(slice(start, stop, step), inclusive=inclusive)

    def _get(self, key):
        node = self._search(key)

        if node is not None and node.get_key() == key:
            return node.get_value()
        else:
            return None

    def __contains__(self, key):
        node = self._search(key)
        return node is not None and node.get_key() == key

    def __setitem__(self, query, value):
        if isinstance(query, slice):
            self.set_slice(query, value)
        else:
            self._insert(query, value)

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
        else:
            child = self._make_node(key, value, insertion_spot)
            insertion_spot.set_child(child, insertion_spot.get_key() > key)
            node = child

        if node is not None:
            self._item_count += 1

            if self._enable_index and insertion_spot is not None:
                self._increment_subtree_size(insertion_spot.get_child(insertion_spot.get_key() > key))

            if self._min_node is None or key < self._min_node.get_key():
                self._min_node = node
            if self._max_node is None or key > self._max_node.get_key():
                self._max_node = node
            self._inserted_hook(node)

    def set_slice(self, slice_query, new_value, inclusive=False):
        for node in self._gen_slice(slice_query, inclusive=inclusive):
            node.set_value(new_value)

    def set_islice(self, slice_query, new_value, inclusive=False):
        for node in self._gen_islice(slice_query, inclusive=inclusive):
            node.set_value(new_value)

    def _increment_subtree_size(self, node):
        """
        Increment the subtree size for the whole path between a node and the root.
        It is used to support fast indexing methods.
        :performance: O(h)
        :param node: the node to start from
        :return: void
        """
        if node is None:
            return

        parent = node.get_parent()

        while parent is not None:
            parent.increment_subtree_size()
            parent = parent.get_parent()

    def _decrement_subtree_size(self, node):
        """
        Decrement the subtree size for the whole path between a node and the root.
        It is used to support fast indexing methods
        :param node: the node to start from
        :return: void
        """
        parent = node.get_parent()

        while parent is not None:
            parent.decrement_subtree_size()
            parent = parent.get_parent()

    def __delitem__(self, key):
        self._remove(key)

    def _remove(self, key):
        node = self._search(key)
        if node is None or node.get_key() != key:
            return
        self._remove_node(node)

    def _remove_node(self, node):

        one_child = node.has_child(LEFT) != node.has_child(RIGHT)
        no_child = not node.has_child(LEFT) and not node.has_child(RIGHT)

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

        if self._enable_index:
            self._decrement_subtree_size(node)

        if node is self._min_node:
            self._min_node = child if child is not None else ancestor

        if node is self._max_node:
            self._max_node = child if child is not None else ancestor

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
        """
        Yield all (key,value) pairs of the tree.
        :return:
        """
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
        if new_child is not None:
            new_child.set_parent(parent)

    def index_of_or_raise(self, key):
        """
        See index_of.
        Will raise an error instead of returning None
        :param key:
        :return:
        """
        index = self.index_of(key)
        if index is None:
            raise ValueError("The key is not in the tree")
        else:
            return index

    def index_of(self, key):
        """
        Return the index of the item with the key.
        It will return the index if the list was a sorted list.
        For instance, if you have a tree with the keys 0,1,2,3, their respective
        indices would be 0,1,2,3. It also matches the inorder traversal index of the tree.
        :performance: O(h)
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

        if node.has_child(RIGHT):
            smaller_than_count += node.get_child(RIGHT).get_subtree_size()

        walk = node

        while ancestor is not None:
            if walk == ancestor.get_child(LEFT):
                smaller_than_count += 1
                if ancestor.get_child(RIGHT) is not None:
                    smaller_than_count += ancestor.get_child(RIGHT).get_subtree_size()
            walk = ancestor
            ancestor = ancestor.get_parent()

        return self._item_count - (smaller_than_count + 1)

    def _at_index(self, index):
        if not self._enable_index:
            raise RuntimeError("The binary search tree has been instantiated without support for index methods.")

        if not -self._item_count <= index < self._item_count:
            raise ValueError("Illegal index")

        if index < 0:
            index = self._item_count + index

        walk = self._root

        if walk is None:
            return None

        total = walk.get_subtree_size()
        smaller_than_count = total - index - 1

        last = walk
        while walk is not None:
            last = walk
            if walk.has_child(RIGHT):
                right_size = walk.get_child(RIGHT).get_subtree_size()

                if smaller_than_count > right_size:
                    walk = walk.get_child(LEFT)
                    smaller_than_count -= right_size + 1
                elif smaller_than_count == right_size:
                    break
                else:
                    walk = walk.get_child(RIGHT)
            elif smaller_than_count > 0:
                smaller_than_count -= 1
                walk = walk.get_child(LEFT)
            else:
                break

        return last

    def at_index(self, index):
        """
        Return the key at the specified index. The index is based of the index where the keys would be seen in an
        inorder traversal of the tree
        :param index: the index
        :return: (tuple)(key, value)
        """
        node = self._at_index(index)
        return node.get_key(), node.get_value()

    def count_in_range(self, start, stop, step=1, inclusive=False):
        """
        Return the number of elements contained in the specified interval.

        :param step: the step between two distinct elements
        :param start: the start of the range (inclusive), None for min_key
        :param stop:  the stop of the range (inclusive if specified else exclusive), None for max_key
        :param inclusive: if we include the stop or not
        :return: the count
        """
        total = 0

        for _, _ in self._get_slice(slice(start, stop, step), inclusive):
            total += 1

        return total

    def find_gt(self, key):
        """
        Find the smallest key greater than the one passed in parameters
        :param key:
        :return:
        """
        walk = self._search(key)

        while walk is not None and walk.get_key() <= key:
            walk = self._inorder_successor(walk)

        if walk is None:
            return None

        return walk.get_key(), walk.get_value()

    def find_gte(self, key):
        """
        Find the smallest or equal key greater than the one passed in parameters
        :param key:
        :return:
        """

        walk = self._search(key)

        while walk is not None and walk.get_key() < key:
            walk = self._inorder_successor(walk)

        if walk is None:
            return None

        return walk.get_key(), walk.get_value()

    def find_st(self, key):
        """
        Find the largest key smaller than the one passed in parameters
        :param key:
        :return:
        """

        walk = self._search(key)

        while walk is not None and walk.get_key() >= key:
            walk = self._inorder_predecessor(walk)

        if walk is None:
            return None

        return walk.get_key(), walk.get_value()

    def find_ste(self, key):
        """
        Find the largest key smaller than the one passed in parameters
        :param key:
        :return:
        """
        walk = self._search(key)

        while walk is not None and walk.get_key() > key:
            walk = self._inorder_predecessor(walk)

        if walk is None:
            return None

        return walk.get_key(), walk.get_value()

    def __setslice__(self, i, j, sequence):
        raise RuntimeError("No clue what this is for since __setitem works for slices...")
