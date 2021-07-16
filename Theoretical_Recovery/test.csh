#!/bin/csh

# Simple script to work out boxcar S/N recovery fractions
foreach gaussian_fwhm ( `seq 0.1 0.1 10`)
    
    set sigma = `echo $gaussian_fwhm | awk '{print $1/2.355}'`
    
    foreach trial_width ( 1 2 4 8 )
    
	# Gaussian calculation
	set A = `echo $sigma $trial_width | awk -v pi=3.14159 '{print (4.0*pi*($1/$2)^2)^(0.25)}'`
	set erf_arg = `echo $trial_width $sigma | awk '{print $1/(sqrt(8.0)*$2)}'`
	set erf_val = `python3.9 test.py $erf_arg`
	set epsilon = `echo $A $erf_val | awk '{print $1*$2}'`
	
	# Boxcar calculation is pretty simple
	set boxcar_epsilon = `echo $gaussian_fwhm $trial_width width | awk '{if ($1>$2) print sqrt($2/$1); else print sqrt($1/$2)}'`

	# Output result for this trial for this injected width
    	echo $gaussian_fwhm $trial_width $epsilon $boxcar_epsilon

    end

end
