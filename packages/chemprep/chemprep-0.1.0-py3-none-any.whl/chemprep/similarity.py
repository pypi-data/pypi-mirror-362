from rdkit import DataStructs
from .fingerprints import generate_fingerprint

def get_available_similarity_metrics():
    """
    Returns a list of available similarity metrics.
    """
    return [
        "Tanimoto",
        "Dice",
        "Cosine",
        "Sokal",
        "Russel",
        "RogotGoldberg",
        "AllBit",
        "Kulczynski",
        "McConnaughey",
        "Asymmetric",
        "BraunBlanquet",
    ]

def calculate_similarity(smiles1: str, smiles2: str, fingerprint_type: str = "Morgan", similarity_metric: str = "Tanimoto"):
    """
    Calculates the similarity between two molecules.

    Args:
        smiles1: The SMILES string of the first molecule.
        smiles2: The SMILES string of the second molecule.
        fingerprint_type: The type of fingerprint to use.
        similarity_metric: The similarity metric to use.

    Returns:
        The calculated similarity score.
    """
    fp1 = generate_fingerprint(smiles1, fingerprint_type)
    fp2 = generate_fingerprint(smiles2, fingerprint_type)

    if similarity_metric == "Tanimoto":
        return DataStructs.TanimotoSimilarity(fp1, fp2)
    elif similarity_metric == "Dice":
        return DataStructs.DiceSimilarity(fp1, fp2)
    elif similarity_metric == "Cosine":
        return DataStructs.CosineSimilarity(fp1, fp2)
    elif similarity_metric == "Sokal":
        return DataStructs.SokalSimilarity(fp1, fp2)
    elif similarity_metric == "Russel":
        return DataStructs.RusselSimilarity(fp1, fp2)
    elif similarity_metric == "RogotGoldberg":
        return DataStructs.RogotGoldbergSimilarity(fp1, fp2)
    elif similarity_metric == "AllBit":
        return DataStructs.AllBitSimilarity(fp1, fp2)
    elif similarity_metric == "Kulczynski":
        return DataStructs.KulczynskiSimilarity(fp1, fp2)
    elif similarity_metric == "McConnaughey":
        return DataStructs.McConnaugheySimilarity(fp1, fp2)
    elif similarity_metric == "Asymmetric":
        return DataStructs.AsymmetricSimilarity(fp1, fp2)
    elif similarity_metric == "BraunBlanquet":
        return DataStructs.BraunBlanquetSimilarity(fp1, fp2)
    else:
        raise ValueError(f"Unsupported similarity metric: {similarity_metric}")
