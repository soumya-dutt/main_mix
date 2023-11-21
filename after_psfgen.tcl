resetpsf

# centereing and preperation for md

mol new temp.psf
mol addfile temp.pdb

set allatoms [atomselect top all]
$allatoms moveby [vecinvert [measure center $allatoms]]
puts [measure center $allatoms]
$allatoms writepdb centered.pdb       ;# writing coordinates of a centered protein.
$allatoms delete

mol delete all

# Solvating the protein

#mol new prot_new.psf
#mol addfile centered.pdb

package require solvate
solvate temp.psf centered.pdb -t 20 -o solvated

#mol delete all

# Adding ions 

#mol new solvated.psf
#mol addfile solvated.pdb

package require autoionize
autoionize -psf solvated.psf -pdb solvated.pdb -neutralize -o ionized   ;# This neutralises the system with Na and Cl 

#mol delete all

# Calculation of the cellBravisvectors
mol new ionized.psf
mol addfile ionized.pdb

set allatoms [atomselect top all]
set min_max [measure minmax $allatoms]
set vec [vecsub [lindex $min_max 1] [lindex $min_max 0]]
set origin [measure center $allatoms]
puts $vec
puts $origin
$allatoms delete

# Writing the configuration file for minimization.

puts -nonewline "For running md Enter the temperature : "
flush stdout
set temperature [gets stdin]

puts -nonewline "Enter outputName1 : "
flush stdout
set outputName1 [gets stdin]

set fo [open "config1.conf" a+]
puts $fo "############################################################
##ADJUSTABLE PARAMETERS                         
#############################################################

structure          ionized.psf
coordinates        ionized.pdb
firsttimestep      0

#############################################################
## SIMULATION PARAMETERS                                   ##
#############################################################

# Input
paraTypeCharmm	    on
parameters          unk.str
parameters          unk.prm
parameters          /scratch/sdutta46/toppar/par_all36m_prot.prm 
parameters          /scratch/sdutta46/toppar/par_all36_carb.prm 
parameters          /scratch/sdutta46/toppar/par_all36_lipid.prm 
parameters          /scratch/sdutta46/toppar/par_all36_cgenff.prm 
parameters          /scratch/sdutta46/toppar/par_all36_na.prm 
parameters          /scratch/sdutta46/toppar/par_interface.prm 
parameters          /scratch/sdutta46/toppar/toppar_water_ions_namd.str 
temperature         $temperature


# Force-Field Parameters
exclude             scaled1-4
1-4scaling          1.0
cutoff              12.0
switching           on
switchdist          10.0
pairlistdist        14.0


# Integrator Parameters
timestep            2.0  ;# 2fs/step
rigidBonds          all  ;# needed for 2fs steps
nonbondedFreq       1
fullElectFrequency  2  
stepspercycle       10


# Constant Temperature Control
langevin            on    ;# do langevin dynamics
langevinDamping     1     ;# damping coefficient (gamma) of 1/ps
langevinTemp        $temperature
langevinHydrogen    off    ;# don't couple langevin bath to hydrogens


# Periodic Boundary Conditions
cellBasisVector1     [lindex $vec 0]   0.0     0.0
cellBasisVector2      0.0   [lindex $vec 1]    0.0
cellBasisVector3      0.0    0.0    [lindex $vec 2]
cellOrigin           $origin

wrapAll             on


# PME (for full-system periodic electrostatics)
PME                 yes
PMEGridSpacing      1.0

#manual grid definition
#PMEGridSizeX        45
#PMEGridSizeY        45
#PMEGridSizeZ        48


# Constant Pressure Control (variable volume)
useGroupPressure      yes ;# needed for rigidBonds
useFlexibleCell       no
useConstantArea       no

langevinPiston        on
langevinPistonTarget  1.01325 ;#  in bar -> 1 atm
langevinPistonPeriod  100.0
langevinPistonDecay   50.0
langevinPistonTemp    $temperature

# Output
outputName          $outputName1

restartfreq         10000     ;# 500steps = every 1ps
dcdfreq             10000
xstFreq             10000
outputEnergies      10000
outputPressure      10000

# Fixing atom constraint ( set pdb beta column to 1 )                           
#fixedAtoms         on                                                           
#fixedAtomsFile     modified.pdb                                                 
#fixedAtomsCol      B        

# Colvars
#colvars            on
#cv configfile      colconf.in
#############################################################
## EXTRA PARAMETERS                                        ##
#############################################################


#############################################################
## EXECUTION SCRIPT                                        ##
#############################################################

# Minimization

CUDASOAintegrate    off
minimize            20000
reinitvels          $temperature


#run 15000000 ; #100ns 
"
close $fo

