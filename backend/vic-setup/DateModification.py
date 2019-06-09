#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 21:37:07 2017

@author: shahryar
"""

import datetime
import os
todayDate = datetime.date.today()
diff2 = datetime.timedelta(days=-1)
todayDate = todayDate + diff2
diff = datetime.timedelta(days=-1095)
startDate = todayDate + diff
endYear = todayDate.strftime("%Y")
endMonth = todayDate.strftime("%m")
endDay = todayDate.strftime("%d")
startYear = startDate.strftime("%Y")
startMonth = startDate.strftime("%m")
startDay  =  startDate.strftime("%d")
print("Start Date of Model simulation: " + startDate.strftime("%Y%m%d"))
print("End Date of Model simulation: " + todayDate.strftime("%Y%m%d"))
print("Modifying parameter files . . . ")
fileArray = ["brahma","ganges","indus", "meghna"]
#for x in range(0, len(fileArray)):
filename = "/home/shahryar/DSS/VIC/Model/Parameters/global.param"
with open(filename, "r") as myfile:
    line = myfile.readlines()
line[10] = line[10][:10] + startYear + line[10][14:]
line[11] = line[11][:11] + startMonth  + line[11][13:]
line[12] = line[12][:9] + startDay + line[12][11:]

line[14] = line[14][:9] + endYear + line[14][13:]
line[15] = line[15][:9] + endMonth  + line[15][11:]
line[16] = line[16][:8] + endDay + line[16][10:]

line[65] = line[65][:10] + startYear + line[65][14:]
line[66] = line[66][:11] + startMonth  + line[66][13:]
line[67] = line[67][:9] + startDay + line[67][11:]
os.remove(filename)
for i in range(0, len(line)):
    with open(filename, "a") as text_file:
        text_file.write(line[i])

filename = "/home/shahryar/DSS/VIC/Model/Parameters/Route.input"
with open(filename, "r") as myfile:
    line = myfile.readlines()
line[23] = startYear + " " + startMonth + " " + startDay + "\n"
line[24] = endYear + " " + endMonth + " " + endDay + "\n"
os.remove(filename)
for i in range(0, len(line)):
    with open(filename, "a") as text_file:
        text_file.write(line[i])
print("Model Simulation files modified successfully.")

## Modify WRF files
sDate = datetime.date.today()
add = datetime.timedelta(days=16)
eDate = sDate + add
wsYear = sDate.strftime("%Y")
wsMonth = sDate.strftime("%m")
wsDay = sDate.strftime("%d")
weYear = eDate.strftime("%Y")
weMonth = eDate.strftime("%m")
weDay = eDate.strftime("%d")

# namelist.wps
filename = "/home/shahryar/wrf/Build_WRF/WPS/namelist.wps"
with open(filename, "r") as myfile:
    line = myfile.readlines()
sd = str(wsYear)+"-"+str(wsMonth)+"-"+str(wsDay)+"_00:00:00" 
ed = str(weYear)+"-"+str(weMonth)+"-"+str(weDay)+"_12:00:00"
line[3] = " start_date = '"+sd+"','"+sd+"', \n"
line[4] = " end_date   = '"+ed+"','"+ed+"', \n"

os.remove(filename)
for i in range(0, len(line)):
    with open(filename, "a") as text_file:
        text_file.write(line[i])
print("namelist.wps modified successfully.")

# namelist.input
filename = "/home/shahryar/wrf/Build_WRF/WRFV3/run/namelist.input"
with open(filename, "r") as myfile:
    line = myfile.readlines()
line[5] = " start_year                          = "+wsYear+", "+wsYear+" , \n"
line[6] = " start_month                         = "+wsMonth+", "+wsMonth+" , \n"
line[7] = " start_day                           = "+wsDay+", "+wsDay+" , \n"
line[11] = " end_year                            = "+weYear+", "+weYear+" , \n"
line[12] = " end_month                           = "+weMonth+", "+weMonth+" , \n"
line[13] = " end_day                             = "+weDay+", "+weDay+" , \n"

os.remove(filename)
for i in range(0, len(line)):
    with open(filename, "a") as text_file:
        text_file.write(line[i])
print("namelist.input modified successfully.")

