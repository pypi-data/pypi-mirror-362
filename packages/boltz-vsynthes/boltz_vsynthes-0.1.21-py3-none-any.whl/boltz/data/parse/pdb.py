import os
from pathlib import Path
from typing import Optional

from Bio import PDB
from Bio.PDB.PDBParser import PDBParser
from Bio.PDB.Polypeptide import PPBuilder
from Bio.Data.IUPACData import protein_letters_3to1
from rdkit import Chem
from rdkit.Chem.rdchem import Mol
from Bio.SeqUtils import seq1
from collections import defaultdict


from boltz.data.types import Target
from boltz.data.parse.schema import parse_boltz_schema


def parse_pdb(
    pdb_path: Path,
    ccd: dict[str, Mol],
    mol_dir: Path,
    boltz2: bool = False,
) -> dict:
    """Parse a PDB file.

    Parameters
    ----------
    pdb_path : Path
        Path to the PDB file.
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
    # Read PDB file
    sequences = []
    sequence_by_chain = defaultdict(list)

    # Parse SEQRES records directly
    with open(pdb_path) as f:
        for line in f:
            if line.startswith("SEQRES"):
                parts = line.split()
                chain_id = parts[2]
                residues = parts[4:]
                for res in residues:
                    try:
                        aa = seq1(res)
                    except KeyError:
                        aa = 'X'
                    sequence_by_chain[chain_id].append(aa)

    # Convert to yaml-style list
    for chain_id, aa_list in sequence_by_chain.items():
        sequences.append({
            "protein": {
                "id": chain_id,
                "sequence": ''.join(aa_list),
                "modifications": [],
            }
        })

    return {
        "sequences": sequences,
        "bonds": [],
        "version": 1,
    }
