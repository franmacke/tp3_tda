from collections import defaultdict
import random
from grafo import Grafo

def calcular_modularidad(grafo, particion):
    m = sum(len(grafo.vecinos(v)) for v in grafo.obtener_vertices()) / 2
    grados = {v: len(grafo.vecinos(v)) for v in grafo.obtener_vertices()}
    comunidades = defaultdict(set)
    for nodo, comunidad in particion.items():
        comunidades[comunidad].add(nodo)

    modularidad = 0
    for comunidad in comunidades.values():
        for u in comunidad:
            for v in comunidad:
                A_uv = 1 if v in grafo.vecinos(u) else 0
                modularidad += A_uv - (grados[u] * grados[v]) / (2 * m)
    return modularidad / (2 * m)

def una_iteracion_louvain(grafo, particion):
    m = sum(len(grafo.vecinos(v)) for v in grafo.obtener_vertices()) / 2
    grados = {v: len(grafo.vecinos(v)) for v in grafo.obtener_vertices()}
    nodos = list(grafo.obtener_vertices())
    mejora = True

    while mejora:
        mejora = False
        random.shuffle(nodos)
        for nodo in nodos:
            comunidad_actual = particion[nodo]
            vecinos = grafo.vecinos(nodo)

            # Conteo de enlaces hacia cada comunidad vecina
            enlaces_por_comunidad = defaultdict(int)
            for vecino in vecinos:
                comunidad_vecino = particion[vecino]
                enlaces_por_comunidad[comunidad_vecino] += 1

            mejor_delta = 0
            mejor_comunidad = comunidad_actual

            # Quito nodo de su comunidad temporalmente
            particion[nodo] = -1
            for comunidad, enlaces in enlaces_por_comunidad.items():
                suma_grados = sum(grados[n] for n in particion if particion[n] == comunidad)
                delta_q = enlaces - grados[nodo] * suma_grados / (2 * m)
                if delta_q > mejor_delta:
                    mejor_delta = delta_q
                    mejor_comunidad = comunidad

            if mejor_comunidad != comunidad_actual:
                particion[nodo] = mejor_comunidad
                mejora = True
            else:
                particion[nodo] = comunidad_actual

    return particion

def grafo_inducido(grafo, particion):
    nuevo_grafo = Grafo()
    comunidad_a_nodos = defaultdict(list)
    for nodo, comunidad in particion.items():
        comunidad_a_nodos[comunidad].append(nodo)

    lista_comunidades = list(comunidad_a_nodos.values())
    for i, comunidad_i in enumerate(lista_comunidades):
        for j, comunidad_j in enumerate(lista_comunidades):
            if i <= j:
                # Cuento aristas entre comunidades
                conexiones = 0
                for u in comunidad_i:
                    for v in comunidad_j:
                        if u != v and v in grafo.vecinos(u):
                            conexiones += 1
                if conexiones > 0:
                    nuevo_grafo.agregar_arista(i, j)
    return nuevo_grafo, comunidad_a_nodos

def algoritmo_louvain_k(grafo: Grafo, k: int):
    particion = {v: v for v in grafo.obtener_vertices()}
    jerarquia = []

    while True:
        particion = una_iteracion_louvain(grafo, particion)

        # Agrupo nodos por comunidad
        comunidades = defaultdict(list)
        for nodo, comunidad in particion.items():
            comunidades[comunidad].append(nodo)

        jerarquia.append(dict(comunidades))

        num_comunidades = len(set(particion.values()))
        if num_comunidades <= k:
            break

        grafo, comunidad_a_nodos = grafo_inducido(grafo, particion)

        # Reasigno nodos originales a nuevas comunidades
        nueva_particion = {}
        for nuevo_id, nodos in comunidad_a_nodos.items():
            for nodo in nodos:
                nueva_particion[nodo] = nuevo_id
        particion = nueva_particion

    # Si se pasó y hay menos de K comunidades, se devuelve la última válida con >= K
    return jerarquia[-1]

#Ejemplo para ver los k clusters

"""
g = Grafo()
g.agregar_conexiones([
    (1, 2), (2, 3), (3, 1),
    (4, 5), (5, 6), (6, 4),
    (7, 8), (8, 9), (9, 7),
    (3, 4), (6, 7)
])

resultado_k = algoritmo_louvain_k(g, k=2)

for id_com, nodos in resultado_k.items():
    print(f"  Comunidad {id_com}: {nodos}")
"""