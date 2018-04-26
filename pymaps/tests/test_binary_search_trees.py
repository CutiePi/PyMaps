import random
import unittest

from pymaps.tests.test_utils import inorder_str, postorder_str
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

    def test_slice(self):

        bt = BinarySearchTree()
        bt[1] = 1
        bt[2] = 2
        bt[3] = 3
        bt[4] = 4

        self.assertEqual([(1, 1)], bt[:2])
        self.assertEqual([(1, 1)], bt[1:2])

        self.assertEqual([(1, 1), (2, 2)], bt[:3])
        self.assertEqual([(1, 1), (2, 2)], bt[1:3])

        self.assertEqual([(1, 1), (2, 2), (3, 3), (4, 4)], bt[:])
        self.assertEqual([(1, 1), (2, 2), (3, 3), (4, 4)], bt[1:])

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

        self.assertEqual(inorder_str(bt), "-11234")

        self.assertEqual(len(bt), 5)

    def test_delete_small(self):
        bt = BinarySearchTree()

        bt[5] = 5
        del bt[5]

        self.assertEqual(len(bt), 0)

        bt[5] = 5
        bt[6] = 6

        self.assertEqual(bt._max_node.get_key(), 6)
        self.assertEqual(bt._min_node.get_key(), 5)
        self.assertEqual(len(bt), 2)

        self.assertEqual(bt._root.get_key(), 5)

        del bt[5]

        self.assertEqual(bt._root.get_key(), 6)
        self.assertEqual(bt._max_node.get_key(), 6)
        self.assertEqual(bt._min_node.get_key(), 6)

        self.assertEqual(len(bt), 1)

    def test_two_child_delete(self):
        bt = BinarySearchTree()
        bt[5] = 5
        bt[4] = 4
        bt[6] = 6
        del bt[5]

        self.assertEqual(len(bt), 2)
        self.assertTrue(4 in bt)
        self.assertTrue(6 in bt)
        self.assertFalse(5 in bt)

        bt[2] = 2
        bt[3] = 3
        bt[1] = 1

        del bt[2]

        self.assertEqual(inorder_str(bt), "1346")
        self.assertEqual(bt._min_node.get_key(), 1)
        self.assertEqual(bt._max_node.get_key(), 6)

        pass

    def assert_match(self, bt, control):
        for k in control:
            self.assertEqual(control[k], bt[k], "Control has a key that BST doesn't")

        for k, v in bt:
            self.assertEqual(v, control[k], "BST as a key that control doesn't")

        self.assertEqual(len(bt), len(control))

    def test_random_insertions(self):
        bt = BinarySearchTree()
        control = dict()

        for i in range(1000):
            key = random.randint(0, 10000)
            value = random.randint(0, 8000)

            bt[key] = value
            control[key] = value

        self.assert_match(bt, control)

    def test_random_inserts_and_delete(self):
        bt = BinarySearchTree()
        control = dict()

        for i in range(10000):
            key = random.randint(0, 10000)
            value = random.randint(0, 8000)

            action = random.randint(0, 100)

            if action > 70 and key in control:
                del bt[key]
                del control[key]
            else:
                bt[key] = value
                control[key] = value

        self.assert_match(bt, control)

    def test_rotate(self):

        bt = BinarySearchTree()

        bt[5] = 5
        bt[6] = 6

        self.assertEqual(bt._root.get_key(), 5)
        bt._rotate(bt._root.get_child(False))
        self.assertEqual(bt._root.get_key(), 6)

        self.assertEqual(bt._root.get_child().get_key(), 5)

        bt.clear()

        bt[5] = 5
        bt[1] = 1
        bt[2] = 2
        bt[6] = 6

        two_node = bt._search(2)
        one_node = bt._search(1)

        self.assertEqual(inorder_str(bt), "1256")
        self.assertEqual(postorder_str(bt), "2165")
        self.assertEqual(one_node.get_parent().get_key(), 5)

        bt._rotate(two_node)

        self.assertEqual(inorder_str(bt), "1256")
        self.assertEqual(postorder_str(bt), "1265")

        self.assertEqual(two_node.get_parent().get_key(), 5)
        self.assertEqual(one_node.get_parent().get_key(), 2)
