
import pulp
from pulp import LpAffineExpression as Sumatoria
from grafo import Grafo
from itertools import combinations


def k_clustering_por_pl(grafo : Grafo, k):
    nodes = grafo.obtener_vertices()
    n = len(nodes)
    model = pulp.LpProblem("Minimax_Diameter_Clustering", pulp.LpMinimize)

    # Variables
    x = pulp.LpVariable.dicts("x", ((v, i) for v in nodes for i in range(k)), cat='Binary')
    D = pulp.LpVariable.dicts("D", (i for i in range(k)), lowBound=0, cat='Continuous')
    D_max = pulp.LpVariable("D_max", lowBound=0, cat='Continuous')
    
    # Restricciones
    for v in nodes:
        model += pulp.lpSum(x[v, i] for i in range(k)) == 1

    # Definir D_i como el máximo entre distancias dentro del cluster i
    for i in range(k):
        for u, v in combinations(nodes, 2):
            dist = grafo.bfs_distancia_uv(u, v)
            model += D[i] >= dist * (x[u, i] + x[v, i] - 1)

    # D_max es el máximo de los D_i
    for i in range(k):
        model += D_max >= D[i]

    # Objetivo: minimizar D_max
    model += D_max
    
    # Resolver
    solver = pulp.PULP_CBC_CMD(msg=True)
    model.solve(solver)
    
    # Procesar resultados
    status = pulp.LpStatus[model.status]
    if status != 'Optimal':
        raise ValueError(f"Solución no óptima: {status}")

    # Construir clusters
    clusters = {i: [] for i in range(k)}
    for v in nodes:
        for i in range(k):
            if pulp.value(x[v, i]) > 0.5:
                clusters[i].append(v)

    return [clusters[i] for i in range(k)]

