#Developed by Shahryar Ahmad, skahmad@uw.edu
#Graduate Student and Research Assistant
#SASWE Research Group, University of Washington

#start date
si=$(date +"%Y" -d "1096 days ago")			
sj=$(date +"%m" -d "1096 days ago")			
sk=$(date +"%d" -d "1096 days ago")		
echo $si$sj$sk > Metadata.info
#end date
ei=$(date +"%Y" -d "1 days ago")			
ej=$(date +"%m" -d "1 days ago")			
ek=$(date +"%d" -d "1 days ago")		
echo $ei$ej$ek >> Metadata.info
