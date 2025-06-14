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
