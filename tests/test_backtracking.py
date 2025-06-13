import unittest
from src.grafo import Grafo
from src.backtracking import backtracking

class TestBacktracking(unittest.TestCase):
    def setUp(self):
        self.grafo = Grafo()
        # Cargar el grafo desde el archivo
        with open("data/10_3.txt", "r") as f:
            for line in f:
                line = line.strip()
                if not line:  # Ignorar líneas vacías
                    continue
                try:
                    v1, v2 = line.split()
                    if v1 not in self.grafo.obtener_vertices():
                        self.grafo.agregar_vertice(v1)
                    if v2 not in self.grafo.obtener_vertices():
                        self.grafo.agregar_vertice(v2)
                    self.grafo.agregar_arista(v1, v2)
                except ValueError:
                    # Ignorar líneas que no tienen el formato esperado
                    continue

    def test_10_3_2_clusters(self):
        """Prueba para el archivo 10_3.txt con 2 clusters"""
        resultado = backtracking(self.grafo, 2)
        self.assertIsNotNone(resultado)
        max_diametro = self._calcular_max_diametro(resultado)
        self.assertEqual(max_diametro, 2)  # Según resultados esperados

    def test_10_3_5_clusters(self):
        """Prueba para el archivo 10_3.txt con 5 clusters"""
        resultado = backtracking(self.grafo, 5)
        self.assertIsNotNone(resultado)
        max_diametro = self._calcular_max_diametro(resultado)
        self.assertEqual(max_diametro, 1)  # Según resultados esperados

    def _calcular_max_diametro(self, clusters):
        """Calcula el máximo diámetro entre todos los clusters."""
        max_diametro = 0
        for cluster in clusters.values():
            if len(cluster) <= 1:
                continue
            for u in cluster:
                for v in cluster:
                    if u != v:
                        dist = self.grafo.distancia(u, v)
                        max_diametro = max(max_diametro, dist)
        return max_diametro

if __name__ == '__main__':
    unittest.main()
