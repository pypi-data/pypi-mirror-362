import unittest
import subprocess
import os
import pandas as pd
from rdkit.DataStructs import ExplicitBitVect, IntSparseIntVect, LongSparseIntVect, UIntSparseIntVect
from chemprep.fingerprints import generate_fingerprint, get_available_fingerprints
from chemprep.similarity import calculate_similarity, get_available_similarity_metrics
from chemprep.descriptors import get_all_descriptors

class TestChemPrep(unittest.TestCase):

    def test_get_available_fingerprints(self):
        fingerprints = get_available_fingerprints()
        self.assertIsInstance(fingerprints, list)
        self.assertIn("Morgan", fingerprints)

    def test_get_available_similarity_metrics(self):
        metrics = get_available_similarity_metrics()
        self.assertIsInstance(metrics, list)
        self.assertIn("Tanimoto", metrics)

    def test_fingerprint_generation(self):
        smiles = "CCO"
        for fp_type in get_available_fingerprints():
            with self.subTest(fp_type=fp_type):
                fp = generate_fingerprint(smiles, fingerprint_type=fp_type)
                self.assertIsNotNone(fp)
                if fp_type in ["MACCS", "RDKit", "Topological/Daylight"]:
                    self.assertIsInstance(fp, ExplicitBitVect)
                elif fp_type == "AtomPair":
                    self.assertIsInstance(fp, IntSparseIntVect)
                elif fp_type == "TopologicalTorsion":
                    self.assertIsInstance(fp, LongSparseIntVect)
                else:
                    self.assertIsInstance(fp, (IntSparseIntVect, LongSparseIntVect, ExplicitBitVect, UIntSparseIntVect))


    def test_similarity_calculation(self):
        smiles1 = "CCO"
        smiles2 = "CCN"
        similarity = calculate_similarity(smiles1, smiles2, fingerprint_type="Morgan", similarity_metric="Tanimoto")
        self.assertIsInstance(similarity, float)

    def test_descriptor_generation(self):
        smiles = "CCO"
        descriptors = get_all_descriptors(smiles)
        self.assertIsInstance(descriptors, dict)
        self.assertIn("MolWt", descriptors)

    def test_cli_fingerprint(self):
        smiles = "CCO"
        result = subprocess.run(["chemprep", "fingerprint", smiles], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        self.assertIn("SMILES", result.stdout)
        self.assertIn("Fingerprint", result.stdout)

    def test_cli_similarity(self):
        smiles1 = "CCO"
        smiles2 = "CCN"
        result = subprocess.run(["chemprep", "similarity", smiles1, smiles2], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        self.assertIn("similarity", result.stdout)

    def test_cli_descriptors(self):
        smiles = "CCO"
        with open("temp_descriptors.csv", "w") as f:
            subprocess.run(["chemprep", "descriptors", smiles, "-o", "temp_descriptors.csv"], check=True)

        df = pd.read_csv("temp_descriptors.csv")
        self.assertIn("MolWt", df.columns)
        os.remove("temp_descriptors.csv")


if __name__ == '__main__':
    unittest.main()
