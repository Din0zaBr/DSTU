class TreeNode:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.val = key


class BinaryTree:
    def __init__(self):
        self.root = None

    def insert(self, key):
        if self.root is None:
            self.root = TreeNode(key)
        else:
            self._insert_rec(self.root, key)

    def _insert_rec(self, node, key):
        if key < node.val:
            if node.left is None:
                node.left = TreeNode(key)
            else:
                self._insert_rec(node.left, key)
        else:
            if node.right is None:
                node.right = TreeNode(key)
            else:
                self._insert_rec(node.right, key)

    def height(self, node):
        if node is None:
            return -1
        else:
            left_height = self.height(node.left)
            right_height = self.height(node.right)
            return max(left_height, right_height) + 1

    def nth_smallest(self, node, n):
        stack = []
        current = node
        count = 0

        while True:
            while current is not None:
                stack.append(current)
                current = current.left

            if not stack:
                return None

            current = stack.pop()
            count += 1

            if count == n:
                return current.val

            current = current.right

    def nodes_at_distance_n(self, node, n):
        result = []
        self._nodes_at_distance_n(node, n, result)
        return result

    def _nodes_at_distance_n(self, node, n, result):
        if node is None:
            return
        if n == 0:
            result.append(node.val)
        else:
            self._nodes_at_distance_n(node.left, n - 1, result)
            self._nodes_at_distance_n(node.right, n - 1, result)

    def find_ancestors(self, node, target):
        ancestors = []
        self._find_ancestors(self.root, target, ancestors)
        return ancestors

    def _find_ancestors(self, current, target, ancestors):
        if current is None:
            return False
        if current.val == target:
            return True

        if (self._find_ancestors(current.left, target, ancestors) or
                self._find_ancestors(current.right, target, ancestors)):
            ancestors.append(current.val)
            return True

        return False


# Пример использования
if __name__ == "__main__":
    tree = BinaryTree()
    elements = [20, 10, 30, 5, 15, 25, 35]
    for el in elements:
        tree.insert(el)

    print("Высота дерева:", tree.height(tree.root))
    print("3-й наименьший элемент:", tree.nth_smallest(tree.root, 3))
    print("Узлы на расстоянии 2 от корня:", tree.nodes_at_distance_n(tree.root, 2))
    print("Предки узла 15:", tree.find_ancestors(tree.root, 15))
