import random
from timeit import default_timer as timer
from utils import plot_and_table

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

if __name__ == "__main__":
    sizes = [1000, 5000, 10000, 15000]
    insertion_times = []
    removal_times = []
    os_select_times = []
    os_rank_times = []

    for size in sizes:
        ordered_list = OrderedLinkedList()

        [elapsed_time, data] = test_insertion(size, ordered_list)
        insertion_times.append(elapsed_time)

        elapsed_time = test_os_select(size, ordered_list)
        os_select_times.append(elapsed_time)

        elapsed_time = test_os_rank(ordered_list, data)
        os_rank_times.append(elapsed_time)

        elapsed_time = test_removal(ordered_list, data)
        removal_times.append(elapsed_time)

    it = plot_and_table(sizes, insertion_times, caption="Inserimento in una lista ordinata", time_caption="Tempo di inserimento (s)")
    rt = plot_and_table(sizes, removal_times, caption="Rimozione in una lista ordinata", time_caption="Tempo di rimozione (s)")
    st = plot_and_table(sizes, os_select_times, caption="OS-Select in una lista ordinata", time_caption="Tempo di OS-Select (s)")
    kt = plot_and_table(sizes, os_rank_times, caption="OS-Rank in una lista ordinata", time_caption="Tempo di OS-Rank (s)")

    # Scrivi il codice LaTeX in un file .tex
    with open('tabelle-lista-ordinata.tex', 'w') as file:
      file.write('\n'.join([it, rt, st, kt]))