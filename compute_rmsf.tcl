puts -nonewline " RMSF in VMD\n"

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

puts -nonewline "Enter the atom selection for which you want to calculate RMSF: "
flush stdout
set sele0 [gets stdin]
set sele1 [atomselect top $sele0]

# Measuring RMSF with automatic last frame determination
set lastFrame [expr {$numFrames - 1}]
set output [measure rmsf $sele1 first 0 last $lastFrame step 1]

puts -nonewline "Enter the name of the output file : "
flush stdout
set sele2 [gets stdin]

#Write the RMSF values to a .dat file
set outFile [open "$sele2.dat" "w"]
foreach rmsfValue $output {
    puts $outFile $rmsfValue
}
close $outFile
