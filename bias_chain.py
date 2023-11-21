import mdtraj as md
import sys
import numpy as np
from itertools import chain

traj = md.load_pdb('prot.pdb')

chain_A_resids = traj.topology.chain(0).residues
complex = [residue.resSeq for residue in chain_A_resids]
print(complex)

pair = []
for i in range(len(complex)):
    for j in range(i+1, len(complex)):
        pair.append([complex[i], complex[j]])

print(pair)

dist = md.compute_contacts(traj, pair, scheme="CA")
print(len(dist[1]))
dis = np.reshape(dist[0], (len(dist[1]), 1))

dist_list = dis.tolist()

file = open('bias.dat', 'w')
accpt = []
for i in zip(pair, dist_list):
    j = [val for sublist in i for val in sublist]

    if 0 < j[2] <= 0.7:  # 7 A
        accpt.append([j[0], j[1], j[2]])
        file.write("{} CA {} CA {}\n".format(j[0], j[1], float(j[2])))

file.close()

def align_columns(input_filename, output_filename):
    # Read the entries from the input file
    with open(input_filename, 'r') as input_file:
        entries = input_file.readlines()

    # Split each entry into columns
    columns = [entry.strip().split() for entry in entries]

    # Find the number of columns
    num_columns = len(columns[0])

    # Find the maximum width for each column
    max_widths = [max(len(entry[i]) for entry in columns) for i in range(num_columns)]

    # Format the aligned entries
    aligned_entries = []
    for entry in columns:
        formatted_entry = ' '.join(entry[i].ljust(max_widths[i]) for i in range(num_columns))
        aligned_entries.append(formatted_entry)

    # Write the aligned entries to the output file
    with open(output_filename, 'w') as output_file:
        output_file.write('\n'.join(aligned_entries))

# Usage example
align_columns('bias.dat', 'bias1.dat')

