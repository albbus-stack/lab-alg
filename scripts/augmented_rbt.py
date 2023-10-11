import random
from timeit import default_timer as timer
import numpy as np
import utils
import statistics
from typing import Optional
from enum import Enum
from bst import TreeNode 

class Color(Enum):
    RED = 1
    BLACK = 2

class RedBlackTreeNode(TreeNode):
    def __init__(self, value: int, color: Color, size: int) -> None:
        super().__init__(value)
        self.color = color
        self.size = size
        self.left: Optional[RedBlackTreeNode] = None
        self.right: Optional[RedBlackTreeNode] = None

class RedBlackTree:
    def __init__(self) -> None:
        self.root: Optional[RedBlackTreeNode] = None

    def insert(self, value: int) -> None:
        self.root = self._insert_recursive(self.root, value)

    def _insert_recursive(self, root: Optional[RedBlackTreeNode], value: int) -> Optional[RedBlackTreeNode]:
        if root is None:
            return RedBlackTreeNode(value, Color.RED, 1)

        if value < root.value:
            root.left = self._insert_recursive(root.left, value)
        elif value > root.value:
            root.right = self._insert_recursive(root.right, value)

        # Bilancia l'albero
        if self.is_red(root.right) and not self.is_red(root.left):
            root = self.rotate_left(root)
        if root and root.left and self.is_red(root.left) and self.is_red(root.left.left):
            root = self.rotate_right(root)
        if root and self.is_red(root.left) and self.is_red(root.right):
            self.flip_colors(root)

        if root: root.size = 1 + self.size(root.left) + self.size(root.right)
        return root

    def os_select(self, k: int) -> Optional[int]:
        return self._os_select_recursive(self.root, k)

    def _os_select_recursive(self, root: Optional[RedBlackTreeNode], k: int) -> Optional[int]:
        if root is None:
            return None

        left_size = self.size(root.left)
        if left_size == k - 1:
            return root.value
        elif left_size > k - 1:
            return self._os_select_recursive(root.left, k)
        else:
            return self._os_select_recursive(root.right, k - left_size - 1)

    def os_rank(self, value: int) -> Optional[int]:
        return self._os_rank_recursive(self.root, value)

    def _os_rank_recursive(self, root: Optional[RedBlackTreeNode], value: int) -> Optional[int]:
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

    def size(self, root: Optional[RedBlackTreeNode]) -> int:
        if root is None:
            return 0
        return root.size

    def is_red(self, node: Optional[RedBlackTreeNode]) -> bool:
        if node is None:
            return False
        return node.color == Color.RED

    def rotate_left(self, h: RedBlackTreeNode) -> Optional[RedBlackTreeNode]:
        if not h.right: return None
        x: RedBlackTreeNode = h.right
        h.right = x.left
        x.left = h
        x.color = h.color
        h.color = Color.RED
        x.size = h.size
        h.size = 1 + self.size(h.left) + self.size(h.right)
        return x

    def rotate_right(self, h: RedBlackTreeNode) -> Optional[RedBlackTreeNode]:
        if not h.left: return None
        x: RedBlackTreeNode = h.left
        h.left = x.right
        x.right = h
        x.color = h.color
        h.color = Color.RED
        x.size = h.size
        h.size = 1 + self.size(h.left) + self.size(h.right)
        return x

    def flip_colors(self, h: RedBlackTreeNode):
        h.color = Color.RED
        if h.left: h.left.color = Color.BLACK
        if h.right: h.right.color = Color.BLACK

# Esegue i test per ogni dimensione con un certo numero di iterazioni
def test_augmented_rbt(sizes: list[int], iterations: int):
    os_rank_times = []
    os_select_times = []

    for size in sizes:
        _os_rank_times = []
        _os_select_times = []

        for i in range(iterations):
            print('ARN - Dimensione:', size, 'Iterazione:', i+1)

            red_black_tree = RedBlackTree()

            data = [random.randint(1, 1000) for _ in range(size)]
            # Inserimento dati di test
            for item in data:
                red_black_tree.insert(item)

            # Esecuzione dei test sulle statistiche d'ordine
            start_time = timer()
            for k in range(size):
                red_black_tree.os_select(k+1)
            end_time = timer()

            _os_select_times.append(end_time - start_time)

            start_time = timer()
            for k in data:
                red_black_tree.os_rank(k)
            end_time = timer()

            _os_rank_times.append(end_time - start_time)
        
        os_select_times.append((statistics.median(_os_select_times), np.std(_os_select_times)))
        os_rank_times.append((statistics.median(_os_rank_times), np.std(_os_rank_times)))

    # Generazione dei grafici e delle tabelle in latex
    return (utils.data_and_table(sizes, os_select_times, caption="OS-Select in un albero RN aumentato"),
            utils.data_and_table(sizes, os_rank_times, caption="OS-Rank in un albero RN aumentato"))

if __name__ == "__main__":
    #sizes = [100, 1000, 2500, 5000, 7500]
    sizes = [10, 20, 30, 40, 50, 60, 70, 80, 100, 500, 1000, 2000, 3000, 4000, 5000]
    iterations = 50

    ((st, mst, dst), (kt, mkt, dkt)) = test_augmented_rbt(sizes, iterations)
    utils.plot(sizes, mst, dst)
    utils.save_plot("rn-os-select", title="OS-Select in un albero RN aumentato")
    utils.clear_plot()

    utils.plot(sizes, mkt, dkt)
    utils.save_plot("rn-os-rank", title="OS-Rank in un albero RN aumentato")

    utils.write_to_latex_file('tabelle-rn-aumentato.tex', [st, kt])
    