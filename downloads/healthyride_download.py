# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 21:41:53 2023

"""

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import requests
import os

dirpath = os.path.join("C:", os.sep, "Users", "Allie", "Projects", "Other", "POGOH", "downloads")

url = "https://data.wprdc.org/dataset/healthyride-trip-data"

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(url)

html = driver.page_source
driver.close()

soup = BeautifulSoup(html)

start_of_url = "https://data.wprdc.org/dataset/"

all_download_links = [link["href"] for link in soup.find_all("a") if link["href"].startswith(start_of_url)]
len(all_download_links) == 17

for link in all_download_links:
    response = requests.get(link)
    filename = link.split("/")[-1]
    filename = os.path.join(dirpath, "healthyride", filename)
    print(filename)
    with open(filename, "wb") as f:
        f.write(response.content)
        #f.close()
        
os.remove("C:/Users/Allie/Projects/Other/POGOH/downloads/healthyride/healthyriderentalsdatadictionary.csv")      

