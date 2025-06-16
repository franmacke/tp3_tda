from src.grafo import Grafo
import time

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

def medir_tiempo(func):
    def wrapper(*args, **kwargs):
        tiempo_inicio = time.time()
        resultado = func(*args, **kwargs)
        tiempo_fin = time.time()
        tiempo_total = tiempo_fin - tiempo_inicio

        if resultado is not None:
            resultado['tiempo_ejecucion'] = tiempo_total
            print(f"Tiempo de ejecución: {tiempo_total:.6f} segundos")

        return resultado
    return wrapper
