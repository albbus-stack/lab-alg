from tester import Tester
from utils import Utils
from typing import Optional
from enum import Enum
from bst import TreeNode
import numpy as np

class Color(Enum):
    RED = 0
    BLACK = 1

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
        if self._is_red(root.right) and not self._is_red(root.left):
            root = self._rotate_left(root)
        if root and root.left and self._is_red(root.left) and self._is_red(root.left.left):
            root = self._rotate_right(root)
        if root and self._is_red(root.left) and self._is_red(root.right):
            self._flip_colors(root)

        if root: root.size = 1 + self._size(root.left) + self._size(root.right)
        return root

    def os_select(self, k: int) -> Optional[int]:
        return self._os_select_recursive(self.root, k)

    def _os_select_recursive(self, root: Optional[RedBlackTreeNode], k: int) -> Optional[int]:
        if root is None:
            return None

        left_size = self._size(root.left)
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
            return self._size(root.left) + 1

        if value < root.value:
            return self._os_rank_recursive(root.left, value)
        else:
            right_rank = self._os_rank_recursive(root.right, value)
            if right_rank is not None:
                return self._size(root.left) + 1 + right_rank
            else:
                return None

    def _size(self, root: Optional[RedBlackTreeNode]) -> int:
        if root is None:
            return 0
        return root.size

    def _is_red(self, node: Optional[RedBlackTreeNode]) -> bool:
        if node is None:
            return False
        return node.color == Color.RED

    def _rotate_left(self, h: RedBlackTreeNode) -> Optional[RedBlackTreeNode]:
        if not h.right: return None
        x: RedBlackTreeNode = h.right
        h.right = x.left
        x.left = h
        x.color = h.color
        h.color = Color.RED
        x.size = h.size
        h.size = 1 + self._size(h.left) + self._size(h.right)
        return x

    def _rotate_right(self, h: RedBlackTreeNode) -> Optional[RedBlackTreeNode]:
        if not h.left: return None
        x: RedBlackTreeNode = h.left
        h.left = x.right
        x.right = h
        x.color = h.color
        h.color = Color.RED
        x.size = h.size
        h.size = 1 + self._size(h.left) + self._size(h.right)
        return x

    def _flip_colors(self, h: RedBlackTreeNode) -> None:
        h.color = Color.RED
        if h.left: h.left.color = Color.BLACK
        if h.right: h.right.color = Color.BLACK