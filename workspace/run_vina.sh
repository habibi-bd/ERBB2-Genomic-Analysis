#!/bin/bash
RECEPTOR="/mnt/d/PriceTracker/ERBB2/docking_inputs/protein/HER2_clean_receptor_vina_ready.pdbqt"
LIGAND_DIR="/mnt/d/PriceTracker/ERBB2/data/prepared_ligands"
OUT_DIR="/mnt/d/PriceTracker/ERBB2/docking_results"

mkdir -p "$OUT_DIR"

CENTER_X=10
CENTER_Y=25
CENTER_Z=30
SIZE_X=20
SIZE_Y=20
SIZE_Z=20

for ligand in "$LIGAND_DIR"/*.pdbqt; do
    name=$(basename "$ligand" .pdbqt)
    echo "Docking $name..."
    vina --receptor "$RECEPTOR" \
         --ligand "$ligand" \
         --center_x $CENTER_X --center_y $CENTER_Y --center_z $CENTER_Z \
         --size_x $SIZE_X --size_y $SIZE_Y --size_z $SIZE_Z \
         --out "$OUT_DIR/${name}_out.pdbqt" \
         --log "$OUT_DIR/${name}_log.txt"
done
