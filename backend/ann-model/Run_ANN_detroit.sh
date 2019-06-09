#!/bin/bash

#@author:  Shahryar Ahmad, skahmad@uw.edu
#Graduate Student and Research Assistant
#SASWE Research Group, University of Washington

nn=1    
cd /home/shahryar/DSS/ANN_Detroit/

#~ for nn in $(seq 6 -1 1); do
i=$(date +"%Y" -d "$nn days ago")			## Year
j=$(date +"%m" -d "$nn days ago")			## Month
k=$(date +"%d" -d "$nn days ago")			## Day
j=$((10#$j)) # converting to decimal form octal in case of 08 or 09
k=$((10#$k))

echo Date: $i$(printf %02d $j)$(printf %02d $k)

python Bin/PullObservedFlowDetroit.py $nn		#Det.Observed
./Bin/ProcessGFSDetroit.sh $nn 					#GFSraw
./Bin/ExtractGFSTimeseriesDetroit.sh $nn		#Predictor_GFS_L.txt
./Bin/ProcessNowcastDetroit.sh	$nn			#Predictor_Nowcast_Detroit.txt

python Bin/detroit_ANN.py 

python Bin/OptimNSGA_ANN.py   

python Bin/AssessBenefits_ANN.py

#~ done
