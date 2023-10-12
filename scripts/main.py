from tester import Tester
from utils import Utils

if __name__ == "__main__":
    # sizes = [100, 1000, 2500, 5000, 7500, 10000, 15000, 20000, 25000]
    sizes = [10, 25, 50, 75, 100, 150, 250, 500, 1000, 1500, 2000, 3000, 4000, 5000, 7500, 10000]
    iterations = 100

    ((ll_st, ll_mst, ll_dst), (ll_kt, ll_mkt, ll_dkt)) = Tester.test_ordered_list(sizes, iterations)
    ((abr_st, abr_mst, abr_dst), (abr_kt, abr_mkt, abr_dkt)) = Tester.test_bst(sizes, iterations)
    ((rn_st, rn_mst, rn_dst), (rn_kt, rn_mkt, rn_dkt)) = Tester.test_augmented_rbt(sizes, iterations)

    Utils.plot(sizes, ll_mst, ll_dst, "OS-Select in una lista ordinata")
    Utils.plot(sizes, abr_mst, abr_dst, "OS-Select in un albero binario")
    Utils.plot(sizes, rn_mst, rn_dst, "OS-Select in un albero RN aumentato")
    Utils.save_plot("os-select", title="OS-Select")
    Utils.clear_plot()

    Utils.plot(sizes, ll_mkt, ll_dkt, "OS-Rank in una lista ordinata")
    Utils.plot(sizes, abr_mkt, abr_dkt, "OS-Rank in un albero binario")
    Utils.plot(sizes, rn_mkt, rn_dkt, "OS-Rank in un albero RN aumentato")
    Utils.save_plot("os-rank", title="OS-Rank")

    Utils.write_to_latex_file('tabelle-lista-ordinata.tex', [ll_st, ll_kt])
    Utils.write_to_latex_file('tabelle-abr.tex', [abr_st, abr_kt])
    Utils.write_to_latex_file('tabelle-rn-aumentato.tex', [rn_st, rn_kt])