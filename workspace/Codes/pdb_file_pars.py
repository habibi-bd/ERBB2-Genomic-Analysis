import os

# Define the absolute directory paths
input_dir = r"data/prepared_ligands_pdbqt"
output_dir = r"data/prepaerd_ligands_pdb"

# Create the output folder if it doesn't exist yet
os.makedirs(output_dir, exist_ok=True)

# Counter for tracking processed files
converted_count = 0

# Scan the input folder for PDBQT files
for filename in os.listdir(input_dir):
    if filename.endswith(".pdbqt"):
        # Build full file paths
        input_path = os.path.join(input_dir, filename)

        # Rename output extension from .pdbqt to .pdb
        pdb_filename = filename.replace(".pdbqt", ".pdb")
        output_path = os.path.join(output_dir, pdb_filename)

        print(f"[*] Converting: {filename} -> {pdb_filename}")

        # Process and slice the file contents
        with open(input_path, "r") as infile, open(output_path, "w") as outfile:
            for line in infile:
                # Keep standard atom coordinate lines but strip PDBQT columns
                if line.startswith(("ATOM", "HETATM")):
                    outfile.write(line[:66] + "\n")
                # Ignore AutoDock metadata tags
                elif line.startswith(
                    (
                        "REMARK",
                        "ROOT",
                        "ENDROOT",
                        "BRANCH",
                        "ENDBRANCH",
                        "TORSDOF",
                    )
                ):
                    continue
                # Keep terminal records like TER and END
                else:
                    outfile.write(line)

        converted_count += 1

print(
    f"\n[✓] Finished! Successfully converted {converted_count} files into: {output_dir}"
)
