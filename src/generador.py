import random
from src.grafo import Grafo
from utils import exportar_txt

class Generador:
    def __init__(self, seed=None):
        if seed is not None:
            random.seed(seed)

    def generar_grafo(self, n, m):
        if m < n - 1:
            raise ValueError("No se puede generar un grafo conexo con menos de n-1 aristas")

        grafo = Grafo()
        vertices = list(range(n))

        aristas = set()
        disponibles = vertices[:]
        random.shuffle(disponibles)

        for i in range(1, n):
            u = disponibles[i]
            v = random.choice(disponibles[:i])
            aristas.add((min(u, v), max(u, v)))

        while len(aristas) < m:
            u, v = random.sample(vertices, 2)
            arista = (min(u, v), max(u, v))
            if arista not in aristas:
                aristas.add(arista)

        grafo.agregar_conexiones(list(aristas))
        return grafo

    def generar_casos(self, cantidad, n_min=10, n_max=30, m_min=None, m_max=None, k_min=2, k_max=5):
        """
        :param cantidad: Cuantos casos se quieren generar
        :param n_min: Cantidad de nodos minimo
        :param n_max: Cantidad de nodos maximo
        :param m_min: Cantidad de aristas minima
        :param m_max: Cantidad de aristas maxima
        :param k_min: Cantidad de clusters minima
        :param k_max: Cantidad de clusters maxima
        :return: list[Grafo, int]
        """

        casos = []
        for _ in range(cantidad):
            n = random.randint(n_min, n_max)
            max_aristas = n * (n - 1) // 2
            m_sup = m_max if m_max else max_aristas
            m_inf = max(n - 1, m_min or n)

            m = random.randint(m_inf, min(m_sup, max_aristas))
            k = random.randint(k_min, min(k_max, n))
            grafo = self.generar_grafo(n, m)
            casos.append((grafo, k))
        return casos


if __name__ == "__main__":
    generador = Generador(seed=123)
    casos = generador.generar_casos(
        cantidad=4, n_min=250, n_max=250, k_min=6, k_max=15
    )
    exportar_txt(casos, 'casos')