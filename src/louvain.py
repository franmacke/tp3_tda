from collections import defaultdict
from src.grafo import Grafo
import random

from utils import medir_tiempo


def calcular_modularidad(grafo: Grafo, particion):
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

def una_iteracion_louvain(grafo: Grafo, particion):
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

            enlaces_por_comunidad = defaultdict(int)
            for vecino in vecinos:
                comunidad_vecino = particion[vecino]
                enlaces_por_comunidad[comunidad_vecino] += 1

            mejor_delta = 0
            mejor_comunidad = comunidad_actual

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

def grafo_inducido(grafo: Grafo, particion):
    nuevo_grafo = Grafo()
    comunidad_a_nodos = defaultdict(list)

    for nodo, comunidad in particion.items():
        comunidad_a_nodos[comunidad].append(nodo)

    comunidad_ids = list(comunidad_a_nodos.keys())

    for i in comunidad_ids:
        for j in comunidad_ids:
            if i > j:
                continue
            conexiones = 0
            for u in comunidad_a_nodos[i]:
                for v in comunidad_a_nodos[j]:
                    if v in grafo.vecinos(u):
                        conexiones += 1
            if conexiones > 0:
                nuevo_grafo.agregar_arista(i, j)
    return nuevo_grafo, comunidad_a_nodos

def diametro_cluster(grafo: Grafo, nodos):
    max_dist = 0
    nodos = list(nodos)
    for i in range(len(nodos)):
        for j in range(i + 1, len(nodos)):
            dist = grafo.bfs_distancia_uv(nodos[i], nodos[j])
            if dist != float('inf') and dist > max_dist:
                max_dist = dist
    return max_dist

def max_diametro_clusters(grafo: Grafo, clusters):
    max_diam = 0
    for nodos in clusters.values():
        diam = diametro_cluster(grafo, nodos)
        if diam > max_diam:
            max_diam = diam
    return max_diam



def obtener_particion_cercana_a_k_no_mayor(jerarquia, k):
    mejor_particion = None
    mejor_diferencia = float('inf')
    for particion in reversed(jerarquia):
        num_clusters = len(particion)
        if num_clusters <= k:
            diff = k - num_clusters
            if diff < mejor_diferencia:
                mejor_diferencia = diff
                mejor_particion = particion
                if diff == 0:
                    break
    return mejor_particion

@medir_tiempo
def algoritmo_louvain_k(grafo: Grafo, k: int):
    grafo_original = grafo
    particion = {v: v for v in grafo.obtener_vertices()}
    jerarquia = []
    historial = {v: [v] for v in grafo.obtener_vertices()}
    particion_anterior = None

    while True:
        particion = una_iteracion_louvain(grafo, particion)
        if particion == particion_anterior:
            break
        particion_anterior = particion.copy()

        comunidades = defaultdict(list)
        for nodo, comunidad in particion.items():
            comunidades[comunidad].append(nodo)

        nuevas_comunidades = defaultdict(list)
        for comunidad, nodos in comunidades.items():
            for nodo in nodos:
                nuevas_comunidades[comunidad].extend(historial[nodo])

        jerarquia.append(dict(nuevas_comunidades))

        num_comunidades = len(nuevas_comunidades)
        print(f"Número de comunidades en iteración: {num_comunidades}")

        if num_comunidades <= k:
            break  
        
        grafo, _ = grafo_inducido(grafo, particion)
        historial = nuevas_comunidades
        particion = {v: v for v in grafo.obtener_vertices()}


    resultado_clusters = obtener_particion_cercana_a_k_no_mayor(jerarquia, k)
    if resultado_clusters is None:
        resultado_clusters = jerarquia[-1]

    max_distancia = max_diametro_clusters(grafo_original, resultado_clusters)

    return {
        "max_distancia": max_distancia,
        "clusters": resultado_clusters
    }
