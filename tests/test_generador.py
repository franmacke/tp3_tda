import unittest
from src.generador import Generador
from src.grafo import Grafo

def es_conexo(grafo: Grafo):
    vertices = grafo.obtener_vertices()
    if not vertices:
        return True
    visitados = set()
    def dfs(v):
        visitados.add(v)
        for vecino in grafo.vecinos(v):
            if vecino not in visitados:
                dfs(vecino)
    dfs(vertices[0])
    return len(visitados) == len(vertices)

class TestGeneradorGrafo(unittest.TestCase):
    def setUp(self):
        self.generador = Generador(seed=123)
        self.casos = self.generador.generar_casos(
            cantidad=5, n_min=5, n_max=10, k_min=2, k_max=4
        )

    def test_adyacencia_bidireccional(self):
        for idx, (grafo, _) in enumerate(self.casos):
            for v in grafo.obtener_vertices():
                for u in grafo.vecinos(v):
                    self.assertIn(
                        v, grafo.vecinos(u),
                        msg=f"[Caso {idx}] {v} no es vecino de {u} (adyacencia no bidireccional)"
                    )

    def test_sin_vertices_duplicados(self):
        for idx, (grafo, _) in enumerate(self.casos):
            vertices = grafo.obtener_vertices()
            self.assertEqual(
                len(set(vertices)), len(vertices),
                msg=f"[Caso {idx}] Hay vértices duplicados"
            )

    def test_es_conexo(self):
        for idx, (grafo, _) in enumerate(self.casos):
            self.assertTrue(
                es_conexo(grafo),
                msg=f"[Caso {idx}] El grafo no es conexo"
            )

    def test_distancias_finitas(self):
        for idx, (grafo, _) in enumerate(self.casos):
            vertices = grafo.obtener_vertices()
            for i, v in enumerate(vertices):
                for u in vertices[i + 1:]:
                    d = grafo.distancia(v, u)
                    self.assertLess(
                        d, float('inf'),
                        msg=f"[Caso {idx}] Distancia infinita entre {v} y {u}"
                    )