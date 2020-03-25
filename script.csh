#!/bin/csh

rm output*ascii pulses*pls
set destroy = ~/GIT/destroy_gutted/destroy

foreach option ( 1 2 3 )

    foreach height ( 40 ) 

	python test.py -option $option -height $height -width 1
	$destroy -ascii -n 8192 -box 2 -nsmax 8 "out"$option".ascii"
	mv pulses.pls "pulses"$option".pls"

    end

end
