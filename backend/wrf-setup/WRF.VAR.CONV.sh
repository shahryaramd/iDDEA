#!/bin/bash


Dom=2	#Number of domain

Y=$(date +"%Y" -d "today")	#For current Year
#Y=2012
for((n=1; n<$((Dom+1)); n+=1))do
for((i=$Y; i<$((Y+2)); i+=1))do		#Will also look for the next year in case of forecast (e.g., 5 day forecast in Dec. 29)
for j in $(seq -f "%02g" 1 12)
do
for k in $(seq -f "%02g" 1 31)
do
for h in $(seq -f "%02g" 0 3 21)	#In case of 3 hourly output (one output file for each 3 hour)
do
	if [ -f wrfout_d0$n\_$i-$j-$k\_$h:00:00 ]; then
		echo wrfout_d0$n\_$i-$j-$k\_$h:00:00
		ncks -h -v Times,XLAT,XLONG,T2,U10,V10,RAINC,RAINNC wrfout_d0$n\_$i-$j-$k\_$h:00:00 temp1.nc
		eval "ncap2 -h -s \"RAIN=RAINC+RAINNC\" temp1.nc temp2.nc"			#Calculate total precipitation
		eval "ncap2 -h -s \"W2=sqrt(U10*U10+V10*V10)*0.74795\" temp2.nc temp3.nc"	#Calculate resultant vector of wind at 10m and converted for 2m
		eval "ncap2 -h -s \"TMP2=T2-273.15\" temp3.nc temp4.nc"				#Converting the 2m temperature from K to C
		ncks -h -v Times,XLAT,XLONG,TMP2,W2,RAIN temp4.nc D0$n.$i$j$k.$h.nc
		ncatted -O -h -a description,RAIN,o,c,"ACCUMULATED TOTAL PRECIPITATION" D0$n.$i$j$k.$h.nc
		ncatted -O -h -a description,W2,o,c,"WIND SPEED at 2 M" D0$n.$i$j$k.$h.nc
		rm temp*
	fi
done
done
done
done
done



