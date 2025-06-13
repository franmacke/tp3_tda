from src.grafo import Grafo

def backtracking(grafo: Grafo, k_clusters):
    vertices = grafo.obtener_vertices()
    if len(vertices) < k_clusters:
        return None

    # Inicialización de la solucion
    clusters = {i: [] for i in range(k_clusters)}
    mejor_solucion = {
        'max_diametro': float('inf'),
        'clusters': None
    }

    def calcular_diametro_cluster(cluster):
        if len(cluster) <= 1:
            return 0
        max_dist = 0
        for u in cluster:
            for v in cluster:
                if u != v:
                    dist = grafo.distancia(u, v)
                    max_dist = max(max_dist, dist)
        return max_dist

    def es_solucion_valida():
        # Verifico que todos los clusters tengan por lo menos un vertice
        return all(len(cluster) > 0 for cluster in clusters.values())

    def backtracking_recursivo(vertice_actual):
        # Caso base
        if vertice_actual == len(vertices):
            # Verificar que la solución sea válida
            if not es_solucion_valida():
                return

            max_diametro = 0
            for cluster in clusters.values():
                diametro = calcular_diametro_cluster(cluster)
                max_diametro = max(max_diametro, diametro)

            if max_diametro < mejor_solucion['max_diametro']:
                mejor_solucion['max_diametro'] = max_diametro
                mejor_solucion['clusters'] = {k: v.copy() for k, v in clusters.items()}
            return

        vertice = vertices[vertice_actual]

        for cluster_index in range(k_clusters):
            if vertice_actual == len(vertices) - 1:
                clusters_vacios = sum(1 for c in clusters.values() if len(c) == 0)
                if clusters_vacios > 0 and len(clusters[cluster_index]) > 0:
                    continue

            es_compatible = True
            for v in clusters[cluster_index]:
                if grafo.distancia(vertice, v) > mejor_solucion['max_diametro']:
                    es_compatible = False
                    break

            if not es_compatible:
                continue

            clusters[cluster_index].append(vertice)

            diametro_actual = calcular_diametro_cluster(clusters[cluster_index])

            if diametro_actual < mejor_solucion['max_diametro']:
                backtracking_recursivo(vertice_actual + 1)

            clusters[cluster_index].pop()

    backtracking_recursivo(0)

    return mejor_solucion
