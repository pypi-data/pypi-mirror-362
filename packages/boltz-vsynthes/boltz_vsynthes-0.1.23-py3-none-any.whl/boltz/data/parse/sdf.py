import os
from pathlib import Path
from typing import Optional

from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem.rdchem import Mol
from rdkit.Chem.rdmolfiles import SDMolSupplier
import rdkit.Chem.rdmolfiles as rdmolfiles

from boltz.data.types import Target
from boltz.data.parse.schema import parse_boltz_schema


def _process_sdf(sdf_path: str) -> dict[str, str]:
    """Process an SDF file and extract SMILES strings.

    Parameters
    ----------
    sdf_path : str
        Path to the SDF file.

    Returns
    -------
    dict[str, str]
        Dictionary mapping molecule names to SMILES strings.
    """
    output_dict = {}
    suppl = SDMolSupplier(sdf_path, removeHs=False, sanitize=False)

    for mol in suppl:
        if mol is not None:
            mol_smiles = rdmolfiles.MolToSmiles(mol, allHsExplicit=True)
            if mol.HasProp("_Name"):
                mol_name = mol.GetProp("_Name")
                if mol_name == "":
                    mol_name = mol_smiles
            else:
                mol_name = mol_smiles

            output_dict[mol_name] = mol_smiles

    return output_dict


def parse_sdf(
    sdf_path: Path,
    ccd: dict[str, Mol],
    mol_dir: Path,
    boltz2: bool = False,
) -> dict:
    """Parse an SDF file.

    Parameters
    ----------
    sdf_path : Path
        Path to the SDF file.
    ccd : Dict
        Dictionary of CCD components.
    mol_dir : Path
        Path to the directory containing the molecules.
    boltz2 : bool, optional
        Whether to use Boltz2 format, by default False.

    Returns
    -------
    dict
        Dictionary containing sequences and bonds.
    """
    # Process SDF file
    mol_dict = _process_sdf(str(sdf_path))

    # Convert to yaml format
    sequences = []
    for mol_name, smiles in mol_dict.items():
        sequences.append({
            "ligand": {
                "id": mol_name,
                "smiles": smiles,
                "modifications": [],
            }
        })

    return {
        "sequences": sequences,
        "bonds": [],
        "version": 1,
    } 