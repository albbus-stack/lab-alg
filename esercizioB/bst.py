from tester import Tester
from utils import Utils
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