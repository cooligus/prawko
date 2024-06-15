import sections
import questions
import images
import json
import ankize
import os
from selenium import webdriver
from selenium.webdriver.firefox.service import Service

try:
    os.mkdir('dest')
except OSError:
    pass

try:
    os.mkdir('tmp')
except OSError:
    pass

firefox_services = Service(executable_path='/usr/local/bin/geckodriver', port=3000, service_args=['--marionette-port', '2828', '--connect-existing'])
driver = webdriver.Firefox(service=firefox_services)

sections.get_sections(driver)

with open('tmp/sections.json') as f:
    sections = json.load(f)
    for key, section in enumerate(sections):
        questions.download_questions(driver, key, section['href'])
        images.download_images(key)

with open('tmp/sections.json') as f:
    sections = json.load(f)
    for key, section in enumerate(sections):
        ankize.generate_anki(section['name'], key)