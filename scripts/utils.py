import pandas as pd
import matplotlib.pyplot as plt
import os
from typing import Optional, Any, List, Tuple
import numpy as np

DataPoints = List[Tuple[float, float]]

TableAndData = Tuple[List[str], List[float], List[float]]

class Utils:
    @staticmethod
    def data_and_table(sizes: list[int], times: DataPoints, caption: str, is_relative_time: Optional[bool] = False) -> TableAndData:
        time_caption = "Tempo (s)"
        size_caption = "Dimensione (n)"
        std_caption = "Deviazione standard"

        medians = [median for median, _ in times]
        devs_std = [dev_std for _, dev_std in times]

        for i, median in enumerate(medians):
            medians[i] = round(median, 4)
            if is_relative_time:
                medians[i] = median / sizes[i]
        for i, dev in enumerate(devs_std):
            devs_std[i] = round(dev, 4)
            if is_relative_time:    
                devs_std[i] = dev / sizes[i]
            if medians[i] - devs_std[i] < 0:
                devs_std[i] = medians[i]
            
        data = {size_caption: sizes, time_caption: medians, std_caption: devs_std}

        df = pd.DataFrame(data)
        df[time_caption] = df[time_caption].apply(lambda x: '{:.4f}'.format(x))
        df[std_caption] = df[std_caption].apply(lambda x: '{:.4f}'.format(x))

        # Esportazione della tabella in formato LaTeX
        segment_size = 40
        segments = [df[i:i+segment_size] for i in range(0, len(df), segment_size)]
        latex_tables: list[str] = []

        for i, segment in enumerate(segments):
            if i == 0:
                latex_tables.append(segment.style.to_latex(clines="all;data", label=caption, caption=caption, position_float="centering", column_format="|c|c|c|c|"))
            else:
                latex_tables.append(segment.style.to_latex(clines="all;data", position_float="centering", column_format="|c|c|c|c|"))
        
        return (latex_tables, medians, devs_std)

    @staticmethod
    def plot(sizes: list[int], medians: list[float], dev_std: list[float], label: Optional[str] = None) -> None:
        time_caption = "Tempo (s)"
        size_caption = "Dimensione (n)"
        
        plt.errorbar(sizes, medians, yerr=dev_std, fmt='o-', label=label)
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
