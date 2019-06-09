#!/bin/bash

#@author:  Shahryar Ahmad, skahmad@uw.edu
#Graduate Student and Research Assistant
#SASWE Research Group, University of Washington

declare -a riv=("detroit" )	# For flow forecast
declare -a invar=("RAIN" "TMAX" "TMIN" "W2")
declare -a var=("precip" "tmax" "tmin" "w_ave")
lead=7
#~ param=( "0.125" "73.375" "88.875" "22.5" "31.5")   #ganges
param=( "0.1" "-122.37" "-121.67" "44.40" "44.90")    #detroit
#param=( "0.04" "-113.9950" "-112.8350" "47.1983" "48.4383")   #hh
#param=( "0.04" "-97.4787" "-93.5787" "36.3204" "38.9204")   #pensacola
#rm ./ProcessedPredictors/Predictor_GFSpcorr*


#~ i=$(date +"%Y" -d "0 day ago")			## Year
#~ j=$(date +"%m" -d "0 day ago")			## Month
#~ k=$(date +"%d" -d "0 day ago")			## Day
now=$(date +"%Y%m%d")
#~ for r in $(seq 1  1 1);do
r=$1
dd=$(date -d "$now-$r days")
k=$(date -d "$dd" '+%d')
j=$(date -d "$dd" '+%m')
i=$(date -d "$dd" '+%Y')
#~ k=28
j=$((10#$j))
k=$((10#$k))
curday=$i$(printf %02d $j)$(printf %02d $k)
echo $curday

for((q=0; q<3; q+=1)) do
		fn=$curday.${var[q]}.txt   
		sshpass -p "Bangla_Power21Feb" scp saswe@ovid.u.washington.edu:public_html/damdss/data/usace_data/$fn  ./;
		gdal_translate -of netcdf  $fn tmpLall_${var[q]}.nc
		ncwa -d lon,${param[1]},${param[2]} -d lat,${param[3]},${param[4]} -a lat,lon tmpLall_${var[q]}.nc tmp_${var[q]}.nc
		ncrename -v Band1,avg tmp_${var[q]}.nc
		ncdump -v avg tmp_${var[q]}.nc > tmp_${var[q]}.txt
		mv $fn Predictors/NowcastRaw/
done
out1=$curday
out2=`echo $( tail -n 2 tmp_${var[0]}.txt ) | grep -Eo '[+-]?[0-9]+([.][0-9]+)?'`
out3=`echo $( tail -n 2 tmp_${var[1]}.txt ) | grep -Eo '[+-]?[0-9]+([.][0-9]+)?'`
out4=`echo $( tail -n 2 tmp_${var[2]}.txt ) | grep -Eo '[+-]?[0-9]+([.][0-9]+)?'`
echo -e $out1"\t"$out2"\t"$out3"\t"$out4 >> ./Predictors/Predictor_Nowcast_Detroit.txt  #get average from ncdump output string
rm tmp*
   
#~ done
