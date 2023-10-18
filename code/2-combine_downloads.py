# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 21:11:46 2023
"""

import os
import pandas as pd

#dirpath = "C:/Users/Allie/Projects/Other/POGOH"
toplevel_dir = os.path.join("C:", os.sep, "Users", "Allie", "Projects", "Other",
                            "POGOH", "data")
os.chdir(toplevel_dir)



##### Combine all POGOH and healthy-ride trip data #####

### First: remove thousands of empty rows from 2019 q3 data
df = pd.read_csv(os.path.join("raw", "healthyride", "healthy-ride-rentals-2019-q3.csv"),
                 dtype = 'unicode')

missing_duration = df[ df["Tripduration"].isnull() ]
df = df.drop(missing_duration.index, axis = 0)

# save in processed data directory
df.to_csv(os.path.join("processed", "healthy-ride-rentals-2019-q3.csv"))


### Loop through trip files & load into dataframes; store dataframes as list
trip_frames = []

# loop through pogoh files
for filename in os.listdir(os.path.join("raw", "pogoh")):
    print(filename)
    if filename.endswith(".xlsx"):
        df = pd.read_excel(os.path.join("raw", "pogoh",filename))
    elif filename.endswith(".csv"):
        df = pd.read_csv(os.path.join("raw", "pogoh",filename))
    # convert date columns to datetime for consistency
    df["Start Date"] = pd.to_datetime( df["Start Date"] )
    df["End Date"] = pd.to_datetime( df["End Date"])
    #add dataframe to list of dataframes
    trip_frames.append(df)
    
# loop through healthy-ride files
for filename in os.listdir(os.path.join("raw", "healthyride")):
    print(filename)
    # load fixed, not raw, version of 2019 q3 file
    if filename == "healthy-ride-rentals-2019-q3.csv":
        df = pd.read_csv(os.path.join("processed", filename))
    elif filename.endswith(".xlsx"):
        df = pd.read_excel(os.path.join("raw", "healthyride", filename))
    elif filename.endswith(".csv"):
        df = pd.read_csv(os.path.join("raw", "healthyride", filename))    
    # rename columns to match with pogoh data
    df = df.rename(columns = {"starttime":"Start Date", "stoptime":"End Date", 
                              "tripduration":"Duration", 
                              "from_station_id":"Start Station Id", 
                              "from_station_name":"Start Station Name",
                              "to_station_id":"End Station Id", 
                              "to_station_name":"End Station Name",
                              "usertype":"Rider Type",
                              "Trip id":"trip_id", "Starttime":"Start Date", 
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
trip_data.to_csv(os.path.join("processed", "trips_combined.csv"))
print("Saved: /data/processed/pogoh_combined.csv")




##### Combine station data for all years #####

### First, put 2021 q2 data in format to match other files
df = pd.read_csv(os.path.join("raw", "healthyride_stations", "healthy-ride-station-2021-q2.csv"))

# drop rows that aren't for standard bike locations
bad_location = df[ df["Place type"] != "Standard place"]
df = df.drop(bad_location.index, axis = 0)

# drop unnec columns
df = df[["Place name", "Station number", "Bike racks"]]

# rename to match other files
df = df.rename(columns = {"Place name":"Name",
                          "Station number":"Id",
                          "Bike racks":"Total Docks"})

# save in processed data directory
df.to_csv(os.path.join("processed", "healthy-ride-station-2021-q2.csv"))


### Loop through station files & load into dataframes; store dataframes as list
stn_frames = []

# loop through POGOH stations files
for filename in os.listdir(os.path.join("raw", "pogoh_stations")):
    print(filename)
    df = pd.read_excel(os.path.join("raw", "pogoh_stations", filename))
    # add month & year to each file before combining
    name = os.path.splitext(filename)[0]
    date = " ".join(name.split("-")[3:5])
    df["Date"] = date
    df["Date"] = pd.to_datetime(df["Date"], format="%B %Y").dt.to_period('M')
    # add to list of dataframes
    stn_frames.append(df)

# loop through healthyride stations files

# first, a function to translate quarter to month
def q_to_mon(q):
    mon = (int(q) - 1)*3 + 1
    return str(mon)

for filename in os.listdir(os.path.join("raw", "healthyride_stations")):
    print(filename)
    
    # load file into dataframe (load processed, not raw, version of 2021 q2 data):
    if filename == "healthy-ride-station-2021-q2.csv":
        df = pd.read_csv(os.path.join("processed", filename))
    else:
        df = pd.read_csv(os.path.join("raw", "healthyride_stations", filename))
        
    # rename columns where nec
    df = df.rename(columns = {"Station Name":"Name",
                              "StationName":"Name",
                              "Station #":"Id",
                              "StationNum":"Id",
                              "# of Racks":"Total Docks",
                              "RackQnty":"Total Docks"})
    
    # extract year & month from filename
    if filename in ("healthyridestations2015.csv", "healthyridestations2016.csv",
                    "healthyridestations2017.csv"):
        year = filename[-8:-4]
        date = " ".join([year, "1"])
    elif filename in ("healthy-ride-station-locations-q3-2019.csv",
                      "healthy-ride-station-locations-q3-2021.csv",
                      "healthy-ride-station-locations-q4-2021.csv"):
        year = filename[-8:-4]
        month = q_to_mon(filename[-10])
        date = " ".join([year, month])
    else:
        year = filename[-11:-7]
        month = q_to_mon(filename[-5])
        date = " ".join([year, month])
        
    # add date column to dataframe
    df["Date"] = date
    df["Date"] = pd.to_datetime(df["Date"], format="%Y %m").dt.to_period('M')

    # add dataframe to stations data list
    stn_frames.append(df)

    
# concatenate all frames in list together
stn_data = pd.concat(stn_frames, ignore_index = True)

stn_data = stn_data.drop(columns = ["Unnamed: 0", "Unnamed: 5", "Unnamed: 6"])

# save
stn_data.to_csv(os.path.join("processed", "stations_combined.csv"))
print("Saved: /data/processed/stations_combined.csv")