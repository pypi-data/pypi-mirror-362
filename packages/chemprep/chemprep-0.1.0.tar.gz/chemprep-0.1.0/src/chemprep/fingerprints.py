from rdkit import Chem
from rdkit.Chem import AllChem, MACCSkeys
from rdkit.Chem.rdmolops import RDKFingerprint
from rdkit.Chem.AtomPairs import Pairs, Torsions
from rdkit.Chem.Fingerprints import FingerprintMols

def get_available_fingerprints():
    """
    Returns a list of available fingerprint types.
    """
    return [
        "MACCS",
        "RDKit",
        "Topological/Daylight",
        "AtomPair",
        "TopologicalTorsion",
        "Morgan",
        "ECFP2",
        "ECFP4",
        "ECFP6",
        "FCFP2",
        "FCFP4",
        "FCFP6",
    ]

def generate_fingerprint(smiles: str, fingerprint_type: str = "Morgan"):
    """
    Generates a molecular fingerprint for a given SMILES string.

    Args:
        smiles: The SMILES string of the molecule.
        fingerprint_type: The type of fingerprint to generate.

    Returns:
        The generated fingerprint.
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        raise ValueError("Invalid SMILES string")

    if fingerprint_type == "MACCS":
        return MACCSkeys.GenMACCSKeys(mol)
    elif fingerprint_type == "RDKit":
        return RDKFingerprint(mol)
    elif fingerprint_type == "Topological/Daylight":
        return FingerprintMols.FingerprintMol(mol)
    elif fingerprint_type == "AtomPair":
        return Pairs.GetAtomPairFingerprint(mol)
    elif fingerprint_type == "TopologicalTorsion":
        return Torsions.GetTopologicalTorsionFingerprint(mol)
    elif fingerprint_type == "Morgan":
        return AllChem.GetMorganFingerprint(mol, 2)
    elif fingerprint_type == "ECFP2":
        return AllChem.GetMorganFingerprint(mol, 1)
    elif fingerprint_type == "ECFP4":
        return AllChem.GetMorganFingerprint(mol, 2)
    elif fingerprint_type == "ECFP6":
        return AllChem.GetMorganFingerprint(mol, 3)
    elif fingerprint_type == "FCFP2":
        return AllChem.GetMorganFingerprint(mol, 1, useFeatures=True)
    elif fingerprint_type == "FCFP4":
        return AllChem.GetMorganFingerprint(mol, 2, useFeatures=True)
    elif fingerprint_type == "FCFP6":
        return AllChem.GetMorganFingerprint(mol, 3, useFeatures=True)
    else:
        raise ValueError(f"Unsupported fingerprint type: {fingerprint_type}")
