from rdkit import Chem
from rdkit.Chem import Descriptors

def get_all_descriptors(smiles: str):
    """
    Calculates all available descriptors for a given SMILES string.

    Args:
        smiles: The SMILES string of the molecule.

    Returns:
        A dictionary of all available descriptors.
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        raise ValueError("Invalid SMILES string")

    descriptors = {}
    for name, func in Descriptors.descList:
        try:
            descriptors[name] = func(mol)
        except Exception as e:
            descriptors[name] = None
            print(f"Could not calculate descriptor {name} for {smiles}: {e}")

    return descriptors
