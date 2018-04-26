import unittest

from pymaps.trees.BinarySearchTree import BinarySearchTree


class TestBinarySearchTrees(unittest.TestCase):

    def test_create_tree(self):
        bt = BinarySearchTree()
        self.assertEqual(len(bt), 0)

    def test_basic_functions(self):
        bt = BinarySearchTree()

        bt[5] = 1

        self.assertEqual(len(bt), 1)
        self.assertEqual(bt._root.get_key(), 5)
        self.assertEqual(bt._root.get_value(), 1)

        bt[4] = 2

        self.assertEqual(bt._root.get_child().get_key(), 4)

        self.assertEqual(bt.get_max(), (5, 1))
        self.assertEqual(bt.get_min(), (4, 2))

        bt[6] = 3

        self.assertEqual(bt._root.get_child(False).get_key(), 6)

    def test_predecessor(self):
        bt = BinarySearchTree()
        bt[1] = 1
        bt[2] = 2
        bt[3] = 3
        bt[-1] = -1
        bt[4] = 4

        start = bt._max_node
        self.assertEqual(start.get_key(), 4)
        walk = bt._inorder_predecessor(start)
        self.assertEqual(walk.get_key(), 3)

        walk = bt._inorder_predecessor(walk)
        self.assertEqual(walk.get_key(), 2)

        walk = bt._inorder_predecessor(walk)
        self.assertEqual(walk.get_key(), 1)

        walk = bt._inorder_predecessor(walk)
        self.assertEqual(walk.get_key(), -1)