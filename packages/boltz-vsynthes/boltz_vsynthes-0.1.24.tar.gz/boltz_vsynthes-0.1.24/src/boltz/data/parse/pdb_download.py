import os
from pathlib import Path
from typing import Optional

import requests
from Bio import PDB
from Bio.PDB.PDBParser import PDBParser
from Bio.PDB.Polypeptide import PPBuilder
from rdkit import Chem
from rdkit.Chem.rdchem import Mol
from Bio.SeqUtils import seq1
from collections import defaultdict

from boltz.data.types import Target
from boltz.data.parse.schema import parse_boltz_schema


def download_pdb(pdb_id: str, cache_dir: Path) -> Path:
    """Download a PDB file by ID.

    Parameters
    ----------
    pdb_id : str
        The PDB ID to download.
    cache_dir : Path
        The directory to cache the downloaded file.

    Returns
    -------
    Path
        The path to the downloaded PDB file.
    """
    # Create cache directory if it doesn't exist
    cache_dir.mkdir(parents=True, exist_ok=True)
    
    # Check if file already exists in cache
    pdb_path = cache_dir / f"{pdb_id.lower()}.pdb"
    if pdb_path.exists():
        return pdb_path
    
    # Download from RCSB PDB
    url = f"https://files.rcsb.org/download/{pdb_id.lower()}.pdb"
    response = requests.get(url, stream=True)
    response.raise_for_status()
    
    # Save to cache
    with pdb_path.open("wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    
    return pdb_path


def parse_pdb_id(
    pdb_id: str,
    ccd: dict[str, Mol],
    mol_dir: Path,
    cache_dir: Path,
    boltz2: bool = False,
) -> dict:
    """Parse a PDB file by ID.

    Parameters
    ----------
    pdb_id : str
        The PDB ID to parse.
    ccd : Dict
        Dictionary of CCD components.
    mol_dir : Path
        Path to the directory containing the molecules.
    cache_dir : Path
        The directory to cache downloaded PDB files.
    boltz2 : bool, optional
        Whether to use Boltz2 format, by default False.

    Returns
    -------
    dict
        Dictionary containing sequences and bonds.
    """
    # Download PDB file
    pdb_path = download_pdb(pdb_id, cache_dir)

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
