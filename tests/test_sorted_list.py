import unittest

from pymaps import AVLSortedList


class TestSortedList(unittest.TestCase):

    def test_basic_append(self):
        sl = AVLSortedList()

        sl.append(5)
        sl.append(6)
        sl.append(3)

        self.assertEqual(sl.get_max(), 6)
        self.assertEqual(sl.get_min(), 3)

        sl[0] = 12

        self.assertEqual(sl.get_max(), 12)
        self.assertEqual(sl.get_min(), 5)

        self.assertEqual(len(sl), 3)

    def test_slice(self):
        sl = AVLSortedList()

        sl.append(5)
        sl.append(4)
        sl.append(1)
        sl.append(10)

        self.assertEqual(sl[0:2], [1, 4])

        self.assertEqual(sl[0:], [1, 4, 5, 10])

        self.assertEqual(sl[-3:-1], [4, 5])

    def test_multiple_same_values(self):
        sl = AVLSortedList()
        sl.append(1)
        sl.append(1)

        self.assertEqual([x for x in sl], [1, 1])
