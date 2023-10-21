from utils import TableAndData, Utils, DataPoints
from typing import Tuple
import random
from timeit import default_timer as timer
import numpy as np
import statistics

TableAndDataPoints = Tuple[TableAndData, TableAndData, TableAndData, TableAndData]

# Ogni metodo contenuto in questa classe ritorna:
#  1. Test dei os-select con tempi effettivi
#  2. Test dei os-rank con tempi effettivi
#  3. Test dei os-select con tempi relativi
#  4. Test dei os-rank con tempi relativi
class Tester:
    @staticmethod
    def test_ordered_list(sizes: list[int], iterations: int) -> TableAndDataPoints:
        from ordered_list import OrderedLinkedList

        os_rank_times: DataPoints = []
        os_select_times: DataPoints = []

        for size in sizes:
            _os_rank_times: list[float] = []
            _os_select_times: list[float] = []

            for i in range(iterations):
                print('LL - Dimensione:', size, 'Iterazione:', i+1)

                ordered_list = OrderedLinkedList()

                data = [random.randint(1, 1000 if size < 1000 else size) for _ in range(size)]
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

            os_select_times.append((statistics.median(_os_select_times), np.std(_os_select_times).astype(float)))
            os_rank_times.append((statistics.median(_os_rank_times), np.std(_os_rank_times).astype(float)))

        return (Utils.data_and_table(sizes, os_select_times, caption="OS-Select in una lista ordinata"), 
                Utils.data_and_table(sizes, os_rank_times, caption="OS-Rank in una lista ordinata"), 
                Utils.data_and_table(sizes, os_select_times, caption="OS-Select in una lista ordinata", is_relative_time=True), 
                Utils.data_and_table(sizes, os_rank_times, caption="OS-Rank in una lista ordinata", is_relative_time=True))
    
    @staticmethod
    def test_bst(sizes: list[int], iterations: int) -> TableAndDataPoints:
        from bst import BinarySearchTree

        os_rank_times: DataPoints = []
        os_select_times: DataPoints = []

        for size in sizes:
            _os_rank_times: list[float] = []
            _os_select_times: list[float] = []

            for i in range(iterations):
                print('ABR - Dimensione:', size, 'Iterazione:', i+1)

                binary_search_tree = BinarySearchTree()

                data = [random.randint(1, 1000 if size < 1000 else size) for _ in range(size)]
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

            os_select_times.append((statistics.median(_os_select_times), np.std(_os_select_times).astype(float)))
            os_rank_times.append((statistics.median(_os_rank_times), np.std(_os_rank_times).astype(float)))

        return (Utils.data_and_table(sizes, os_select_times, caption="OS-Select in un ABR"), 
                Utils.data_and_table(sizes, os_rank_times, caption="OS-Rank in un ABR"),
                Utils.data_and_table(sizes, os_select_times, caption="OS-Select in un ABR", is_relative_time=True), 
                Utils.data_and_table(sizes, os_rank_times, caption="OS-Rank in un ABR", is_relative_time=True))
    
    @staticmethod
    def test_augmented_rbt(sizes: list[int], iterations: int) -> TableAndDataPoints:
        from augmented_rbt import RedBlackTree

        os_rank_times: DataPoints = []
        os_select_times: DataPoints = []

        for size in sizes:
            _os_rank_times: list[float] = []
            _os_select_times: list[float] = []

            for i in range(iterations):
                print('ARN - Dimensione:', size, 'Iterazione:', i+1)

                red_black_tree = RedBlackTree()

                data = [random.randint(1, 1000 if size < 1000 else size) for _ in range(size)]
                for item in data:
                    red_black_tree.insert(item)

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
            
            os_select_times.append((statistics.median(_os_select_times), np.std(_os_select_times).astype(float)))
            os_rank_times.append((statistics.median(_os_rank_times), np.std(_os_rank_times).astype(float)))

        return (Utils.data_and_table(sizes, os_select_times, caption="OS-Select in un albero RN aumentato"),
                Utils.data_and_table(sizes, os_rank_times, caption="OS-Rank in un albero RN aumentato"),
                Utils.data_and_table(sizes, os_select_times, caption="OS-Select in un albero RN aumentato", is_relative_time=True),
                Utils.data_and_table(sizes, os_rank_times, caption="OS-Rank in un albero RN aumentato", is_relative_time=True))