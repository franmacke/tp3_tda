import matplotlib.pyplot as plt
import numpy as np

def graficar_comparacion(resultados):

    casos = range(1, len(resultados) + 1)
    tiempos_bt = [r['backtracking']['tiempo'] for r in resultados]
    tiempos_pl = [r['programacion_lineal']['tiempo'] for r in resultados]

    # Crear figura con dos subplots
    fig, ax1 = plt.subplots(1, 1, figsize=(12, 8))

    # Configurar el gráfico de tiempos
    x = np.arange(len(casos))
    width = 0.35

    ax1.bar(x - width/2, tiempos_bt, width, label='Backtracking', color='skyblue', alpha=0.7)
    ax1.bar(x + width/2, tiempos_pl, width, label='Programación Lineal', color='lightgreen', alpha=0.7)

    # Agregar información de parámetros para cada caso
    for i, caso in enumerate(resultados):
        info_text = f"n={caso['n']}\nm={caso['m']}\nk={caso['k']}"
        ax1.text(i, max(tiempos_bt[i] or 0, tiempos_pl[i] or 0) + 0.1,
                info_text, ha='center', va='bottom', fontsize=8)

    ax1.set_ylabel('Tiempo (segundos)')
    ax1.set_title('Comparación de Tiempos de Ejecución')
    ax1.set_xticks(x)
    ax1.set_xticklabels([f'Caso {i}' for i in casos])
    ax1.legend()

    plt.subplots_adjust(top=0.85)
    plt.tight_layout()
    plt.show()