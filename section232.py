import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from datetime import datetime


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
page_source = driver.page_source # gets the page source with 100 entries, which we will use in BeuatifulSoup

soup = BeautifulSoup(page_source, "lxml")

# retrieves the column names from the table and append them to list
column_names = []
th = soup.find_all("thead")[0].find_all("th")
for each in th:
    column_names.append(each.text.strip())
print(column_names)

# creates an empty dictionry with keys from the extracted column names
exclusion_request_dict = dict.fromkeys(column_names)

# initialize exclusion_request_dict with each column to be an empty list
for each in column_names:
    exclusion_request_dict[each] = []

# print(exclusion_request_dict)

# finds all rows in the table
tr = soup.find_all("tbody")[0].find_all("tr")

# loops through the rows and append the data to the dictionary
count = 0
for record in tr:
    count += 1
    tr_data = record.find_all("td")
    # print(count, tr_data)

    date = datetime.strptime(tr_data[6].string, "%m/%d/%Y").date()

    exclusion_request_dict["ID"].append(int(tr_data[0].string))
    exclusion_request_dict["Company"].append(tr_data[1].string)
    exclusion_request_dict["Product"].append(tr_data[2].string)
    exclusion_request_dict["HTSUSCode"].append(tr_data[3].string)
    exclusion_request_dict["Status"].append(tr_data[4].string)
    exclusion_request_dict["Days Remaining"].append(int(tr_data[5].string))
    exclusion_request_dict["Posted Date"].append(date)
    exclusion_request_dict["Details"].append(tr_data[7].string)


# page = soup.find("div", id = "erdashboard_paginate")
# page_links = page.find_all("span")[0].find_all("a")
# print(page_links[0])
# page_links[0]

page_div = driver.find_element(By.ID, "erdashboard_paginate")
page_span = page_div.find_element(By.TAG_NAME, "span")
page_links = page_span.find_element(By.TAG_NAME, "a")

driver.find_element(By.XPATH, "//a[text()='2']").click()
time.sleep(5)
