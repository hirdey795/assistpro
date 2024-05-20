# importing necessary packages 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

"""
XPath Cheat Sheet = "https://quickref.me/xpath"
Assist.org = "https://assist.org"
Extra websites = " "
"""

# for holding the resultant list 
page_url = "https://assist.org"
options = Options()
options.add_experimental_option("detach", True) # So browser don't close prematurely
driver = webdriver.Chrome(options=options)
driver.get(page_url)