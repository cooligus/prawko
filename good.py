from dotenv import load_dotenv
import os
import time 
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options

load_dotenv()

#options = Options()
#options.add_argument("--headless")
#options.binary_location='/usr/bin/firefox'
#options.add_argument('--connect-existing')
#driver = webdriver.Firefox(service=Service('/usr/local/bin/geckodriver'),options=options)

firefox_services = Service(executable_path='/usr/local/bin/geckodriver', port=3000, service_args=['--marionette-port', '2828', '--connect-existing'])
driver = webdriver.Firefox(service=firefox_services)

#driver.get("https://testy.portalnaukijazdy.pl/konto/logowanie")
#login = driver.find_element(By.ID, "email")
#login.clear()
#login.send_keys(os.getenv('LOGIN'))
#login.send_keys(Keys.RETURN)
#
#password = driver.find_element(By.ID, "password")
#password.clear()
#password.send_keys(os.getenv('PASSWORD'))
#password.send_keys(Keys.RETURN)
#
#submit = driver.find_element(By.CLASS_NAME, "btn-yellow")
#submit.click()

driver.get("https://testy.portalnaukijazdy.pl/konto/moje-kursy/1,b")
elements = driver.find_element(By.ID, "nauka").find_elements(By.CLASS_NAME, "list-row")

sections = []
for element in elements:
    section = {}
    section['href']=element.find_element(By.XPATH, "//a[@title='Rozpocznij naukę']").get_attribute("href")
    section['name']=element.find_element(By.CLASS_NAME, "col1").get_attribute("innerHTML")
    sections.append(section)


driver.get(sections[0]['href'])
questionBoxes = driver.find_elements(By.CLASS_NAME, "owl-item")

results = []
comeOn = True

while comeOn:
    for box in questionBoxes:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'question')))
        driver.execute_script("window.scrollTo(0, 300)")
        question = box.find_element(By.CLASS_NAME, "question")
        comment = box.find_element(By.CLASS_NAME, "comment")

        image = ''
        video = ''
        try:
            image = box.find_element(By.TAG_NAME, "img").get_attribute('src')
        except:
            video = box.find_element(By.TAG_NAME, "video").get_attribute('src')

        answers = box.find_elements(By.CLASS_NAME, "answer")

        # Select answer
        box.find_element(By.CLASS_NAME, 'taknie').click()
        correctAnswer = box.find_element(By.XPATH, "//div[contains(@class, 'correct')]//div")

        result = {}
        result['question'] = question.get_attribute('innerHTML') # OK
        result['image'] = image
        result['video'] = video
        result['answers'] = []
        for answer in answers:
            result['answers'].append(answer.find_element(By.CLASS_NAME, "answer-text").get_attribute('innerHTML'))
        result['correctAnswer'] = correctAnswer.get_attribute('innerHTML')
        result['comment'] = comment.find_element(By.XPATH, "(//p)[1]").get_attribute('innerHTML')
        results.append(result)

        try:
            #WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.nav.next.disabled'))).click()
            box.find_element(By.CSS_SELECTOR, '.nav.next.disabled').click()
        except:
            try:
                box.find_element(By.CSS_SELECTOR, '.nav.next').click()
            except:
                try:
                    box.find_element(By.CSS_SELECTOR, '.nav.refresh').click()
                except:
                    comeOn = False

        driver.execute_script("window.scrollTo(0, 300)")


f = open(format("tmp/{}.json", section[0]['name']), "w")
f.write(json.dumps(results))
f.close()