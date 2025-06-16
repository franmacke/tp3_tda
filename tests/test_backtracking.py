import os
from src.backtracking import backtracking
from utils import leer_archivo_conexiones
from tests.base_test_case import BaseTestClass

class TestBacktracking(BaseTestClass):

    def test_all_files(self):
        if not self.expected_results:
            self.fail("No se encontraron resultados esperados en el archivo")

        for (filename, k), expected_max_dist in self.expected_results.items():
            with self.subTest(filename=filename, k=k):
                print(f"\nTesting {filename} with k={k}")

                grafo = leer_archivo_conexiones(os.path.join(self.data_dir, filename))
                resultado = backtracking(grafo, k)
                self.assertIsNotNone(resultado, f"Backtracking retorno None para {filename} con k={k}")

                print(f"Maxima distancia obtenida: {resultado["max_diametro"]}, esperada: {expected_max_dist}")
                self.assertEqual(resultado["max_diametro"], expected_max_dist,
                               f"Failed for {filename} with k={k}. Expected max distance {expected_max_dist}, got {resultado["max_diametro"]}")
