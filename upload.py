
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d

import tkinter as tk
from tkinter import filedialog
from tkinter import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d


def abrir_arquivo():
    root = tk.Tk()
    root.withdraw()  # Esconde a janela principal

    arquivo = filedialog.askopenfilename(filetypes=[('CSV files', '*.csv')])
    if arquivo:

        data = pd.read_csv(arquivo, sep=';')

        result_names = data['Result'].unique()
        bay_names = data['Bay'].unique()

        fig, ax = plt.subplots(figsize=(10, 6))

        bay_categories = sorted(data['Bay'].unique())
        colors = plt.cm.Set1(np.linspace(0, 1, len(bay_categories)))

        bay_colors = {
            '1': 'green',
            '2': 'mediumorchid',
            '3': 'gold',
            '4': 'deeppink',
            '5': 'dodgerblue',
            '6': 'grey',
            '7': 'maroon',
            '8': 'lime',
            'sump': 'black',
            '9': 'lightcoral',
            '10': 'darkcyan',
        }

        bay_categories = sorted(data['Bay'].unique())
        colors = plt.cm.Set1(np.linspace(0, 1, len(bay_categories)))

        for result_name in result_names:
            result_data = data[data['Result'] == result_name]
            result_data = result_data.sort_values('Water Content')
            x_values = result_data['Water Content']
            y_values = result_data['Dry Density']
            bay_values = result_data['Bay']

            if len(x_values) >= 2:
                interp_func = interp1d(
                    x_values, y_values, assume_sorted=False, kind='quadratic')
                x_smooth = np.linspace(x_values.min(), x_values.max(), 100)
                y_smooth = interp_func(x_smooth)

                for bay_value in bay_values:
                    color = bay_colors.get(str(bay_value), 'gray')
                    ax.plot(x_smooth, y_smooth, c=color)

        custom_handles = []
        custom_labels = []
        for bay in bay_categories:
            color = bay_colors.get(str(bay), 'black')
            custom_handles.append(plt.Line2D(
                [], [], color=color, marker='None', linestyle='-'))
            custom_labels.append(str(bay))

        ax.set_xlabel('Teor de Umidade (%)')
        ax.set_ylabel('Densidade Seca (g/cm³)')
        ax.set_title('TESTES DE SOLO')

        ax.set_ylim(1.60, 2.20)
        ax.set_yticks(np.arange(1.60, 2.20, 0.05))

        ax.set_xlim(min(data['Water Content']), max(data['Water Content']))
        ax.set_xticks(np.arange(3, 19, 1))

        ax.grid(color='lightgray', linestyle='--')

        custom_labels = [str(bay) for bay in bay_categories]

        legend = ax.legend(custom_handles, custom_labels, loc='center left',
                           bbox_to_anchor=(1, 0.5), fontsize='large', ncol=1)

        legend.set_title('Baías')

        title_text = legend.get_title()

        title_text.set_fontweight('bold')

        for handle in legend.legend_handles:
            handle.set_markersize(8)

        plt.show()


# Cria a janela principal
janela = tk.Tk()
janela.title("TESTES DE SOLO")

label2 = Label(janela, text="TESTES DE SOLO", font="arial 15", fg="blue")
label2.pack(pady=12)

janela.geometry('550x350')
img = PhotoImage(file="imagen_bvp.png")
Label_imagem = Label(janela, image=img).pack()

# Cria o botão
botao = tk.Button(janela, text="Abrir arquivo", command=abrir_arquivo)
botao.pack(padx=20, pady=20)

# Inicia o loop da interface gráfica
janela.mainloop()
