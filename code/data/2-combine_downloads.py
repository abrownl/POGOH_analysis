# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 21:11:46 2023
"""

import os
import pandas as pd

#dirpath = "C:/Users/Allie/Projects/Other/POGOH"
toplevel_dir = os.path.join("C:", os.sep, "Users", "Allie", "Projects", "Other",
                            "POGOH")
os.chdir(toplevel_dir)


### First: remove thousands of empty rows from 2019 q3 data
df = pd.read_csv(os.path.join("data", "raw", "healthyride", "healthy-ride-rentals-2019-q3.csv"),
                 dtype = 'unicode')

missing_duration = df[ df["Tripduration"].isnull() ]
df = df.drop(missing_duration.index, axis = 0)

df.to_csv(os.path.join("data", "raw", "healthyride", "healthy-ride-rentals-2019-q3.csv"))



### Combine all POGOH and healthy-ride trip data
# loop through files & load into dataframes; store dataframes as list
trip_frames = []

# loop through pogoh files
for filename in os.listdir(os.path.join("data", "raw", "pogoh")):
    if filename.endswith(".xlsx"):
        print(filename)
        df = pd.read_excel(os.path.join("data", "raw", "pogoh",filename))
    elif filename.endswith(".csv"):
        print(filename)
        df = pd.read_csv(os.path.join("data", "raw", "pogoh",filename))
    # convert date columns to datetime for consistency
    df["Start Date"] = pd.to_datetime( df["Start Date"] )
    df["End Date"] = pd.to_datetime( df["End Date"])
    #add dataframe to list of dataframes
    trip_frames.append(df)
    

# loop through healthy-ride files
for filename in os.listdir(os.path.join("data", "raw", "healthyride")):
    if filename.endswith(".xlsx"):
        print(filename)
        df = pd.read_excel(os.path.join("data", "raw", "healthyride", filename))
    elif filename.endswith(".csv"):
        print(filename)
        df = pd.read_csv(os.path.join("data", "raw", "healthyride", filename))    
    # rename columns to match with pogoh data
    df = df.rename(columns = {"starttime":"Start Date", "stoptime":"End Date", 
                              "tripduration":"Duration", 
                              "from_station_id":"Start Station Id", 
                              "from_station_name":"Start Station Name",
                              "to_station_id":"End Station Id", 
                              "to_station_name":"End Station Name",
                              "usertype":"Rider Type"})
    df = df.rename(columns = {"Trip id":"trip_id", "Starttime":"Start Date", 
                              "Stoptime":"End Date",
                              "Bikeid":"bikeid", "Tripduration":"Duration",
                              "From station id":"Start Station Id",
                              "From station name":"Start Station Name",
                              "To station id":"End Station Id",
                              "To station name":"End Station Name",
                              "Usertype":"Rider Type" })   
    # convert date columns to datetime for consistency     
    df["Start Date"] = pd.to_datetime( df["Start Date"] )
    df["End Date"] = pd.to_datetime( df["End Date"])
    #add dataframe to list of dataframes
    trip_frames.append(df)

# concatenate all trip dataframes together
trip_data = pd.concat(trip_frames, ignore_index = True)

trip_data = trip_data.drop(columns = ["Unnamed: 0.1", "Unnamed: 0"])

# save
trip_data.to_csv(os.path.join("data", "processed", "pogoh_combined.csv"))
print("Saved: /data/processed/pogoh_combined.csv")



### Combine POGOH Station data for all years
stn_frames = []

for filename in os.listdir(os.path.join("data", "raw", "pogoh_stations")):
    print(filename)
    df = pd.read_excel(os.path.join("data", "raw", "pogoh_stations", filename))
    # add month & year to each file before combining
    name = os.path.splitext(filename)[0]
    date = " ".join(name.split("-")[3:5])
    df["Date"] = date
    df["Date"] = pd.to_datetime(df["Date"]).dt.to_period('M')
    # add to list of dataframes
    stn_frames.append(df)
    
# concatenate all frames in list together
stn_data = pd.concat(stn_frames, ignore_index = True)

# save
stn_data.to_csv(os.path.join("data", "processed", "stations.csv"))
print("Saved: /data/processed/stations.csv")