#!/bin/bash 
#SBATCH --job-name=meld_MSA_2
#SBATCH -N 1                                                                    
#SBATCH -n 4                                                                    
#SBATCH -t 3-00:00:00           # time in d-hh:mm:s                             
#SBATCH -p general                # partition                                       
#SBATCH -q public            # QOS                                            
#SBATCH -G a100:4                                                            
#SBATCH -o slurm.%j.out         # file to save job's STDOUT (%j = JobId)        
#SBATCH -e slurm.%j.err         # file to save job's STDERR (%j = JobId)        
#SBATCH --export=NONE           # Purge the job-submitting shell environmet     
                                                                                 
module purge                                                                    
                                                                                 
module load mamba/latest                                                     
                                                                                
source activate MELD                                                            
                                                                                 
mpirun launch_remd 
