import sys
import unittest

from utils import leer_archivo_conexiones
from src.backtracking import backtracking
from src.programacion_lineal import k_clustering_por_pl
from src.louvain import algoritmo_louvain_k



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
    bt = backtracking(grafo, K)

    print(f"Maxima distancia: {bt['max_diametro']}")
    print(f"Clusters: {bt['clusters']}")
    print("================================")

    print("\n\n")
    
    # Programacion Lineal
    print("================================")
    print("Resultados PLE:")
    pl = k_clustering_por_pl(grafo, K)

    print(f"Maxima distancia: {pl['max_diametro']}")
    print(f"Clusters: {pl['clusters']}")
    print("================================")

    print("\n\n")
    
    # Louvain
    print("================================")
    print("Resultados Louvain:")
    al = algoritmo_louvain_k(grafo, K)

    print(f"Maxima distancia: {al['max_distancia']}")
    print(f"Clusters: {al['clusters']}")
    print("================================")

    print("\n\n")
    
    
    # Diferencias de tiempo
    print("================================")
    print(f"Tiempo backtracking: {bt['tiempo_ejecucion']}")
    print(f"Tiempo PLE: {pl['tiempo_ejecucion']}")
    print(f"Diferencia: {bt['tiempo_ejecucion'] - pl['tiempo_ejecucion']}")
    print("================================")
    