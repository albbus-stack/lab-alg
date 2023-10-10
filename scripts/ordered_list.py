import random
from timeit import default_timer as timer
import numpy as np
import utils
import statistics
from typing import Optional

class Node:
    def __init__(self, value: int) -> None:
        self.value = value
        self.next: Optional[Node] = None

class OrderedLinkedList:
    def __init__(self) -> None:
        self.head: Optional[Node] = None

    def insert(self, value: int) -> None:
        new_node = Node(value)
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

        current: Optional[Node] = self.head
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

        current: Optional[Node] = self.head
        rank = 1

        while current:
            if current.value == value:
                return rank
            current = current.next
            rank += 1
        return None

# Funzione per eseguire il test di inserimento
def test_insertion(ordered_list: OrderedLinkedList, size: int) -> tuple[float, list[int]]:
    data = [random.randint(1, 1000) for _ in range(size)]
    start_time = timer()
    for item in data:
        ordered_list.insert(item)
    end_time = timer()

    return (end_time - start_time, data)

# Funzione per eseguire il test di os-select
def test_os_select(ordered_list: OrderedLinkedList, size: int) -> float:
    start_time = timer()
    for k in [random.randint(1, size) for _ in range(size)]:
        ordered_list.os_select(k)
    end_time = timer()

    return end_time - start_time

# Funzione per eseguire il test di os-rank
def test_os_rank(ordered_list: OrderedLinkedList, data: list[int]) -> float:
    start_time = timer()
    for k in data:
        ordered_list.os_rank(k)
    end_time = timer()

    return end_time - start_time

def test_ordered_list(sizes: list[int], iterations: int) -> None:
    os_select_times = []
    os_rank_times = []

    for size in sizes:
        _os_select_times = []
        _os_rank_times = []

        for i in range(iterations):
            print('LL - Dimensione:', size, 'Iterazione:', i+1)

            ordered_list = OrderedLinkedList()

            elapsed_time, data = test_insertion(ordered_list, size)

            elapsed_time = test_os_select(ordered_list, size)
            _os_select_times.append(elapsed_time)

            elapsed_time = test_os_rank(ordered_list, data)
            _os_rank_times.append(elapsed_time)

        os_select_times.append((statistics.median(_os_select_times), np.std(_os_select_times)))
        os_rank_times.append((statistics.median(_os_rank_times), np.std(_os_rank_times)))

    st = utils.plot_and_table(sizes, os_select_times, std=True, caption="OS-Select in una lista ordinata", plot_filename="os-select-lista")
    kt = utils.plot_and_table(sizes, os_rank_times, std=True, caption="OS-Rank in una lista ordinata",  plot_filename="os-rank-lista")

    # Scrivi il codice LaTeX in un file .tex
    utils.write_to_latex_file('tabelle-lista-ordinata.tex', [st, kt])

if __name__ == "__main__":
    # sizes = [100, 1000, 2500, 5000, 7500, 10000, 15000, 20000, 25000]
    sizes = [10, 20, 30, 40, 50, 60, 70, 80, 100]
    iterations = 50

    test_ordered_list(sizes, iterations)