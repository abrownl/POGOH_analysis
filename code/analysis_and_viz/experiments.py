# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 18:33:59 2023

"""

import pandas as pd
import numpy as np
import os
from matplotlib import pyplot as plt

# set directory path
dirpath = os.path.join("C:", os.sep, "Users", "Allie", "Projects", "Other", "POGOH")
os.chdir(dirpath)

# read in data
trips_cln = pd.read_csv(os.path.join("data", "processed", "trips_clean.csv"), 
                        dtype={'Closed Status': str})
trips_cln = trips_cln.drop(columns = {"Unnamed: 0"}) 

stns_by_mon = pd.read_csv(os.path.join("data", "processed", "stations_by_month.csv"))
stns_by_mon = stns_by_mon.rename(columns = {"Unnamed: 0":"Date"})


trips_cln["Duration"].describe()

trips_mean = trips_cln["Duration"].mean()
trips_med = trips_cln["Duration"].median()
trips_sd = trips_cln["Duration"].std()


# plot histograms of ride durations
plt.figure()
plt.hist(trips_cln["Duration"], bins=100)
plt.xlabel("Trip Duration")
plt.title("Frequency of Ride Durations, All Trips")
plt.savefig(os.path.join("visualizations", "rides_hist.png"))

# all rides together isn't a v helpful graphic; break up by length of rides
x1 = trips_cln[ trips_cln["Duration"] <= 7200 ]["Duration"]
plt.figure()
plt.hist(x1, bins=100)
plt.xlabel("Trip Duration")
plt.title("Frequency of Trip Durations, Short Trips(<= 2 hrs)")
plt.savefig(os.path.join("visualizations", "short_rides.png"))

x2 = trips_cln[ trips_cln["Duration"] > 7200 ]["Duration"]
plt.figure()
plt.hist(x2, bins=100)
plt.xlabel("Trip Duration")
plt.title("Frequency of Trip Durations, Short Trips(> 2 hrs)")
plt.savefig(os.path.join("visualizations", "long_rides.png"))

x3 = trips_cln[ trips_cln["Duration"] > 86400 ]["Duration"]
plt.figure()
plt.hist(x3, bins=100)
plt.xlabel("Trip Duration")
plt.title("Frequency of Trip Durations, Very Long Trips (> 24 hrs)")
plt.savefig(os.path.join("visualizations", "v_long_rides.png"))





# rides by month
trips_by_month = trips_cln.groupby(["Start Yr-Mon"])["Start Yr-Mon"].size()

x = trips_by_month.index
y = trips_by_month
plt.figure()
plt.plot(x,y)
plt.scatter(x,y)
plt.gca().xaxis.grid(True)
plt.xlabel("Month")
plt.ylabel("Number of Trips")
plt.xticks(np.arange(1,100,step=6),rotation = 90)
plt.title("Total Trips by Month")
plt.savefig(os.path.join("visualizations", "rides_per_month.png"), bbox_inches="tight")


# rides per month by rider type (POGOH only)
trips_pogoh = trips_cln[ trips_cln["Start Yr-Mon"] >= "2022-05" ]
trips_type = trips_pogoh.groupby(['Start Yr-Mon', 'Rider Type'], as_index=False)["Duration"].count()

x = trips_type[ trips_type["Rider Type"] == "CASUAL"]["Start Yr-Mon"]
y_cas = trips_type[ trips_type["Rider Type"] == "CASUAL"]["Duration"]
y_mem = trips_type[ trips_type["Rider Type"] == "MEMBER"]["Duration"]

plt.figure()
plt.plot(x, y_cas, label="Casual")
plt.plot(x, y_mem, label="Member")
plt.xticks(rotation = 90)
plt.legend(loc="upper left")
plt.xlabel("Month")
plt.ylabel("Number of Trips")
plt.title("Number of Trips per Month, by Customer Type")
plt.savefig(os.path.join("visualizations", "rides_by_month_and_ridertype.png"), bbox_inches="tight")




# number of rides by location (sept '23)
trips_sept23 = trips_cln[ trips_cln["Start Yr-Mon"] == "2023-09" ]

trips_loc = trips_sept23.groupby(["Start Station Name"], as_index=False).size()
trips_loc = trips_loc.sort_values(by=['size'], ascending=False)

stns = trips_loc["Start Station Name"]
rentals = trips_loc["size"]

fig, ax = plt.subplots(figsize=(5,10))
ax.barh(stns, rentals)
ax.invert_yaxis()
plt.yticks(fontsize=8)
plt.xlabel("Number of Trips")
plt.ylabel("Start Station Name")
plt.title("Number of Trips by Starting Station, September 2023")
plt.savefig(os.path.join("visualizations", "rides_by_loc_sept23.png"), bbox_inches='tight')

# avg ride duration by location (pogoh only)

trips_loc_dur = trips_sept23.groupby("Start Station Name", 
                                    as_index=False)["Duration"].agg(['mean',
                                                                     'median', 
                                                                     'count'])
trips_loc_dur = trips_loc_dur.sort_values(by = "count", ascending=False)
trips_loc_dur[["mean", "median"]] = trips_loc_dur[["mean", "median"]]/60

fig, ax = plt.subplots(figsize=(5,10))
ax.barh(trips_loc_dur["Start Station Name"], trips_loc_dur["mean"])
ax.invert_yaxis()
plt.yticks(fontsize=8)
plt.xlabel("Mean Trip Duration")
plt.ylabel("Start Station Name")
plt.title("Mean Duration of Trip by Starting Station, September 2023")
plt.savefig(os.path.join("visualizations", "ride_dur_by_loc_sept23.png"))






# number of stations and bikes by month

plt.figure()
plt.plot(stns_by_mon["Date"], stns_by_mon["Station Count"])
plt.xlabel("Month")
plt.ylabel("Total Number of Stations")
plt.xticks(np.arange(1,100,step=6),rotation = 90)
plt.title("Total Trips by Month")

plt.savefig(os.path.join("visualizations", "stations_by_month.png"))

plt.figure()
plt.plot(stns_by_mon["Date"], stns_by_mon["Total Docks"])
plt.xlabel("Month")
plt.ylabel("Total Number of Docks")
plt.xticks(np.arange(1,100,step=6), rotation=90)
plt.savefig(os.path.join("visualizations", "docks_by_month.png"))