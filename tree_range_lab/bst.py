class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None


def insert(root, key):
    if root is None:
        return Node(key)
    if key < root.key:
        root.left = insert(root.left, key)
    elif key > root.key:
        root.right = insert(root.right, key)
    return root


def build_bst(values):
    root = None
    for key in values:
        root = insert(root, key)
    return root


def search(root, key):
    current = root
    visited = 0
    while current is not None:
        visited += 1
        if key == current.key:
            return current, visited
        if key < current.key:
            current = current.left
        else:
            current = current.right
    return None, visited


def preorder(root, result=None):
    if result is None:
        result = []
    if root is not None:
        result.append(root.key)
        preorder(root.left, result)
        preorder(root.right, result)
    return result


def inorder(root, result=None):
    if result is None:
        result = []
    if root is not None:
        inorder(root.left, result)
        result.append(root.key)
        inorder(root.right, result)
    return result


def postorder(root, result=None):
    if result is None:
        result = []
    if root is not None:
        postorder(root.left, result)
        postorder(root.right, result)
        result.append(root.key)
    return result


def delete(root, key):
    if root is None:
        return None
    if key < root.key:
        root.left = delete(root.left, key)
    elif key > root.key:
        root.right = delete(root.right, key)
    else:
        if root.left is None:
            return root.right
        if root.right is None:
            return root.left
        successor = root.right
        while successor.left is not None:
            successor = successor.left
        root.key = successor.key
        root.right = delete(root.right, successor.key)
    return root


def height(root):
    if root is None:
        return -1
    return 1 + max(height(root.left), height(root.right))


def balance_factor(root):
    if root is None:
        return 0
    return height(root.left) - height(root.right)


def rotate_right(root):
    new_root = root.left
    middle = new_root.right
    new_root.right = root
    root.left = middle
    return new_root


def rotate_left(root):
    new_root = root.right
    middle = new_root.left
    new_root.left = root
    root.right = middle
    return new_root


def show_tree(root, level=0, side="Корень"):
    if root is None:
        return
    print("  " * level + side + ": " + str(root.key))
    show_tree(root.left, level + 1, "Л")
    show_tree(root.right, level + 1, "П")
