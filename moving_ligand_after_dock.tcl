# This code is for moving a lifgand to a desired place in the complex

resetpsf

set lig [atomselect top "resname Y70"]
set bindsite [atomselect top "resid 1431 to 1441"]

set lig_center [measure center $lig]
puts $lig_center

set bs_center [measure center $bindsite]
puts $bs_center

set mov [vecsub $bs_center $lig_center]

#scaling the movement 

set scaler 0.6

set actual_move {}

foreach component $mov {
    lappend actual_move [expr {$scaler * $component}]
}

$lig moveby $actual_move

set allatoms [atomselect top all]
$allatoms writepdb adjusted.pdb