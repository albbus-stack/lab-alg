import pandas as pd
import matplotlib.pyplot as plt
import os

def plot_and_table(sizes, times, caption: str, std=None, plot_filename=None):
    time_caption = "Tempo (s)"
    size_caption = "Dimensione (n)"
    std_caption = "Deviazione standard"

    if std:
        means = [mean for mean, _ in times]
        devs_std = [dev_std for _, dev_std in times]
        data = {size_caption: sizes, time_caption: means, std_caption: devs_std}

        df = pd.DataFrame(data)
        df[time_caption] = df[time_caption].apply(lambda x: '{:.3f}'.format(round(x, 3)))
        df[std_caption] = df[std_caption].apply(lambda x: '{:.3f}'.format(round(x, 3)))

        plt.errorbar(sizes, means, yerr=devs_std, fmt='o-')
        plt.xlabel(size_caption)
        plt.ylabel(time_caption)
        plt.title(caption)
        plt.grid(True)

        # Esportazione della tabella in formato LaTeX
        latex_table = df.style.to_latex(clines="all;data", label=caption, caption=caption, position_float="centering", column_format="cccc", position="H")
    else:
        # Creazione della tabella con pandas
        data = {size_caption: sizes, time_caption: times}

        df = pd.DataFrame(data)
        df[time_caption] = df[time_caption].apply(lambda x: '{:.3f}'.format(round(x, 3)))

        # Plot
        plt.plot(sizes, df[time_caption], marker='o', linestyle='-')
        plt.xlabel(size_caption)
        plt.ylabel(time_caption)
        plt.title(caption)
        plt.grid(True)

        # Esportazione della tabella in formato LaTeX
        latex_table = df.style.to_latex(clines="all;data", label=caption, caption=caption, position_float="centering", column_format="ccc")

    # Salva il grafico come immagine nella directory "images"
    if plot_filename:
        images_dir = "images"
        if not os.path.exists(images_dir):
            os.makedirs(images_dir)
        plt.savefig(os.path.join(images_dir, plot_filename), bbox_inches='tight')

    # plt.show()
    plt.clf()

    # Stampa del codice LaTeX della tabella
    return latex_table

def write_to_latex_file(filename, lines):
    latex_dir = "../latex"
    full_path = os.path.join(latex_dir, filename)

    try:
        os.makedirs(latex_dir, exist_ok=True)
        with open(full_path, 'w') as file:
            file.write('\n'.join(lines))
    except Exception as e:
        print(f"Si è verificato un errore durante la scrittura del file '{full_path}': {str(e)}")
