#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 23:01:23 2017

@author: shahryar
"""

import datetime
import pandas as pd 

key=['hp']
full = ['Hydropower']
val=['DET.Power.Total.~1Day.1Day.CBT-REV']
unit=['MWh']

todayDate = datetime.date.today()
sdiff = datetime.timedelta(days=-366)
ediff = datetime.timedelta(days=0)
stDate = todayDate+sdiff
enDate = todayDate+ediff
sDay = stDate.day
sMonth = stDate.month
sYear = stDate.year
eDay = enDate.day
eMonth = enDate.month
eYear = enDate.year

sDate = str(sMonth)+'%2F'+str(sDay)+'%2F'+str(sYear)+'%2F'
eDate = str(eMonth)+'%2F'+str(eDay)+'%2F'+str(eYear)+'%2F'
print str(stDate)+" to "+str(enDate)

for i in range(len(key)):
    print "Writing {}".format(key[i])
    url = 'http://www.nwd-wc.usace.army.mil/dd/common/web_service/webexec/ecsv?id='+val[i]+'%3Aunits%3D'+unit[i]+'&headers=true&filename=&timezone=PST&startdate='+sDate+'&enddate='+eDate
    df=pd.read_csv(url,header=0,sep=",")
    df.to_csv(r'USACEData/det_'+key[i]+'.txt', header=['Date',full[i]], index=None, sep=',', mode='w')
print "Writing Inflow and Outflow"
url_flow = 'http://www.nwd-wc.usace.army.mil/dd/common/web_service/webexec/ecsv?id=DET.Flow-In.Ave.~1Day.1Day.Best%3Aunits%3Dcfs%7CDET.Flow-Out.Ave.~1Day.1Day.Best%3Aunits%3Dcfs&headers=true&filename=&timezone=PST&startdate='+sDate+'&enddate='+eDate
df=pd.read_csv(url_flow,header=0,sep=",")
df.to_csv(r'USACEData/det_flow.txt', header=['Date','Inflow','Release'], index=None, sep=',',na_rep='', mode='w')
print "Writing Elevation"
url_elev='http://www.nwd-wc.usace.army.mil/dd/common/web_service/webexec/ecsv?id=DET.Elev-Forebay.Ave.~1Day.1Day.Best%3Aunits%3DFT%7CDET.Elev-RuleCurve.Inst.~1Day.0.CENWP-CALC%3Aunits%3DFT&headers=true&filename=&timezone=PST&startdate='+sDate+'&enddate='+eDate
df=pd.read_csv(url_elev,header=0,sep=",")
df.to_csv(r'USACEData/det_elev.txt', header=['Date','Forebay Elevation','Rule Curve Elevation'], index=None, sep=',',na_rep='', mode='w')
