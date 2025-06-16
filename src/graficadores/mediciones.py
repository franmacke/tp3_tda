from src.generador import Generador
from src.programacion_lineal import k_clustering_por_pl
from src.backtracking import backtracking
from visualizacion import graficar_comparacion


def realizar_mediciones(cantidad_casos=10, n_min=10, n_max=30, m_min=None, m_max=None, k_min=2, k_max=5, seed=None):
    generador = Generador(seed)
    casos = generador.generar_casos(cantidad_casos, n_min, n_max, m_min, m_max, k_min, k_max)

    resultados = []

    for i, (grafo, k) in enumerate(casos):
        print(f"Procesando caso {i+1}/{cantidad_casos}")

        try:
            resultado_backtracking = backtracking(grafo, k)
        except Exception as e:
            print(f"Error en backtracking para caso {i+1}: {str(e)}")
            resultado_backtracking = None

        try:
            resultado_pl  = k_clustering_por_pl(grafo, k)

        except Exception as e:
            print(f"Error en PL para caso {i+1}: {str(e)}")
            resultado_pl = None

        caso = {
            'n': len(grafo.obtener_vertices()),
            'm': sum(len(grafo.vecinos(v)) for v in grafo.obtener_vertices()) // 2,
            'k': k,
            'backtracking': {
                'tiempo': resultado_backtracking['tiempo_ejecucion'] if resultado_backtracking else None,
                'max_diametro': resultado_backtracking['max_diametro'] if resultado_backtracking else None
            },
            'programacion_lineal': {
                'tiempo': resultado_pl['tiempo_ejecucion'] if resultado_pl else None,
                'max_diametro': resultado_pl['max_diametro'] if resultado_pl else None
            }
        }
        resultados.append(caso)

    return resultados

def mostrar_comparacion_texto(resultados):
    print(f"{'Caso':<4} {'n':<3} {'m':<4} {'k':<3} {'Tiempo BT (s)':<15} {'Tiempo PL (s)':<15} {'Diam. BT':<8} {'Diam. PL':<8} {'Ganador':<10}")
    for i, caso in enumerate(resultados, 1):
        n = caso['n']
        m = caso['m']
        k = caso['k']
        tiempo_bt = caso['backtracking']['tiempo']
        tiempo_pl = caso['programacion_lineal']['tiempo']
        diam_bt = caso['backtracking']['max_diametro']
        diam_pl = caso['programacion_lineal']['max_diametro']

        # Decidir ganador
        if tiempo_bt < tiempo_pl:
            ganador = 'Backtracking'
        elif tiempo_pl < tiempo_bt:
            ganador = 'Program. Lineal'
        else:
            # Tiempos iguales, comparar diámetro
            if diam_bt < diam_pl:
                ganador = 'Backtracking'
            elif diam_pl < diam_bt:
                ganador = 'Program. Lineal'
            else:
                ganador = 'Empate'

        print(f"{i:<4} {n:<3} {m:<4} {k:<3} {tiempo_bt:<15.6f} {tiempo_pl:<15.6f} {diam_bt:<8} {diam_pl:<8} {ganador:<10}")

if __name__ == "__main__":
    resultados = realizar_mediciones(
        cantidad_casos=10,  # Número de casos a probar
        n_min=10,          # Mínimo número de vértices
        n_max=20,          # Máximo número de vértices
        k_min=2,           # Mínimo número de clusters
        k_max=4,           # Máximo número de clusters
        seed=42            # Semilla para reproducibilidad
    )

    mostrar_comparacion_texto(resultados)
    # graficar_comparacion(resultados)