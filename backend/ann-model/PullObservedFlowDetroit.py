#@author:  Shahryar Ahmad, skahmad@uw.edu
#Graduate Student and Research Assistant
#SASWE Research Group, University of Washington

import re,sys,os
import urllib2
import datetime
import pandas as pd
from datetime import datetime,timedelta

#~ for dd in range(183,-1,-1):
dd=int(sys.argv[1])-1  #0
homedir='/home/shahryar/DSS/ANN_Detroit/'
curdate = datetime.today() - timedelta(days=dd)
curstr = datetime.strftime(curdate,'%Y%m%d') 
nday=1
reqdate = curdate #+ timedelta(days=nday)
reqdate = datetime.strftime(reqdate,'%Y%m%d') 
wrdate = curdate - timedelta(days=nday)

stDate = datetime.strptime(reqdate,'%Y%m%d')
ediff = timedelta(days=nday)
enDate = stDate+ediff
sDay = stDate.day
sMonth = stDate.month
sYear = stDate.year
eDay = enDate.day
eMonth = enDate.month
eYear = enDate.year
sDate = str(sMonth)+'%2F'+str(sDay)+'%2F'+str(sYear)+'%2F'
eDate = str(eMonth)+'%2F'+str(eDay)+'%2F'+str(eYear)+'%2F'
sdt = str(stDate.month)+"%2F"+str(stDate.day)+"%2F"+str(stDate.year)
dd=datetime.strftime(stDate, '%d-%b-%Y %H:%M') # format route output date to USACE date

#Obtain observed inflow and outflow
url_flow = 'http://www.nwd-wc.usace.army.mil/dd/common/web_service/webexec/ecsv?id=DET.Flow-In.Ave.~1Day.1Day.Best%3Aunits%3Dcfs%7CDET.Flow-Out.Ave.~1Day.1Day.Best%3Aunits%3Dcfs&headers=true&filename=&timezone=MDT&startdate='+sDate+'&enddate='+eDate
df=pd.read_csv(url_flow,header=0,sep=",")
infCol = 'DET.Flow-In.Ave.~1Day.1Day.Best [cfs]'
relCol = 'DET.Flow-Out.Ave.~1Day.1Day.Best [cfs]'
flowG = df[infCol][0]

print 'observed flow (cfs):{},{}'.format(curdate,flowG)

fG=homedir+'Det.Observed'
lines = open(fG, 'r').readlines()
# remove first day flow
#~ lines=lines[1:]
#~ lines[0] = "Date,Streamflow\n"
lines[-1]=lines[-1]+wrdate.strftime("%Y-%m-%d")+","+str(round(flowG,0))+"\n"
file = open(fG, 'w')
for line in lines:
	file.write(line)
file.close()

