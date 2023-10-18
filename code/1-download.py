# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 21:33:27 2023

"""

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import requests
import os

datapath = os.path.join("C:", os.sep, "Users", "Allie", "Projects", "Other", 
                        "POGOH", "data", "raw")

driver = webdriver.Chrome(ChromeDriverManager().install())


### DOWNLOAD POGOH DATA ###
url = "https://data.wprdc.org/dataset/pogoh-trip-data"

driver.get(url)

html = driver.page_source
#driver.close()

soup = BeautifulSoup(html)

start_of_url = "https://data.wprdc.org/dataset/"

all_download_links = [link["href"] for link in soup.find_all("a") if link["href"].startswith(start_of_url)]
len(all_download_links) == 17

for link in all_download_links:
    response = requests.get(link)
    filename = link.split("/")[-1]
    filename = os.path.join(datapath, "pogoh", filename)
    print(filename)
    with open(filename, "wb") as f:
        f.write(response.content)
        #f.close()
        
        
        
### DOWNLOAD HEALTHY-RIDE DATA ###
url = "https://data.wprdc.org/dataset/healthyride-trip-data"

driver.get(url)

html = driver.page_source
#driver.close()

soup = BeautifulSoup(html)

start_of_url = "https://data.wprdc.org/dataset/"

all_download_links = [link["href"] for link in soup.find_all("a") if link["href"].startswith(start_of_url)]
len(all_download_links) == 17

for link in all_download_links:
    response = requests.get(link)
    filename = link.split("/")[-1]
    filename = os.path.join(datapath, "healthyride", filename)
    print(filename)
    with open(filename, "wb") as f:
        f.write(response.content)
        #f.close()
        
#os.remove("C:/Users/Allie/Projects/Other/POGOH/downloads/healthyride/healthyriderentalsdatadictionary.csv")      



### DOWNLOAD POGOH STATION DATA ###
url = "https://data.wprdc.org/dataset/station-locations"

driver.get(url)

html = driver.page_source

soup = BeautifulSoup(html)

start_of_url = "https://data.wprdc.org/dataset/"

all_download_links = [link["href"] for link in soup.find_all("a") if link["href"].startswith(start_of_url)]
len(all_download_links) == 5

for link in all_download_links:
    response = requests.get(link)
    filename = link.split("/")[-1]
    filename = os.path.join(datapath, "pogoh_stations", filename)
    print(filename)
    with open(filename, "wb") as f:
        f.write(response.content)



### DOWNLOAD HEALTHY RIDE STATION DATA ###
url = "https://data.wprdc.org/dataset/healthyride-stations"

driver.get(url)

html = driver.page_source

soup = BeautifulSoup(html)

start_of_url = "https://data.wprdc.org/dataset/"

all_download_links = [link["href"] for link in soup.find_all("a") if link["href"].startswith(start_of_url)]
len(all_download_links) == 20

for link in all_download_links:
    response = requests.get(link)
    filename = link.split("/")[-1]
    filename = os.path.join(datapath, "healthyride_stations", filename)
    print(filename)
    with open(filename, "wb") as f:
        f.write(response.content)



driver.close()
