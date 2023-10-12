from utils import Utils
import random
from timeit import default_timer as timer
import numpy as np
import statistics

class Tester:
    @staticmethod
    def test_ordered_list(sizes: list[int], iterations: int):
        from ordered_list import OrderedLinkedList

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

        return (Utils.data_and_table(sizes, os_select_times, caption="OS-Select in una lista ordinata"), 
                Utils.data_and_table(sizes, os_rank_times, caption="OS-Rank in una lista ordinata"))
    
    @staticmethod
    def test_bst(sizes: list[int], iterations: int):
        from bst import BinarySearchTree

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
    
    @staticmethod
    def test_augmented_rbt(sizes: list[int], iterations: int):
        from augmented_rbt import RedBlackTree

        os_rank_times = []
        os_select_times = []

        for size in sizes:
            _os_rank_times = []
            _os_select_times = []

            for i in range(iterations):
                print('ARN - Dimensione:', size, 'Iterazione:', i+1)

                red_black_tree = RedBlackTree()

                data = [random.randint(1, 1000) for _ in range(size)]
                # Inserimento dati di test
                for item in data:
                    red_black_tree.insert(item)

                # Esecuzione dei test sulle statistiche d'ordine
                start_time = timer()
                for k in range(size):
                    red_black_tree.os_select(k+1)
                end_time = timer()

                _os_select_times.append(end_time - start_time)

                start_time = timer()
                for k in data:
                    red_black_tree.os_rank(k)
                end_time = timer()

                _os_rank_times.append(end_time - start_time)
            
            os_select_times.append((statistics.median(_os_select_times), np.std(_os_select_times)))
            os_rank_times.append((statistics.median(_os_rank_times), np.std(_os_rank_times)))

        return (Utils.data_and_table(sizes, os_select_times, caption="OS-Select in un albero RN aumentato"),
                Utils.data_and_table(sizes, os_rank_times, caption="OS-Rank in un albero RN aumentato"))