import random
from timeit import default_timer as timer
import numpy as np
import utils
import statistics

class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, value):
        self.root = self._insert_recursive(self.root, value)

    def _insert_recursive(self, root, value):
        if root is None:
            return TreeNode(value)
        if value < root.value:
            root.left = self._insert_recursive(root.left, value)
        elif value > root.value:
            root.right = self._insert_recursive(root.right, value)
        return root

    def os_select(self, k):
        return self._os_select_recursive(self.root, k)

    def _os_select_recursive(self, root, k):
        if root is None:
            return None

        left_size = self._tree_size(root.left)
        if left_size == k - 1:
            return root.value
        elif left_size > k - 1:
            return self._os_select_recursive(root.left, k)
        else:
            return self._os_select_recursive(root.right, k - left_size - 1)

    def _tree_size(self, root):
        if root is None:
            return 0
        return 1 + self._tree_size(root.left) + self._tree_size(root.right)

    def os_rank(self, value):
        return self._os_rank_recursive(self.root, value)

    def _os_rank_recursive(self, root, value):
        if root is None:
            return None

        if value == root.value:
            return self._tree_size(root.left) + 1

        if value < root.value:
            return self._os_rank_recursive(root.left, value)
        else:
            right_rank = self._os_rank_recursive(root.right, value)
            if right_rank is not None:
                return self._tree_size(root.left) + 1 + right_rank
            else:
                return None

# Funzione per eseguire il test di inserimento
def test_abr_insertion(binary_search_tree, size):
    data = [random.randint(1, 1000) for _ in range(size)]
    start_time = timer()
    for item in data:
        binary_search_tree.insert(item)
    end_time = timer()

    return [end_time - start_time, data]

# Funzione per eseguire il test di os-select
def test_abr_os_select(binary_search_tree, size):
    start_time = timer()
    for k in [random.randint(1, size) for _ in range(size)]:
        binary_search_tree.os_select(k)
    end_time = timer()

    return end_time - start_time

# Funzione per eseguire il test di os-rank
def test_abr_os_rank(binary_search_tree, data):
    start_time = timer()
    for value in data:
        binary_search_tree.os_rank(value)
    end_time = timer()

    return end_time - start_time

def test_bst(sizes, iterations):
    os_select_times = []
    os_rank_times = []

    for size in sizes:
        _os_select_times = []
        _os_rank_times = []

        for i in range(iterations):
            print('ABR - Dimensione:', size, 'Iterazione:', i+1)

            binary_search_tree = BinarySearchTree()

            [elapsed_time, data] = test_abr_insertion(binary_search_tree, size)

            elapsed_time = test_abr_os_select(binary_search_tree, size)
            _os_select_times.append(elapsed_time)

            elapsed_time = test_abr_os_rank(binary_search_tree, data)
            _os_rank_times.append(elapsed_time)

        os_select_times.append((statistics.median(_os_select_times), np.std(_os_select_times)))
        os_rank_times.append((statistics.median(_os_rank_times), np.std(_os_rank_times)))

    st = utils.plot_and_table(sizes, os_select_times, std=True, caption="OS-Select in un ABR", plot_filename="os-select-abr")
    kt = utils.plot_and_table(sizes, os_rank_times, std=True, caption="OS-Rank in un ABR", plot_filename="os-rank-abr")

    # Scrivi il codice LaTeX in un file .tex
    utils.write_to_latex_file('tabelle-abr.tex', [st, kt])

if __name__ == "__main__":
    # sizes = [100, 1000, 2500, 5000, 7500, 10000, 15000, 20000, 25000]
    sizes = [10, 20, 30, 40, 50, 60, 70, 80, 100]
    iterations = 50

    test_bst(sizes, iterations)