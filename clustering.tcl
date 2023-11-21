# To run this code in vmd without the gui run the following command in the terminal - 
# vmd -dispdev text -e clustering.tcl

puts -nonewline " Clustering in VMD\n"

# Align all frames to the first frame
set numFrames [molinfo top get numframes]
set selFirstFrame [atomselect top "protein" frame 0]
for {set i 1} {$i < $numFrames} {incr i} {
    set selCurrentFrame [atomselect top "protein" frame $i]
    set transformation [measure fit $selCurrentFrame $selFirstFrame]
    $selCurrentFrame move $transformation
    puts " $i frame aligned"
    $selCurrentFrame delete
}
$selFirstFrame delete
puts -nonewline "Frames are aligned\n"

puts -nonewline "Enter the atomselection for which you want to cluster :"
flush stdout
set sele0 [gets stdin]
set sele1 [atomselect top $sele0]

puts -nonewline "Number of clusters :"
flush stdout
set number [gets stdin]

puts -nonewline "Enter RMSD cutoff :"
flush stdout
set cutoff_value [gets stdin]


set clusterLists [measure cluster $sele1 num $number distfunc rmsd cutoff $cutoff_value]

for {set i 0} {$i < [llength $clusterLists]} {incr i} {
    set clusterList [lindex $clusterLists $i]
    set fileName "cluster_$i.dat"
    
    set fileHandle [open $fileName "w"]
    puts $fileHandle [join $clusterList " "]
    close $fileHandle
    
    puts "Saved cluster $i to file $fileName"
}

