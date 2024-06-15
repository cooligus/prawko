import os
import time 
import json
from collections import defaultdict
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options


load_dotenv()

firefox_services = Service(executable_path='/usr/local/bin/geckodriver', port=3000, service_args=['--marionette-port', '2828', '--connect-existing'])
driver = webdriver.Firefox(service=firefox_services)

driver.get(os.getenv('WEBSITE'))
elements = driver.find_element(By.ID, "nauka").find_elements(By.CLASS_NAME, "list-row")

sections = []
for element in elements:
    section = {}
    section['href']=element.find_element(By.CLASS_NAME, "btn-half-blue").get_attribute("href")
    section['name']=element.find_element(By.CLASS_NAME, "col1").get_attribute("innerHTML")
    sections.append(section)

fileName = "tmp/sections.json"
f = open(fileName, "w")
f.write(json.dumps(sections))
f.close()
