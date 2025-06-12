from src.grafo import Grafo

def leer_archivo_conexiones(path):

    with open(path, 'r') as f:
        f.readline()

        conexiones = []
        for linea in f:
            linea = linea.strip().split(',')
            conexiones.append((linea[0], linea[1]))

    grafo = Grafo()
    grafo.agregar_conexiones(conexiones)

    return grafo
