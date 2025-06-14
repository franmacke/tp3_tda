# from src.grafo import Grafo
#
# def backtracking(grafo: Grafo, k_clusters):
#     vertices = grafo.obtener_vertices()
#     if len(vertices) < k_clusters:
#         return None
#
#     # Inicialización de la solucion
#     clusters = {i: [] for i in range(k_clusters)}
#     mejor_solucion = {
#         'max_diametro': float('inf'),
#         'clusters': None
#     }
#
#     def calcular_diametro_cluster(cluster):
#         if len(cluster) <= 1:
#             return 0
#         max_dist = 0
#         for u in cluster:
#             for v in cluster:
#                 if u != v:
#                     dist = grafo.distancia(u, v)
#                     max_dist = max(max_dist, dist)
#         return max_dist
#
#     def es_solucion_valida():
#         # Verifico que todos los clusters tengan por lo menos un vertice
#         return all(len(cluster) > 0 for cluster in clusters.values())
#
#     def backtracking_recursivo(vertice_actual):
#         # Caso base
#         if vertice_actual == len(vertices):
#             # Verificar que la solución sea válida
#             if not es_solucion_valida():
#                 return
#
#             max_diametro = 0
#             for cluster in clusters.values():
#                 diametro = calcular_diametro_cluster(cluster)
#                 max_diametro = max(max_diametro, diametro)
#
#             if max_diametro < mejor_solucion['max_diametro']:
#                 mejor_solucion['max_diametro'] = max_diametro
#                 mejor_solucion['clusters'] = {k: v.copy() for k, v in clusters.items()}
#             return
#
#         vertice = vertices[vertice_actual]
#
#         for cluster_index in range(k_clusters):
#             if vertice_actual == len(vertices) - 1:
#                 clusters_vacios = sum(1 for c in clusters.values() if len(c) == 0)
#                 if clusters_vacios > 0 and len(clusters[cluster_index]) > 0:
#                     continue
#
#             es_compatible = True
#             for v in clusters[cluster_index]:
#                 if grafo.distancia(vertice, v) > mejor_solucion['max_diametro']:
#                     es_compatible = False
#                     break
#
#             if not es_compatible:
#                 continue
#
#             clusters[cluster_index].append(vertice)
#
#             diametro_actual = calcular_diametro_cluster(clusters[cluster_index])
#
#             if diametro_actual < mejor_solucion['max_diametro']:
#                 backtracking_recursivo(vertice_actual + 1)
#
#             clusters[cluster_index].pop()
#
#     backtracking_recursivo(0)
#
#     return mejor_solucion
#

from src.grafo import Grafo


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

    def es_solucion_valida():
        return all(len(cluster) > 0 for cluster in clusters.values())

    def backtracking_recursivo(vertice_actual):
        if vertice_actual == len(vertices):
            if not es_solucion_valida():
                return

            max_diametro = max(diametros_clusters)
            if max_diametro < mejor_solucion['max_diametro']:
                mejor_solucion['max_diametro'] = max_diametro
                mejor_solucion['clusters'] = {k: v.copy() for k, v in clusters.items()}
            return

        # Poda: no hay suficientes vértices restantes para llenar clusters vacíos
        clusters_vacios = sum(1 for c in clusters.values() if len(c) == 0)
        if len(vertices) - vertice_actual < clusters_vacios:
            return

        vertice = vertices[vertice_actual]

        for cluster_index in range(k_clusters):
            # Simetría: no asignar a un cluster si hay uno anterior vacío
            if any(len(clusters[i]) == 0 for i in range(cluster_index)):
                continue

            # Poda por distancia: si ya no puede mejorar, no seguimos
            es_compatible = True
            nuevo_diametro = diametros_clusters[cluster_index]
            for v in clusters[cluster_index]:
                d = distancias[vertice][v]
                if d == float('inf'):
                    es_compatible = False
                    break
                nuevo_diametro = max(nuevo_diametro, d)

            if not es_compatible or nuevo_diametro >= mejor_solucion['max_diametro']:
                continue

            clusters[cluster_index].append(vertice)
            anterior = diametros_clusters[cluster_index]
            diametros_clusters[cluster_index] = nuevo_diametro

            backtracking_recursivo(vertice_actual + 1)

            clusters[cluster_index].pop()
            diametros_clusters[cluster_index] = anterior

    backtracking_recursivo(0)
    return mejor_solucion
