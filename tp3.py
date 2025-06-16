import sys
import unittest

from utils import leer_archivo_conexiones
from src.backtracking import backtracking
from src.programacion_lineal import k_clustering_por_pl


if __name__ == "__main__":

    args = sys.argv
    if len(args) == 2 and args[1] == "test":
        loader = unittest.TestLoader()
        start_dir = 'tests'
        suite = loader.discover(start_dir, pattern='test_*.py')
        runner = unittest.TextTestRunner()
        runner.run(suite)
        exit()

    if len(args) != 3:
        print("Uso: python tp3.py <path/a/archivo.txt> <K>")
        exit()

    grafo = leer_archivo_conexiones(args[1])
    K = int(args[2])

    # Backtracking
    print("================================")
    print("Resultados backtracking:")
    mejor_solucion = backtracking(grafo, K)

    print(f"Maxima distancia: {mejor_solucion['max_diametro']}")
    print(f"Clusters: {mejor_solucion['clusters']}")
    print("================================")

    print("\n\n")

    # Programacion Lineal
    print("================================")
    print(k_clustering_por_pl(grafo, K))