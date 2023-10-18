# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 21:56:50 2023

"""

import os
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

dirpath = os.path.join("C:", os.sep, "Users", "Allie", "Projects", "Other", "POGOH")
os.chdir(dirpath)

trips_data = pd.read_csv(os.path.join("data", "processed", "trips_clean.csv"), 
                        dtype={'Closed Status': str}, index_col=0)
trips_data = trips_data.drop(columns = {"Unnamed: 0.4","Unnamed: 0.3","Unnamed: 0.2"})

trips_desc = trips_data.describe()
print(trips_desc["Duration"])
print(trips_data["Duration"].quantile(np.arange(0.1,1.0,0.05)))
print(trips_data["Duration"].quantile(np.arange(0.9,1.0,0.01)))
print(trips_data["Duration"].quantile(np.arange(0.99,1.0,0.001)))



# looking for cutoff points on right hand tail of data (v long trips)
plt.hist(trips_data[trips_data["Duration"]<=86400]["Duration"], bins=150)
plt.hist(trips_data[(trips_data["Duration"]>=15000) & (trips_data["Duration"]<=86400)]["Duration"], bins=150)
plt.hist(trips_data[(trips_data["Duration"]>=15000)]["Duration"], bins=150)
plt.axvline(95000, color="red")
plt.axvline(110000, color="orange")



# looking for cutoff points on lefthand 'tail' of data (v short trips)
plt.hist(trips_data[trips_data["Duration"] < 1000]["Duration"], bins=100)
plt.axvline(150, color="r") 

trips_short = trips_data[ trips_data["Duration"] < 600]
plt.hist(trips_short["Duration"], bins=60)
plt.axvline(150, color="r")

trips_short["Start Yr-Mon"].unique()   #no obv months/years with weird data
len(trips_short["Start Station Name"].unique()) # no obv stations with weird data
len(trips_short["End Station Name"].unique()) # no obv stations with weird data
len(trips_short)    

#not all are bikes returned to same station
trips_short_same = trips_short[ trips_short["Start Station Name"] == trips_short["End Station Name"]]
len(trips_short_same)
trips_short_same["Duration"].describe()
trips_short_same["Start Yr-Mon"].unique() #no patterns in date

# in fact, more are bikes returned to diff station
trips_short_diff = trips_short[ trips_short["Start Station Name"] != trips_short["End Station Name"]]
len(trips_short_diff)
trips_short_diff["Duration"].describe()
trips_short_same["Start Yr-Mon"].unique() #no patterns in date...

# random selections from trips_short_diff look reasonable
trips_short_diff.iloc[2]
trips_short_diff.iloc[53]
trips_short_diff.iloc[35000]
trips_short_diff.iloc[-50]
trips_short_diff.iloc[-1]

trips_v_short = trips_data[ trips_data["Duration"] < 150]
len(trips_v_short)
trips_v_short["Start Yr-Mon"].unique() # still no patterns!

trips_v_short_same = trips_v_short[ trips_v_short["Start Station Name"] == trips_v_short["End Station Name"]]
len(trips_v_short_same)
# most of the v short trips start and end at the same station... but not a huge majority
