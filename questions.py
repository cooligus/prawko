import os
import time 
import json
from collections import defaultdict
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options


def download_questions(driver, sectionId, href):
    driver.get(href)
    questionBoxes = driver.find_elements(By.CLASS_NAME, "owl-item")

    results = []
    comeOn = True

    while comeOn:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'question')))
        questionBoxes = driver.find_elements(By.CLASS_NAME, "owl-item")
        for box in questionBoxes:
            driver.execute_script("window.scrollTo(0, 300)")
            question = box.find_element(By.CLASS_NAME, "question")
            comment = box.find_element(By.CLASS_NAME, "comment")

            image = ''
            video = ''
            try:
                image = box.find_element(By.TAG_NAME, "img").get_attribute('src')
            except:
                video = box.find_element(By.TAG_NAME, "source").get_attribute('src')

            answers = box.find_elements(By.CLASS_NAME, "answer")

            # Select answer
            box.find_element(By.CLASS_NAME, 'answer').click()
            correctAnswer = box.find_element(By.CSS_SELECTOR, ".answer.correct").find_element(By.TAG_NAME, "div")

            result = defaultdict(list)
            result['Question'] = question.get_attribute('innerHTML') # OK
            result['Image'] = image
            result['Video'] = video
            result['Answers'] = []
            for answer in answers:
                result['Answers'].append(answer.find_element(By.CLASS_NAME, "answer-text").get_attribute('innerHTML'))
            result['CorrectAnswer'] = correctAnswer.get_attribute('innerHTML')
            result['Comment'] = comment.find_elements(By.TAG_NAME, "p")[1].get_attribute('innerHTML')
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


    fileName = "tmp/{}.json"
    fileName = fileName.format(sectionId)
    f = open(fileName, "w")
    f.write(json.dumps(results))
    f.close()