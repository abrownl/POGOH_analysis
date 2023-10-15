# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 21:11:46 2023
"""

import os
import pandas as pd

#dirpath = "C:/Users/Allie/Projects/Other/POGOH"
dirpath = os.path.join("C:", os.sep, "Users", "Allie", "Projects", "Other", "POGOH")
os.chdir(dirpath)


# loop through files & load into dataframes; store dataframes as list
frames = []
#numrows = 0

for filename in os.listdir(os.path.join("downloads","pogoh")):
    if filename.endswith(".xlsx"):
        print(filename)
        df = pd.read_excel(os.path.join("downloads","pogoh",filename))
    elif filename.endswith(".csv"):
        print(filename)
        df = pd.read_csv(os.path.join("downloads","pogoh",filename))
    df["Start Date"] = pd.to_datetime( df["Start Date"] )
    df["End Date"] = pd.to_datetime( df["End Date"])
    frames.append(df)
    #numrows = numrows + len(df)    


for filename in os.listdir(os.path.join("downloads","healthyride")):
    if filename.endswith(".xlsx"):
        print(filename)
        df = pd.read_excel(os.path.join("downloads","healthyride", filename))
    elif filename.endswith(".csv"):
        print(filename)
        df = pd.read_csv(os.path.join("downloads","healthyride", filename))    
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
    df["Start Date"] = pd.to_datetime( df["Start Date"] )
    df["End Date"] = pd.to_datetime( df["End Date"])
    frames.append(df)
    #numrows = numrows + len(df)
    #print("Numrows: ", len(df))
    

# concatenate all the dataframes together
data = pd.concat(frames, ignore_index = True)

data = data.drop(columns = ["Unnamed: 0.1", "Unnamed: 0"])

# save
data.to_csv("pogoh_combined.csv")
print("Saved: pogoh_combined.csv")