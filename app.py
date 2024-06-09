import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
import tkinter as tk
from tkinter import scrolledtext

# Constantes
constants = {
    'a': 1e-9,  # 1 nm em metros
    'u_initial': 10,
    'qa_min': -12,
    'qa_max': 12,
    'qa_steps': 1000,
    'm': 9.10938356e-31,  # Massa do elétron em kg
    'hbar': 1.054571817e-34,  # Constante de Planck reduzida em J.s
    'J_to_eV': 1.60219e-19  # Conversão de Joules para eV
}

# Valores derivados das constantes
qa_values = np.linspace(constants['qa_min'], constants['qa_max'], constants['qa_steps'])


# Função para calcular f(qa) de acordo com a equação (2)
def f_qa(qa, u):
    return np.cos(qa) + u * np.sinc(qa / np.pi)  # np.sinc é sin(pi*x)/(pi*x)


# Identificar band gaps utilizando vetorização
def identify_band_gaps(values):
    gaps = np.abs(values) > 1
    gap_changes = np.diff(gaps.astype(int))
    start_indices = np.where(gap_changes == 1)[0] + 1
    end_indices = np.where(gap_changes == -1)[0] + 1
    if gaps[0]:
        start_indices = np.insert(start_indices, 0, 0)
    if gaps[-1]:
        end_indices = np.append(end_indices, len(gaps) - 1)
    return list(zip(qa_values[start_indices], qa_values[end_indices]))


# Função para calcular a energia a partir de q em eV
def energy_eV(q):
    return (q * constants['hbar']) ** 2 / (2 * constants['m']) / constants['J_to_eV']


# Função para criar uma janela Tkinter com texto e botões
def create_info_window(title, text):
    root = tk.Tk()
    root.title(title)
    txt = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=15)
    txt.pack(padx=10, pady=10)
    txt.config(state='normal')
    txt.delete(1.0, tk.END)
    txt.insert(tk.INSERT, text)
    txt.config(state='disabled')
    btn_close = tk.Button(root, text="Close", command=root.destroy)
    btn_close.pack(padx=10, pady=10)
    root.mainloop()


# Função para mostrar informações sobre os band gaps
def show_band_gaps():
    band_gap_text = '\n'.join([
        f'Intervalo: [{start:.2f}, {end:.2f}] - Energia: {energy_eV(start / constants["a"]):.2f} eV a {energy_eV(end / constants["a"]):.2f} eV'
        for start, end in gap_intervals])
    create_info_window("Informações sobre Band Gaps", band_gap_text)


# Função para mostrar informações sobre o gráfico
def show_graph_info():
    graph_info_text = (
        "Este gráfico representa a função f(qa) para um elétron em um potencial periódico. \n"
        "As regiões vermelhas indicam os band gaps, onde |f(qa)| > 1.\n\n"
        "A função f(qa) é calculada como:\n"
        "f(qa) = cos(qa) + u * sinc(qa / π)\n\n"
        "Você pode ajustar o parâmetro u utilizando o controle deslizante abaixo do gráfico.\n"
        "As linhas horizontais tracejadas indicam os limites y = ±1, que definem os band gaps."
    )

    create_info_window("Informações sobre o Gráfico", graph_info_text)


# Função para mostrar as equações usadas
def show_equations():
    equations_text = (
        "Equações Utilizadas:\n\n"
        "1. Função f(qa):\n"
        "   f(qa) = cos(qa) + u * sinc(qa / π)\n"
        "   Onde: sinc(x) = sin(πx) / (πx)\n\n"
        "2. Relação de q com a Energia:\n"
        "   q = sqrt(2mE / ħ^2)\n"
        "   Onde: E é a energia, m é a massa do elétron e ħ é a constante de Planck reduzida.\n\n"
        "3. Energia em eV:\n"
        "   E = (q * ħ)^2 / (2 * m) / J_to_eV\n"
        "   Esta equação converte a energia calculada de Joules para elétron-volts (eV)."
    )

    create_info_window("Equações Utilizadas", equations_text)


