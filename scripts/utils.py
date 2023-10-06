import matplotlib.pyplot as plt
import pandas as pd

def plot_and_table(sizes, times, caption: str, time_caption: str):
    # Creazione della tabella con pandas
    data = {'Dimensione dell\'insieme di dati': sizes, time_caption: times}
    df = pd.DataFrame(data)
    df[time_caption] = df[time_caption].apply(lambda x: '{:.3f}'.format(round(x, 3)))

    # Esportazione della tabella in formato LaTeX
    latex_table = df.style.to_latex(clines="all;data", label=caption, caption=caption, position_float="centering", column_format="ccc")

    # Plot
    plt.plot(sizes, df[time_caption], marker='o', linestyle='-')
    plt.xlabel('Dimensione dell\'insieme di dati')
    plt.ylabel(time_caption)
    plt.title(caption)
    plt.grid(True)
    plt.show()

    # Stampa del codice LaTeX della tabella
    return latex_table