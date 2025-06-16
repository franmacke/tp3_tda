from src.grafo import Grafo
from utils import medir_tiempo

@medir_tiempo
def backtracking(grafo: Grafo, k_clusters):
    vertices = sorted(grafo.obtener_vertices(), key=lambda v: -len(grafo.vecinos(v)))

    if len(vertices) < k_clusters:
        return None

    distancias = grafo.matriz_distancias
    clusters = {i: [] for i in range(k_clusters)}
    diametros_clusters = [0 for _ in range(k_clusters)]

    mejor_solucion = {
        'max_diametro': float('inf'),
        'clusters': None
    }

    def esta_lleno_los_clusters_anteriores(clusters, cluster_index):
        if any(len(clusters[i]) == 0 for i in range(cluster_index)):
            return False
        return True

    def me_paso(diametros_clusters, mejor_solucion):
        return max(diametros_clusters) >= mejor_solucion['max_diametro']

    def calcular_nuevo_diametro(vertice, cluster, distancias, diametro_actual, mejor_solucion):
        nuevo_diametro = diametro_actual

        for v in cluster:
            d = distancias[vertice][v]
            if d == float('inf'):
                break
            nuevo_diametro = max(nuevo_diametro, d)

            if nuevo_diametro >= mejor_solucion['max_diametro']:
                break

        return nuevo_diametro

    def backtracking_recursivo(vertice_actual):
        if vertice_actual == len(vertices):

            max_diametro = max(diametros_clusters)

            if max_diametro < mejor_solucion['max_diametro']:
                mejor_solucion['max_diametro'] = max_diametro
                mejor_solucion['clusters'] = {k: v.copy() for k, v in clusters.items()}
            return

        vertice = vertices[vertice_actual]

        if me_paso(diametros_clusters, mejor_solucion):
            return

        for cluster_index in range(k_clusters):
            if not esta_lleno_los_clusters_anteriores(clusters, cluster_index):
                continue

            nuevo_diametro = calcular_nuevo_diametro(
                vertice,
                clusters[cluster_index],
                distancias,
                diametros_clusters[cluster_index],
                mejor_solucion
            )

            clusters[cluster_index].append(vertice)
            anterior = diametros_clusters[cluster_index]
            diametros_clusters[cluster_index] = nuevo_diametro

            backtracking_recursivo(vertice_actual + 1)

            clusters[cluster_index].pop()
            diametros_clusters[cluster_index] = anterior

    backtracking_recursivo(0)
    return mejor_solucion