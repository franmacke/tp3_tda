from collections import deque

class Grafo:
    def __init__(self):
        self.adyacencias = {}
        self.matriz_distancias = {}

    def agregar_conexiones(self, conexiones: list[tuple]):
        for u, v in conexiones:
            self.agregar_arista(u, v)
        self._calcular_matriz_distancias()

    def agregar_vertice(self, v):
        if v not in self.adyacencias:
            self.adyacencias[v] = []

    def agregar_arista(self, u, v):
        self.agregar_vertice(u)
        self.agregar_vertice(v)

        if v not in self.adyacencias[u]:
            self.adyacencias[u].append(v)
        if u not in self.adyacencias[v]:
            self.adyacencias[v].append(u)

    def vecinos(self, v):
        return self.adyacencias.get(v, [])

    def obtener_vertices(self):
        return list(self.adyacencias.keys())

    def bfs_distancia_uv(self, u, v):
        if u == v:
            return 0
        visitado = set()
        # (nodo, distancia)
        cola = deque([(u, 0)]) 
        while cola:
            actual, distancia = cola.popleft()
            if actual == v:
                return distancia
            if actual not in visitado:
                visitado.add(actual)
                for vecino in self.vecinos(actual):
                    if vecino not in visitado:
                        cola.append((vecino, distancia + 1))
        return None
    
    def __str__(self):
        return "\n".join(
            f"{v}: {self.adyacencias[v]}" for v in sorted(self.adyacencias)
        )

    def _calcular_matriz_distancias(self):
        self.matriz_distancias = {}
        for origen in self.adyacencias:
            self.matriz_distancias[origen] = self._bfs_distancias(origen)

    def _bfs_distancias(self, origen):
        distancias = {v: float("inf") for v in self.adyacencias}
        distancias[origen] = 0
        cola = deque([origen])
        while cola:
            actual = cola.popleft()
            for vecino in self.vecinos(actual):
                if distancias[vecino] == float("inf"):
                    distancias[vecino] = distancias[actual] + 1
                    cola.append(vecino)
        return distancias

    def distancia(self, origen, destino):
        if origen not in self.matriz_distancias:
            return float("inf")
        return self.matriz_distancias[origen].get(destino, float("inf"))