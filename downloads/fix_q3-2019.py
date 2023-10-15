# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 00:43:36 2023

@author: Allie
"""

import os
import pandas as pd

#dirpath = "C:/Users/Allie/Projects/Other/POGOH"
dirpath = os.path.join("C:", os.sep, "Users", "Allie", "Projects", "Other", "POGOH")
os.chdir(dirpath)

df = pd.read_csv(os.path.join("downloads","healthyride", "healthy-ride-rentals-2019-q3.csv"),
                 dtype = 'unicode')


# remove empty rows
missing_duration = df[ df["Tripduration"].isnull() ]
df = df.drop(missing_duration.index, axis = 0)

len(df)

df.to_csv(os.path.join("downloads", "healthyride", "healthy-ride-rentals-2019-q3.csv"))
