import random
from timeit import default_timer as timer
import numpy as np
import utils
import statistics

class Node:
    def __init__(self, data):
        self.data = data
        self.next: Node | None = None

class OrderedLinkedList:
    def __init__(self):
        self.head = None

    def insert(self, value):
        new_node = Node(value)
        if self.head is None or value < self.head.data:
            new_node.next = self.head
            self.head = new_node
        else:
            current = self.head
            while current.next is not None and current.next.data < value:
                current = current.next
            new_node.next = current.next
            current.next = new_node

    def remove(self, value):
        current = self.head
        previous = None
        found = False

        while current is not None and not found:
            if current.data == value:
                found = True
            else:
                previous = current
                current = current.next

        if found and current is not None:
            if previous is None:
                self.head = current.next
            else:
                previous.next = current.next

    def search(self, value):
        current = self.head
        while current is not None:
            if current.data == value:
                return True
            current = current.next
        return False

    def os_select(self, k):
        if not self.head or k < 1:
            return None

        current = self.head
        count = 1

        while current:
            if count == k:
                return current.data
            current = current.next
            count += 1
        return None

    def os_rank(self, value):
        if not self.head:
            return None

        current = self.head
        rank = 1

        while current:
            if current.data == value:
                return rank
            current = current.next
            rank += 1
        return None

# Funzione per eseguire il test di inserimento
def test_insertion(size, ordered_list):
    data = [random.randint(1, 1000) for _ in range(size)]
    start_time = timer()
    for item in data:
        ordered_list.insert(item)
    end_time = timer()

    return [end_time - start_time, data]

# Funzione per eseguire il test di ricerca
def test_search(ordered_list, data):
    start_time = timer()
    for item in data:
        ordered_list.search(item)
    end_time = timer()

    return end_time - start_time

# Funzione per eseguire il test di rimozione
def test_removal(ordered_list, data):
    # Rimozione degli elementi
    start_time = timer()
    for item in data:
        ordered_list.remove(item)
    end_time = timer()

    return end_time - start_time

# Funzione per eseguire il test di os-select
def test_os_select(size, ordered_list):
    start_time = timer()
    for k in [random.randint(1, size) for _ in range(size)]:
        ordered_list.os_select(k)
    end_time = timer()

    return end_time - start_time

# Funzione per eseguire il test di os-rank
def test_os_rank(ordered_list, data):
    start_time = timer()
    for k in data:
        ordered_list.os_rank(k)
    end_time = timer()

    return end_time - start_time

def test_linked_list(sizes, iterations):
    insertion_times = []
    removal_times = []
    search_times = []
    os_select_times = []
    os_rank_times = []

    for size in sizes:
        _insertion_times = []
        _removal_times = []
        _search_times = []
        _os_select_times = []
        _os_rank_times = []

        for i in range(iterations):
            print('LL - Dimensione:', size, 'Iterazione:', i+1)

            ordered_list = OrderedLinkedList()

            [elapsed_time, data] = test_insertion(size, ordered_list)
            # _insertion_times.append(elapsed_time)

            # elapsed_time = test_search(ordered_list, data)
            # _search_times.append(elapsed_time)

            elapsed_time = test_os_select(size, ordered_list)
            _os_select_times.append(elapsed_time)

            elapsed_time = test_os_rank(ordered_list, data)
            _os_rank_times.append(elapsed_time)

            # elapsed_time = test_removal(ordered_list, data)
            # _removal_times.append(elapsed_time)

        # insertion_times.append((np.mean(_insertion_times), np.std(_insertion_times)))
        # search_times.append((np.mean(_search_times), np.std(_search_times)))
        os_select_times.append((statistics.median(_os_select_times), np.std(_os_select_times)))
        os_rank_times.append((statistics.median(_os_rank_times), np.std(_os_rank_times)))
        # removal_times.append((np.mean(_removal_times), np.std(_removal_times)))
    
    # it = plot_and_table(sizes, insertion_times, std=True, caption="Inserimento in una lista ordinata", time_caption="Tempo di inserimento (s)")
    it = ""
    # rt = plot_and_table(sizes, removal_times, std=True, caption="Rimozione in una lista ordinata", time_caption="Tempo di rimozione (s)")
    rt = ""
    # ht = plot_and_table(sizes, search_times, std=True, caption="Ricerca in una lista ordinata", time_caption="Tempo di ricerca (s)")
    ht = ""
    st = utils.plot_and_table(sizes, os_select_times, std=True, caption="OS-Select in una lista ordinata", plot_filename="os-select-lista")
    kt = utils.plot_and_table(sizes, os_rank_times, std=True, caption="OS-Rank in una lista ordinata",  plot_filename="os-rank-lista")

    # Scrivi il codice LaTeX in un file .tex
    utils.write_to_latex_file('tabelle-lista-ordinata.tex', [it, rt, ht, st, kt])

if __name__ == "__main__":
    # sizes = [100, 1000, 2500, 5000, 7500, 10000, 15000, 20000, 25000]
    sizes = [10, 20, 30, 40, 50, 60, 70, 80, 100]
    iterations = 50

    test_linked_list(sizes, iterations)