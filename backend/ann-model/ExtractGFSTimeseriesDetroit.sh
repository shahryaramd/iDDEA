#!/bin/bash

#@author:  Shahryar Ahmad, skahmad@uw.edu
#Graduate Student and Research Assistant
#SASWE Research Group, University of Washington

declare -a riv=( 'detroit' ) 
declare -a invar=("RAIN" "TMAX" "TMIN" "W2")
declare -a var=("precip" "ts_max" "ts_min" "w_ave")
lead=7
param=( "0.05" ) 
rm stmp*

bb=0
maskfile=ws_${riv[bb]}.nc

#~ for nn in $(seq 35 -1 9); do
nn=$1
	i=$(date +"%Y" -d "$nn days ago")			## Year
	j=$(date +"%m" -d "$nn days ago")			## Month
	k=$(date +"%d" -d "$nn days ago")			## Day

	j=$((10#$j))
	k=$((10#$k))
	day=$i$(printf %02d $j)$(printf %02d $k)
	echo $day 
	fgfs=/home/shahryar/DSS/ANN_Detroit/Predictors/GFSraw/detroit.${day}.GFS.nc

	p=0
	q=0
	for((l=1; l<=$lead; l+=1))do
		echo LEAD $l
		for((q=0; q<4; q+=1))do
			#~ if [ $q -eq 0 ]; then
				#~ cdo remapcon,$maskfile $fgfs0p25 stmp1.nc		#take RAIN from 0p25 till 20150115
			#~ else
				cdo remapcon,$maskfile $fgfs stmp1.nc   
			#~ fi
			ncks -h -A $maskfile stmp1.nc
			gdalwarp -of netcdf -tr ${param[0]} ${param[0]} -r bilinear netcdf:"stmp1.nc":${invar[q]} stmp_${var[q]}.nc
			gdal_translate -of netcdf netcdf:"stmp_${var[q]}.nc":Band$l stmpLall_${var[q]}.nc
			ncwa    -a lat,lon stmpLall_${var[q]}.nc stmp_${var[q]}L$l.nc
			ncrename -v Band$l,avg stmp_${var[q]}L$l.nc
			ncdump -v avg stmp_${var[q]}L$l.nc > stmp_${var[q]}L$l.txt
		done
		
		out1=$day
		out2=`echo $( tail -n 2 stmp_${var[0]}L$l.txt ) | egrep -o '[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?.'`
		out3=`echo $( tail -n 2 stmp_${var[1]}L$l.txt ) | egrep -o '[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?.'`
		out4=`echo $( tail -n 2 stmp_${var[2]}L$l.txt ) | egrep -o '[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?.'`
		out5=`echo $( tail -n 2 stmp_${var[3]}L$l.txt ) | egrep -o '[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?.'`

		
		echo $out1 $out2 $out3 $out4 $out5 >>./Predictors/GFSprocessed/Predictor_GFS_L${l}.txt   #get average from ncdump output string
		rm stmpL* stmp*
		
			
	done
#~ done

