import unittest

from pymaps import AVLSortedList


class TestSortedList(unittest.TestCase):

    def test_multiple_instances(self):
        sl = AVLSortedList()
        sl.append(1)
        sl.append(1)

        self.assertEqual([x for x in sl], [1, 1])
        self.assertEqual(len(sl), 2)

        self.assertEqual(sl.index_of(1), 0)
        self.assertEqual(sl.at_index(0), 1)
        self.assertEqual(sl.at_index(1), 1)

    def test_general_insertions(self):
        sl = AVLSortedList()

        sl.append(1)
        sl.append(3)
        sl.append(2)
        sl.append(1)
        sl.append(5)
        sl.append(6)
        sl.append(3)

        self.assertEqual([x for x in sl], [1, 1, 2, 3, 3, 5, 6])

        self.assertEqual(sl.at_index(0), 1)
        self.assertEqual(sl.at_index(1), 1)
        self.assertEqual(sl.at_index(2), 2)
        self.assertEqual(sl.at_index(3), 3)
        self.assertEqual(sl.at_index(4), 3)
        self.assertEqual(sl.at_index(5), 5)
        self.assertEqual(sl.at_index(6), 6)

        self.assertEqual(sl.index_of(1), 0)
        self.assertEqual(sl.index_of(2), 2)
        self.assertEqual(sl.index_of(3), 3)
        self.assertEqual(sl.index_of(5), 5)
        self.assertEqual(sl.index_of(6), 6)

        self.assertEqual(sl.get_min(), 1)
        self.assertEqual(sl.get_max(), 6)

        self.assertEqual(sl.find_st(1), None)
        self.assertEqual(sl.find_ste(1), 1)
        self.assertEqual(sl.find_gt(6), None)
        self.assertEqual(sl.find_gte(6), 6)
