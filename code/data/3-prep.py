# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 01:20:04 2023

@author: Allie
"""

import os
import pandas as pd

dirpath = os.path.join("C:", os.sep, "Users", "Allie", "Projects", "Other", "POGOH")
os.chdir(dirpath)


# read in trip data
trip_data = pd.read_csv(os.path.join("data", "processed", "pogoh_combined.csv"), 
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

# save
trip_data.to_csv(os.path.join("data", "processed", "pogoh_prepped.csv"))
print("Saved: pogoh_prepped.csv")


