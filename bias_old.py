import mdtraj as md
import sys
import numpy as np
from itertools import chain
import glob as glob


templates = glob.glob('*Untitled1.pdb')
traj=md.load_pdb(templates[0])
# if(536 == 0):
#     complex = []
#     a = range(29-1,227)
#     for i in a:
#         complex.append(i)
# else:   
complex = []
a = range(0,traj.n_residues)
# b = range(536-1,734)
# m = chain(a,b)
for i in a:
    complex.append(i)
pair=[]
for i in range(len(complex)):
    for j in range(i+1, len(complex)):
        pair.append([complex[i],complex[j]])

print(traj.n_residues)

dist = md.compute_contacts(traj, pair, scheme="CA")
print(len(dist[1]))
dis=np.reshape(dist[0],(len(dist[1]),1))

dist_list=dis.tolist()

file = open('bias1.dat','w')
accpt=[]
for i in zip(pair, dist_list):
    j  = [val for sublist in i for val in sublist]
    
    if 0 < j[2] <= 0.7: # 7 A
        accpt.append([j[0],j[1],j[2]])
        file.write( "{} CA {} CA {}\n".format(j[0]+1, j[1]+1,float(j[2])))
        file.write("\n")

        