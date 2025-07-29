from pathlib import Path
import yaml
from typing import Dict, Any
import copy

def get_next_ligand_id(config: Dict[str, Any], index: int) -> str:
    base_id = None
    for item in config["sequences"]:
        if "ligand" in item:
            base_id = item["ligand"]["id"]
            break
    if base_id is None:
        raise ValueError("No ligand ID found in template")
    base_id = ''.join(c for c in base_id if not c.isdigit())
    return f"{base_id}{index}"

def dump_with_compact_contacts(config: Dict[str, Any], output_path: Path):
    contacts_str = None

    if "constraints" in config:
        for c in config["constraints"]:
            if "pocket" in c and "contacts" in c["pocket"]:
                contacts_list = c["pocket"]["contacts"]
                contacts_str = yaml.dump({"contacts": contacts_list}, default_flow_style=True).strip()
                del c["pocket"]["contacts"]  # temporarily remove it to prevent multiline dump

    # Dump rest of config
    yaml_str = yaml.dump(config, default_flow_style=False, sort_keys=False)

    # Re-inject contacts string if it existed
    if contacts_str:
        yaml_lines = yaml_str.splitlines()
        new_lines = []
        inserted = False

        for line in yaml_lines:
            new_lines.append(line)
            if not inserted and line.strip().startswith("pocket:"):
                indent = " " * (len(line) - len(line.lstrip()) + 2)
                new_lines.append(indent + contacts_str)
                inserted = True

        yaml_str = "\n".join(new_lines)

    output_path.write_text(yaml_str)

def generate_yamls_from_sdfs(
    template_yaml: Path,
    sdf_dir: Path,
    output_dir: Path,
    yaml_prefix: str = "config_",
    start_index: int = 1,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    with open(template_yaml) as f:
        template = yaml.safe_load(f)
    sdf_files = sorted(sdf_dir.glob("*.sdf"))

    for i, sdf_file in enumerate(sdf_files):
        config = copy.deepcopy(template)
        ligand_id = get_next_ligand_id(config, start_index + i)

        # Update ligand info
        for item in config["sequences"]:
            if "ligand" in item:
                item["ligand"]["id"] = ligand_id
                item["ligand"]["sdf"] = str(sdf_file)

        # Update affinity binder
        if "properties" in config:
            for prop in config["properties"]:
                if "affinity" in prop:
                    prop["affinity"]["binder"] = ligand_id

        # Update constraints binder
        if "constraints" in config:
            for constraint in config["constraints"]:
                if "pocket" in constraint and "binder" in constraint["pocket"]:
                    constraint["pocket"]["binder"] = ligand_id

        output_file = output_dir / f"{yaml_prefix}{start_index + i}.yaml"
        dump_with_compact_contacts(config, output_file)
        print(f"✅ Created {output_file} with ligand ID {ligand_id}")

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Generate YAML files from a template and SDF files")
    parser.add_argument("template_yaml", type=str, help="Path to template YAML file")
    parser.add_argument("sdf_dir", type=str, help="Path to directory containing SDF files")
    parser.add_argument("output_dir", type=str, help="Path to output directory")
    parser.add_argument("--yaml-prefix", type=str, default="config_", help="Prefix for output YAML filenames")
    parser.add_argument("--start-index", type=int, default=1, help="Starting index for output filenames")
    args = parser.parse_args()

    generate_yamls_from_sdfs(
        template_yaml=Path(args.template_yaml),
        sdf_dir=Path(args.sdf_dir),
        output_dir=Path(args.output_dir),
        yaml_prefix=args.yaml_prefix,
        start_index=args.start_index,
    )

if __name__ == "__main__":
    main()
