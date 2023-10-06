import random
from timeit import default_timer as timer
from utils import plot_and_table

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

if __name__ == "__main__":
    sizes = [1000, 5000, 10000, 25000, 50000]
    insertion_times = []
    removal_times = []
    os_select_times = []
    os_rank_times = []

    for size in sizes:
        _insertion_times = []
        _removal_times = []
        _os_select_times = []
        _os_rank_times = []

        for _ in range(20):
            red_black_tree = RedBlackTree()
            
            [elapsed_time, data] = test_rn_insertion(size, red_black_tree)
            _insertion_times.append(elapsed_time)

            elapsed_time = test_rn_os_select(size, red_black_tree)
            _os_select_times.append(elapsed_time)

            elapsed_time = test_rn_os_rank(red_black_tree, data)
            _os_rank_times.append(elapsed_time)

            elapsed_time = test_rn_removal(red_black_tree, data)
            _removal_times.append(elapsed_time)

        mean = sum(_insertion_times) / len(_insertion_times)
        insertion_times.append(mean)

        mean = sum(_os_select_times) / len(_os_select_times)
        os_select_times.append(mean)

        mean = sum(_os_rank_times) / len(_os_rank_times)
        os_rank_times.append(mean)

        mean = sum(_removal_times) / len(_removal_times)
        removal_times.append(mean)

    it = plot_and_table(sizes, insertion_times, caption="Inserimento in un albero RN aumentato", time_caption="Tempo di inserimento (s)")
    rt = plot_and_table(sizes, removal_times, caption="Rimozione in un albero RN aumentato", time_caption="Tempo di rimozione (s)")
    st = plot_and_table(sizes, os_select_times, caption="OS-Select in un albero RN aumentato", time_caption="Tempo di OS-Select (s)")
    kt = plot_and_table(sizes, os_rank_times, caption="OS-Rank in un albero RN aumentato", time_caption="Tempo di OS-Rank (s)")

    # Scrivi il codice LaTeX in un file .tex
    with open('tabelle-rn-aumentato.tex', 'w') as file:
      file.write('\n'.join([it, rt, st, kt]))