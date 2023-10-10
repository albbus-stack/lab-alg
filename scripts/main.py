from ordered_list import test_ordered_list
from bst import test_bst
from augmented_rbt import test_augmented_rbt

if __name__ == "__main__":
    # sizes = [100, 1000, 2500, 5000, 7500, 10000, 15000, 20000, 25000]
    sizes = [50, 100, 500, 1000, 1500]
    iterations = 250

    test_ordered_list(sizes, iterations)
    test_bst(sizes, iterations)
    test_augmented_rbt(sizes, iterations)