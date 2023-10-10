import random
from timeit import default_timer as timer
import numpy as np
import utils
import statistics
from enum import Enum

class Color(Enum):
    RED = 1
    BLACK = 2

class RedBlackTreeNode:
    def __init__(self, value: int, color: Color, size: int):
        self.value = value
        self.color = color
        self.size = size
        self.left = None
        self.right = None

class RedBlackTree:
    def __init__(self):
        self.root = None

    def insert(self, value: int):
        self.root = self._insert_recursive(self.root, value)

    def _insert_recursive(self, root: RedBlackTreeNode | None, value: int):
        if root is None:
            return RedBlackTreeNode(value, Color.RED, 1)

        if value < root.value:
            root.left = self._insert_recursive(root.left, value)
        elif value > root.value:
            root.right = self._insert_recursive(root.right, value)

        # Bilancia l'albero
        if self.is_red(root.right) and not self.is_red(root.left):
            root = self.rotate_left(root)
        if self.is_red(root.left) and self.is_red(root.left.left):
            root = self.rotate_right(root)
        if self.is_red(root.left) and self.is_red(root.right):
            self.flip_colors(root)

        root.size = 1 + self.size(root.left) + self.size(root.right)
        return root

    def os_select(self, k: int):
        return self._os_select_recursive(self.root, k)

    def _os_select_recursive(self, root: RedBlackTreeNode | None, k: int):
        if root is None:
            return None

        left_size = self.size(root.left)
        if left_size == k - 1:
            return root.value
        elif left_size > k - 1:
            return self._os_select_recursive(root.left, k)
        else:
            return self._os_select_recursive(root.right, k - left_size - 1)

    def os_rank(self, value: int):
        return self._os_rank_recursive(self.root, value)

    def _os_rank_recursive(self, root: RedBlackTreeNode | None, value: int):
        if root is None:
            return None

        if value == root.value:
            return self.size(root.left) + 1

        if value < root.value:
            return self._os_rank_recursive(root.left, value)
        else:
            right_rank = self._os_rank_recursive(root.right, value)
            if right_rank is not None:
                return self.size(root.left) + 1 + right_rank
            else:
                return None

    def size(self, root: RedBlackTreeNode | None):
        if root is None:
            return 0
        return root.size

    def is_red(self, node: RedBlackTreeNode | None):
        if node is None:
            return False
        return node.color == Color.RED

    def rotate_left(self, h: RedBlackTreeNode):
        x = h.right
        h.right = x.left
        x.left = h
        x.color = h.color
        h.color = Color.RED
        x.size = h.size
        h.size = 1 + self.size(h.left) + self.size(h.right)
        return x

    def rotate_right(self, h: RedBlackTreeNode):
        x = h.left
        h.left = x.right
        x.right = h
        x.color = h.color
        h.color = Color.RED
        x.size = h.size
        h.size = 1 + self.size(h.left) + self.size(h.right)
        return x

    def flip_colors(self, h: RedBlackTreeNode):
        h.color = Color.RED
        h.left.color = Color.BLACK
        h.right.color = Color.BLACK

# Funzione per eseguire l'inserimento dei dati
def test_rn_insertion(red_black_tree: RedBlackTree, size: int):
    data = [random.randint(1, 1000) for _ in range(size)]
    start_time = timer()
    for item in data:
        red_black_tree.insert(item)
    end_time = timer()

    return [end_time - start_time, data]

# Funzione di test per OS-select
def test_rn_os_select(red_black_tree: RedBlackTree, size: int):
    start_time = timer()
    for k in [random.randint(1, size) for _ in range(size)]:
        red_black_tree.os_select(k)
    end_time = timer()

    return end_time - start_time

# Funzione di test per OS-rank
def test_rn_os_rank(red_black_tree: RedBlackTree, data: list[int]):
    start_time = timer()
    for k in data:
        red_black_tree.os_rank(k)
    end_time = timer()

    return end_time - start_time

# Esegue i test per ogni dimensione con un certo numero di iterazioni
def test_augmented_rbt(sizes: list[int], iterations: int):
    os_select_times = []
    os_rank_times = []

    for size in sizes:
        _os_select_times = []
        _os_rank_times = []

        for i in range(iterations):
            print('ARN - Dimensione:', size, 'Iterazione:', i+1)

            red_black_tree = RedBlackTree()

            [elapsed_time, data] = test_rn_insertion(red_black_tree, size)

            elapsed_time = test_rn_os_select(red_black_tree, size)
            _os_select_times.append(elapsed_time)

            elapsed_time = test_rn_os_rank(red_black_tree, data)
            _os_rank_times.append(elapsed_time)

        os_select_times.append((statistics.median(_os_select_times), np.std(_os_select_times)))
        os_rank_times.append((statistics.median(_os_rank_times), np.std(_os_rank_times)))

    st = utils.plot_and_table(sizes, os_select_times, std=True, caption="OS-Select in un albero RN aumentato", plot_filename="os-select-rn")
    kt = utils.plot_and_table(sizes, os_rank_times, std=True, caption="OS-Rank in un albero RN aumentato", plot_filename="os-rank-rn")

    # Scrivi il codice LaTeX in un file .tex
    utils.write_to_latex_file('tabelle-rn-aumentato.tex', [st, kt])

if __name__ == "__main__":
    # sizes = [100, 1000, 2500, 5000, 7500, 10000, 15000, 20000, 25000]
    sizes = [10, 20, 30, 40, 50, 60, 70, 80, 100]
    iterations = 50

    test_augmented_rbt(sizes, iterations)