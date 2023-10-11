import random
from timeit import default_timer as timer
import numpy as np
from utils import Utils
import statistics
from typing import Optional

class TreeNode:
    def __init__(self, value: int) -> None:
        self.value = value
        self.left: Optional[TreeNode] = None
        self.right: Optional[TreeNode] = None

class BinarySearchTree:
    def __init__(self) -> None:
        self.root: Optional[TreeNode] = None

    def insert(self, value: int) -> None:
        self.root = self._insert_recursive(self.root, value)

    def _insert_recursive(self, root: Optional[TreeNode], value: int) -> TreeNode:
        if root is None:
            return TreeNode(value)
        if value < root.value:
            root.left = self._insert_recursive(root.left, value)
        elif value > root.value:
            root.right = self._insert_recursive(root.right, value)
        return root

    def os_select(self, k: int) -> Optional[int]:
        return self._os_select_recursive(self.root, k)

    def _os_select_recursive(self, root: Optional[TreeNode], k: int) -> Optional[int]:
        if root is None:
            return None

        left_size = self._tree_size(root.left)
        if left_size == k - 1:
            return root.value
        elif left_size > k - 1:
            return self._os_select_recursive(root.left, k)
        else:
            return self._os_select_recursive(root.right, k - left_size - 1)

    def _tree_size(self, root: Optional[TreeNode]) -> int:
        if root is None:
            return 0
        return 1 + self._tree_size(root.left) + self._tree_size(root.right)

    def os_rank(self, value: int) -> Optional[int]:
        return self._os_rank_recursive(self.root, value)

    def _os_rank_recursive(self, root: Optional[TreeNode], value: int) -> Optional[int]:
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

def test_bst(sizes: list[int], iterations: int):
    os_rank_times = []
    os_select_times = []

    for size in sizes:
        _os_rank_times = []
        _os_select_times = []

        for i in range(iterations):
            print('ABR - Dimensione:', size, 'Iterazione:', i+1)

            binary_search_tree = BinarySearchTree()

            data = [random.randint(1, 1000) for _ in range(size)]
            for item in data:
                binary_search_tree.insert(item)

            start_time = timer()
            for k in range(size):
                binary_search_tree.os_select(k+1)
            end_time = timer()

            _os_select_times.append(end_time - start_time)

            start_time = timer()
            for value in data:
                binary_search_tree.os_rank(value)
            end_time = timer()

            _os_rank_times.append(end_time - start_time)

        os_select_times.append((statistics.median(_os_select_times), np.std(_os_select_times)))
        os_rank_times.append((statistics.median(_os_rank_times), np.std(_os_rank_times)))

    return (Utils.data_and_table(sizes, os_select_times, caption="OS-Select in un ABR"), 
            Utils.data_and_table(sizes, os_rank_times, caption="OS-Rank in un ABR"))

if __name__ == "__main__":
    # sizes = [100, 1000, 2500, 5000, 7500, 10000, 15000, 20000, 25000]
    sizes = [10, 20, 30, 40, 50, 60, 70, 80, 100, 200, 300, 400, 500]
    iterations = 50

    ((st, mst, dst), (kt, mkt, dkt))  = test_bst(sizes, iterations)
    Utils.plot(sizes, mst, dst)
    Utils.save_plot("abr-os-select", title="OS-Select in un ABR")
    Utils.clear_plot()

    Utils.plot(sizes, mkt, dkt)
    Utils.save_plot("abr-os-rank", title="OS-Rank in un ABR")
    
    Utils.write_to_latex_file('tabelle-abr.tex', [st, kt])