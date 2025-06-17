import os
from src.louvain import algoritmo_louvain_k
from utils import leer_archivo_conexiones
from tests.base_test_class import BaseTestClass

class TestLouvain(BaseTestClass):

    def test_all_files(self):
        if not self.expected_results:
            self.fail("No se encontraron resultados esperados en el archivo")

        for (filename, k), expected_max_dist in self.expected_results.items():
            with (self.subTest(filename=filename, k=k)):
                print(f"\nTesting {filename} with k={k}")

                grafo = leer_archivo_conexiones(os.path.join(self.data_dir, filename))
                resultado = algoritmo_louvain_k(grafo, k)

                self.assertIsNotNone(resultado, f"Louvain retorno None para {filename} con k={k}")