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




# plot histograms of ride durations
fig, ax = plt.subplots()
ax.hist(trips_cln["Duration"]/60, bins=100)
ax.set_xlabel("Trip Duration (min)")
ax.set_title("Frequency of Ride Durations, All Trips")
fig.savefig(os.path.join("visualizations", "rides_hist.png"))

# all rides together isn't a v helpful graphic; break up by length of rides
x0 = trips_cln[ trips_cln["Duration"] <= 3600 ]["Duration"]/60
fig, ax = plt.subplots()
ax.hist(x0, bins=100)
ax.set_xlabel("Trip Duration (min)")
ax.set_title("Frequency of Trip Duration, Short Trips (< 1 hr)")
fig.savefig(os.path.join("visualizations", "very_short_rides.png"))

x1 = trips_cln[ trips_cln["Duration"] <= 7200 ]["Duration"]/60
fig, ax = plt.subplots()
ax.hist(x1, bins=100)
ax.set_xlabel("Trip Duration (min)")
ax.set_title("Frequency of Trip Durations, Short Trips (<= 2 hrs)")
fig.savefig(os.path.join("visualizations", "short_rides.png"))

x2 = trips_cln[ trips_cln["Duration"] > 7200 ]["Duration"]/60
fig, ax = plt.subplots()
ax.hist(x2, bins=100)
ax.set_xlabel("Trip Duration (min)")
ax.set_title("Frequency of Trip Durations, Long Trips(> 2 hrs)")
fig.savefig(os.path.join("visualizations", "long_rides.png"))

x3 = trips_cln[ trips_cln["Duration"] > 86400 ]["Duration"]/60
fig, ax = plt.subplots()
ax.hist(x3, bins=100)
ax.set_xlabel("Trip Duration (min)")
ax.set_title("Frequency of Trip Durations, Very Long Trips (> 24 hrs)")
fig.savefig(os.path.join("visualizations", "v_long_rides.png"))





# rides by month
trips_by_month = trips_cln.groupby(["Start Yr-Mon"])["Start Yr-Mon"].size()

x = trips_by_month.index
y = trips_by_month
labels = trips_by_month.index[np.arange(1,100,6)]

fig, ax = plt.subplots()
ax.plot(x,y)
ax.scatter(x,y)
ax.set_xticks(np.arange(1,100,step=6))
ax.set_xticklabels(labels, rotation=90)
ax.xaxis.grid(True)
ax.set_xlabel("Month")
ax.set_ylabel("Number of Trips")
ax.set_title("Total Trips by Month")
plt.savefig(os.path.join("visualizations", "rides_per_month.png"), bbox_inches="tight")


# rides per month by rider type (POGOH only)
trips_pogoh = trips_cln[ trips_cln["Start Yr-Mon"] >= "2022-05" ]
trips_type = trips_pogoh.groupby(['Start Yr-Mon', 'Rider Type'], as_index=False)["Duration"].count()

x = trips_type[ trips_type["Rider Type"] == "CASUAL"]["Start Yr-Mon"]
y_cas = trips_type[ trips_type["Rider Type"] == "CASUAL"]["Duration"]
y_mem = trips_type[ trips_type["Rider Type"] == "MEMBER"]["Duration"]

fig, ax = plt.subplots()
ax.plot(x, y_cas, label="Casual")
ax.plot(x, y_mem, label="Member")
ax.set_xticklabels(x, rotation=90)
ax.legend(loc="upper left")
ax.set_xlabel("Month")
ax.set_ylabel("Number of Trips")
ax.set_title("Number of Trips per Month, by Customer Type")
fig.savefig(os.path.join("visualizations", "rides_by_month_and_ridertype.png"), bbox_inches="tight")




# number of rides by location (sept '23)
trips_sept23 = trips_cln[ trips_cln["Start Yr-Mon"] == "2023-09" ]

trips_loc = trips_sept23.groupby(["Start Station Name"], as_index=False).size()
trips_loc = trips_loc.sort_values(by=['size'], ascending=False)

stns = trips_loc["Start Station Name"]
rentals = trips_loc["size"]

fig, ax = plt.subplots(figsize=(5,10))
ax.barh(stns, rentals)
ax.invert_yaxis()
ax.set_xlabel("Number of Trips")
ax.set_ylabel("Start Station Name")
plt.yticks(fontsize=8)
ax.set_title("Number of Trips by Starting Station, September 2023")
fig.savefig(os.path.join("visualizations", "rides_by_loc_sept23.png"), bbox_inches='tight')

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
ax.set_xlabel("Mean Trip Duration (min)")
ax.set_ylabel("Start Station Name")
plt.yticks(fontsize=8)
ax.set_title("Mean Duration of Trip by Starting Station, September 2023")
plt.savefig(os.path.join("visualizations", "ride_dur_by_loc_sept23.png"), bbox_inches="tight")




# number of stations and bikes by month
stns_by_month = pd.read_csv(os.path.join("data", "processed", "stations_by_month.csv"))
stns_by_month = stns_by_month.rename(columns = {"Unnamed: 0":"Date"})

labels = stns_by_month["Date"][np.arange(1,100,6)]

fig, ax = plt.subplots()
ax.plot(stns_by_month["Date"], stns_by_month["Station Count"])
ax.set_xlabel("Month")
ax.set_ylabel("Total Number of Stations")
ax.set_ylim(bottom = 0)
ax.set_xticks(np.arange(1,100,step=6))
ax.set_xticklabels(labels, rotation=90)
ax.set_title("Total Stations by Month")
plt.savefig(os.path.join("visualizations", "stations_by_month.png"), bbox_inches="tight")

fig, ax = plt.subplots()
ax.plot(stns_by_month["Date"], stns_by_month["Total Docks"])
ax.set_xlabel("Month")
ax.set_ylabel("Total Number of Docks")
ax.set_ylim(bottom = 0)
ax.set_xticks(np.arange(1,100,step=6))
ax.set_xticklabels(labels, rotation=90)
ax.set_title("Total Bike Docks by Month")
plt.savefig(os.path.join("visualizations", "docks_by_month.png"), bbox_inches="tight")




# trips AND stations by month
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
ax1.plot(stns_by_month["Date"], stns_by_month["Station Count"], color="orange")
ax2.plot(stns_by_month["Date"], trips_by_month, color="royalblue")
plt.xticks(np.arange(1, 100, step=6))
ax1.set_xticklabels(stns_by_month["Date"][np.arange(1,100,6)], rotation=90)
ax1.set_ylabel("Total Stations", color="orange")
ax1.set_ylim(bottom = 0)
ax2.set_ylabel("Total Trips", color="royalblue")
plt.title("Trips and Stations by Month")
plt.savefig(os.path.join("visualizations","stns_and_trips_by_month.png"),
            bbox_inches="tight")

# trips and DOCKS by month
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
ax1.plot(stns_by_month["Date"], stns_by_month["Total Docks"], color="orange")
ax2.plot(stns_by_month["Date"], trips_by_month, color="royalblue")
plt.xticks(np.arange(1, 100, step=6))
ax1.set_xticklabels(stns_by_month["Date"][np.arange(1,100,6)], rotation=90)
ax1.set_ylabel("Total Docks", color="orange")
ax1.set_ylim(bottom = 0)
ax2.set_ylabel("Total Trips", color="royalblue")
plt.title("Number of Trips and Number of Bike Docks by Month")
plt.savefig(os.path.join("visualizations","docks_and_trips_by_month.png"),
            bbox_inches="tight")

