#!/bin/bash
#@author:  Shahryar Ahmad, skahmad@uw.edu
#Graduate Student and Research Assistant
#SASWE Research Group, University of Washington

declare -a dm=(31 28 31 30 31 30 31 31 30 31 30 31)
declare -a dml=(31 29 31 30 31 30 31 31 30 31 30 31)

declare -a invar=("RAIN" "TMAX" "TMIN" "W2" "RHMAX" "RHMIN" "TMP")
declare -a var=("precip" "ts_max" "ts_min" "w_ave" "RHmax" "RHmin" "t_ave")
declare -a riv=( "detroit" )
declare -a basin=( "detroit" )	# For flow forecast


lead=7			# Lead time in day (For ETo and precipitation)
LF=10			# GFS Forecast lead in day (data downlaod, for flow forecast)

nn=$1
#~ for nn in $(seq 3 -1 1); do

i=$(date +"%Y" -d "$nn days ago")			## Year
j=$(date +"%m" -d "$nn days ago")			## Month
k=$(date +"%d" -d "$nn days ago")			## Day

j=$((10#$j)) # converting to decimal form octal in case of 08 or 09
k=$((10#$k))
#i=2017				## Given Year
#j=10				## Given Month
#k=23				## Given Day

echo Date: $i$(printf %02d $j)$(printf %02d $k)
day=$i$(printf %02d $j)$(printf %02d $k)
## GFS Forecast data processing

for l in $(seq -f "%03g" 3 3 $((24*LF)))		## GFS Forecast hour
do
file=gfs.0p25.$day\00.f$l.grib2
wget --no-check-certificate -N --load-cookies Bin/auth.rda_ucar_edu http://rda.ucar.edu/data/ds084.1/$i/$day/$file
## SUBSET
#~ file=gfs.t00z.pgrb2.0p25.f$l
#~ wget https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl?file=${file}&var_APCP=on&var_TMAX=on&var_TMIN=on&var_UGRD=on&var_VGRD=on&subregion=&leftlon=-123&rightlon=-121&toplat=45&bottomlat=44&dir=%2Fgfs.$day\00


if [ -f $file ]; then
	wgrib2 $file -match "APCP:|(TMAX|TMIN|UGRD|VGRD|RH):(2|10) m" -not "APTMP|mb" -netcdf tmp.nc
	ncks -h -d longitude,237.00,239.00 -d latitude,44.0,45.0 tmp.nc $l.nc
	P=$P' '$l.nc
	if [ $((10#$l%2)) -eq 0 ]; then
		R=$R' '$l.nc
	fi
	rm tmp*
fi
done

eval "ncrcat -h $P W1.nc"
eval "ncap2 -h -s \"W2=sqrt(UGRD_10maboveground*UGRD_10maboveground+VGRD_10maboveground*VGRD_10maboveground)*0.74795\" W1.nc W2.nc"
ncks -h -v W2 W2.nc wind.nc
ncatted -O -h -a long_name,W2,o,c,"Wind Speed" wind.nc
ncatted -O -h -a short_name,W2,o,c,"W_2maboveground" wind.nc
ncatted -O -h -a level,W2,o,c,"2 m above ground" wind.nc
ncks -h -v RH_2maboveground W1.nc RH.nc

eval "ncrcat -h $R M1.nc"
eval "ncap2 -h -s \"TMAX=TMAX_2maboveground-273.13\" M1.nc M2.nc"
eval "ncap2 -h -s \"TMIN=TMIN_2maboveground-273.13\" M2.nc M3.nc"
eval "ncap2 -h -s \"TMP=(TMAX+TMIN)/2\" M3.nc M4.nc"
ncks -h -v APCP_surface,TMAX,TMIN,TMP M4.nc main.nc
ncatted -O -h -a units,TMAX,o,c,"C" main.nc
ncatted -O -h -a units,TMIN,o,c,"C" main.nc
ncatted -O -h -a units,TMP,o,c,"C" main.nc
ncrename -h -v APCP_surface,RAIN main.nc
rm $P W* M*.nc
unset P R

for n in $(seq 1 8 $(($LF*8)))
do
	ncra -F -h -v W2 -y avg -d time,$n,$(($n+7)) wind.nc WIND.$(($(($n+7))/8)).nc	
	ncra -F -h -v RH_2maboveground -y max -d time,$n,$(($n+7)) RH.nc RHMAX.$(($(($n+7))/8)).nc
	ncra -F -h -v RH_2maboveground -y min -d time,$n,$(($n+7)) RH.nc RHMIN.$(($(($n+7))/8)).nc
	ncrename -h -v RH_2maboveground,RHMAX RHMAX.$(($(($n+7))/8)).nc
	ncrename -h -v RH_2maboveground,RHMIN RHMIN.$(($(($n+7))/8)).nc
done

for n in $(seq 1 4 $(($LF*4)))
do
	ncra -F -h -v RAIN -y ttl -d time,$n,$(($n+3)) main.nc $(($(($n+3))/4)).nc
	ncra -F -h -v TMAX -y max -d time,$n,$(($n+3)) main.nc TMAX.$(($(($n+3))/4)).nc
	ncra -F -h -v TMIN -y min -d time,$n,$(($n+3)) main.nc TMIN.$(($(($n+3))/4)).nc
	ncra -F -h -v TMP -y avg -d time,$n,$(($n+3)) main.nc TMP.$(($(($n+3))/4)).nc
	ncks -h -A TMAX.$(($(($n+3))/4)).nc $(($(($n+3))/4)).nc
	ncks -h -A TMIN.$(($(($n+3))/4)).nc $(($(($n+3))/4)).nc
	ncks -h -A TMP.$(($(($n+3))/4)).nc $(($(($n+3))/4)).nc
	ncks -h -A WIND.$(($(($n+3))/4)).nc $(($(($n+3))/4)).nc
	ncks -h -A RHMAX.$(($(($n+3))/4)).nc $(($(($n+3))/4)).nc
	ncks -h -A RHMIN.$(($(($n+3))/4)).nc $(($(($n+3))/4)).nc
	Q=$Q' '$(($(($n+3))/4)).nc
done
eval "ncrcat -h $Q GFS.10.nc"
rm $Q TM* WIND*
unset Q
rm main.nc wind.nc RH*.nc gfs*

z=0 
cdo remapcon,Bin/ws_${basin[z]}.nc  GFS.10.nc Predictors/GFSraw/${basin[z]}.$day.GFS.nc

rm GFS.1*.nc
#~ done

