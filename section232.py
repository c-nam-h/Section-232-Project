import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd


options = webdriver.ChromeOptions()
options.add_argument("--ignore-certificate-errors")
options.add_argument("--incognito")
# options.add_argument("--headless") # runs the Chrome without opening a browser window
driver = webdriver.Chrome("/usr/lib/chromium-browser/chromdriver", chrome_options = options)

url = "https://232app.azurewebsites.net/steelalum"
driver.get(url)
time.sleep(2)


# locates the filter and updates the unmber of entries to show to 100
show_entries = driver.find_element(By.NAME, "erdashboard_length")
show_entries.send_keys("100")
time.sleep(2) # waits for the page to reload when the filter is updated to show 100 entries
page_source = driver.page_source # gets the page with 100 entries, which we will use in BeuatifulSoup

soup = BeautifulSoup(page_source, "lxml")

# retrieves the column names from the table and append them to list
column_names = []
th = soup.find_all("thead")[0].find_all("th")
for each in th:
    column_names.append(each.text.strip())
print(column_names)


tr = soup.find_all("tbody")[0].find_all("tr")

# count = 0
# for record in tr:
#     count += 1
#     print(count, record)
