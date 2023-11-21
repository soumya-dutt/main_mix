#!/usr/bin/env python
# encoding: utf-8

import numpy as np
from meld.remd import ladder, adaptor, leader
from meld import comm, vault
from meld import system
from meld import parse
import meld.system.montecarlo as mc
from meld.system.restraints import LinearRamp,ConstantRamp
from collections import namedtuple
import glob as glob
import os

N_REPLICAS = 4
N_STEPS = 20000
BLOCK_SIZE = 500

def gen_state_templates(index, templates):                                      
    n_templates = len(templates)
    print((index,n_templates,index%n_templates))
    a = system.ProteinMoleculeFromPdbFile(templates[index%n_templates])
    b = system.SystemBuilder(forcefield="ff14sbside")
    c = b.build_system_from_molecules([a])
    pos = c._coordinates
    c._box_vectors=np.array([0.,0.,0.])
    vel = np.zeros_like(pos)
    alpha = index / (N_REPLICAS - 1.0)
    energy = 0
    return system.SystemState(pos, vel, alpha, energy,c._box_vectors)

def get_cartesian_restraints(s, scaler, residues, delta=None, k = 250.):
    cart = []
    backbone = ['CA']
    for i in residues:
        for b in backbone:
            atom_index = s.index_of_atom(i,b) - 1
            x,y,z = s.coordinates[atom_index]/10
            rest = s.restraints.create_restraint('cartesian',scaler,
            LinearRamp(0,15,0,1), res_index = i, atom_name = b, x=x, 
            y=y, z=z, delta=delta, force_const=k)
            cart.append(rest)
    return cart

def get_dist_restraints(filename, s, scaler): 
    dists = []
    rest_group = []
    lines = open(filename).read().splitlines()
    lines = [line.strip() for line in lines]
    for line in lines:
        if not line:
            dists.append(s.restraints.create_restraint_group(rest_group, 1)) 
            rest_group = []
        else:
            cols = line.split()
            i = int(cols[0])
            name_i = cols[1]
            j = int(cols[2])
            name_j = cols[3]
            dist = float(cols[4])                          

            rest = s.restraints.create_restraint('distance', scaler,LinearRamp(0,100,0,1),     
                                              r1=0, r2=0, r3=dist, r4=dist+0.1, k=350,
                                              atom_1_res_index=i, atom_2_res_index=j,
                                              atom_1_name=name_i, atom_2_name=name_j)
            rest_group.append(rest)
    return dists

def setup_system():
    templates = glob.glob('*Untitled1.pdb')
    
    # build the system
    p = system.ProteinMoleculeFromPdbFile(templates[0])
    b = system.SystemBuilder(forcefield="ff14sbside")
    s = b.build_system_from_molecules([p])
    s.temperature_scaler = system.GeometricTemperatureScaler(0, 1, 300, 340.0)
    n_res = s.residue_numbers[-1]

    
    const_scaler = s.restraints.create_scaler('constant')   
    nonconst_scaler = s.restraints.create_scaler('nonlinear', alpha_min=0.4, alpha_max=1.0, factor=4.0)  


    distance_restraints_1 = get_dist_restraints('bias1.dat',s,scaler=nonconst_scaler) 
    s.restraints.add_selectively_active_collection(distance_restraints_1, int(len(distance_restraints_1)*0.5))

    '''# distance_restraints_2 = get_dist_restraints('bias2.dat',s,scaler=nonconst_scaler) 
    # s.restraints.add_selectively_active_collection(distance_restraints_2, int(len(distance_restraints_2)*.90))

    # distance_restraints_3 = get_dist_restraints('bias3.dat',s,scaler=nonconst_scaler) 
    # s.restraints.add_selectively_active_collection(distance_restraints_3, int(len(distance_restraints_3)*1.0))

    # distance_restraints_4 = get_dist_restraints('bias4.dat',s,scaler=nonconst_scaler) 
    # s.restraints.add_selectively_active_collection(distance_restraints_4, int(len(distance_restraints_4)*.90))

    # distance_restraints_5 = get_dist_restraints('bias5.dat',s,scaler=nonconst_scaler) 
    # s.restraints.add_selectively_active_collection(distance_restraints_5, int(len(distance_restraints_5)*1.0))

    # distance_restraints_6 = get_dist_restraints('bias6.dat',s,scaler=nonconst_scaler) 
    # s.restraints.add_selectively_active_collection(distance_restraints_6, int(len(distance_restraints_6)*.90))

    # distance_restraints_7 = get_dist_restraints('bias7.dat',s,scaler=nonconst_scaler) 
    # s.restraints.add_selectively_active_collection(distance_restraints_7, int(len(distance_restraints_7)*1.0))

    # distance_restraints_8 = get_dist_restraints('bias8.dat',s,scaler=nonconst_scaler) 
    # s.restraints.add_selectively_active_collection(distance_restraints_8, int(len(distance_restraints_8)*1.0))

    # distance_restraints_9 = get_dist_restraints('bias9.dat',s,scaler=nonconst_scaler) 
    # s.restraints.add_selectively_active_collection(distance_restraints_9, int(len(distance_restraints_9)*1.0))

    # distance_restraints_10 = get_dist_restraints('bias10.dat',s,scaler=nonconst_scaler) 
    # s.restraints.add_selectively_active_collection(distance_restraints_10, int(len(distance_restraints_10)*.90))'''

   #create the options
    options = system.RunOptions()
    options.implicit_solvent_model = 'gbNeck2'
    options.use_big_timestep = False
    options.use_bigger_timestep = False
    options.cutoff = 1.8

    options.use_amap = False
    options.amap_alpha_bias = 1.0
    options.amap_beta_bias = 1.0
    options.timesteps = 11111
    options.minimize_steps = 500000
    options.min_mc = None
    options.run_mc = None

    # create a store
    store = vault.DataStore(s.n_atoms, N_REPLICAS, s.get_pdb_writer(), block_size=BLOCK_SIZE)
    store.initialize(mode='w')
    store.save_system(s)
    store.save_run_options(options)

    # create and store the remd_runner
    l = ladder.NearestNeighborLadder(n_trials=100)
    policy = adaptor.AdaptationPolicy(2.0, 50, 50)
    a = adaptor.EqualAcceptanceAdaptor(n_replicas=N_REPLICAS, adaptation_policy=policy)

    remd_runner = leader.LeaderReplicaExchangeRunner(N_REPLICAS, max_steps=N_STEPS, ladder=l, adaptor=a)
    store.save_remd_runner(remd_runner)

    # create and store the communicator
    c = comm.MPICommunicator(s.n_atoms, N_REPLICAS)
    store.save_communicator(c)

    # create and save the initial states
    #states = [gen_state(s, i) for i in range(N_REPLICAS)]
    states = [gen_state_templates(i,templates) for i in range(N_REPLICAS)]
    store.save_states(states, 0)

    # save data_store
    store.save_data_store()

    return s.n_atoms


setup_system()












