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



# looking for NaN values
trips_data.isnull().any(axis=0) #ok if Closed Status, Rider Type, trip_id or bikeid == NaN

trips_startid_null = trips_data[ trips_data["Start Station Id"].isnull() ]
trips_startid_null["Duration"].describe()
# 29942 obs with missing start station id; durations appear distrib'd similar to full dataset
trips_startid_null["Start Yr-Mon"].unique()
# occur only in Apr-Sept 2018, and Jan 2020 - Apr 2022

# drop rows from trips_startid_null with missing Start Station Name
tsin1 = trips_startid_null[trips_startid_null["Start Station Name"].notnull()]
# how many obs have start stn name of the form "BIKE XXXXX"?
len(tsin1[ tsin1["Start Station Name"].str.contains("BIKE")]) #28541
# what about the obs that *aren't* "BIKE XXXXX"?
tsin1[ ~tsin1["Start Station Name"].str.contains("BIKE")]["Start Station Name"].head(10)
tsin1[ ~tsin1["Start Station Name"].str.contains("BIKE")]["Start Station Name"].tail(10)
tsin1[ ~tsin1["Start Station Name"].str.contains("BIKE")]["Start Station Name"].iloc[[135,53,70,234,14,397]]
# some have names "<Address> <Num>", some "Missing", at least one "recording_77225245"

trips_startnm_null = trips_data[ trips_data["Start Station Name"].isnull() ]
trips_startnm_null.describe()  #only 6 such obs
trips_startnm_null["Duration_Min"]  #3 very short, 1 short, 1 30 min, 1 long
trips_startnm_null["Start Station Id"] # all NaNs

trips_endid_null = trips_data[trips_data["End Station Id"].isnull()]
trips_endid_null.describe() 
# 39010 obs with missing end stn id; durations appear distrib'd similar to full dataset
trips_endid_null["Start Yr-Mon"].unique()
# occur in Apr-Sept 2018 and Jan 2019-May 2022

# drop rows from trips_endid_null with missing End Station Name
tein1 = trips_endid_null[ trips_endid_null["End Station Name"].notnull()]
# how many obs have end stn name of form "BIKE #####"?
len(tein1[ tein1["End Station Name"].str.contains("BIKE")]) #37637
# what about the obs that *aren't* "BIKE XXXXX"?
tein1[ ~tein1["End Station Name"].str.contains("BIKE")]["End Station Name"].head(10)
tein1[ ~tein1["End Station Name"].str.contains("BIKE")]["End Station Name"].tail(10)
tein1[ ~tein1["End Station Name"].str.contains("BIKE")]["End Station Name"].iloc[[1055,637,973,13,1087]]
# same as for tsin1

trips_endnm_null = trips_data[trips_data["End Station Name"].isnull()]
trips_endnm_null.describe() # only 22 such obs
trips_endnm_null["Duration_Min"]  #looks like these rides skew longer
trips_endnm_null["End Station Id"]  # all NaN

# I don't think we want to drop obs with missing start/end ID's... too many! And
# no apparent pattern in duration to explain missing #s. Given that they only
# occur in some months, which don't show unusual trip patterns... maybe it's a
# bug with the station reporting software or something? They do all have duration
# data. 
# Since all the trips in question do have start/end/duration times, it's probably
# OK to leave them all alone?
