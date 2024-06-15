import os
import json
from dotenv import load_dotenv
from selenium.webdriver.common.by import By


def get_sections(driver):
    load_dotenv()
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
