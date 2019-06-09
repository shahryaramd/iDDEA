#!/usr/bin/env python

#Developed by Shahryar Ahmad, skahmad@uw.edu
#Graduate Student and Research Assistant
#SASWE Research Group, University of Washington

import numpy as np
import os
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import netCDF4 as nc
import math
import glob
import sys

lead = int(sys.argv[1])
fdate = str(sys.argv[2])

def polar_stere(axidx, axidy, lon_w, lon_e, lat_s, lat_n):
     lon_0 = lon_w + (lon_e - lon_w) / 2.
     ref = lat_s if abs(lat_s) > abs(lat_n) else lat_n
     lat_0 = math.copysign(90., ref)
     proj = 'npstere' if lat_0 > 0 else 'spstere'
     prj = Basemap(projection=proj, lon_0=lon_0, lat_0=lat_0,
                   boundinglat=0, resolution='c')
     lons = [lon_w, lon_e, lon_w, lon_e, lon_0, lon_0]
     lats = [lat_s, lat_s, lat_n, lat_n, lat_s, lat_n]
     x, y = prj(lons, lats)
     ll_lon, ll_lat = prj(min(x), min(y), inverse=True)
     ur_lon, ur_lat = prj(max(x), max(y), inverse=True)
     return Basemap(projection='stere', lat_0=lat_0, lon_0=lon_0,
                    llcrnrlon=ll_lon, llcrnrlat=ll_lat,
                    urcrnrlon=ur_lon, urcrnrlat=ur_lat, ax=axes[axidx, axidy])


def get_nc_rain_data(file, day):
     rootgroup = nc.Dataset(file, 'r', format='NETCDF4')
     outdata = rootgroup.variables['RAIN'][:][day]
     rootgroup.close()
     return outdata


def get_nc_tmax_data(file,day):
     rootgroup = nc.Dataset(file, 'r', format='NETCDF4')
     outdata = rootgroup.variables['TMAX'][:][day]
     rootgroup.close()
     return outdata


def get_nc_tmin_data(file,day):
     rootgroup = nc.Dataset(file, 'r', format='NETCDF4')
     outdata = rootgroup.variables['TMIN'][:][day]
     rootgroup.close()
     return outdata

def get_nc_wind_data(file,day):
     rootgroup = nc.Dataset(file, 'r', format='NETCDF4')
     outdata = rootgroup.variables['W2'][:][day]
     rootgroup.close()
     return outdata


infile = 'wrf2vic.'+fdate+'.VAR.D02.nc'
rootgroup = nc.Dataset(infile, 'r', format='NETCDF4')
lats_orig = rootgroup.variables['XLAT'][:]
lons_orig = rootgroup.variables['XLONG'][:]
lats_wrf = lats_orig[0, :, :]
lons_wrf = lons_orig[0, :, :]
day = 0

prec = [None]*lead
tmax = [None]*lead
tmin = [None]*lead
wind = [None]*lead
print "Appending WRF forecast forcings to hindcast..."
for i in range(lead):
         
         prec_data = get_nc_rain_data(infile, day)  # + 1) - get_nc_rain_data(infile, day)
         prec[day] = prec_data
         tmax[day] = get_nc_tmax_data(infile,day)
         tmin[day] = get_nc_tmin_data(infile,day)
         wind[day] = get_nc_wind_data(infile,day)
         day += 1	

## append to forcing
lats1_wrf =  lats_wrf[:,0]  #convert to 1d
lons1_wrf = lons_wrf[0,:]
forcingpath = "/home/shahryar/DSS/VIC/Model/Forcing/"  ## CHANGE name to allow this to run
for inner in glob.glob(forcingpath+"*"):
    with open(inner,'a') as infile:
        base= os.path.basename(inner)
        base_spl = base.split("_")
        forc_lat = float(base_spl[1])
        forc_lon = float(base_spl[2])
        #find closest to lat lon in lat_wrf and lon_wrf
        idxlat = (np.abs(forc_lat - lats1_wrf)).argmin()
        idxlon = (np.abs(forc_lon - lons1_wrf)).argmin()
        #print forc_lat, latst_wrf[idxlat]
        for day in range(lead):
            prec_forc = prec[day][idxlat][idxlon]
            tmax_forc = tmax[day][idxlat][idxlon]
            tmin_forc = tmin[day][idxlat][idxlon]
            wind_forc = wind[day][idxlat][idxlon]
            
            data = "{0:.2f}".format(float(prec_forc)) + " " + "{0:.2f}".format(float(tmax_forc)) + " " + "{0:.2f}".format(float(tmin_forc)) + " " + "{0:.2f}".format(float(wind_forc))            
            infile.write("{}\n".format(data))
print "Successfully appended forecast forcings to hindcast"
