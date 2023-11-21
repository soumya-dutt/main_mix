import mdtraj as md
import os
import numpy as np

os.chdir('/scratch/jmchap10/Projects/catch_bonds/structures/m5s1')

topology = md.load_topology('modified.pdb')
print('Chain 0 Nitrogen atoms: ')
print([atom.index for atom in topology.chain(0).atoms if atom.element.symbol is 'N'])
print('Chain 1 Nitrogen atoms: ')
print([atom.index for atom in topology.chain(1).atoms if atom.element.symbol is 'N'])

atom_pairs = [(0, 1553)]
trajectory = md.load('m5s1t4.dcd', top = 'modified.pdb')
print('Measuring Distances!')
measure = md.compute_distances(trajectory, atom_pairs)

np.savetxt('distances.dat', measure)
print('Distances Saved!')
