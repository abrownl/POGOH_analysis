# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 01:20:04 2023

@author: Allie
"""

import os
import pandas as pd

dirpath = os.path.join("C:", os.sep, "Users", "Allie", "Projects", "Other", "POGOH")
os.chdir(dirpath)

data = pd.read_csv(os.path.join(dirpath, "pogoh_combined.csv"), dtype={'Closed Status': str})
data["Start Date"] = pd.to_datetime(data["Start Date"])
data["End Date"] = pd.to_datetime(data["End Date"])

# sort oldest to newest
data = data.sort_values(by=["Start Date", "End Date"])

# pull out year, month, day, hour
data["Start Year"] = data["Start Date"].dt.year
data["Start Month"] = data["Start Date"].dt.month
data["Start Yr-Mon"] = data["Start Date"].dt.to_period('M')
data["Start Day"] = data["Start Date"].dt.day
data["Start Hour"] = data["Start Date"].dt.hour

# Duration only gives time in seconds
data["Duration_Min"] = data["Duration"]/60
data["Duration_Min_Rd"] = data["Duration_Min"].round()
data["Duration_Hr"] = data["Duration_Min"]/60
data["Duration_Hr_Rd"] = data["Duration_Hr"].round()

data = data.drop(columns = {"Unnamed: 0"})


# save
data.to_csv("pogoh_prepped.csv")
print("Saved: pogoh_prepped.csv")