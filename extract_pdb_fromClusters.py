import os
from tqdm import tqdm
import MDAnalysis as mda


input_directory = os.getcwd()  # Use current directory as the input directory
output_file = "extractedFrameNumbers.dat"

# Get a list of .dat files in the input directory
dat_files = [file for file in os.listdir(input_directory) if file.startswith("group_") and file.endswith(".dat")]

# Sort the files based on their numerical suffix
dat_files.sort(key=lambda x: int(x.split("_")[1].split(".")[0]))

# Extract the first number from each .dat file and store them in a list
first_numbers = []
for file in tqdm(dat_files, desc="Extracting numbers"):
    with open(os.path.join(input_directory, file), "r") as f:
        line = f.readline().strip()
        first_number = line.split()[0]
        first_numbers.append(first_number)

# Write the extracted numbers to the output file
with open(output_file, "w") as f:
    for number in tqdm(first_numbers, desc="Writing to file"):
        f.write(number + "\n")

print("Extraction complete. First numbers written to", output_file)

# Load the DCD trajectory file
dcd_file = 'trajectory0.dcd'
topology_file = '1stframe.pdb'
u = mda.Universe(topology_file, dcd_file)

# Load the .dat file and extract frame numbers
dat_file = 'extractedFrameNumbers.dat'
with open(dat_file, 'r') as f:
    frame_numbers = [int(line.strip()) for line in f]

# Extract frames based on the frame numbers and save as separate PDB files
for i, frame_number in enumerate(tqdm(frame_numbers)):
    u.trajectory[frame_number]  # -1 since frame numbers are 1-indexed
    pdb_filename = f'repstr_clu_{i}.pdb'  # Generate a unique filename for each frame
    with mda.Writer(pdb_filename) as pdb_writer:
        pdb_writer.write(u.atoms)


