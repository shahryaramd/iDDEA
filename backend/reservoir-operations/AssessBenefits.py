# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 09:20:30 2017

@author: Shahryar K Ahmad
"""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime,timedelta

for nn in range(0,1,1):
    curdate = datetime.today() - timedelta(days=nn)    #datetime(2018, 03, nn) 
    curstr = datetime.strftime(curdate,'%Y%m%d') 
    print nn,curdate
    tfact = 1.98345919969 #cfs to ac-ft/day
    assessdays = 8 #number of days for asssessment
    updatestep=2
    turbc = 5340
    TW_elev = 1200  #assumed constant
    homedir = '/home/shahryar/DSS/'
    fpath = os.path.join(homedir,'OptimData')
    reqdate = curdate - timedelta(days=assessdays)
    reqdate = datetime.strftime(reqdate,'%Y%m%d') 
    
    # Area-elevation curve
    def aec(S): 
        H = (S/10**-38)**(1/13.657)
        return H
    
    # Define the objective (to be minimized)
    def benefit(R, *args):
        I,nvar,tfact,Smax,Smin,Hmin,So,turbc,RC = args
        S = [None]*nvar
        H = [None]*nvar
        S[0]=So+tfact*(I[0]-R[0])
        H[0]=aec(S[0])
        for t in range(nvar-1):
            S[t+1]= S[t]+tfact*(I[t+1]-R[t+1])
            H[t+1] = aec(S[t+1])
        H =np.array(H)
        Rp=np.array(R)
        Rp[Rp>turbc]=turbc
        hp=[None]*nvar
        for i in range(nvar):
            hp[i] = (H[i]-TW_elev)*Rp[i]/11810
    
    fRopt = os.path.join(fpath,"release_optim_"+reqdate+".txt")
    df = pd.read_csv(fRopt, skiprows=0)
    Ropt = list(df[' Release'].head(assessdays))
    str_dt = list(df['Date'].head(assessdays))
    map(float,Ropt)
    nvar = len(Ropt)
    
    stDate = datetime.strptime(reqdate,'%Y%m%d')
    ediff = timedelta(days=(assessdays))  ###+1  if one less observed data
    enDate = stDate+ediff
    sDay = stDate.day
    sMonth = stDate.month
    sYear = stDate.year
    eDay = enDate.day
    eMonth = enDate.month
    eYear = enDate.year
    sDate = str(sMonth)+'%2F'+str(sDay)+'%2F'+str(sYear)+'%2F'
    eDate = str(eMonth)+'%2F'+str(eDay)+'%2F'+str(eYear)+'%2F'
    dt_lst= stDate-timedelta(days=1) #
    sdt = str(stDate.month)+"%2F"+str(stDate.day)+"%2F"+str(stDate.year)
    sdt_lst = str(dt_lst.month)+"%2F"+str(dt_lst.day)+"%2F"+str(dt_lst.year) 
    dd=datetime.strftime(stDate, '%d-%b-%Y %H:%M') # format route output date to USACE date
    
    #Obtain initial storage (S_o) from USACE
    url = "http://www.nwd-wc.usace.army.mil/dd/common/web_service/webexec/ecsv?id=DET.Stor.Inst.0.0.Best%3Aunits%3Dac-ft&headers=true&filename=&timezone=PST&startdate="+sdt_lst+"+08%3A00&enddate="+sdt+"+08%3A00"
    dfCurr = pd.read_csv(url)
    storCol = 'DET.Stor.Inst.0.0.Best [ac-ft]'
    So = float(dfCurr.loc[dfCurr['Date Time'] == dd, storCol].item())
    
    #Obtain observed inflow and outflow
    url_flow = 'http://www.nwd-wc.usace.army.mil/dd/common/web_service/webexec/ecsv?id=DET.Flow-In.Ave.~1Day.1Day.Best%3Aunits%3Dcfs%7CDET.Flow-Out.Ave.~1Day.1Day.Best%3Aunits%3Dcfs&headers=true&filename=&timezone=PST&startdate='+sDate+'&enddate='+eDate
    print url_flow
    df=pd.read_csv(url_flow,header=0,sep=",")
    infCol = 'DET.Flow-In.Ave.~1Day.1Day.Best [cfs]'
    relCol = 'DET.Flow-Out.Ave.~1Day.1Day.Best [cfs]'
    Iobs = map(float,df[infCol])
    Robs = map(float,df[relCol])
    if len(Iobs)<8:    #in case of missing obs data
		Iobs.insert(2+nn,Iobs[1+nn])
		Robs.insert(2+nn,Robs[1+nn])
    
    #Obtain sequential release, updated every alternate day
    Rseq = []
    stDate = datetime.strptime(reqdate,'%Y%m%d')
    for i in range(0,nvar,updatestep):
        ediff = timedelta(days=i)
        enDate = stDate+ediff
        seqdate = datetime.strftime(enDate,'%Y%m%d')
        fRopt = os.path.join(fpath,"release_optim_"+seqdate+".txt")
        df_rel = pd.read_csv(fRopt, skiprows=0)
        Rseq.append(list(df_rel[' Release'].head(updatestep)))        #for every update step, append first 2 releases
    Rseq=np.array(Rseq).flatten()
    
    ##Obtain actual forecast benefits: Forecasted Optimized Release and Forecasted Inflow
    #fhp = "OptimData/hp_optim_"+reqdate+".txt"
    #df_hp = pd.read_csv(fhp, skiprows=0)
    #hp_forecast = list(df_hp[' Hydropower'].head(8))
    #print "Total Forecast HP: ",sum(hp_forecast)
    
    # 1. Obtain realized benefits: Sequentially Optimized Release and Observed Inflow

    Sreal = [None]*nvar
    Hreal = [None]*nvar
    print Iobs
    Sreal[0]=So+tfact*(Iobs[0]-Rseq[0])
    Hreal[0]=aec(Sreal[0])
    for t in range(nvar-1):
        #~ print "t {} \n Rseq {} \n Iobs{} \n Sreal {} \n ".format(t, Rseq,Iobs,Sreal)
        Sreal[t+1]= Sreal[t]+tfact*(Iobs[t+1]-Rseq[t+1])
        Hreal[t+1] = aec(Sreal[t+1])
    
    hp_real=[None]*nvar
    Rp_real=np.array(Rseq)
    Rp_real[Rp_real>turbc]=turbc
    for i in range(nvar):
            hp_real[i] = (Hreal[i]-1200)*Rp_real[i]/11810
    print "Total Realized HP: ",sum(hp_real)
    he = list(map(lambda x:x*19.722,hp_real ))  #energy in MWh
    he_real = list(map(lambda x:2400 if x>2400 else x, he)) #limit to 2400MWh
    
    # 2. Obtain actual benefits: Observed Release and Observed Inflow
    Sact = [None]*nvar
    Hact = [None]*nvar
    Sact[0]=So+tfact*(Iobs[0]-Robs[0])
    Hact[0]=aec(Sact[0])
    for t in range(nvar-1):
        Sact[t+1]= Sact[t]+tfact*(Iobs[t+1]-Robs[t+1])
        Hact[t+1] = aec(Sact[t+1])
    
    hp_act=[None]*nvar
    Rp_act=np.array(Robs)
    Rp_act[Rp_act>turbc]=turbc
    for i in range(nvar):
            hp_act[i] = (Hact[i]-1200)*Rp_act[i]/11810
    print "Total Actual HP: ",sum(hp_act)
    he = list(map(lambda x:x*19.722,hp_act ))  #energy in MWh
    he_act = list(map(lambda x:2400 if x>2400 else x, he)) #limit to 2400MWh
    
    wrfile = os.path.join(fpath,"assess_"+curstr+".txt")
    inflowfile = os.path.join(fpath,"obs_inflow_"+curstr+".txt")
    with open(wrfile,'w') as wrfile:
        wrfile.write("Date, Optimized, Observed\n")
        for i in range(nvar):
            data = str_dt[i] + ", " + "{0:.2f}".format(float(he_real[i])) + ", " + "{0:.2f}".format(float(he_act[i])) 
            wrfile.write("{}\n".format(data))
    with open(inflowfile,'w') as wrfile:
        wrfile.write("Date, ObservedInflow\n")
        for i in range(nvar):
            data = str_dt[i] + ", " + "{0:.2f}".format(float(Iobs[i]))  
            wrfile.write("{}\n".format(data))
            
