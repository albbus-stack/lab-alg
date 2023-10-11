import pandas as pd
import matplotlib.pyplot as plt
import os
from typing import Optional, Any
import numpy as np

class Utils:
    @staticmethod
    def data_and_table(sizes: list[int], times: list[tuple[float, np.floating[Any]]], caption: str, plot_filename: Optional[str] = None):
        time_caption = "Tempo (s)"
        size_caption = "Dimensione (n)"
        std_caption = "Deviazione standard"

        means = [mean for mean, _ in times]
        devs_std = [dev_std for _, dev_std in times]
        data = {size_caption: sizes, time_caption: means, std_caption: devs_std}

        df = pd.DataFrame(data)
        df[time_caption] = df[time_caption].apply(lambda x: '{:.3f}'.format(round(x, 3)))
        df[std_caption] = df[std_caption].apply(lambda x: '{:.3f}'.format(round(x, 3)))

        # Esportazione della tabella in formato LaTeX
        latex_table = df.style.to_latex(clines="all;data", label=caption, caption=caption, position_float="centering", column_format="cccc", position="H")
        
        # Salva il grafico come immagine nella directory "images"
        if plot_filename:
            Utils.save_plot(plot_filename)

        return (latex_table, means, devs_std)

    @staticmethod
    def plot(sizes: list[int], means: list[float], dev_std: list[np.floating[Any]], label: Optional[str] = None):
        time_caption = "Tempo (s)"
        size_caption = "Dimensione (n)"
        
        plt.errorbar(sizes, means, yerr=dev_std, fmt='o-', label=label)
        plt.xlabel(size_caption)
        plt.ylabel(time_caption)
        if label: plt.legend()
        plt.grid(True)

    @staticmethod
    def clear_plot():
        plt.clf()

    @staticmethod
    def save_plot(plot_filename: str, title: Optional[str] = None):
        if title: plt.title(title)

        images_dir = "../latex/images"
        if not os.path.exists(images_dir):
            os.makedirs(images_dir)
        plt.savefig(os.path.join(images_dir, plot_filename), bbox_inches='tight')

    @staticmethod
    def write_to_latex_file(filename, lines):
        latex_dir = "../latex"
        full_path = os.path.join(latex_dir, filename)

        try:
            os.makedirs(latex_dir, exist_ok=True)
            with open(full_path, 'w') as file:
                file.write('\n'.join(lines))
        except Exception as e:
            print(f"Si è verificato un errore durante la scrittura del file '{full_path}': {str(e)}")
