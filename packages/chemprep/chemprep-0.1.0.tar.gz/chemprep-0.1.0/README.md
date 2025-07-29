# ChemPrep

A Python library and command-line tool for molecular fingerprinting, similarity calculations, and descriptor generation using RDKit.

## Installation

```bash
pip install chemprep
```

## Usage

### As a Library

```python
from chemprep.fingerprints import generate_fingerprint, get_available_fingerprints
from chemprep.similarity import calculate_similarity, get_available_similarity_metrics
from chemprep.descriptors import get_all_descriptors

# Get available fingerprints and similarity metrics
print(get_available_fingerprints())
print(get_available_similarity_metrics())

# Generate a fingerprint
smiles = "CCO"
fp = generate_fingerprint(smiles, fingerprint_type="Morgan")
print(fp)

# Calculate similarity
smiles1 = "CCO"
smiles2 = "CCN"
similarity = calculate_similarity(smiles1, smiles2, fingerprint_type="Morgan", similarity_metric="Tanimoto")
print(similarity)

# Generate descriptors
descriptors = get_all_descriptors(smiles)
print(descriptors)
```

### Command-Line Interface

```bash
# Get help
chemprep --help
chemprep fingerprint --help
chemprep similarity --help
chemprep descriptors --help

# Generate a fingerprint for a single SMILES
chemprep fingerprint "CCO"

# Generate fingerprints from a file
chemprep fingerprint -i smiles.txt -t RDKit -o fingerprints.csv

# Calculate similarity
chemprep similarity "CCO" "CCN" -t Morgan -m Tanimoto

# Generate descriptors for a single SMILES
chemprep descriptors "CCO"

# Generate descriptors from a file
chemprep descriptors -i smiles.csv -o descriptors.csv
```

## Development

### Setup

```bash
git clone https://github.com/santuchal/ChemPrep.git
cd chemprep
pip install -e .[dev]
```

### Running Tests

```bash
python -m unittest discover tests
```
