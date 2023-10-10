import random
from timeit import default_timer as timer
import numpy as np
import utils
import statistics

class RedBlackTreeNode:
    def __init__(self, key, color, size):
        self.key = key
        self.color = color  # "R" per rosso, "B" per nero
        self.size = size
        self.left = None
        self.right = None

class RedBlackTree:
    def __init__(self):
        self.root = None

    def insert(self, key):
        self.root = self._insert_recursive(self.root, key)

    def _insert_recursive(self, root, key):
        if root is None:
            return RedBlackTreeNode(key, "R", 1)

        if key < root.key:
            root.left = self._insert_recursive(root.left, key)
        elif key > root.key:
            root.right = self._insert_recursive(root.right, key)

        # Bilancia l'albero
        if self.is_red(root.right) and not self.is_red(root.left):
            root = self.rotate_left(root)
        if self.is_red(root.left) and self.is_red(root.left.left):
            root = self.rotate_right(root)
        if self.is_red(root.left) and self.is_red(root.right):
            self.flip_colors(root)

        root.size = 1 + self.size(root.left) + self.size(root.right)
        return root

    def remove(self, key):
        if self.root is not None:
            self.root = self._remove_recursive(self.root, key)

    def _remove_recursive(self, root, key):
        if root is None:
            return None

        if key < root.key:
            root.left = self._remove_recursive(root.left, key)
        elif key > root.key:
            root.right = self._remove_recursive(root.right, key)
        else:
            if root.left is None:
                return root.right
            elif root.right is None:
                return root.left

            min_right = self._find_min_key(root.right)
            root.key = min_right.key
            root.right = self._remove_recursive(root.right, min_right.key)

        root.size = 1 + self.size(root.left) + self.size(root.right)

        # Bilancia l'albero dopo la rimozione
        if self.is_red(root.right) and not self.is_red(root.left):
            root = self.rotate_left(root)
        if self.is_red(root.left) and self.is_red(root.left.left):
            root = self.rotate_right(root)
        if self.is_red(root.left) and self.is_red(root.right):
            self.flip_colors(root)
        return root

    def _find_min_key(self, root):
        while root.left is not None:
            root = root.left
        return root

    def search(self, key):
        return self._search_recursive(self.root, key)

    def _search_recursive(self, root, key):
        if root is None:
            return False
        if root.key == key:
            return True
        if key < root.key:
            return self._search_recursive(root.left, key)
        return self._search_recursive(root.right, key)

    def os_select(self, k):
        return self._os_select_recursive(self.root, k)

    def _os_select_recursive(self, root, k):
        if root is None:
            return None

        left_size = self.size(root.left)
        if left_size == k - 1:
            return root.key
        elif left_size > k - 1:
            return self._os_select_recursive(root.left, k)
        else:
            return self._os_select_recursive(root.right, k - left_size - 1)

    def os_rank(self, value):
        return self._os_rank_recursive(self.root, value)

    def _os_rank_recursive(self, root, value):
        if root is None:
            return None

        if value == root.key:
            return self.size(root.left) + 1

        if value < root.key:
            return self._os_rank_recursive(root.left, value)
        else:
            right_rank = self._os_rank_recursive(root.right, value)
            if right_rank is not None:
                return self.size(root.left) + 1 + right_rank
            else:
                return None

    def size(self, root):
        if root is None:
            return 0
        return root.size

    def is_red(self, node):
        if node is None:
            return False
        return node.color == "R"

    def rotate_left(self, h):
        x = h.right
        h.right = x.left
        x.left = h
        x.color = h.color
        h.color = "R"
        x.size = h.size
        h.size = 1 + self.size(h.left) + self.size(h.right)
        return x

    def rotate_right(self, h):
        x = h.left
        h.left = x.right
        x.right = h
        x.color = h.color
        h.color = "R"
        x.size = h.size
        h.size = 1 + self.size(h.left) + self.size(h.right)
        return x

    def flip_colors(self, h):
        h.color = "R"
        h.left.color = "B"
        h.right.color = "B"

