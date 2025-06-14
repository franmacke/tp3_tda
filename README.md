# TP3: BT, PL y Aproximaciones

Este repositorio contiene la solución para el "Trabajo Práctico 3", que explora el Backtracking (BT), Lenguajes de Programación (PL) y varios algoritmos de aproximación.
## Configuración del Proyecto
### 1. Crear un Entorno Virtual

Se recomienda usar un entorno virtual para gestionar las dependencias del proyecto. Esto asegura que las librerías que instales no entren en conflicto con otros proyectos de Python en tu sistema.

    python3 -m venv venv

### 2. Activar el Entorno Virtual

Antes de instalar las dependencias o ejecutar el proyecto, activa el entorno virtual:

En Linux/macOS:

    source .venv/bin/activate

En Windows:

    .venv\Scripts\activate

### 3. Instalar Dependencias

Una vez que el entorno virtual esté activo, instala las librerías requeridas usando pip:

    pip install -r requirements.txt
---
## Ejecución del Programa Principal
### Tests
El script principal tp3.py permite ejecutar el algoritmo de backtracking con un grafo y un número de clusters específicos, o ejecutar las pruebas unitarias.
Pruebas Unitarias

    python tp3.py test

## Ejecutar el Algoritmo de Backtracking y Programacion Lineal

Para ejecutar los algoritmos, debes proporcionar la ruta a un archivo que contenga la definición del grafo y un valor K que representa el número de clusters deseado.

Uso:

    python tp3.py <ruta/a/archivo.txt> <K>

**<ruta/a/archivo.txt>**: La ruta al archivo de texto que describe las conexiones del grafo.
**<K>**: Un número entero que indica la cantidad de clusters a formar.

Ejemplo:

    python tp3.py data/grafo_ejemplo.txt 3

El programa imprimirá la máxima distancia (diámetro) encontrada en la mejor solución de clusters y los clusters resultantes.
