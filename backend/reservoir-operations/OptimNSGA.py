#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  9 23:01:05 2017

Solves Reservoir Operation Optimization Problem using NSGA-II Optimization
Dependency: pyOpt, pandas, numpy
@author: Shahryar K Ahmad
         SASWE Research Group
         skahmad@uw.edu
"""


# =============================================================================
# Standard Python modules
# =============================================================================
import os, sys, random
from datetime import datetime,timedelta
# =============================================================================
# Extension modules
# =============================================================================
#from pyOpt import *
from pyOpt import Optimization
from pyOpt import NSGA2
import numpy as np
import pandas as pd
# =============================================================================
# Define constants and objective function
# =============================================================================
lead = 16#int(sys.argv[1])
# Constants
tfact = 1.98345919969; # cfs to ac-ft/day
Smax = 455100
Smin = 135700
Hmin = 1440
turbc = 5340
TW_elev = 1200  # assumed constant
capf = 19.722  # factor for capacity factor, turbine hrs, efficiency

'''
Obtains forecast inflow, corresponding rule curve elevations and initial storage 
for optimization over lead-day period. The dates are all derived from forecast
inflow file 
'''
# Get the forecast inflow from Route output file after forecasting for lead-days lead
homedir = '/home/shahryar/DSS/'
#for filename in glob.glob('OptimData/forecastFull_inflow_*.txt'):
#    print(filename)
#    fname = os.path.join(homedir,filename)
fname = os.path.join(homedir,"VIC/Model/Route_Results/LCATproc.day" )  #"OptimData/forecastFull_inflow_20180204.txt") 
df = pd.read_csv(fname, skiprows=0)
Ifrc = list(df['Streamflow'].tail(lead))
print Ifrc
map(float,Ifrc)
nvar = len(Ifrc)
I=Ifrc
while min(I)<1000:
    I=list(map(lambda x:x+100,I))  #fix very low inflow forecasts
print I

# Define number of days (at end of optim period) to follow rule curve
num_daysRC = 2 

# Obtain dates for download links from above forecast inflow file
str_dt = list(df['Date'].tail(lead))
dt=[datetime.strptime(x, '%Y-%m-%d') for x in str_dt]  # Dates for optimization period
dt_lst= dt[0]-timedelta(days=1) # One day before only for latest storage
sdt = str(dt[0].month)+"%2F"+str(dt[0].day)+"%2F"+str(dt[0].year)
sdt_lst = str(dt_lst.month)+"%2F"+str(dt_lst.day)+"%2F"+str(dt_lst.year) 
dd=datetime.strftime(dt[0], '%d-%b-%Y %H:%M') # format route output date to USACE date
 
print "Running NSGA-II Optimization from {} to {}".format(dt[0],dt[-1])
 
# Obtain initial storage (S_o) as current realtime value from USACE
url = "http://www.nwd-wc.usace.army.mil/dd/common/web_service/webexec/ecsv?id=DET.Stor.Inst.0.0.Best%3Aunits%3Dac-ft&headers=true&filename=&timezone=PST&startdate="+sdt_lst+"+08%3A00&enddate="+sdt+"+08%3A00"

dfCurr = pd.read_csv(url)
storCol = 'DET.Stor.Inst.0.0.Best [ac-ft]'
So = float(dfCurr.loc[dfCurr['Date Time'] == dd, storCol].item())

# Get future lead days in last year for latest lead-day RC 
prevyr = dt[0]-timedelta(days=365)
dt_rc= prevyr+timedelta(days=lead) # Next lead days for lead day RC
start_rc =  str(prevyr.month)+"%2F"+str(prevyr.day)+"%2F"+str(prevyr.year) # Use last years' RC  for next lead days
end_rc = str(dt_rc.month)+"%2F"+str(dt_rc.day)+"%2F"+str(dt_rc.year) 

dt_RC = [prevyr + timedelta(days=x) for x in range(0, lead)] # Future lead days for latest lead-day RC 
dd_RC = list(map(lambda x:datetime.strftime(x, '%d-%b-%Y %H:%M'),dt_RC))

# Obtain lead days Rule Curve from USACE
url = "http://www.nwd-wc.usace.army.mil/dd/common/web_service/webexec/ecsv?id=DET.Elev-RuleCurve.Inst.~1Day.0.CENWP-CALC%3Aunits%3DFT&headers=true&filename=&timezone=PST&startdate="+start_rc+"+08%3A00&enddate="+end_rc+"+08%3A00"

dfRC= pd.read_csv(url)
RC_Col = 'DET.Elev-RuleCurve.Inst.~1Day.0.CENWP-CALC [FT]'
RC = np.array(map(lambda x:float(dfRC.loc[dfRC['Date Time'] == x, RC_Col].item()), dd_RC))
print "Rule Curve Elevation: \n", RC

# Area-elevation curve
def aec(S): 
    H = (S/10**-38)**(1/13.657)
    return H

# Define the objective (to be minimized)
def benefit(R):
    S = [None]*nvar
    H = [None]*nvar
    S[0]=So+tfact*(I[0]-R[0])
    H[0]=aec(S[0])
    for t in range(nvar-1):
        S[t+1]= S[t]+tfact*(I[t+1]-R[t+1])
        H[t+1] = aec(S[t+1])
    Rp=np.array(R)
    Rp[Rp>turbc]=turbc
    hp=[None]*nvar
    for i in range(nvar):
        hp[i] = (H[i]-TW_elev)*Rp[i]/11810
    dev = sum(np.abs(H[nvar-num_daysRC:]-RC[nvar-num_daysRC:]))
    f =  1000*dev- sum(hp) -sum(R[:4])   
    g1 = list(map(lambda x:x-Smax, S))
    g2 = list(map(lambda x:Smin-x, S))
    g3 = list(map(lambda x:Hmin-x, H))
    g = g1 + g2 + g3
    fail=0
    return f,g,fail
    

# =============================================================================
# Run the NSGA Optimizer
# ============================================================================= 
#Define the lower and upper bounds for R
LB = [500]*nvar 
UB = [9000]*nvar 
InitR=[]
for i in range(nvar):
    InitR.append(random.randint(1500,9000))
opt_prob = Optimization('Reservoir Operations Optimization',benefit)
opt_prob.addVarGroup('x',nvar,'c',lower=LB,upper=UB,value=InitR)
opt_prob.addObj('f')
opt_prob.addConGroup('g',nvar*3,'i')  # 3 inequality constraints Smin, Smax, Hmin

# Instantiate Optimizer (NSGA2) & Solve Problem
nsga2 = NSGA2()
nsga2.setOption('PrintOut',0)
nsga2.setOption('PopSize',1000)
nsga2.setOption('maxGen',150)
nsga2.setOption('pMut_real',0.075)

nsga2(opt_prob)
print "Optimization Completed Successfully!"
a= opt_prob.solution(0)
print a
Ropt=[]
for i in range(nvar):
    sf = str(a.getVar(i))
    Ropt.append(float(sf.split('\t')[2].strip().split(' ')[0]))
print Ropt

Sopt = [None]*nvar
Hopt = [None]*nvar
Sopt[0]=So+tfact*(I[0]-Ropt[0])
Hopt[0]=aec(Sopt[0])
for t in range(nvar-1):
    Sopt[t+1]= Sopt[t]+tfact*(I[t+1]-Ropt[t+1])
    Hopt[t+1] = aec(Sopt[t+1])

hp_opt=[None]*nvar
Rp_opt=np.array(Ropt)
Rp_opt[Rp_opt>turbc]=turbc
for i in range(nvar):
        hp_opt[i] = (Hopt[i]-TW_elev)*Rp_opt[i]/11810
print "Total HP: ",sum(hp_opt)

he = list(map(lambda x:x*capf,hp_opt ))  #energy in MWh
he_lim = list(map(lambda x:2400 if x>2400 else x, he)) #limit to 2400MWh

## Write to output files
print "Writing optimized decision variables..."
opath = os.path.join(homedir,"OptimData/")
with open(opath+"elev_optim_"+datetime.strftime(dt[0], '%Y%m%d')+".txt",'w') as wrfile:
    wrfile.write("Date, Elevation, RC Elevation\n")
    for i in range(nvar):
        data = str_dt[i] + ", " + "{0:.2f}".format(float(Hopt[i])) + ", " + "{0:.2f}".format(float(RC[i])) 
        wrfile.write("{}\n".format(data))
        
with open(opath+"release_optim_"+datetime.strftime(dt[0], '%Y%m%d')+".txt",'w') as wrfile:
    wrfile.write("Date, Release\n")
    for i in range(nvar):
        data = str_dt[i] + ", " + "{0:.2f}".format(float(Ropt[i])) 
        wrfile.write("{}\n".format(data))
        
with open(opath+"forecast_inflow_"+datetime.strftime(dt[0], '%Y%m%d')+".txt",'w') as wrfile:
    wrfile.write("Date, Inflow\n")
    for i in range(nvar):
        data = str_dt[i] + ", " + "{0:.2f}".format(float(I[i])) 
        wrfile.write("{}\n".format(data))
    
with open(opath+"hp_optim_"+datetime.strftime(dt[0], '%Y%m%d')+".txt",'w') as wrfile:
    wrfile.write("Date, Hydropower\n")
    for i in range(nvar):
        data = str_dt[i] + ", " + "{0:.2f}".format(float(he_lim[i])) 
        wrfile.write("{}\n".format(data))
    
with open(opath+"rulecurve_"+datetime.strftime(dt[0], '%Y%m%d')+".txt",'w') as wrfile:
    wrfile.write("Date, RC Elevation\n")
    for i in range(nvar):
        data = str_dt[i] + ", " + "{0:.2f}".format(float(RC[i])) 
        wrfile.write("{}\n".format(data))
        

