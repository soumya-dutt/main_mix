# This code is for calculating residue wise sasa
resetpsf
# Alinging the frames
# puts -nonewline " Aligning frames \n"

# # Align all frames to the first frame
# set numFrames [molinfo top get numframes]
# set selFirstFrame [atomselect top "protein" frame 0]
# for {set i 1} {$i < $numFrames} {incr i} {
#     set selCurrentFrame [atomselect top "protein" frame $i]
#     set transformation [measure fit $selCurrentFrame $selFirstFrame]
#     $selCurrentFrame move $transformation
#     puts " $i frame aligned"
#     $selCurrentFrame delete
# }
# $selFirstFrame delete
# puts -nonewline "Frames are aligned\n"

mol new withforce_structure_frame487.pdb
# Taking in initial atomselection
puts -nonewline "\n \t \t Selection1: "             ;# Make selection1 
gets stdin selection1
set sele1 [atomselect top $selection1]

# Listing all the unique residues 
set list1 [lsort -unique [$sele1 get resid]] 
puts "list of resids in selection1 : $list1"   


foreach num1 $list1 {
    set res1 [atomselect top " $selection1 and resid $num1"]                
    set sele2 [lsort -unique [$res1 get resid]]
    set sele3 [lsort -unique [$res1 get resname]]
    set sele4 [lsort -unique [$res1 get chain]]
    puts "$sele2 $sele3 $sele4"
    set output [open "SASA_bindingsite_withforce_{$sele4}_{$sele3}_{$sele2}.dat" w]        ;# Also change the file name 
    set sasa [measure sasa 1.4 $sele1 -restrict $res1]
	puts $output "$sele4 $sele3 $sele2 $sasa"
    close $output 

}
quit


