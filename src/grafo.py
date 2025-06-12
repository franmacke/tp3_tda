

class Grafo:
    def __init__(self):
        self.adyacencias = {}

    def agregar_conexiones(self, conexiones: list[tuple]):
        for u, v in conexiones:
            self.agregar_arista(u, v)

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
        return self.adyacencias.keys()

    def __str__(self):
        return '\n'.join(f'{v}: {self.adyacencias[v]}' for v in sorted(self.adyacencias))