# Função para mostrar os métodos usados
def show_methods():
    methods_text = (
        "Métodos Utilizados:\n\n"
        "1. **Vetorização**:\n"
        "   - Aplicação de operações vetorizadas para melhorar a eficiência computacional.\n"
        "   - Exemplo: `np.cos(qa)`, `u * np.sinc(qa / np.pi)`.\n\n"
        "2. **Identificação de Band Gaps**:\n"
        "   - Uso de diferenciação de arrays booleanos para identificar mudanças de estado.\n"
        "   - Exemplo: `np.diff(gaps.astype(int))`, `np.where(gap_changes == 1)[0] + 1`.\n\n"
        "3. **Criação de Interface Gráfica**:\n"
        "   - Utilização da biblioteca Tkinter para criar janelas interativas.\n"
        "   - Exemplo: `tk.Tk()`, `scrolledtext.ScrolledText()`, `tk.Button()`.\n\n"
        "4. **Gráficos Interativos**:\n"
        "   - Utilização da biblioteca Matplotlib para criar gráficos interativos com sliders e botões.\n"
        "   - Exemplo: `Slider`, `Button`, `ax.plot()`, `ax.fill_between()`."
    )

    create_info_window("Métodos Utilizados", methods_text)


# Configuração inicial dos valores de f(qa) e os band gaps
f_values = f_qa(qa_values, constants['u_initial'])
gap_intervals = identify_band_gaps(f_values)

# Criar a figura e os eixos com um estilo melhorado
plt.style.use('ggplot')  # Alterado para usar o estilo 'ggplot'
fig, ax = plt.subplots(figsize=(12, 7))
plt.subplots_adjust(left=0.1, bottom=0.3)
line, = ax.plot(qa_values, f_values, label=r'$f(qa)$', color='blue')
ax.fill_between(qa_values, -1, 1, where=np.abs(f_values) > 1, color='red', alpha=0.3, label='Band Gaps (|f(qa)| > 1)')
ax.set_title('Visualização de $f(qa)$ para Elétron em um Potencial Periódico', fontsize=16)
ax.set_xlabel('$qa$', fontsize=14)
ax.set_ylabel('$f(qa)$', fontsize=14)
ax.axhline(y=1, color='k', linestyle='--')
ax.axhline(y=-1, color='k', linestyle='--')
ax.legend(fontsize=12)
ax.grid(True)

# Slider para ajustar o parâmetro u
ax_u = plt.axes([0.1, 0.15, 0.65, 0.03], facecolor='lightgoldenrodyellow')
slider_u = Slider(ax_u, 'Parâmetro u', 0.1, 30.0, valinit=constants['u_initial'], valstep=0.1)


# Botões para exibir informações e métodos
def add_button(ax, label, callback, position):
    ax_button = plt.axes(position)
    button = Button(ax_button, label, color='lightgoldenrodyellow', hovercolor='0.975')
    button.on_clicked(callback)
    return button


btn_show_gaps = add_button(plt.axes([0.8, 0.1, 0.1, 0.04]), 'Mostrar Gaps', lambda event: show_band_gaps(),
                           [0.8, 0.1, 0.1, 0.04])
btn_graph_info = add_button(plt.axes([0.8, 0.05, 0.1, 0.04]), 'Info Gráfico', lambda event: show_graph_info(),
                            [0.8, 0.05, 0.1, 0.04])
btn_equations = add_button(plt.axes([0.8, 0.15, 0.1, 0.04]), 'Equações', lambda event: show_equations(),
                           [0.8, 0.15, 0.1, 0.04])
btn_methods = add_button(plt.axes([0.8, 0.2, 0.1, 0.04]), 'Métodos', lambda event: show_methods(),
                         [0.8, 0.2, 0.1, 0.04])


# Função de atualização ao mover o slider
def update(val):
    new_u = slider_u.val
    new_f_values = f_qa(qa_values, new_u)
    line.set_ydata(new_f_values)
    global gap_intervals
    gap_intervals = identify_band_gaps(new_f_values)
    ax.collections.clear()
    ax.fill_between(qa_values, -1, 1, where=np.abs(new_f_values) > 1, color='red', alpha=0.3)
    fig.canvas.draw_idle()

    # Mostrar os gaps de energia no terminal
    print('Gaps de Energia Permitida:')
    for start, end in gap_intervals:
        energy_start = energy_eV(start / constants['a'])
        energy_end = energy_eV(end / constants['a'])
        print(f'Intervalo: [{start:.2f}, {end:.2f}] - Energia: {energy_start:.2f} eV a {energy_end:.2f} eV')


slider_u.on_changed(update)

# Imprimir os gaps de energia permitida
print('Gaps de Energia Permitida:')
for start, end in gap_intervals:
    energy_start = energy_eV(start / constants['a'])
    energy_end = energy_eV(end / constants['a'])
    print(f'Intervalo: [{start:.2f}, {end:.2f}] - Energia: {energy_start:.2f} eV a {energy_end:.2f} eV')

# Mostrar o gráfico interativo
plt.show()
