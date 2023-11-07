from enum import Enum
from utils import TableAndData, Utils, DataPoints
from typing import Any, Tuple, List
import random
from timeit import default_timer as timer
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
    def test_ordered_list(sizes: list[int], iterations: int, is_float_test: bool, title_termination: str) -> TableAndDataPoints:
        (os_select_times, os_rank_times) = Tester._execute_test(sizes, iterations, DataStructures.OL, is_float_test) 

        return (Utils.table_and_medians(sizes, os_select_times, caption="OS-Select in una lista ordinata" + title_termination), 
                Utils.table_and_medians(sizes, os_rank_times, caption="OS-Rank in una lista ordinata" + title_termination), 
                Utils.table_and_medians(sizes, os_select_times, caption="OS-Select in una lista ordinata" + title_termination, is_relative_time=True), 
                Utils.table_and_medians(sizes, os_rank_times, caption="OS-Rank in una lista ordinata" + title_termination, is_relative_time=True))
    
    @staticmethod
    def test_bst(sizes: list[int], iterations: int, is_float_test: bool, title_termination: str) -> TableAndDataPoints:
        (os_select_times, os_rank_times) = Tester._execute_test(sizes, iterations, DataStructures.BST, is_float_test) 

        return (Utils.table_and_medians(sizes, os_select_times, caption="OS-Select in un ABR" + title_termination), 
                Utils.table_and_medians(sizes, os_rank_times, caption="OS-Rank in un ABR" + title_termination),
                Utils.table_and_medians(sizes, os_select_times, caption="OS-Select in un ABR" + title_termination, is_relative_time=True), 
                Utils.table_and_medians(sizes, os_rank_times, caption="OS-Rank in un ABR" + title_termination, is_relative_time=True))

    @staticmethod
    def test_augmented_rbt(sizes: list[int], iterations: int, is_float_test: bool, title_termination: str) -> TableAndDataPoints:
        (os_select_times, os_rank_times) = Tester._execute_test(sizes, iterations, DataStructures.RBT, is_float_test) 

        return (Utils.table_and_medians(sizes, os_select_times, caption="OS-Select in un albero RN aumentato" + title_termination),
                Utils.table_and_medians(sizes, os_rank_times, caption="OS-Rank in un albero RN aumentato" + title_termination),
                Utils.table_and_medians(sizes, os_select_times, caption="OS-Select in un albero RN aumentato" + title_termination, is_relative_time=True),
                Utils.table_and_medians(sizes, os_rank_times, caption="OS-Rank in un albero RN aumentato" + title_termination, is_relative_time=True))

    @staticmethod
    def _execute_test(sizes: list[int], iterations: int, data_structure: DataStructures, is_float_test: bool) -> Tuple[DataPoints, DataPoints]:
        os_rank_times: DataPoints = []
        os_select_times: DataPoints = []

        for size in sizes:
            _os_rank_times: list[float] = []
            _os_select_times: list[float] = []

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

            for i in range(iterations):
                print(f"{data_structure.name} -", "FLOAT" if is_float_test else "INT",  "- Dimensione:", size, "Iterazione:", i+1)

                k = random.randint(1, size)
                start_time = timer()
                ds.os_select(k)
                end_time = timer()

                _os_select_times.append(end_time - start_time)

                k = data[random.randint(0, size-1)]
                start_time = timer()
                ds.os_rank(k)
                end_time = timer()
                
                _os_rank_times.append(end_time - start_time)

            asymmetric_error_select = [statistics.median(_os_select_times) - min(_os_select_times), max(_os_select_times) - statistics.median(_os_select_times)]
            asymmetric_error_rank = [statistics.median(_os_rank_times) - min(_os_rank_times), max(_os_rank_times) - statistics.median(_os_rank_times)]

            os_select_times.append((statistics.median(_os_select_times), asymmetric_error_select))
            os_rank_times.append((statistics.median(_os_rank_times), asymmetric_error_rank))

        return (os_select_times, os_rank_times)