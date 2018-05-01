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