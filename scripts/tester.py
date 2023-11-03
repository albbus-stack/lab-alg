from enum import Enum
from utils import TableAndData, Utils, DataPoints
from typing import Any, Tuple, List
import random
from timeit import default_timer as timer
import numpy as np
import statistics

class DataStructures(Enum):
    OL = 0
    BST = 1
    RBT = 2

# Ogni metodo contenuto nella classe `Tester` ritorna una tupla che contiene i valori seguenti:
#  1. Test di os-select con tempi effettivi
#  2. Test di os-rank con tempi effettivi
#  3. Test di os-select con tempi relativi
#  4. Test di os-rank con tempi relativi
TableAndDataPoints = Tuple[TableAndData, TableAndData, TableAndData, TableAndData]

class Tester:
    @staticmethod
    def test_ordered_list(sizes: list[int], iterations: int, is_float_test: bool = False) -> TableAndDataPoints:
        (os_select_times, os_rank_times) = Tester._execute_test(sizes, iterations, DataStructures.OL, is_float_test) 

        return (Utils.data_and_table(sizes, os_select_times, caption="OS-Select in una lista ordinata"), 
                Utils.data_and_table(sizes, os_rank_times, caption="OS-Rank in una lista ordinata"), 
                Utils.data_and_table(sizes, os_select_times, caption="OS-Select in una lista ordinata", is_relative_time=True), 
                Utils.data_and_table(sizes, os_rank_times, caption="OS-Rank in una lista ordinata", is_relative_time=True))
    
    @staticmethod
    def test_bst(sizes: list[int], iterations: int, is_float_test: bool = False) -> TableAndDataPoints:
        (os_select_times, os_rank_times) = Tester._execute_test(sizes, iterations, DataStructures.BST, is_float_test) 

        return (Utils.data_and_table(sizes, os_select_times, caption="OS-Select in un ABR"), 
                Utils.data_and_table(sizes, os_rank_times, caption="OS-Rank in un ABR"),
                Utils.data_and_table(sizes, os_select_times, caption="OS-Select in un ABR", is_relative_time=True), 
                Utils.data_and_table(sizes, os_rank_times, caption="OS-Rank in un ABR", is_relative_time=True))

    @staticmethod
    def test_augmented_rbt(sizes: list[int], iterations: int, is_float_test: bool = False) -> TableAndDataPoints:
        (os_select_times, os_rank_times) = Tester._execute_test(sizes, iterations, DataStructures.RBT, is_float_test) 

        return (Utils.data_and_table(sizes, os_select_times, caption="OS-Select in un albero RN aumentato"),
                Utils.data_and_table(sizes, os_rank_times, caption="OS-Rank in un albero RN aumentato"),
                Utils.data_and_table(sizes, os_select_times, caption="OS-Select in un albero RN aumentato", is_relative_time=True),
                Utils.data_and_table(sizes, os_rank_times, caption="OS-Rank in un albero RN aumentato", is_relative_time=True))

    @staticmethod
    def _execute_test(sizes: list[int], iterations: int, data_structure: DataStructures, is_float_test: bool) -> Tuple[DataPoints, DataPoints]:
        os_rank_times: DataPoints = []
        os_select_times: DataPoints = []

        for size in sizes:
            _os_rank_times: list[float] = []
            _os_select_times: list[float] = []

            for i in range(iterations):
                print(f'{data_structure.name} -', 'FLOAT' if is_float_test else 'INT',  '- Dimensione:', size, 'Iterazione:', i+1)
                
                ds: Any = None
                if data_structure == DataStructures.OL:
                    from ordered_list import OrderedLinkedList
                    ds = OrderedLinkedList()
                elif data_structure == DataStructures.BST:
                    from bst import BinarySearchTree
                    ds = BinarySearchTree()
                elif data_structure == DataStructures.RBT:
                    from augmented_rbt import RedBlackTree
                    ds = RedBlackTree()

                data: List[Any] = []
                if is_float_test:
                    data = [random.uniform(1, 1000) for _ in range(size)]
                else:
                    data = [random.randint(1, 5000) for _ in range(size)]

                for item in data:
                    ds.insert(item)

                start_time = timer()
                for k in range(size):
                    ds.os_select(k+1)
                end_time = timer()

                _os_select_times.append(end_time - start_time)

                start_time = timer()
                for k in data:
                    ds.os_rank(k)
                end_time = timer()

                _os_rank_times.append(end_time - start_time)

            os_select_times.append((statistics.median(_os_select_times), np.std(_os_select_times, dtype=float)))
            os_rank_times.append((statistics.median(_os_rank_times), np.std(_os_rank_times, dtype=float)))

        return (os_select_times, os_rank_times)