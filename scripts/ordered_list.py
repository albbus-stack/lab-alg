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
    sizes = [10, 20, 30, 40, 50, 60, 70, 80, 100, 200, 300, 400, 500, 1000, 1500]
    iterations = 100

    ((st, mst, dst), (kt, mkt, dkt), (st_rel, mst_rel, dst_rel), (kt_rel, mkt_rel, dkt_rel)) = Tester.test_ordered_list(sizes, iterations)
    Utils.plot(sizes, mst, dst, "OS-Select")
    Utils.plot(sizes, mkt, dkt, "OS-Rank")
    Utils.save_plot("lista-ordinata", title="OS-Select e OS-Rank in una lista ordinata")
    Utils.clear_plot()

    Utils.plot(sizes, mst_rel, dst_rel, "OS-Select")
    Utils.plot(sizes, mkt_rel, dkt_rel, "OS-Rank")
    Utils.save_plot("lista-ordinata-rel", title="OS-Select e OS-Rank relativi in una lista ordinata")
    Utils.clear_plot()

    ((st, mst, dst), (kt, mkt, dkt), (st_rel, mst_rel, dst_rel), (kt_rel, mkt_rel, dkt_rel)) = Tester.test_ordered_list(sizes, iterations, is_float_test=True)
    Utils.plot(sizes, mst, dst, "OS-Select")
    Utils.plot(sizes, mkt, dkt, "OS-Rank")
    Utils.save_plot("lista-ordinata-float", title="OS-Select e OS-Rank in una lista ordinata con float")
    Utils.clear_plot()

    Utils.plot(sizes, mst_rel, dst_rel, "OS-Select")
    Utils.plot(sizes, mkt_rel, dkt_rel, "OS-Rank")
    Utils.save_plot("lista-ordinata-float-rel", title="OS-Select e OS-Rank relativi in una lista ordinata con float")