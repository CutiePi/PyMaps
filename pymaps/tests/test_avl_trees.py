import random
import unittest

from pymaps.tests.test_utils import preorder_str
from pymaps.trees.AVLTree import AVLTree


class TestAvlTrees(unittest.TestCase):

    def test_known_restructures(self):
        avl = AVLTree()
        avl[5] = 5
        avl[6] = 6

        self.assertEqual(avl._root.get_key(), 5)

        avl[7] = 7

        self.assertEqual(avl._root.get_key(), 6)

        avl[8] = 8

        self.assertEqual(avl._root.get_key(), 6)

        avl[9] = 9

        self.assertEqual(preorder_str(avl), "65879")

        del avl

    def test_random_insertions(self):
        bt = AVLTree()
        control = dict()

        for i in range(10000):
            key = random.randint(0, 10000)
            value = random.randint(0, 8000)

            bt[key] = value
            control[key] = value

        self.assert_match(bt, control)

    def test_random_inserts_and_delete(self):
        bt = AVLTree()
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

    def test_index(self):
        bt = AVLTree()

        for i in range(50):
            bt[i] = i

        for i in range(50):
            self.assertEqual(i, bt.at_index(i)[0])

        for i in range(50):
            self.assertEqual(bt.index_of(i), i)

    def test_subtree_size_avl(self):

        bt = AVLTree()

        for i in range(10):
            bt[i] = i

        self.assertEqual(bt._root.get_subtree_size(), 10)

    def assert_match(self, bt, control):
        for k in control:
            self.assertEqual(control[k], bt[k], "Control has a key that BST doesn't")

        for k, v in bt:
            self.assertEqual(v, control[k], "BST as a key that control doesn't")

        self.assertEqual(len(bt), len(control))
