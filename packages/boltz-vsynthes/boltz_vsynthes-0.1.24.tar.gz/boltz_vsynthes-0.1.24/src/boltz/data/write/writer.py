import json
from dataclasses import asdict, replace
from pathlib import Path
from typing import Literal

import numpy as np
import torch
from pytorch_lightning import LightningModule, Trainer
from pytorch_lightning.callbacks import BasePredictionWriter
from torch import Tensor

from boltz.data.types import Coords, Interface, Record, Structure, StructureV2
from boltz.data.write.mmcif import to_mmcif
from boltz.data.write.pdb import to_pdb


class BoltzWriter(BasePredictionWriter):
    """Custom writer for predictions."""

    def __init__(
        self,
        data_dir: str,
        output_dir: str,
        output_format: Literal["pdb", "mmcif"] = "mmcif",
        boltz2: bool = False,
        write_embeddings: bool = False,
    ) -> None:
        super().__init__(write_interval="batch")
        if output_format not in ["pdb", "mmcif"]:
            raise ValueError(f"Invalid output format: {output_format}")

        self.data_dir = Path(data_dir)
        self.output_dir = Path(output_dir)
        self.output_format = output_format
        self.failed = 0
        self.boltz2 = boltz2
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.write_embeddings = write_embeddings

    def write_on_batch_end(
        self,
        trainer: Trainer,
        pl_module: LightningModule,
        prediction: dict[str, Tensor],
        batch_indices: list[int],
        batch: dict[str, Tensor],
        batch_idx: int,
        dataloader_idx: int,
    ) -> None:
        if prediction["exception"]:
            self.failed += 1
            return

        records: list[Record] = batch["record"]
        coords = prediction["coords"].unsqueeze(0)
        pad_masks = prediction["masks"]

        if "confidence_score" in prediction:
            argsort = torch.argsort(prediction["confidence_score"], descending=True)
            idx_to_rank = {idx.item(): rank for rank, idx in enumerate(argsort)}
        else:
            idx_to_rank = {i: i for i in range(len(records))}

        for record, coord, pad_mask in zip(records, coords, pad_masks):
            path = self.data_dir / f"{record.id}.npz"
            structure = StructureV2.load(path) if self.boltz2 else Structure.load(path)

            chain_map = {
                len([True for j in structure.mask[:i] if j]): i
                for i, m in enumerate(structure.mask) if m
            }
            structure = structure.remove_invalid_chains()

            for model_idx in range(coord.shape[0]):
                model_coord = coord[model_idx]
                coord_unpad = model_coord[pad_mask.bool()].cpu().numpy()

                atoms = structure.atoms
                atoms["coords"] = coord_unpad
                atoms["is_present"] = True

                if self.boltz2:
                    coord_unpad = np.array([(x,) for x in coord_unpad], dtype=Coords)

                residues = structure.residues
                residues["is_present"] = True

                interfaces = np.array([], dtype=Interface)
                if self.boltz2:
                    new_structure = replace(structure, atoms=atoms, residues=residues, interfaces=interfaces, coords=coord_unpad)
                else:
                    new_structure = replace(structure, atoms=atoms, residues=residues, interfaces=interfaces)

                chain_info = []
                for chain in new_structure.chains:
                    old_chain_idx = chain_map[chain["asym_id"]]
                    old_chain_info = record.chains[old_chain_idx]
                    new_chain_info = replace(old_chain_info, chain_id=int(chain["asym_id"]), valid=True)
                    chain_info.append(new_chain_info)

                struct_dir = self.output_dir / record.id
                struct_dir.mkdir(exist_ok=True)

                plddts = prediction.get("plddt", None)
                outname = f"{record.id}_model_{idx_to_rank[model_idx]}"

                if self.output_format == "pdb":
                    path = struct_dir / f"{outname}.pdb"
                    with path.open("w") as f:
                        f.write(to_pdb(new_structure, plddts=plddts[model_idx] if plddts is not None else None, boltz2=self.boltz2))
                elif self.output_format == "mmcif":
                    path = struct_dir / f"{outname}.cif"
                    with path.open("w") as f:
                        f.write(to_mmcif(new_structure, plddts=plddts[model_idx] if plddts is not None else None, boltz2=self.boltz2))
                else:
                    path = struct_dir / f"{outname}.npz"
                    np.savez_compressed(path, **asdict(new_structure))

                if self.boltz2 and record.affinity and idx_to_rank[model_idx] == 0:
                    path = struct_dir / f"pre_affinity_{record.id}.npz"
                    np.savez_compressed(path, **asdict(new_structure))

                if "plddt" in prediction:
                    path = struct_dir / f"confidence_{record.id}_model_{idx_to_rank[model_idx]}.json"
                    summary = {
                        k: prediction[k][model_idx].item()
                        for k in [
                            "confidence_score", "ptm", "iptm", "ligand_iptm",
                            "protein_iptm", "complex_plddt", "complex_iplddt",
                            "complex_pde", "complex_ipde"
                        ] if k in prediction
                    }
                    summary["chains_ptm"] = {
                        idx: prediction["pair_chains_iptm"][idx][idx][model_idx].item()
                        for idx in prediction.get("pair_chains_iptm", {})
                    }
                    summary["pair_chains_iptm"] = {
                        idx1: {
                            idx2: prediction["pair_chains_iptm"][idx1][idx2][model_idx].item()
                            for idx2 in prediction["pair_chains_iptm"][idx1]
                        }
                        for idx1 in prediction.get("pair_chains_iptm", {})
                    }
                    with path.open("w") as f:
                        json.dump(summary, f, indent=4)

                    plddt_path = struct_dir / f"plddt_{record.id}_model_{idx_to_rank[model_idx]}.npz"
                    np.savez_compressed(plddt_path, plddt=plddts[model_idx].cpu().numpy())

                if "pae" in prediction:
                    path = struct_dir / f"pae_{record.id}_model_{idx_to_rank[model_idx]}.npz"
                    np.savez_compressed(path, pae=prediction["pae"][model_idx].cpu().numpy())

                if "pde" in prediction:
                    path = struct_dir / f"pde_{record.id}_model_{idx_to_rank[model_idx]}.npz"
                    np.savez_compressed(path, pde=prediction["pde"][model_idx].cpu().numpy())

            if self.write_embeddings and "s" in prediction and "z" in prediction:
                s = prediction["s"].cpu().numpy()
                z = prediction["z"].cpu().numpy()
                emb_path = struct_dir / f"embeddings_{record.id}.npz"
                np.savez_compressed(emb_path, s=s, z=z)

    def on_predict_epoch_end(self, trainer: Trainer, pl_module: LightningModule) -> None:
        print(f"Number of failed examples: {self.failed}")


