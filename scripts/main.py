from ordered_list import test_ordered_list
from bst import test_bst
from augmented_rbt import test_augmented_rbt

import utils
import matplotlib.pyplot as plt

if __name__ == "__main__":
    # sizes = [100, 1000, 2500, 5000, 7500, 10000, 15000, 20000, 25000]
    sizes = [10, 25, 50, 75, 100, 150, 250, 500, 1000, 1500, 2000, 3000, 4000, 5000, 7500, 10000]
    iterations = 100

    ((ll_st, ll_mst, ll_dst), (ll_kt, ll_mkt, ll_dkt)) = test_ordered_list(sizes, iterations)
    ((abr_st, abr_mst, abr_dst), (abr_kt, abr_mkt, abr_dkt))  = test_bst(sizes, iterations)
    ((rn_st, rn_mst, rn_dst), (rn_kt, rn_mkt, rn_dkt)) = test_augmented_rbt(sizes, iterations)

    utils.plot(sizes, ll_mst, ll_dst, "OS-Select in una lista ordinata")
    utils.plot(sizes, abr_mst, abr_dst, "OS-Select in un albero binario")
    utils.plot(sizes, rn_mst, rn_dst, "OS-Select in un albero RN aumentato")
    utils.save_plot("os-select", title="OS-Select")
    utils.clear_plot()

    utils.plot(sizes, ll_mkt, ll_dkt, "OS-Rank in una lista ordinata")
    utils.plot(sizes, abr_mkt, abr_dkt, "OS-Rank in un albero binario")
    utils.plot(sizes, rn_mkt, rn_dkt, "OS-Rank in un albero RN aumentato")
    utils.save_plot("os-rank", title="OS-Rank")

    utils.write_to_latex_file('tabelle-lista-ordinata.tex', [ll_st, ll_kt])
    utils.write_to_latex_file('tabelle-abr.tex', [abr_st, abr_kt])
    utils.write_to_latex_file('tabelle-rn-aumentato.tex', [rn_st, rn_kt])