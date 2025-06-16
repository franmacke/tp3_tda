from src.generador import Generador
from src.backtracking import backtracking
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import ScalarFormatter

def analizar_backtracking(cantidad_casos=10, n_min=10, n_max=30, m_min=None, m_max=None, k_min=2, k_max=5, seed=None):
    generador = Generador(seed)
    casos = generador.generar_casos(cantidad_casos, n_min, n_max, m_min, m_max, k_min, k_max)

    resultados = []
    for i, (grafo, k) in enumerate(casos):
        print(f"Procesando caso {i+1}/{cantidad_casos}")
        try:
            resultado = backtracking(grafo, k)
            resultados.append({
                'n': len(grafo.obtener_vertices()),
                'm': sum(len(grafo.vecinos(v)) for v in grafo.obtener_vertices()) // 2,
                'k': k,
                'tiempo': resultado['tiempo_ejecucion'] if resultado else None,
                'max_diametro': resultado['max_diametro'] if resultado else None
            })
        except Exception as e:
            print(f"Error en caso {i+1}: {str(e)}")
            resultados.append({
                'n': len(grafo.obtener_vertices()),
                'm': sum(len(grafo.vecinos(v)) for v in grafo.obtener_vertices()) // 2,
                'k': k,
                'tiempo': None,
                'max_diametro': None
            })

    return resultados

def graficar_backtracking(resultados):
    casos = range(1, len(resultados) + 1)
    tiempos = [r['tiempo'] for r in resultados]

    fig, ax = plt.subplots(figsize=(12, 6))

    x = np.arange(len(casos))
    width = 0.5

    # Tiempos: reemplazar None por 0
    tiempos_validos = [t if t is not None else 0 for t in tiempos]

    # Graficar las barras de tiempo
    ax.bar(x, tiempos_validos, width, color='salmon', alpha=0.8)

    # Mostrar info sobre cada barra (n, m, k, tiempo)
    for i, caso in enumerate(resultados):
        info_text = (
            f"n={caso['n']}, m={caso['m']}, k={caso['k']}\n"
            f"{tiempos_validos[i]:.5f} s"
        )
        y_pos = tiempos_validos[i] - max(tiempos_validos) * 0.1
        ax.text(x[i], y_pos, info_text, ha='center', va='bottom', fontsize=9)

    # Ejes y etiquetas
    ax.set_ylabel('Tiempo (segundos)')
    ax.set_title('Tiempos de Ejecución - Backtracking')
    ax.set_xticks(x)
    ax.set_xticklabels([f'Caso {i+1}' for i in x])

    # Mostrar números normales en el eje Y
    ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=False))
    ax.ticklabel_format(style='plain', axis='y')

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    resultados = analizar_backtracking(
        cantidad_casos=10,
        n_min=10,
        n_max=20,
        k_min=2,
        k_max=4,
        seed=42
    )
    graficar_backtracking(resultados)