class BoltzAffinityWriter(BasePredictionWriter):
    """Writer for affinity predictions."""

    def __init__(self, data_dir: str, output_dir: str) -> None:
        super().__init__(write_interval="batch")
        self.failed = 0
        self.data_dir = Path(data_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def write_on_batch_end(
        self,
        trainer: Trainer,
        pl_module: LightningModule,
        prediction: dict[str, Tensor],
        batch_indices: list[int],
        batch: dict[str, Tensor],
        batch_idx: int,
        dataloader_idx: int,
    ) -> None:
        if prediction["exception"]:
            self.failed += 1
            return

        for i, record in enumerate(batch["record"]):
            summary = {
                "affinity_pred_value": prediction["affinity_pred_value"][i].item(),
                "affinity_probability_binary": prediction["affinity_probability_binary"][i].item(),
            }

            if "affinity_pred_value1" in prediction:
                summary["affinity_pred_value1"] = prediction["affinity_pred_value1"][i].item()
                summary["affinity_probability_binary1"] = prediction["affinity_probability_binary1"][i].item()
                summary["affinity_pred_value2"] = prediction["affinity_pred_value2"][i].item()
                summary["affinity_probability_binary2"] = prediction["affinity_probability_binary2"][i].item()

            struct_dir = self.output_dir / record.id
            struct_dir.mkdir(exist_ok=True)
            path = struct_dir / f"affinity_{record.id}.json"
            with path.open("w") as f:
                json.dump(summary, f, indent=4)

    def on_predict_epoch_end(self, trainer: Trainer, pl_module: LightningModule) -> None:
        print(f"Number of failed examples: {self.failed}")
