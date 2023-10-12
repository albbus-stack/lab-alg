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

if __name__ == "__main__":
    # sizes = [100, 1000, 2500, 5000, 7500, 10000, 15000, 20000, 25000]
    sizes = [10, 20, 30, 40, 50, 60, 70, 80, 100, 200, 300, 400, 500]
    iterations = 50

    ((st, mst, dst), (kt, mkt, dkt)) = Tester.test_ordered_list(sizes, iterations)
    Utils.plot(sizes, mst, dst)
    Utils.save_plot("lista-os-select", title="OS-Select in una lista ordinata")
    Utils.clear_plot()

    Utils.plot(sizes, mkt, dkt)
    Utils.save_plot("lista-os-rank", title="OS-Rank in una lista ordinata")

    Utils.write_to_latex_file('tabelle-lista-ordinata.tex', [st, kt])
