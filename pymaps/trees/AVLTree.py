from pymaps.trees.BinarySearchTree import TreeNode, LEFT, RIGHT, BinarySearchTree


class HeightAwareNode(TreeNode):
    __slots__ = ["_height"]

    def __init__(self, key, value, parent):
        super().__init__(key, value, parent)
        self._height = 1

    def get_height(self):
        return self._height

    def set_height(self, height):
        old_height = self._height
        self._height = height
        return old_height

    def get_left_height(self):
        left_height = 0 if not self.has_child(LEFT) else self.get_child(LEFT).get_height()
        return left_height

    def get_right_height(self):
        right_height = 0 if not self.has_child(RIGHT) else self.get_child(RIGHT).get_height()
        return right_height

    def is_balanced(self):
        left_height, right_height = self.get_left_height(), self.get_right_height()
        return abs(left_height - right_height) <= 1

    def heavy_child(self):
        left_height, right_height = self.get_left_height(), self.get_right_height()
        return self.get_child(left_height > right_height)

    def recompute_height(self):
        old_height = self._height
        self._height = 1 + max(self.get_left_height(), self.get_right_height())
        return old_height


class AVLTree(BinarySearchTree):

    def __init__(self):
        super().__init__()

    def _inserted_hook(self, inserted_node):
        self._rebalance(inserted_node, True)

    def _deleted_hook(self, parent_node):
        self._rebalance(parent_node, False)

    def _rebalance(self, node, insert):

        walk = node

        while walk is not None:

            if not walk.is_balanced():
                tall_child = walk.heavy_child()

                if tall_child.get_left_height() == tall_child.get_right_height():
                    tall_grandchild = tall_child.get_child(walk.get_child() == tall_child)
                else:
                    tall_grandchild = tall_child.heavy_child()

                root = self._trinode_restructure(tall_grandchild)

                left = root.get_child(LEFT)
                right = root.get_child(RIGHT)

                if left is not None:
                    left.recompute_height()
                if right is not None:
                    right.recompute_height()

                root.recompute_height()

                if insert:
                    break  # no more restructured required

            walk.recompute_height()

            walk = walk.get_parent()

    def _make_node(self, key, value, parent):
        return HeightAwareNode(key, value, parent)
