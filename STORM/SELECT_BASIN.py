# -*- coding: utf-8 -*-
"""
@author: Nadia Bloemendaal, nadia.bloemendaal@vu.nl, Marjolein Ribberink, m.r.s.ribberink@vu.nl

For more information, please see 
Bloemendaal, N., Haigh, I.D., de Moel, H. et al. 
Generation of a global synthetic tropical cyclone hazard dataset using STORM. 
Sci Data 7, 40 (2020). https://doi.org/10.1038/s41597-020-0381-2

This is the STORM module for simulation of genesis month, frequency, and basin boundaries

Copyright (C) 2020 Nadia Bloemendaal. All versions released under the GNU General Public License v3.0
"""
import numpy as np
import random
import os
import sys
dir_path=os.path.dirname(os.path.realpath(sys.argv[0]))
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

#Basin indices: 
# 0 = EP = Eastern Pacific
# 1 = NA = North Atlantic
# 2 = NI = North Indian
# 3 = SI = South Indian
# 4 = SP = South Pacific
# 5 = WP = Western Pacific

def Genesis_date(idx, storms):
    """
    Sample the genesis dates for every TC
    Parameters
    ----------
    idx : basin index (0=EP 1=NA 2=NI 3=SI 4=SP 5=WP).
    storms : number of TCs.

    Returns
    -------
    months : list of all genesis months.
    days : list of all genesis days.
    hours : list of all genesis hours.
    """
    monthlist=np.load(os.path.join(__location__,'../STORM_variables','GENESIS_MONTHS.npy'),allow_pickle=True,encoding='latin1').item()
    monthlength=[31,28,31,30,31,30,31,31,30,31,30,31]
    hourlist=[0,3,6,9,12,15,18,21]
    
    months=[]
    days=[]
    hours=[]
    for i in range(0,storms):
        months.append(int(np.random.choice(monthlist[idx])))#randomly choose formation month
        days.append(int(np.random.randint(1,monthlength[months[i]-1]+1))) #based on formation month length, choose day from uniform distribution
        hours.append(int(np.random.choice(hourlist))) #pick randomly out of 3-hourly interval
    return months,days,hours

    
def Storms(idx): 
    """
    Sample the number of TC formations in a given year

    Parameters
    ----------
    idx : basin index (0=EP 1=NA 2=NI 3=SI 4=SP 5=WP).

    Returns
    -------
    s : number of storms.

    """
    mu_list=np.loadtxt(os.path.join(__location__,'../STORM_variables','POISSON_GENESIS_PARAMETERS.txt'))
    #mu_list has the shape [EP,NA,NI,SI,SP,WP]
    
    mu=mu_list[idx]

    poisson=np.random.poisson(mu,10000)
    s=random.choice(poisson)
    return s

def Basins_WMO(idx):
    """
    Basin definitions

    Parameters
    ----------
    idx : basin index.

    Returns
    -------
    lat0 : lower left corner latitude.
    lat1 : upper right corner latitude.
    lon0 : lower left corner longitude.
    lon1 : upper right corner longitude.

    """
    #We follow the basin definitions from the IBTrACS dataset, but with lat boundaries set at 60 N/S
    #The ENP/AO border will be defined in the algorithm later. 
    
  
    if idx==0: #Eastern Pacific
        lat0,lat1,lon0,lon1=5,90,180,285
    if idx==1: #North Atlantic
        lat0,lat1,lon0,lon1=5,90,255,390
    if idx==2: #North Indian
        lat0,lat1,lon0,lon1=5,90,30,100
    if idx==3: #South Indian
        lat0,lat1,lon0,lon1=-90,-5,10,105
    if idx==4: #South Pacific
        lat0,lat1,lon0,lon1=-90,-5,105,240
    if idx==5: #Western Pacific
        lat0,lat1,lon0,lon1=5,90,100,180

    return lat0,lat1,lon0,lon1 

def Gen_basin(basin):
    """
    Generate the number of storms and date of formation for each

    Parameters
    ----------
    basin : basin.

    Returns
    -------
    s : number of storms.
    month : list of genesis months.
    day : list of genesis days.
    hour: list of genesis hours.
    idx: index of current basin.
    
    """
    #We follow the basin definitions from the IBTrACS dataset, but with lat 
    #boundaries set at 90 N/S, and a shifted SI/SP border
    #The ENP/AO border will be defined in the algorithm later. 
    
    basins=['EP','NA','NI','SI','SP','WP']
    basin_name = dict(zip(basins,[0,1,2,3,4,5]))
    idx=basin_name[basin]
    
    s=Storms(idx)
    
    month,day,hour=Genesis_date(idx,s)
  
        
    return s,month,day,hour,idx 

