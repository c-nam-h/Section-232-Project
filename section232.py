import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By


options = webdriver.ChromeOptions()
options.add_argument("--ignore-certificate-errors")
options.add_argument("--incognito")
# options.add_argument("--headless") # runs the Chrome without opening a browser window
driver = webdriver.Chrome("/usr/lib/chromium-browser/chromdriver", chrome_options = options)

url = "https://232app.azurewebsites.net/steelalum"
driver.get(url)
time.sleep(3)



show_entries = driver.find_element(By.NAME, "erdashboard_length")
show_entries.send_keys("100")
time.sleep(3)
page_source = driver.page_source


soup = BeautifulSoup(page_source, "lxml")

record_selector = soup.find_all("tbody")
print(record_selector)
# for record in record_selector:
#     print(record)
