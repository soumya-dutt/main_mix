#This file is to dry up pdb and psf files, source it to vmd TKconsole.
#resetpsf clears catche, so if you get an error in the first place, resetpsf will make the program forget that error.

resetpsf

mol load psf ionized.psf pdb ionized.pdb

set a [atomselect top "not protein"]
set l [lsort -unique [$a get segid]]

package require psfgen
readpsf ionized.psf
coordpdb  ionized.pdb

foreach s $l {
delatom $s
}

writepsf prot_dry.psf
writepdb prot_dry.pdb


