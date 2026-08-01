import os
import glob
import subprocess

# 1. Define your path directories explicitly
# 1. Update these paths to use the Linux /mnt/d/ format
ROOT_DIR = "/mnt/d/PriceTracker/colab"
LIGAND_DIR = "/mnt/d/PriceTracker/colab/prepared_ligands"
RECEPTOR_PATH = "/mnt/d/PriceTracker/colab/3RCD.pdbqt"


# Path to your Vina executable (assumed to be in system PATH or root)
# If vina is not in your PATH, replace "vina" with the absolute path: r"C:\path\to\vina.exe"
VINA_EXE = "vina"

# Change the working directory to the root directory
os.chdir(ROOT_DIR)

# 2. Grab all matching ligand files inside the prepared_ligands folder
ligand_pattern = os.path.join(LIGAND_DIR, "ligand_*.pdbqt")
ligand_files = glob.glob(ligand_pattern)

print(f"[*] Target Receptor: {RECEPTOR_PATH}")
print(f"[*] Found {len(ligand_files)} ligands to dock in: {LIGAND_DIR}\n")

# 3. Process every ligand programmatically using a loop
for ligand_path in ligand_files:
    # Extract the file name (e.g., 'ligand_130275249.pdbqt')
    file_name = os.path.basename(ligand_path)

    # Extract the numerical ID (e.g., '130275249')
    ligand_id = file_name.replace("ligand_", "").replace(".pdbqt", "")

    # Define your dynamic output paths inside the 'prepared_ligands' folder
    output_pose = os.path.join(LIGAND_DIR, f"ligand_{ligand_id}_out.pdbqt")
    output_log = os.path.join(LIGAND_DIR, f"ligand_{ligand_id}_log.txt")

    print(f"==================================================")
    print(f" 🧪 PROCESSING LIGAND ID: {ligand_id}")
    print(f"==================================================")
    print(f"[*] Running AutoDock Vina simulation...")

    # 4. Build the exact command line flags as a list for safety
    cmd = [
        VINA_EXE,
        "--receptor",
        RECEPTOR_PATH,
        "--ligand",
        ligand_path,
        "--center_x",
        "10",
        "--center_y",
        "25",
        "--center_z",
        "30",
        "--size_x",
        "20",
        "--size_y",
        "20",
        "--size_z",
        "20",
        "--out",
        output_pose,
        "--exhaustiveness",
        "8",
        "--num_modes",
        "9",
    ]
    try:
        # 5. Execute Vina and write the terminal print logs directly into the text file
        with open(output_log, "w", encoding="utf-8") as log_file:
            subprocess.run(cmd, stdout=log_file, stderr=subprocess.PIPE, check=True)

        print(f"[✓] Docking complete! Log saved to: {os.path.basename(output_log)}")

    except subprocess.CalledProcessError as e:
        print(
            f"[-] ERROR: Vina execution failed for Ligand {ligand_id}. Check if Vina path is correct."
        )
    except FileNotFoundError:
        print(
            f"[-] ERROR: 'vina' command could not be found. Please ensure AutoDock Vina is installed and in your environment variables."
        )
        break

print("[✓] Batch processing run finished completely!")
