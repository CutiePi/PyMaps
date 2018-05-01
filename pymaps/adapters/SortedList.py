from pymaps.trees.AVLTree import AVLTree


class SortedList:

    def __init__(self):
        self._backing_tree = AVLTree(enable_index=True)

    def __len__(self):
        return len(self._backing_tree)

    def append(self, element):
        pass
