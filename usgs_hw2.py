# OCNG 689 Python for Geoscientists 
# Kelley Bradley
# HW 2

import numpy as np
from datetime import date, timedelta 
import matplotlib.pyplot as plt
import urllib

class usgs_read():
    
    '''This code contains a class that will:
     - read in data from the USGS website for river discharge 
     - return dates and corresponding flowrate
     - calculate annual mean and standard deviation of river discharge.'''
    
    #initializing class 
    def __init__(self,start,end,loc):
        self.start = start
        self.end = end
        self.loc = loc
        #accessing and opening website 
        website = urllib.urlopen\
                ('http://waterdata.usgs.gov/nwis/dv?cb_00060=on&format=rdb'+\
                '&begin_date='+self.start+'&end_date='+self.end+'&site_no='+self.loc)
        
        #setting up blank lists for input variables        
        dates = []
        discharge = []

        #reading in data 
        for line in website.readlines()[29:]:
            data  = line.split()
            year  = int(data[2].split('-')[0])
            month = int(data[2].split('-')[1])
            day   = int(data[2].split('-')[2])
            dates.append(date(year, month, day))
            discharge.append(int(data[3]))
    
        # converting lists to arrays
        dates = np.array(dates)
        discharge  = np.array(discharge)

        #converting river discharge data to SI units  
        discharge = discharge / 35.315 

        # calculating annual mean and std of discharge for daily data
        months = np.array([x.month for x in dates])
        days   = np.array([x.day for x in dates])
        
        #setting up blank lists for calculations
        ann_mean = []
        std = []
        
        for index in dates:
            date_discharge = discharge[(months==index.month) & (days==index.day)]
            ann_mean.append(np.mean(date_discharge))
            std.append(np.std(date_discharge))
            
        # converting lists to arrays...again
        ann_mean  = np.array(ann_mean) 
        std = np.array(std)

        #output of class! 
        self.dates = dates
        self.discharge = discharge
        self.ann_mean = ann_mean 
        self.std = std

if __name__ == "__main__":

#input time and location variables to obtain data  
        start = str(date(1931,1,1))
        end   = str(date(2013,1,1))
        loc  = '01100000'

#calling on the class         
merrimack_river = usgs_read(start, end, loc)

#output variables named for this specific instance/data set 
dates = merrimack_river.dates
discharge  = merrimack_river.discharge
ann_mean  = merrimack_river.ann_mean
std = merrimack_river.std

# narrowing down timeseries to plot it better
p_year  = np.array([x.year for x in dates])
index = np.where(p_year >= 2009)
p_dates = dates[index]
p_discharge  = discharge[index]
p_ann_mean  = ann_mean[index]
p_std_top = ann_mean[index] + std[index]
p_std_bottom = ann_mean[index] - std[index]

# plotting daily timeseries
fig = plt.figure()
plt.plot(p_dates, p_discharge, 'b', lw = 1.0,label = "Daily Time Series ")
plt.plot(p_dates, p_ann_mean, 'k', lw= 2.0, label = "Annual Mean")
plt.plot(p_dates, p_std_top,'k:', label = 'Std Upper Bound')
plt.plot(p_dates, p_std_bottom,'k:', label = 'Std Lower Bound')
plt.fill_between(p_dates,p_std_top,p_std_bottom, facecolor='black',alpha=0.3)
plt.legend(loc = 'upper right')
plt.title('River Discharge for location number:'+ loc)
plt.xlabel('Date')
plt.ylabel('Discharge (m$^{3}$/sec)')
plt.show()
plt.savefig('river_discharge.pdf')








