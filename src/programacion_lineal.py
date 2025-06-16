import pulp
from src.grafo import Grafo
from itertools import combinations
from utils import medir_tiempo


@medir_tiempo
def k_clustering_por_pl(grafo : Grafo, k):
    nodes = grafo.obtener_vertices()
    n = len(nodes)

    distancias = grafo.matriz_distancias

    model = pulp.LpProblem("Minimax_Diameter_Clustering", pulp.LpMinimize)

    # Variables
    x = pulp.LpVariable.dicts("x", ((v, i) for v in nodes for i in range(k)), cat='Binary')
    D = pulp.LpVariable.dicts("D", (i for i in range(k)), lowBound=0, cat='Integer')
    D_max = pulp.LpVariable("D_max", lowBound=0, cat='Integer')

    # Restricciones
    for v in nodes:
        model += pulp.lpSum(x[v, i] for i in range(k)) == 1

    # Only add constraints for pairs with finite distances
    for i in range(k):
        for u, v in combinations(nodes, 2):
            dist = distancias[u][v]
            if dist != float('inf'):
                model += D[i] >= dist * (x[u, i] + x[v, i] - 1)

    # D_max es el máximo de los D_i
    for i in range(k):
        model += D_max >= D[i]

    # Objetivo: minimizar D_max
    model += D_max

    # Resolver
    solver = pulp.PULP_CBC_CMD(msg=False)
    model.solve(solver)

    # Procesar resultados
    status = pulp.LpStatus[model.status]
    if status != 'Optimal':
        return {
            'max_diametro': float('inf'),
            'clusters': None,
            'tiempo_ejecucion': 0
        }

    # Construir clusters
    clusters = {i: [] for i in range(k)}
    for v in nodes:
        for i in range(k):
            if pulp.value(x[v, i]) > 0.5:
                clusters[i].append(v)

    return {
        'max_diametro': int(pulp.value(D_max)),
        'clusters': clusters,
        'tiempo_ejecucion': 0
    }
