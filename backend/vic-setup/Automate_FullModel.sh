#!/bin/bash
#Developed by Shahryar Ahmad, skahmad@uw.edu
#Graduate Student and Research Assistant
#SASWE Research Group, University of Washington

LEAD=16
#1. Clear system
cd DSS/VIC/
rm ForcingData/ASCII/*
rm ForcingData/CSV/*
rm ForcingData/NCDC_Data/*
rm Model/Forcing/*

#2. Prepare Forcing Data
./Basin_Grid_Generation.sh
python Metadata.py
 #./Land_Surface_Parameter_Preparation.sh
./Forcing_Data_from_NCDC_Stations.sh

#3. Modify simulation dates
cd ../
python DateModification.py $LEAD  

#4. Run WRF and post-process forecast output
./Automate_WRF.sh $LEAD 

#5. Run VIC and Route
cd	#go to home directory
cd DSS/VIC/Model/
rm ./VIC_Results/*
./VIC_Model/vicNl -g ./Parameters/global.param
python rename_2decimal.py   
rm ./Route_Results/*
./Route_Model/rout ./Parameters/Route.input
python routeprocess.py $LEAD  
rm *.day_mm
rm *.uh_s

#6. Process TIFFs for Raster Vis
#~ rm ForcingASCII/*
./wrf2ascii.sh

#7. Run Reservors Operation Optimization
cd ../../
python OptimNSGA.py $LEAD  

#8. Download current observed data from USACE
python Download_USACEdata.py




