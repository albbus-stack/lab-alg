from tester import Tester
from utils import Utils
import numpy as np

if __name__ == "__main__":
    # Primo test (s)
    # sizes = [*np.arange(10, 1010, 10)]
    # Secondo test (m)
    # sizes = [*np.arange(1000, 10100, 100)]
    # Terzo test (l)
    sizes = [*np.arange(10000, 20500, 500)]

    # test_ranges = [[*np.arange(10, 1010, 10)], [*np.arange(1000, 10100, 100)], [*np.arange(10000, 20500, 500)]]

    iterations = 1000

    for is_float_test in [False, True]:
        float_string = "-float" if is_float_test else ""

        #FIXME: Complete the script by combining the three tests togheter, 
        #       saving the corresponing files in the appropriate folders.
        # for sizes in test_ranges:
        # size_string = "s" if sizes == test_ranges[0] else "m" if sizes == test_ranges[1] else "l"

        ((ll_st, ll_mst), (ll_kt, ll_mkt),
        (ll_st_rel, ll_mst_rel), (ll_kt_rel, ll_mkt_rel)) = Tester.test_ordered_list(sizes, iterations, is_float_test)
       
        # Plot singoli per lista ordinata con tempi assoluti e relativi
        Utils.plot(sizes, ll_mst, "OS-Select")
        Utils.plot(sizes, ll_mkt, "OS-Rank")
        Utils.save_plot("lista-ordinata" + float_string, title="OS-Select e OS-Rank in una lista ordinata")
        Utils.clear_plot()

        Utils.plot(sizes, ll_mst_rel, "OS-Select")
        Utils.plot(sizes, ll_mkt_rel, "OS-Rank")
        Utils.save_plot("lista-ordinata" + float_string + "-rel", title="OS-Select e OS-Rank relativi in una lista ordinata")
        Utils.clear_plot()

        ((abr_st, abr_mst), (abr_kt, abr_mkt),
        (abr_st_rel, abr_mst_rel), (abr_kt_rel, abr_mkt_rel)) = Tester.test_bst(sizes, iterations, is_float_test)

        # Plot singoli per abr con tempi assoluti e relativi
        Utils.plot(sizes, abr_mst, "OS-Select")
        Utils.plot(sizes, abr_mkt, "OS-Rank")
        Utils.save_plot("abr" + float_string, title="OS-Select e OS-Rank in un ABR")
        Utils.clear_plot()

        Utils.plot(sizes, abr_mst_rel, "OS-Select")
        Utils.plot(sizes, abr_mkt_rel, "OS-Rank")
        Utils.save_plot("abr" + float_string + "-rel", title="OS-Select e OS-Rank relativi in un ABR")
        Utils.clear_plot()

        ((rn_st, rn_mst), (rn_kt, rn_mkt),
        (rn_st_rel, rn_mst_rel), (rn_kt_rel, rn_mkt_rel)) = Tester.test_augmented_rbt(sizes, iterations, is_float_test)

        # Plot singoli per arn aumentato con tempi assoluti e relativi
        Utils.plot(sizes, rn_mst, "OS-Select")
        Utils.plot(sizes, rn_mkt, "OS-Rank")
        Utils.save_plot("rn-aumentato" + float_string, title="OS-Select e OS-Rank in un albero RN aumentato")
        Utils.clear_plot()

        Utils.plot(sizes, rn_mst_rel, "OS-Select")
        Utils.plot(sizes, rn_mkt_rel, "OS-Rank")
        Utils.save_plot("rn-aumentato" + float_string + "-rel", title="OS-Select e OS-Rank relativi in un albero RN aumentato")
        Utils.clear_plot()

        # Plot complessivi per le tre strutture dati con tempi assoluti
        Utils.plot(sizes, ll_mst, "OS-Select in una lista ordinata")
        Utils.plot(sizes, abr_mst, "OS-Select in un albero binario")
        Utils.plot(sizes, rn_mst, "OS-Select in un albero RN aumentato")
        Utils.save_plot("os-select" + float_string, title="OS-Select")
        Utils.clear_plot()

        Utils.plot(sizes, ll_mkt, "OS-Rank in una lista ordinata")
        Utils.plot(sizes, abr_mkt, "OS-Rank in un albero binario")
        Utils.plot(sizes, rn_mkt, "OS-Rank in un albero RN aumentato")
        Utils.save_plot("os-rank" + float_string, title="OS-Rank")
        Utils.clear_plot()

        # Plot complessivi per le tre strutture dati con tempi relativi
        Utils.plot(sizes, ll_mst_rel, "OS-Select in una lista ordinata")
        Utils.plot(sizes, abr_mst_rel, "OS-Select in un albero binario")
        Utils.plot(sizes, rn_mst_rel, "OS-Select in un albero RN aumentato")
        Utils.save_plot("os-select" + float_string + "-rel", title="OS-Select relativo")
        Utils.clear_plot()

        Utils.plot(sizes, ll_mkt_rel, "OS-Rank in una lista ordinata")
        Utils.plot(sizes, abr_mkt_rel, "OS-Rank in un albero binario")
        Utils.plot(sizes, rn_mkt_rel, "OS-Rank in un albero RN aumentato")
        Utils.save_plot("os-rank" + float_string + "-rel", title="OS-Rank relativo")
        Utils.clear_plot()

        # Tabelle per le tre strutture dati con tempi assoluti
        Utils.write_to_latex_file("tabelle-lista-ordinata" + float_string + ".tex", [*ll_st, *ll_kt])
        Utils.write_to_latex_file("tabelle-abr" + float_string + ".tex", [*abr_st, *abr_kt])
        Utils.write_to_latex_file("tabelle-rn-aumentato" + float_string + ".tex", [*rn_st, *rn_kt])
        
        # Tabelle per le tre strutture dati con tempi relativi
        Utils.write_to_latex_file("tabelle-lista-ordinata" + float_string + "-rel.tex", [*ll_st_rel, *ll_kt_rel])
        Utils.write_to_latex_file("tabelle-abr" + float_string + "-rel.tex", [*abr_st_rel, *abr_kt_rel])
        Utils.write_to_latex_file("tabelle-rn-aumentato" + float_string + "-rel.tex", [*rn_st_rel, *rn_kt_rel])
