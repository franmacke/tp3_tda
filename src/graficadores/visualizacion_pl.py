import matplotlib.pyplot as plt
import numpy as np
from src.generador import Generador
from src.programacion_lineal import k_clustering_por_pl

def analizar_pl(cantidad_casos=10, n_min=10, n_max=30, m_min=None, m_max=None, k_min=2, k_max=5, seed=None):
    generador = Generador(seed)
    casos = generador.generar_casos(cantidad_casos, n_min, n_max, m_min, m_max, k_min, k_max)

    resultados = []
    for i, (grafo, k) in enumerate(casos):
        print(f"Procesando caso {i+1}/{cantidad_casos}")
        try:
            resultado = k_clustering_por_pl(grafo, k)
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

def graficar_pl(resultados):
    casos = range(1, len(resultados) + 1)
    tiempos = [r['tiempo'] for r in resultados]

    fig, ax1 = plt.subplots(figsize=(12, 6))

    # Gráfico de tiempos
    x = np.arange(len(casos))
    width = 0.35

    ax1.bar(x, tiempos, width, label='Tiempo', color='lightgreen', alpha=0.7)

    # Agregar información de parámetros
    for i, caso in enumerate(resultados):
        info_text = f"n={caso['n']}\nm={caso['m']}\nk={caso['k']}"
        ax1.text(i, (tiempos[i] or 0) - 0.05, info_text, ha='center', va='bottom', fontsize=8)

    ax1.set_ylabel('Tiempo (segundos)')
    ax1.set_title('Tiempos de Ejecución - Programación Lineal')
    ax1.set_xticks(x)
    ax1.set_xticklabels([f'Caso {i}' for i in casos])


    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    resultados = analizar_pl(
        cantidad_casos=10,
        n_min=10,
        n_max=20,
        k_min=2,
        k_max=4,
        seed=42
    )
    graficar_pl(resultados)