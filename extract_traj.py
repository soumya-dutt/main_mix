## This script is for extracting the trajectory snippets that are generated from the clustering.tcl file.

import glob
import re
import MDAnalysis as mda
from tqdm import tqdm


def extract_indices(dat_files, dcd_file):
    for dat_file in tqdm(dat_files, desc='Processing files', unit='file'):
        # Extract index from file name
        index = re.findall(r'cluster_(\d+).dat', dat_file)[0]

        # Load .dat file
        with open(dat_file, 'r') as f:
            indices_line = f.readline().strip()
            indices = [int(idx) for idx in indices_line.split()]

        # Load .dcd file using MDAnalysis
        u = mda.Universe(dcd_file)

        # Create an empty trajectory
        traj = mda.Writer(
            f"extracted_traj_{index}.dcd", n_atoms=u.atoms.n_atoms)

        # Iterate over frames and extract desired indices
        for ts in u.trajectory:
            if ts.frame in indices:
                traj.write(u)

        traj.close()


# Usage example
dat_files_path = 'cluster_*.dat'
dcd_file_path = 'trajectory0.dcd'
dat_files = glob.glob(dat_files_path)
extract_indices(dat_files, dcd_file_path)
