import argparse
import pandas as pd
from .fingerprints import generate_fingerprint, get_available_fingerprints
from .similarity import calculate_similarity, get_available_similarity_metrics
from .descriptors import get_all_descriptors

def main():
    parser = argparse.ArgumentParser(description="A command-line tool for molecular fingerprinting, similarity calculations, and descriptor generation.")
    subparsers = parser.add_subparsers(dest="command")

    # Fingerprint command
    parser_fp = subparsers.add_parser("fingerprint", help="Generate molecular fingerprints.")
    parser_fp.add_argument("smiles", nargs="?", help="SMILES string of the molecule.")
    parser_fp.add_argument("-i", "--input", help="Path to a file with SMILES (one per line, or a CSV with a 'SMILES' column).")
    parser_fp.add_argument("-t", "--type", default="Morgan", choices=get_available_fingerprints(), help="The type of fingerprint to generate.")
    parser_fp.add_argument("-o", "--output", help="Path to the output file (CSV).")

    # Similarity command
    parser_sim = subparsers.add_parser("similarity", help="Calculate molecular similarity.")
    parser_sim.add_argument("smiles1", help="SMILES string of the first molecule.")
    parser_sim.add_argument("smiles2", help="SMILES string of the second molecule.")
    parser_sim.add_argument("-t", "--type", default="Morgan", choices=get_available_fingerprints(), help="The type of fingerprint to use.")
    parser_sim.add_argument("-m", "--metric", default="Tanimoto", choices=get_available_similarity_metrics(), help="The similarity metric to use.")

    # Descriptor command
    parser_desc = subparsers.add_parser("descriptors", help="Generate molecular descriptors.")
    parser_desc.add_argument("smiles", nargs="?", help="SMILES string of the molecule.")
    parser_desc.add_argument("-i", "--input", help="Path to a file with SMILES (one per line, or a CSV with a 'SMILES' column).")
    parser_desc.add_argument("-o", "--output", help="Path to the output file (CSV).")

    args = parser.parse_args()

    if args.command == "fingerprint":
        if args.smiles:
            smiles_list = [args.smiles]
        elif args.input:
            if args.input.endswith(".csv"):
                df = pd.read_csv(args.input)
                smiles_list = df["SMILES"].tolist()
            else:
                with open(args.input) as f:
                    smiles_list = [line.strip() for line in f]
        else:
            parser_fp.error("Either a SMILES string or an input file must be provided.")

        fingerprints = [generate_fingerprint(s, args.type) for s in smiles_list]
        df_out = pd.DataFrame({"SMILES": smiles_list, "Fingerprint": fingerprints})

        if args.output:
            df_out.to_csv(args.output, index=False)
        else:
            print(df_out)

    elif args.command == "similarity":
        similarity = calculate_similarity(args.smiles1, args.smiles2, args.type, args.metric)
        print(f"The {args.metric} similarity between {args.smiles1} and {args.smiles2} is: {similarity}")

    elif args.command == "descriptors":
        if args.smiles:
            smiles_list = [args.smiles]
        elif args.input:
            if args.input.endswith(".csv"):
                df = pd.read_csv(args.input)
                smiles_list = df["SMILES"].tolist()
            else:
                with open(args.input) as f:
                    smiles_list = [line.strip() for line in f]
        else:
            parser_desc.error("Either a SMILES string or an input file must be provided.")

        all_descriptors = [get_all_descriptors(s) for s in smiles_list]
        df_out = pd.DataFrame(all_descriptors)
        df_out.insert(0, "SMILES", smiles_list)


        if args.output:
            df_out.to_csv(args.output, index=False)
        else:
            print(df_out)

if __name__ == "__main__":
    main()