# Funzione per eseguire il test di inserimento
def test_rn_insertion(size, red_black_tree):
    data = [random.randint(1, 1000) for _ in range(size)]
    start_time = timer()
    for item in data:
        red_black_tree.insert(item)
    end_time = timer()

    return [end_time - start_time, data]

# Funzione per eseguire il test di ricerca
def test_rn_search(red_black_tree, data):
    start_time = timer()
    for item in data:
        red_black_tree.search(item)
    end_time = timer()

    return end_time - start_time

# Funzione per eseguire il test di OS-select
def test_rn_os_select(size, red_black_tree):
    start_time = timer()
    for k in [random.randint(1, size) for _ in range(size)]:
        red_black_tree.os_select(k)
    end_time = timer()

    return end_time - start_time

# Funzione per eseguire il test di OS-rank
def test_rn_os_rank(red_black_tree, data):
    start_time = timer()
    for k in data:
        red_black_tree.os_rank(k)
    end_time = timer()

    return end_time - start_time

# Funzione per eseguire il test di rimozione
def test_rn_removal(red_black_tree, data):
    # Rimozione degli elementi
    start_time = timer()
    for item in data:
        red_black_tree.remove(item)
    end_time = timer()

    return end_time - start_time

def test_augmented_rbt(sizes, iterations):
    insertion_times = []
    search_times = []
    removal_times = []
    os_select_times = []
    os_rank_times = []

    for size in sizes:
        _insertion_times = []
        _search_times = []
        _removal_times = []
        _os_select_times = []
        _os_rank_times = []

        for i in range(iterations):
            print('ARN - Dimensione:', size, 'Iterazione:', i+1)

            red_black_tree = RedBlackTree()

            [elapsed_time, data] = test_rn_insertion(size, red_black_tree)
            # _insertion_times.append(elapsed_time)

            # elapsed_time = test_rn_search(red_black_tree, data)
            # _search_times.append(elapsed_time)

            elapsed_time = test_rn_os_select(size, red_black_tree)
            _os_select_times.append(elapsed_time)

            elapsed_time = test_rn_os_rank(red_black_tree, data)
            _os_rank_times.append(elapsed_time)

            # elapsed_time = test_rn_removal(red_black_tree, data)
            # _removal_times.append(elapsed_time)

        # insertion_times.append((np.mean(_insertion_times), np.std(_insertion_times)))
        # search_times.append((np.mean(_search_times), np.std(_search_times)))
        os_select_times.append((statistics.median(_os_select_times), np.std(_os_select_times)))
        os_rank_times.append((statistics.median(_os_rank_times), np.std(_os_rank_times)))
        # removal_times.append((np.mean(_removal_times), np.std(_removal_times)))

    # it = plot_and_table(sizes, insertion_times, std=True, caption="Inserimento in un albero RN aumentato", time_caption="Tempo di inserimento (s)")
    it = ""
    # rt = plot_and_table(sizes, removal_times, std=True, caption="Rimozione in un albero RN aumentato", time_caption="Tempo di rimozione (s)")
    rt = ""
    # ht = plot_and_table(sizes, search_times, std=True, caption="Ricerca in un albero RN aumentato", time_caption="Tempo di ricerca (s)")
    ht = ""
    st = utils.plot_and_table(sizes, os_select_times, std=True, caption="OS-Select in un albero RN aumentato", plot_filename="os-select-rn")
    kt = utils.plot_and_table(sizes, os_rank_times, std=True, caption="OS-Rank in un albero RN aumentato", plot_filename="os-rank-rn")

    # Scrivi il codice LaTeX in un file .tex
    utils.write_to_latex_file('tabelle-rn-aumentato.tex', [it, rt, ht, st, kt])

if __name__ == "__main__":
    # sizes = [100, 1000, 2500, 5000, 7500, 10000, 15000, 20000, 25000]
    sizes = [10, 20, 30, 40, 50, 60, 70, 80, 100]
    iterations = 50

    test_augmented_rbt(sizes, iterations)