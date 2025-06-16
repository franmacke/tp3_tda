import unittest
import os


class BaseTestClass(unittest.TestCase):
    def setUp(self):
        self.data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
        print(f"\nLooking for results file in: {self.data_dir}")

        self.expected_results = self._cargar_resultados_esperados()
        print(f"\nLoaded {len(self.expected_results)} test cases:")

        for (filename, k), max_dist in self.expected_results.items():
            print(f"- {filename} with k={k}, expected max distance: {max_dist}")

    def _cargar_resultados_esperados(self):
        results = {}
        current_file = None
        current_k = None

        results_file = os.path.join(self.data_dir, "Resultados Esperados.txt")
        print(f"Opening results file: {results_file}")

        if not os.path.exists(results_file):
            print(f"ERROR: Results file not found at {results_file}")
            return results

        with open(results_file, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                if line.startswith("Como siempre"):
                    continue

                if ".txt" in line and not line.startswith("Asignación"):
                    parts = line.split()
                    if len(parts) >= 2:
                        current_file = parts[0]
                        try:
                            current_k = int(parts[1])
                            print(f"Found test case: {current_file} with k={current_k}")
                        except ValueError:
                            print(f"Warning: Could not parse k value from line: {line}")
                            continue

                elif "Maxima distancia dentro del cluster:" in line:
                    if current_file and current_k is not None:
                        try:
                            max_dist = int(line.split(":")[1].strip())
                            results[(current_file, current_k)] = max_dist
                            print(f"Added result for {current_file} with k={current_k}: max_dist={max_dist}")
                        except (ValueError, IndexError):
                            print(f"Warning: Could not parse max distance from line: {line}")
                        current_file = None
                        current_k = None
        return results