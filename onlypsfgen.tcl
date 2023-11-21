resetpsf
# Loading the molecule
mol new prot.pdb

# seperating all the protein chains.

set protein [atomselect top protein]
set chains [lsort -unique [$protein get pfrag]]        ;# change pfrag to fragment in case of ligands
foreach chain $chains {
set sel [atomselect top "pfrag $chain"]                ;# change pfrag to fragment in case of ligands
$sel writepdb prot_frag${chain}.pdb
}

# Making PSF from PDB using psfgen
package require psfgen 
#topology unk.rtf
#topology unk.prm
#topology top_all36_prot_mod.rtf
#topology unk.str
topology /home/sdutta46/Desktop/toppar/top_all36_carb.rtf    
topology /home/sdutta46/Desktop/toppar/top_all36_lipid.rtf   
topology /home/sdutta46/Desktop/toppar/top_all36_prot.rtf    
topology /home/sdutta46/Desktop/toppar/top_all36_cgenff.rtf
topology /home/sdutta46/Desktop/toppar/top_all36_na.rtf      
topology /home/sdutta46/Desktop/toppar/top_interface.rtf 
topology /home/sdutta46/Desktop/toppar/toppar_water_ions_namd.str


pdbalias residue HIS HSE
pdbalias residue HIE HSE
pdbalias residue HID HSD 
pdbalias residue HIP HSP
pdbalias atom ILE CD1 CD

foreach chain $chains {
segment $chain {pdb prot_frag${chain}.pdb}  
coordpdb prot_frag${chain}.pdb $chain      
guesscoord  
}
writepdb prot_new.pdb
writepsf prot_new.psf

mol delete all          ;# clearing the queue.

# Centering the protein.

# mol new prot_new.psf
# mol addfile prot_new.pdb

# set allatoms [atomselect top all]
# $allatoms moveby [vecinvert [measure center $allatoms]]
# puts [measure center $allatoms]
# $allatoms writepdb centered.pdb       ;# writing coordinates of a centered protein.
# $allatoms delete