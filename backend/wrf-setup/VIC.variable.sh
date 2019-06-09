#!/bin/bash

declare -a dm=(31 28 31 30 31 30 31 31 30 31 30 31)
declare -a dml=(31 29 31 30 31 30 31 31 30 31 30 31)

#D=20120311	#Any given day
D=$(date +"%Y%m%d" -d "today")		#For current day
lead=16		#Forecast lead in day
dom=2		#Number of domain

i=$(echo $D | cut -b 1-4)
j=$(echo $D | cut -b 5-6)
k=$(echo $D | cut -b 7-8)

day[0]=$i$j$k
echo $D
j=$((10#$j))
k=$((10#$k))

for((m=1; m<=lead; m+=1))do
	
	if [ $j -lt 12 ] && [ $((i%4)) -ne 0 ]; then
		if [ $k -lt ${dm[$j-1]} ]; then
			((k+=1))
		else
			k=1
			((j+=1))
		fi
		day[m]=$i$(printf %02d $j)$(printf %02d $k)
	elif [ $j -lt 12 ]; then
		if [ $k -lt ${dml[$j-1]} ]; then
			((k+=1))
		else
			k=1
			((j+=1))
		fi
		day[m]=$i$(printf %02d $j)$(printf %02d $k)
	else
		if [ $k -lt ${dm[$j-1]} ]; then
			((k+=1))
		else
			((i+=1))
			j=1
			k=1
		fi
		day[m]=$i$(printf %02d $j)$(printf %02d $k)
	fi
done

wspd=()
tmax=()
tmin=()
fn=()

for((m=1; m<=dom; m+=1))do
	for((n=0; n<=lead; n+=1))do
		yr=$(echo ${day[n]} | cut -b 1-4)
		mn=$(echo ${day[n]} | cut -b 5-6)
		dy=$(echo ${day[n]} | cut -b 7-8)
		hr="00"
		if [ -f D0$m.$yr$mn$dy.$hr.nc ]; then
			ncra -h -C -y avg -v W2 D0$m.$yr$mn$dy.$hr.nc all.di0$m-$n.nc
			ncra -h -C -y max -v TMP2 D0$m.$yr$mn$dy.$hr.nc tmax.di0$m-$n.nc
			ncra -h -C -y min -v TMP2 D0$m.$yr$mn$dy.$hr.nc tmin.di0$m-$n.nc
			ncrename -h -v TMP2,TMAX tmax.di0$m-$n.nc
			ncrename -h -v TMP2,TMIN tmin.di0$m-$n.nc
			ncatted -O -h -a description,TMAX,o,c,"MAX TEMP at 2M" tmax.di0$m-$n.nc
			ncatted -O -h -a description,TMIN,o,c,"MIN TEMP at 2M" tmin.di0$m-$n.nc
			ncks -h -A tmax.di0$m-$n.nc all.di0$m-$n.nc
			ncks -h -A tmin.di0$m-$n.nc all.di0$m-$n.nc
			ncks -h -F -d Time,1,1 D0$m.$yr$mn$dy.$hr.nc temp.nc
			ncks -h -v Times,XLAT,XLONG,RAIN temp.nc di0$m-$n.nc
			rm temp.nc tmax*nc tmin*nc
			
		fi
	done
done

for((m=1; m<=dom; m+=1))do

	for((n=0; n<lead; n+=1))do
		yr=$(echo ${day[n]} | cut -b 1-4)
		mn=$(echo ${day[n]} | cut -b 5-6)
		dy=$(echo ${day[n]} | cut -b 7-8)
		hr="00"

		if [ -f di0$m-$((n+1)).nc ]; then
			
			eval "ncdiff -h di0$m-$((n+1)).nc di0$m-$n.nc d0$m\_$yr-$mn-$dy.nc"
			ncks -h -A all.di0$m-$n.nc d0$m\_$yr-$mn-$dy.nc
			ncatted -O -h -a description,RAIN,o,c,"TOTAL PRECIPITATION" d0$m\_$yr-$mn-$dy.nc
			fn[$m]=${fn[$m]}' 'd0$m\_$yr-$mn-$dy.nc
		fi
	done
	
	eval "ncrcat -h ${fn[$m]} wrf2vic.$D.VAR.D0$m.nc"

	rm *di0$m*.nc d0$m*.nc
done

unset wspd tmax tmin fn
