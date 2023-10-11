import random
from timeit import default_timer as timer
import numpy as np
import utils
import statistics
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

def test_ordered_list(sizes: list[int], iterations: int):
    os_rank_times = []
    os_select_times = []

    for size in sizes:
        _os_rank_times = []
        _os_select_times = []

        for i in range(iterations):
            print('LL - Dimensione:', size, 'Iterazione:', i+1)

            ordered_list = OrderedLinkedList()

            data = [random.randint(1, 1000) for _ in range(size)]
            for item in data:
                ordered_list.insert(item)

            start_time = timer()
            for k in range(size):
                ordered_list.os_select(k+1)
            end_time = timer()

            _os_select_times.append(end_time - start_time)

            start_time = timer()
            for k in data:
                ordered_list.os_rank(k)
            end_time = timer()

            _os_rank_times.append(end_time - start_time)

        os_select_times.append((statistics.median(_os_select_times), np.std(_os_select_times)))
        os_rank_times.append((statistics.median(_os_rank_times), np.std(_os_rank_times)))

    return (utils.data_and_table(sizes, os_select_times, caption="OS-Select in una lista ordinata"), 
            utils.data_and_table(sizes, os_rank_times, caption="OS-Rank in una lista ordinata"))

if __name__ == "__main__":
    # sizes = [100, 1000, 2500, 5000, 7500, 10000, 15000, 20000, 25000]
    sizes = [10, 20, 30, 40, 50, 60, 70, 80, 100, 200, 300, 400, 500]
    iterations = 50

    ((st, mst, dst), (kt, mkt, dkt)) = test_ordered_list(sizes, iterations)
    utils.plot(sizes, mst, dst)
    utils.save_plot("lista-os-select", title="OS-Select in una lista ordinata")
    utils.clear_plot()

    utils.plot(sizes, mkt, dkt)
    utils.save_plot("lista-os-rank", title="OS-Rank in una lista ordinata")

    utils.write_to_latex_file('tabelle-lista-ordinata.tex', [st, kt])
