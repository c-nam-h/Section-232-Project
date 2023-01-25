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
time.sleep(4)

show_entries = driver.find_element(By.NAME, "erdashboard_length")
show_entries.send_keys("100")
time.sleep(4)



# page = requests.get(url)

# soup = BeautifulSoup(page.content, "html.parser")

# print(soup.prettify())
