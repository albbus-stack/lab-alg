import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np
from typing import Optional, List, Tuple

DataPoints = List[Tuple[float, List[float]]]

TableAndData = Tuple[List[str], List[float]]

class Utils:
    @staticmethod
    def data_and_table(sizes: list[int], times: DataPoints, caption: str, is_relative_time: Optional[bool] = False) -> TableAndData:
        time_caption = "Mediana (s)"
        size_caption = "Dimensione (n)"
        yerr_caption = "Tempi -/+ (s)"

        medians = [median for median, _ in times]
        yerrs = [yerr for _, yerr in times]

        for i, median in enumerate(medians):
            if is_relative_time:
                medians[i] = median / sizes[i]
        for i, yerr in enumerate(yerrs):
            for j in range(2):
                if is_relative_time:    
                    yerrs[i][j] = yerr[j] / sizes[i]

        data = {size_caption: sizes, time_caption: medians, yerr_caption: yerrs}

        df = pd.DataFrame(data)
        df[time_caption] = df[time_caption].apply(lambda x: '{:.1e}'.format(x))
        df[yerr_caption] = df[yerr_caption].apply(lambda x: '-{:.1e}'.format(x[0]) + ', ' + '+{:.1e}'.format(x[1]))

        # Esportazione della tabella in formato LaTeX
        segment_size = 40
        segments = [df[i:i+segment_size] for i in range(0, len(df), segment_size)]
        latex_tables: list[str] = []

        for i, segment in enumerate(segments):
            if i == 0:
                latex_tables.append(segment.style.to_latex(clines="all;data", label=caption, caption=caption, position_float="centering", column_format="|c|c|c|c|"))
            else:
                latex_tables.append(segment.style.to_latex(clines="all;data", position_float="centering", column_format="|c|c|c|c|"))
        
        return (latex_tables, medians)

    @staticmethod
    def plot(sizes: list[int], medians: list[float], label: Optional[str] = None) -> None:
        time_caption = "Tempo (s)"
        size_caption = "Dimensione (n)"

        plt.plot(sizes, medians, label=label)
        plt.xlabel(size_caption)
        plt.ylabel(time_caption)
        if label: plt.legend()
        plt.grid(True)

    @staticmethod
    def clear_plot() -> None:
        plt.clf()

    @staticmethod
    def save_plot(plot_filename: str, title: Optional[str] = None) -> None:
        if title: plt.title(title)

        images_dir = "../latex/images/plots"
        if not os.path.exists(images_dir):
            os.makedirs(images_dir)
        plt.savefig(os.path.join(images_dir, plot_filename), bbox_inches='tight')

    @staticmethod
    def write_to_latex_file(filename: str, lines: list[str]) -> None:
        latex_dir = "../latex"
        full_path = os.path.join(latex_dir, filename)

        _lines = []
        for line in lines:
            _lines.append(
                line.replace(
                    "\\begin{tabular}{|c|c|c|c|}", 
                    "\\begin{adjustbox}{width=1\\textwidth/2}\n\\begin{tabular}{|c|c|c|c|}\n\\hline"
                ).replace(
                    "\\end{tabular}",
                    "\\end{tabular}\n\\end{adjustbox}"
                )
            )
        
        try:
            os.makedirs(latex_dir, exist_ok=True)
            with open(full_path, 'w') as file:
                file.write('\n'.join(_lines))
        except Exception as e:
            print(f"Si è verificato un errore durante la scrittura del file '{full_path}': {str(e)}")
