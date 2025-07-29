from pathlib import Path
from typing import Optional
from rdkit import Chem

def split_sdf_to_individuals(
    input_sdf: Path,
    output_dir: Path,
    prefix: str = "ligand_",
    start_index: int = 1,
) -> None:
    """Split a large SDF file into individual SDF files, one molecule per file.
    
    Parameters
    ----------
    input_sdf : Path
        Path to the input SDF file.
    output_dir : Path
        Path to the output directory where individual files will be saved.
    prefix : str, optional
        Prefix for output filenames, by default "ligand_".
    start_index : int, optional
        Starting index for output filenames, by default 1.
    """
    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Read all molecules from input SDF
    supplier = Chem.SDMolSupplier(str(input_sdf), removeHs=False, sanitize=False)
    molecules = [mol for mol in supplier if mol is not None]
    total_molecules = len(molecules)
    
    # Write each molecule to a separate file
    for i, mol in enumerate(molecules):
        # Create output filename
        output_file = output_dir / f"{prefix}{start_index + i}.sdf"
        
        # Write molecule to file
        writer = Chem.SDWriter(str(output_file))
        writer.write(mol)
        writer.close()
        
        print(f"Created {output_file}")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Split a large SDF file into individual files")
    parser.add_argument("input_sdf", type=str, help="Path to input SDF file")
    parser.add_argument("output_dir", type=str, help="Path to output directory")
    parser.add_argument("--prefix", type=str, default="ligand_", help="Prefix for output filenames")
    parser.add_argument("--start-index", type=int, default=1, help="Starting index for output filenames")
    
    args = parser.parse_args()
    
    split_sdf_to_individuals(
        input_sdf=Path(args.input_sdf),
        output_dir=Path(args.output_dir),
        prefix=args.prefix,
        start_index=args.start_index,
    )

if __name__ == "__main__":
    main() 