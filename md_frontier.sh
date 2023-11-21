#!/bin/bash
#SBATCH -A bie119 
#SBATCH -J meld_MSA
#SBATCH -N 1     
#SBATCH --ntasks-per-node=8
#SBATCH -t 3-00:00:00           # time in d-hh:mm:s                                                                         
#SBATCH --gpus = 8                                                            
#SBATCH -o jobout.%j.out         # file to save job's STDOUT (%j = JobId)        
#SBATCH -e joberr.%j.err         # file to save job's STDERR (%j = JobId)        
#SBATCH --export=NONE           # Purge the job-submitting shell environmet     
                                                                                 
                                                      
source activate meld_test                                                          
                                                                                 
mpirun launch_remd 
