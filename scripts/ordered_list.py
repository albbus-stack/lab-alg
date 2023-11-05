from tester import Tester
from utils import Utils
from typing import Optional

class LinkedListNode:
    def __init__(self, value: int) -> None:
        self.value = value
        self.next: Optional[LinkedListNode] = None

class OrderedLinkedList:
    def __init__(self) -> None:
        self.head: Optional[LinkedListNode] = None

    def insert(self, value: int) -> None:
        new_node = LinkedListNode(value)
        if self.head is None or value < self.head.value:
            new_node.next = self.head
            self.head = new_node
        else:
            current = self.head
            while current.next is not None and current.next.value < value:
                current = current.next
            new_node.next = current.next
            current.next = new_node

    def os_select(self, k: int) -> Optional[int]:
        if not self.head or k < 1:
            return None

        current: Optional[LinkedListNode] = self.head
        count = 1

        while current:
            if count == k:
                return current.value
            current = current.next
            count += 1
        return None

    def os_rank(self, value: int) -> Optional[int]:
        if not self.head:
            return None

        current: Optional[LinkedListNode] = self.head
        rank = 1

        while current:
            if current.value == value:
                return rank
            current = current.next
            rank += 1
        return None