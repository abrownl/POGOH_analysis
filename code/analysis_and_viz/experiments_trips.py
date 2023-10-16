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

# read in trip data
data = pd.read_csv(os.path.join(dirpath, "pogoh_prepped.csv"), dtype={'Closed Status': str})
data = data.drop(columns = {"Unnamed: 0"}) 

# drop interactions less than/eq to 1 min or with unusual Closed Status
drop_index = data[ ((data["Duration"] < 60) |
                    (data["Closed Status"] == "GRACE_PERIOD") |   #grace period: returned within <60 sec
                    (data["Closed Status"] == "TERMINATED") |
                    (data["Closed Status"] == "FORCED_CLOSED")) ].index  
rides = data.drop(drop_index)

#%% 

# scatterplots of ride durations
for yr in range(2015, 2024):
    filename = "ride_dur_" + str(yr) + ".png"
    
    x = rides[ rides["Start Year"] == yr ]["Start Month"]
    y = rides[ rides["Start Year"] == yr ]["Duration"]
    
    plt.figure()
    plt.scatter(x,y)
    plt.axhline(y=200000, color="r")
    plt.savefig(os.path.join(dirpath, "figures", filename))  

    
# 200K looks like a good max cutoff?
# no, 175K better
plt.figure()
plt.hist(rides[rides["Duration"] > 175000]["Duration"], bins=100)
plt.savefig(os.path.join(dirpath, "figures", "rides_over_175K.png"))

drop_index = rides[ rides["Duration"] > 175000 ].index
rides_cln = rides.drop(drop_index)


# plot histograms of ride durations
plt.figure()
plt.hist(rides_cln["Duration"], bins=100)
plt.savefig(os.path.join(dirpath, "figures", "rides_hist.png"))

# all rides together isn't a v helpful graphic; break up by length of rides
x1 = rides_cln[ rides_cln["Duration"] <= 7200 ]["Duration"]
plt.figure()
plt.hist(x1, bins=100)
plt.savefig(os.path.join(dirpath, "figures", "short_rides.png"))

x2 = rides_cln[ rides_cln["Duration"] > 7200 ]["Duration"]
plt.figure()
plt.hist(x2, bins=100)
plt.savefig(os.path.join(dirpath, "figures", "long_rides.png"))

x3 = rides_cln[ rides_cln["Duration"] > 100000 ]["Duration"]
plt.figure()
plt.hist(x3, bins=100)
plt.savefig(os.path.join(dirpath, "figures", "v_long_rides.png"))



rides_cln["Duration"].describe()

rides_mean = rides_cln["Duration"].mean()
rides_med = rides_cln["Duration"].median()
rides_sd = rides_cln["Duration"].std()


#%%

# rides by month
rides_by_month = rides_cln.groupby(["Start Yr-Mon"])["Start Yr-Mon"].size()

x = rides_by_month.index
y = rides_by_month
plt.figure()
plt.plot(x,y)
plt.scatter(x,y)
plt.gca().xaxis.grid(True)
plt.ylabel("Number of Rides")
plt.xticks(np.arange(1,100,step=6),rotation = 90)
plt.title("POGOH Rides by Month")
plt.savefig(os.path.join(dirpath, "figures", "rides_per_month.png"), bbox_inches="tight")


# rides per month by rider type (POGOH only)
rides_pogoh = rides_cln[ rides_cln["Start Yr-Mon"] >= "2022-05" ]
rides_type = rides_pogoh.groupby(['Start Yr-Mon', 'Rider Type'], as_index=False)["Duration"].count()

x = rides_type[ rides_type["Rider Type"] == "CASUAL"]["Start Yr-Mon"]
y_cas = rides_type[ rides_type["Rider Type"] == "CASUAL"]["Duration"]
y_mem = rides_type[ rides_type["Rider Type"] == "MEMBER"]["Duration"]

plt.figure()
plt.plot(x, y_cas, label="Casual")
plt.plot(x, y_mem, label="Member")
plt.xticks(rotation = 90)
plt.legend(loc="upper left")
plt.savefig(os.path.join(dirpath, "figures", "rides_by_month_and_ridertype.png"), bbox_inches="tight")


#%%

# number of rides by location (sept '23)
rides_sept23 = rides_cln[ rides_cln["Start Yr-Mon"] == "2023-09" ]

rides_loc = rides_sept23.groupby(["Start Station Name"], as_index=False).size()
rides_loc = rides_loc.sort_values(by=['size'], ascending=False)

stns = rides_loc["Start Station Name"]
rentals = rides_loc["size"]

fig, ax = plt.subplots(figsize=(5,10))
ax.barh(stns, rentals)
ax.invert_yaxis()
plt.yticks(fontsize=8)
plt.savefig(os.path.join(dirpath, "figures", "rides_by_loc_sept23.png"), bbox_inches='tight')

# avg ride duration by location (pogoh only)

rides_loc_dur = rides_pogoh.groupby("Start Station Name")["Duration"].agg(['mean','median'])
rides_loc_dur[["mean", "median"]] = rides_loc_dur[["mean", "median"]]/60
rides_loc_dur = rides_loc_dur.sort_values(by = "median")
