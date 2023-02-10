import requests
import time
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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
time.sleep(3) # waits for the page to reload when the filter is updated to show 100 entries
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


# to keep track of numbers of records and pages in the website
count = 0
page = 0


# loops through the table rows and append the data to the dictionary until the next button is disabled
while True:
    page += 1

    # waits until the table elements are visible when the page is loaded
    # this is a must step for Selenium to scrap data from the dynamic table when we navigate through different pages
    tr = WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.XPATH, "//table[@id='erdashboard']/tbody//tr")))

    for record in tr:
        count += 1

        posted_date = datetime.strptime(record.find_element(By.XPATH, './td[7]').text, "%m/%d/%Y").date()

        exclusion_request_dict["ID"].append(int(record.find_element(By.XPATH, './td[1]').text))
        exclusion_request_dict["Company"].append(record.find_element(By.XPATH, './td[2]').text)
        exclusion_request_dict["Product"].append(record.find_element(By.XPATH, './td[3]').text)
        exclusion_request_dict["HTSUSCode"].append(record.find_element(By.XPATH, './td[4]').text)
        exclusion_request_dict["Status"].append(record.find_element(By.XPATH, './td[5]').text)
        exclusion_request_dict["Days Remaining"].append(int(record.find_element(By.XPATH, './td[6]').text))
        exclusion_request_dict["Posted Date"].append(posted_date)
        exclusion_request_dict["Details"].append(record.find_element(By.XPATH, './td[8]').text)
    
    next_button = driver.find_element(By.ID, "erdashboard_next")
    next_button_clickable = driver.find_element(By.ID, "erdashboard_next").get_attribute("class").split(" ")
    print(next_button_clickable)
    print(count, page)
    if next_button_clickable[-1] == "disabled":
        break

    print(exclusion_request_dict)
    next_button.click() # goes to the next page
    time.sleep(3)


    # date = datetime.strptime(tr_data[6].string, "%m/%d/%Y").date()

    # exclusion_request_dict["ID"].append(int(tr_data[0].string))
    # exclusion_request_dict["Company"].append(tr_data[1].string)
    # exclusion_request_dict["Product"].append(tr_data[2].string)
    # exclusion_request_dict["HTSUSCode"].append(tr_data[3].string)
    # exclusion_request_dict["Status"].append(tr_data[4].string)
    # exclusion_request_dict["Days Remaining"].append(int(tr_data[5].string))
    # exclusion_request_dict["Posted Date"].append(date)
    # exclusion_request_dict["Details"].append(tr_data[7].string)





driver.quit()