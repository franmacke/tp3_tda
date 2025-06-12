import sys
from utils import leer_archivo_conexiones


if __name__ == '__main__':

    args = sys.argv

    if len(args) != 3:
        print("Uso: python tp3.py <path/a/archivo.txt> <K>")
        exit()

    grafo = leer_archivo_conexiones(args[1])
    K = int(args[2])



