import subprocess, os

# receptor = "/mnt/d/PriceTracker/ERBB2/docking_inputs/protein/HER2_clean_receptor_vina_ready.pdbqt"
# ligand_dir = "/mnt/d/PriceTracker/ERBB2/data/prepared_ligands"
# out_dir = "/mnt/d/PriceTracker/ERBB2/docking_results"
# os.makedirs(out_dir, exist_ok=True)

# center = (10, 25, 30)
# size = (20, 20, 20)

# for ligand in os.listdir(ligand_dir):
#     if ligand.endswith(".pdbqt"):
#         ligand_path = os.path.join(ligand_dir, ligand)
#         out_path = os.path.join(out_dir, ligand.replace(".pdbqt", "_out.pdbqt"))
#         log_path = os.path.join(out_dir, ligand.replace(".pdbqt", "_log.txt"))
#         cmd = [
#             "vina",
#             "--receptor",
#             receptor,
#             "--ligand",
#             ligand_path,
#             "--center_x",
#             str(center[0]),
#             "--center_y",
#             str(center[1]),
#             "--center_z",
#             str(center[2]),
#             "--size_x",
#             str(size[0]),
#             "--size_y",
#             str(size[1]),
#             "--size_z",
#             str(size[2]),
#             "--out",
#             out_path,
#             "--cpu",
#             "4",
#             "--exhaustiveness",
#             "8",
#         ]

#         subprocess.run(cmd)


import re, csv, glob

# Folder containing your docking result files
log_files = glob.glob("/mnt/d/PriceTracker/ERBB2/docking_results/*.pdbqt")

output_csv = "/mnt/d/PriceTracker/ERBB2/docking_results/Table2_results.csv"
rows = []

for result in log_files:
    compound_id = os.path.basename(result).replace("_out.pdbqt", "")
    # Read the docking score from the terminal output or Vina result file
    score = None
    with open(result, "r") as f:
        for line in f:
            if "REMARK VINA RESULT:" in line:
                score = line.split(":")[1].strip().split()[0]
                break

    # Extract amino acid residues (if you have interaction data)
    residues = "Met115, Leu137, Ala149, Val156"  # placeholder — replace with your actual residues from visualization

    if score:
        rows.append([compound_id, score, residues])

# Write to CSV
with open(output_csv, "w", newline="") as out:
    writer = csv.writer(out)
    writer.writerow(["CompoundID", "Docking Score (kcal/mol)", "Amino Acid Residues"])
    writer.writerows(rows)

print(f"✅ Results saved to {output_csv}")
