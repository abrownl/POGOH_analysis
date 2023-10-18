# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 01:20:04 2023

@author: Allie
"""

import os
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

dirpath = os.path.join("C:", os.sep, "Users", "Allie", "Projects", "Other", "POGOH")
os.chdir(dirpath)



### Trip Data ###
# read in trip data
trip_data = pd.read_csv(os.path.join("data", "processed", "trips_combined.csv"), 
                                     dtype={'Closed Status': str})

# reconvert date columns to datetime - csv does not store datetimes
trip_data["Start Date"] = pd.to_datetime(trip_data["Start Date"])
trip_data["End Date"] = pd.to_datetime(trip_data["End Date"])

# sort oldest to newest
trip_data = trip_data.sort_values(by=["Start Date", "End Date"])

# pull out year, month, day, hour
trip_data["Start Year"] = trip_data["Start Date"].dt.year
trip_data["Start Month"] = trip_data["Start Date"].dt.month
trip_data["Start Yr-Mon"] = trip_data["Start Date"].dt.to_period('M')
trip_data["Start Day"] = trip_data["Start Date"].dt.day
trip_data["Start Hour"] = trip_data["Start Date"].dt.hour

# Duration only gives time in seconds
trip_data["Duration_Min"] = trip_data["Duration"]/60
trip_data["Duration_Min_Rd"] = trip_data["Duration_Min"].round()
trip_data["Duration_Hr"] = trip_data["Duration_Min"]/60
trip_data["Duration_Hr_Rd"] = trip_data["Duration_Hr"].round()

trip_data = trip_data.drop(columns = {"Unnamed: 0"})


# drop interactions less than/eq to 1 min or with unusual Closed Status
drop_index = trip_data[ ((trip_data["Duration"] < 60) |
                    (trip_data["Closed Status"] == "GRACE_PERIOD") |   #grace period: returned within <60 sec
                    (trip_data["Closed Status"] == "TERMINATED") |
                    (trip_data["Closed Status"] == "FORCED_CLOSED")) ].index  
trips = trip_data.drop(drop_index)


# scatterplots of ride durations
for yr in range(2015, 2024):
    filename = "ride_dur_" + str(yr) + ".png"
    
    x = trips[ trips["Start Year"] == yr ]["Start Month"]
    y = trips[ trips["Start Year"] == yr ]["Duration"]
    
    fig, ax = plt.subplots()
    ax.scatter(x,y)
    ax.axhline(y=200000, color="r")
    ax.axhline(y=175000, color="orange")
    fig.savefig(os.path.join(dirpath, "visualizations", filename))  

# 200K looks like a good max cutoff?
# no, 175K better
fig, ax = plt.subplots()
ax.hist(trips[trips["Duration"] > 175000]["Duration"], bins=100)
fig.savefig(os.path.join("visualizations", "rides_over_175K.png"))

drop_index = trips[ trips["Duration"] > 175000 ].index
trips_cln = trips.drop(drop_index)

# save
trips_cln.to_csv(os.path.join("data", "processed", "trips_clean.csv"))
print("Saved: trips_clean.csv")



### Station Data ###
stn_data = pd.read_csv(os.path.join("data", "processed", "stations_combined.csv"))

# order by date and station id
stn_data = stn_data.sort_values(by=["Date", "Id"])


# count total stations and total docks per month
stns_by_month = stn_data.groupby("Date", as_index=False).agg({"Id": 'count',
                                                            "Total Docks": "sum"})
stns_by_month = stns_by_month.rename(columns = {'Id':'Station Count'})

# fill in missing dates with values from previous dates
stns_by_month["Date"] = pd.to_datetime(stns_by_month["Date"]).dt.to_period('M')
stns_by_month = stns_by_month.set_index("Date", drop=True)

idx = pd.period_range("2015-05","2023-09", freq='M')
stns_by_month = stns_by_month.reindex(idx, method='ffill')

# save
stns_by_month.to_csv(os.path.join("data", "processed", "stations_by_month.csv"))
print("Saved: stations_by_month.csv")