# writing the config file for production run.
puts -nonewline "Enter outputName2 for production run : "
flush stdout
set outputName2 [gets stdin]

set f1 [open "config2.conf" a+]
puts $f1 "############################################################
##ADJUSTABLE PARAMETERS                         
#############################################################

structure          ionized.psf
coordinates        ionized.pdb
firsttimestep      20000
binCoordinates     $outputName1.restart.coor
binVelocities      $outputName1.restart.vel
extendedSystem     $outputName1.restart.xsc

#############################################################
## SIMULATION PARAMETERS                                   ##
#############################################################

# Input
paraTypeCharmm	    on
parameters          unk.str
parameters          unk.prm
parameters          /scratch/sdutta46/toppar/par_all36m_prot.prm 
parameters          /scratch/sdutta46/toppar/par_all36_carb.prm 
parameters          /scratch/sdutta46/toppar/par_all36_lipid.prm 
parameters          /scratch/sdutta46/toppar/par_all36_cgenff.prm 
parameters          /scratch/sdutta46/toppar/par_all36_na.prm 
parameters          /scratch/sdutta46/toppar/par_interface.prm 
parameters          /scratch/sdutta46/toppar/toppar_water_ions_namd.str 
#temperature         $temperature


# Force-Field Parameters
exclude             scaled1-4
1-4scaling          1.0
cutoff              12.0
switching           on
switchdist          10.0
pairlistdist        14.0


# Integrator Parameters
timestep            2.0  ;# 2fs/step
rigidBonds          all  ;# needed for 2fs steps
nonbondedFreq       1
fullElectFrequency  2  
stepspercycle       10


# Constant Temperature Control
langevin            on    ;# do langevin dynamics
langevinDamping     1     ;# damping coefficient (gamma) of 1/ps
langevinTemp        $temperature
langevinHydrogen    off    ;# don't couple langevin bath to hydrogens


# Periodic Boundary Conditions
cellBasisVector1     [lindex $vec 0]   0.0     0.0
cellBasisVector2      0.0   [lindex $vec 1]    0.0
cellBasisVector3      0.0    0.0    [lindex $vec 2]
cellOrigin           $origin

wrapAll             on


# PME (for full-system periodic electrostatics)
PME                 yes
PMEGridSpacing      1.0

#manual grid definition
#PMEGridSizeX        45
#PMEGridSizeY        45
#PMEGridSizeZ        48


# Constant Pressure Control (variable volume)
useGroupPressure      yes ;# needed for rigidBonds
useFlexibleCell       no
useConstantArea       no

langevinPiston        on
langevinPistonTarget  1.01325 ;#  in bar -> 1 atm
langevinPistonPeriod  100.0
langevinPistonDecay   50.0
langevinPistonTemp    $temperature

# Output
outputName          $outputName2

restartfreq         10000     ;# 500steps = every 1ps
dcdfreq             10000
xstFreq             10000
outputEnergies      10000
outputPressure      10000

# Fixing atom constraint ( set pdb beta column to 1 )                           
#fixedAtoms         on                                                           
#fixedAtomsFile     modified.pdb                                                 
#fixedAtomsCol      B        

# Colvars
#colvars            on
#cv configfile      colconf.in
#############################################################
## EXTRA PARAMETERS                                        ##
#############################################################


#############################################################
## EXECUTION SCRIPT                                        ##
#############################################################

# Minimization
#minimize            10000
#reinitvels          $temperature

CUDASOAintegrate     on
run 500000000 ; #100ns 
"
close $f1

# Writing the sbatch script

set f2 [open "md.sh" a+]
puts $f2 "#!/bin/bash

#SBATCH --job-name=$outputName2            # Job name 
#SBATCH -N 1                    # number of nodes
#SBATCH -n 1                    # number of tasks (default: allocates 1 core per task)
#SBATCH -t 7-00:00:00           # time in d-hh:mm:s
#SBATCH -p general              # partition 
#SBATCH -q public               # QOS
#SBATCH --mem=20G
#SBATCH -G a100:1
#SBATCH -o slurm.%j.out         # file to save job's STDOUT (%j = JobId)
#SBATCH -e slurm.%j.err         # file to save job's STDERR (%j = JobId)
#SBATCH --export=NONE           # Purge the job-submitting shell environment

# Always purge modules to ensure consistent environments
module purge    
# Load required modules for job's environment
module load namd/3.0b2

#command

namd3 config1.conf > $outputName1.log

namd3 config2.conf > $outputName2.log
"
close $f2

# writing 
puts " ................There you have it, go run md...............
####################### WRITTEN BY SOUMYA DUTTA #######################
"