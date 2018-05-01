from queue import Queue


def inorder_str(bt):
    keys = []

    for key, value in bt:
        keys.append(str(key))

    return "".join(keys)


def postorder_str(bt):
    keys = []

    for node in bt._postorder_traversal(bt._root):
        keys.append(str(node.get_key()))

    return "".join(keys)


def preorder_str(bt):
    keys = []

    for node in bt._preorder_traversal(bt._root):
        keys.append(str(node.get_key()))

    return "".join(keys)


def bfs_str(bt):
    q = Queue()
    q.put(bt._root)

    keys = []

    while q.qsize() > 0:
        node = q.get()
        keys.append(node.get_key())

        if node.has_child(True):
            q.put(node.get_child())
        if node.has_child(False):
            q.put(node.get_child(False))

    return "".join(keys)
