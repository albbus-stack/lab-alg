from tester import Tester
from utils import Utils
import numpy as np

if __name__ == "__main__":
    # sizes = [100, 1000, 2500, 5000, 7500, 10000, 15000, 20000, 25000]
    #sizes = [10, 25, 50, 75, 100, 150, 250, 500, 1000, 1500, 2000, 3000, 4000, 5000, 7500, 10000]
    sizes = [*np.arange(10, 100, 10)]
    iterations = 100

    for is_float_test in [False, True]:
        float_string = "-float" if is_float_test else ""

        ((ll_st, ll_mst, ll_dst), (ll_kt, ll_mkt, ll_dkt),
        (ll_st_rel, ll_mst_rel, ll_dst_rel), (ll_kt_rel, ll_mkt_rel, ll_dkt_rel)) = Tester.test_ordered_list(sizes, iterations, is_float_test)
        ((abr_st, abr_mst, abr_dst), (abr_kt, abr_mkt, abr_dkt),
        (abr_st_rel, abr_mst_rel, abr_dst_rel), (abr_kt_rel, abr_mkt_rel, abr_dkt_rel)) = Tester.test_bst(sizes, iterations, is_float_test)
        ((rn_st, rn_mst, rn_dst), (rn_kt, rn_mkt, rn_dkt),
        (rn_st_rel, rn_mst_rel, rn_dst_rel), (rn_kt_rel, rn_mkt_rel, rn_dkt_rel)) = Tester.test_augmented_rbt(sizes, iterations, is_float_test)

        # Plot singoli per lista ordinata con tempi assoluti e relativi
        Utils.plot(sizes, ll_mst, ll_dst, "OS-Select")
        Utils.plot(sizes, ll_mkt, ll_dkt, "OS-Rank")
        Utils.save_plot("lista-ordinata" + float_string, title="OS-Select e OS-Rank in una lista ordinata")
        Utils.clear_plot()

        Utils.plot(sizes, ll_mst_rel, ll_dst_rel, "OS-Select")
        Utils.plot(sizes, ll_mkt_rel, ll_dkt_rel, "OS-Rank")
        Utils.save_plot("lista-ordinata" + float_string + "-rel", title="OS-Select e OS-Rank relativi in una lista ordinata")
        Utils.clear_plot()

        # Plot singoli per abr con tempi assoluti e relativi
        Utils.plot(sizes, abr_mst, abr_dst, "OS-Select")
        Utils.plot(sizes, abr_mkt, abr_dkt, "OS-Rank")
        Utils.save_plot("abr" + float_string, title="OS-Select e OS-Rank in un ABR")
        Utils.clear_plot()

        Utils.plot(sizes, abr_mst_rel, abr_dst_rel, "OS-Select")
        Utils.plot(sizes, abr_mkt_rel, abr_dkt_rel, "OS-Rank")
        Utils.save_plot("abr" + float_string + "-rel", title="OS-Select e OS-Rank relativi in un ABR")
        Utils.clear_plot()

        # Plot singoli per arn aumentato con tempi assoluti e relativi
        Utils.plot(sizes, rn_mst, rn_dst, "OS-Select")
        Utils.plot(sizes, rn_mkt, rn_dkt, "OS-Rank")
        Utils.save_plot("rn-aumentato" + float_string, title="OS-Select e OS-Rank in un albero RN aumentato")
        Utils.clear_plot()

        Utils.plot(sizes, rn_mst_rel, rn_dst_rel, "OS-Select")
        Utils.plot(sizes, rn_mkt_rel, rn_dkt_rel, "OS-Rank")
        Utils.save_plot("rn-aumentato" + float_string + "-rel", title="OS-Select e OS-Rank relativi in un albero RN aumentato")
        Utils.clear_plot()

        # Plot complessivi per le tre strutture dati con tempi assoluti
        Utils.plot(sizes, ll_mst, ll_dst, "OS-Select in una lista ordinata")
        Utils.plot(sizes, abr_mst, abr_dst, "OS-Select in un albero binario")
        Utils.plot(sizes, rn_mst, rn_dst, "OS-Select in un albero RN aumentato")
        Utils.save_plot("os-select" + float_string, title="OS-Select")
        Utils.clear_plot()

        Utils.plot(sizes, ll_mkt, ll_dkt, "OS-Rank in una lista ordinata")
        Utils.plot(sizes, abr_mkt, abr_dkt, "OS-Rank in un albero binario")
        Utils.plot(sizes, rn_mkt, rn_dkt, "OS-Rank in un albero RN aumentato")
        Utils.save_plot("os-rank" + float_string, title="OS-Rank")
        Utils.clear_plot()

        # Plot complessivi per le tre strutture dati con tempi relativi
        Utils.plot(sizes, ll_mst_rel, ll_dst_rel, "OS-Select in una lista ordinata")
        Utils.plot(sizes, abr_mst_rel, abr_dst_rel, "OS-Select in un albero binario")
        Utils.plot(sizes, rn_mst_rel, rn_dst_rel, "OS-Select in un albero RN aumentato")
        Utils.save_plot("os-select" + float_string + "-rel", title="OS-Select relativo")
        Utils.clear_plot()

        Utils.plot(sizes, ll_mkt_rel, ll_dkt_rel, "OS-Rank in una lista ordinata")
        Utils.plot(sizes, abr_mkt_rel, abr_dkt_rel, "OS-Rank in un albero binario")
        Utils.plot(sizes, rn_mkt_rel, rn_dkt_rel, "OS-Rank in un albero RN aumentato")
        Utils.save_plot("os-rank" + float_string + "-rel", title="OS-Rank relativo")

        # Tabelle per le tre strutture dati con tempi assoluti
        Utils.write_to_latex_file("tabelle-lista-ordinata" + float_string + ".tex", [*ll_st, *ll_kt])
        Utils.write_to_latex_file("tabelle-abr" + float_string + ".tex", [*abr_st, *abr_kt])
        Utils.write_to_latex_file("tabelle-rn-aumentato" + float_string + ".tex", [*rn_st, *rn_kt])
        
        # Tabelle per le tre strutture dati con tempi relativi
        Utils.write_to_latex_file("tabelle-lista-ordinata" + float_string + "-rel.tex", [*ll_st_rel, *ll_kt_rel])
        Utils.write_to_latex_file("tabelle-abr" + float_string + "-rel.tex", [*abr_st_rel, *abr_kt_rel])
        Utils.write_to_latex_file("tabelle-rn-aumentato" + float_string + "-rel.tex", [*rn_st_rel, *rn_kt_rel])
