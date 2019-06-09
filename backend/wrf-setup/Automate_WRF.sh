#!/bin/bash

#clear system
cd ../wrf/Build_WRF/DATA/
rm *

#Download GFS
echo "Downloading GFS Data..."
lead=$1   #read argument
i=$(date +"%Y" -d "0 day ago")	 ## "today")		## Year
j=$(date +"%m" -d "0 day ago")	 ## "today")			## Month
k=$(date +"%d" -d "0 day ago")	 ##"today")			## Day

j=$((10#$j)) # converting to decimal form octal in case of 08 or 09
k=$((10#$k))

echo $i-$(printf %02d $j)-$(printf %02d $k)_00:00:00
## GFS Forecast data processing
for l in $(seq -f "%03g" 0 12 $((24*$lead)))		## GFS Forecast hour
do
file=gfs.t00z.pgrb2.0p25.f$l  
wget ftp://ftp.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/gfs.$i$(printf %02d $j)$(printf %02d $k)\00/$file
done

#RUN WPS 
echo "Running WPS"
cd ../WPS/
rm FILE:*
rm met_em.d0*
./geogrid.exe >& log.geogrid
./link_grib.csh ~/wrf/Build_WRF/DATA/
ln -sf ungrib/Variable_Tables/Vtable.GFS Vtable
./ungrib.exe 
./metgrid.exe >& log.metgrid

#RUN WRF
echo "Running WRF"
cd ../WRFV3/run
rm met_em.d0*
rm wrfout_d0*
rm wrfrst_d0*
ln -sf ../../WPS/met_em* . 
mpirun -np 8 ./real.exe
tail rsl.error.0000
mpirun -np 8 ./wrf.exe
tail rsl.error.0000

# Post-process WRF output
echo "Post-processing WRF output"
rm D0*
rm temp*
./WRF.VAR.CONV.sh
./VIC.variable.sh

# Append forecast forcings to hindcast
python appendWRF_forcing_Automate.py $lead $i$(printf %02d $j)$(printf %02d $k)


