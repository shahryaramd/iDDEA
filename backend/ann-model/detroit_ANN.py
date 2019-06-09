#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu May 30 14:56:08 2019

@author:  Shahryar Ahmad, skahmad@uw.edu
#Graduate Student and Research Assistant
#SASWE Research Group, University of Washington
"""
# %%
import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pyrenn as prn
from datetime import datetime,timedelta
from scipy.interpolate import interp1d
###
sz=23
indxV=range(sz)
lead=7
datdir='/home/shahryar/DSS/ANN_Detroit/'
basin = 'detroit'
# load dataset
dfobs = pd.read_csv(datdir+'Det.Observed',sep=',')	 #read_excel(datdir+'Predictors/ObservedInflowDetroit.xlsx',sheet_name=basin, header=None)
dfgsod = pd.read_csv(datdir+'Predictors/Predictor_Nowcast_Detroit.txt',header=None,sep='\t')
ant=3   #number of antecedent days of predictors
dprecL=np.zeros([sz,lead+ant])
dtmaxL=np.zeros([sz,lead+ant])
dtminL=np.zeros([sz,lead+ant])
dwspdL=np.zeros([sz,lead+ant])
for nn in range(ant):  #doesn't run for ant=0
    dprecL[:,nn]=np.array(dfgsod.iloc[nn:sz+nn,1])
    dtmaxL[:,nn]=np.array(dfgsod.iloc[nn:sz+nn,2])
    dtminL[:,nn]=np.array(dfgsod.iloc[nn:sz+nn,3])
# %%
qobsV=np.zeros([len(indxV),lead])
yV=np.zeros([len(indxV),lead])
for nn in range(lead):
	df = pd.read_csv(datdir+'Predictors/GFSprocessed/Predictor_GFS_L'+str(nn+1) +'.txt',header=None,sep=' ')
	df = df.fillna(0)
	str_day = list(df.iloc[-sz:,0])
	dayorg=np.array([datetime.strptime(str(x), '%Y%m%d') for x in str_day])  # Dates
	dprecL[:,nn+ant]=np.array(df.iloc[-sz:,1])
	dtmaxL[:,nn+ant]=np.array(df.iloc[-sz:,2])
	dtminL[:,nn+ant]=np.array(df.iloc[-sz:,3])
	dwspdL[:,nn+ant]=np.array(df.iloc[-sz:,4])
	
b=np.zeros([len(dprecL),7])
r=np.zeros([len(dprecL),7])
byV=np.zeros([len(indxV),lead])
ryV=np.zeros([len(indxV),lead])
QhcL=np.zeros([len(dprecL),7])
nse,nseV,corr,corrV,finF,finDate=[],[],[],[],[],[]

a=0.08
BFImax=0.58

for nl in range(7,0,-1):
    nn=7-nl
    if nn==0:
		QhcL[:,nn]=dfobs.iloc[-sz:,1]
    else:
		QhcL[:,nn]=dfobs.iloc[-sz-nn:-nn,1]

    for k in range(1,len(dprecL)):
        b[k,nn]=min(QhcL[k,nn],((1 - BFImax) * a * b[k-1,nn] + ( 1 - a ) * BFImax * QhcL[k,nn]) / ( 1 - a * BFImax) )
        r[k,nn]=QhcL[k,nn]-b[k,nn]
		
# %%

forec=np.zeros(lead)
# Define Predictors
for nn in range(7):
    daysV=dayorg[indxV]
    doyV=np.array(map(lambda x: x.timetuple().tm_yday,daysV))
    if nn==0:
        xQV = np.column_stack((QhcL[indxV,0], QhcL[indxV,1]))
        bQV = np.column_stack((b[indxV,0], b[indxV,1]))
        rQV = np.column_stack((r[indxV,0], r[indxV,1]))
    elif nn==1:
        xQV = np.column_stack((yV[:,nn-1], QhcL[indxV,0], QhcL[indxV,1]))
        bQV = np.column_stack((byV[:,nn-1], b[indxV,0]))
        rQV = np.column_stack((ryV[:,nn-1], r[indxV,0]))
    elif nn==2:
        xQV = np.column_stack((yV[:,nn-1], yV[:,nn-2], QhcL[indxV,0]))
        bQV = np.column_stack((byV[:,nn-1], byV[:,nn-2]))
        rQV = np.column_stack((ryV[:,nn-1], ryV[:,nn-2]))
    else:
        xQV = np.column_stack((yV[:,nn-1], yV[:,nn-2], yV[:,nn-3], QhcL[indxV,0]))
        bQV = np.column_stack((byV[:,nn-1], byV[:,nn-2], byV[:,nn-3]))
        rQV = np.column_stack((ryV[:,nn-1], ryV[:,nn-2], ryV[:,nn-3]))


    xV=np.column_stack(( dprecL[indxV,nn+ant], dprecL[indxV,nn+ant-1], dprecL[indxV,nn+ant-2], \
                         dtmaxL[indxV,nn+ant], \
                         dtminL[indxV,nn+ant], \
#                         dwspdL[indxV,nn+ant], \
                         xQV, bQV,\
                         ))

    xV = np.transpose(xV)
 
    mdl_name = datdir+'Bin/pyrennNet4_'+basin+'_L'+str(nn)+'.csv'
#    #Create and train NN
#    print 'Training NN..'
#    net = prn.CreateNN([x.shape[0],7,1])
#    net = prn.train_LM(x,t,net,verbose=True,k_max=500,E_stop=1e-5) 
#    prn.saveNN(net,mdl_name)

    #Load saved NN
    net=prn.loadNN(mdl_name)
    #Calculate outputs of the trained NN for train and test data
    yV[:,nn] = prn.NNOut(xV,net)

#    tmp=y[:,nn]
#    tmp[tmp<0]=0
#    tmp[tmp>400000]=0 
#    y[:,nn]=tmp
#    tmp=yV[:,nn]
#    tmp[tmp<0]=0
#    tmp[tmp>400000]=0
#    yV[:,nn]=tmp
    
    byV[0,nn]=yV[0,nn]

    for k in range(1,len(yV)):
        byV[k,nn]=min(yV[k,nn],((1 - BFImax) * a * byV[k-1,nn] + ( 1 - a ) * BFImax * yV[k,nn]) / ( 1 - a * BFImax) );
        ryV[k,nn]=yV[k,nn]-byV[k,nn];

##        
#    tmp=yV[:,nn]
#    xip=np.array([2,3,4])
#    for i in range(3,len(yV)):       
#        if np.abs(tmp[i]-tmp[i-1])>15000 or tmp[i]>50000 or tmp[i]<0:
#            
#            yip=np.array([tmp[i-1],tmp[i-2],tmp[i-3]])
#            f = interp1d(xip, yip, fill_value = "extrapolate")
#            tmp[i]=tV[i-1]+np.mean([tV[i-1]-tV[i-2]])#,tV[i-2]-tV[i-3]])
#    yV[:,nn]=tmp
#    
	#print "Lead "+str(nn)+"\n", yV[:lead,nn]
    forec[nn]=yV[-1,nn]
    fdt=(daysV[-1]+timedelta(days=nn+1)).strftime("%Y-%m-%d")
    finF.append([fdt,forec[nn]])  
 
#fixing
print "orig ANN forecast", yV[-1,:] #finF
for i in range(len(finF)):
	if i==0:
		prev=QhcL[-1,0]
		prev2=QhcL[-2,0]
	elif i==1:
		prev=finF[i-1][1]
		prev2=QhcL[-1,0]
	else:
		prev=finF[i-1][1]
		prev2=finF[i-2][1]
	cur=finF[i][1]	       
	if  np.abs(cur-prev)>15000 or cur>200000 or cur<0:
		print "High value", cur      
		cur=2*prev-prev2
	finF[i][1]=cur
print finF

fn=datdir+"Det.ANNForecast"
with open(fn, "w") as text_file:
	text_file.write("Date,Streamflow\n")
	text_file.write("{},{}\n".format(daysV[-1].strftime("%Y-%m-%d"),round(QhcL[-1,0],1)))

with open(fn, "a") as text_file:
	for n in range(len(finF)):
		text_file.write("{},{}\n".format(finF[n][0],round(finF[n][1],1)))

# store the same file in ANN forecast history
fn=datdir+'ANNForecastHistory/'+(daysV[-1]+timedelta(days=1)).strftime("%Y%m%d")+".Det.ANNForecast"
with open(fn, "w") as text_file:
	text_file.write("Date,Streamflow\n")
	text_file.write("{},{}\n".format(daysV[-1].strftime("%Y-%m-%d"),round(QhcL[-1,0],1)))

with open(fn, "a") as text_file:
	for n in range(len(finF)):
		text_file.write("{},{}\n".format(finF[n][0],round(finF[n][1],1)))
