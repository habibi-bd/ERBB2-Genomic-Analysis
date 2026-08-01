import os
import glob

# Define your paths
ROOT_DIR = "/mnt/d/PriceTracker/colab"
LIGAND_DIR = os.path.join(ROOT_DIR, "prepared_ligands")

# Find all generated log files
log_files = glob.glob(os.path.join(LIGAND_DIR, "ligand_*_log.txt"))

results = []

for log_path in log_files:
    file_name = os.path.basename(log_path)
    # Extract the molecule ID from the file name
    ligand_id = file_name.replace("ligand_", "").replace("_log.txt", "")

    best_score = None

    # Read the log file line by line to extract the top Vina score
    with open(log_path, "r", encoding="utf-8") as f:
        for line in f:
            # Look for the row containing the first mode (Mode 1)
            # Typically looks like: "   1        -6.2      0.000      0.000"
            parts = line.split()
            if len(parts) >= 2 and parts[0] == "1":
                try:
                    best_score = float(parts[1])
                    break
                except ValueError:
                    continue

    # Only append if a valid score was found
    if best_score is not None:
        results.append((ligand_id, best_score))

# Sort the results so the most negative score (strongest binder) comes first
results.sort(key=lambda x: x[1])

print("\n" + "=" * 50)
print(" 🏆 FINAL RANKING OF MOLECULES (BEST TO WORST)")
print("=" * 50)

for rank, (ligand_id, score) in enumerate(results, start=1):
    marker = "⭐ " if rank <= 3 else "   "
    print(
        f"{marker}Rank {rank:02d} | Molecule ID: {ligand_id:<12} | Score: {score:+.2f} kcal/mol"
    )

print("=" * 50)
if len(results) >= 3:
    print(
        f"\n[✓] Your top 3 target IDs for GROMACS are: {results[0][0]}, {results[1][0]}, and {results[2][0]}"
    )
else:
    print(
        "\n[-] Not enough complete log files found yet. Make sure your docking script finished."
    )
