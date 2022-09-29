from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests
import time
import json

PATH = 'chromedriver.exe'
driver = webdriver.Chrome(PATH)
driver.get('https://youtube.com')
search = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.NAME, 'search_query')))
search_btn = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.ID, 'search-icon-legacy')))
search.clear()
search.send_keys("Ukraine")
time.sleep(5)
search_btn.click()

time.sleep(5)
# WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.TAG_NAME, "ytd-video-renderer")))
videos = driver.find_elements(By.TAG_NAME, "ytd-video-renderer")
urls = [videos[i].find_element(By.CSS_SELECTOR, 'a#thumbnail').get_attribute('href') for i in range(10)]

data = {}
for i in range(10):
    driver.get(urls[i])
    time.sleep(5)
    driver.execute_script("window.scrollTo(0, 600)")
    time.sleep(5)
    all_comments = driver.find_elements(By.XPATH, '//*[@id="content-text"]')
    if len(all_comments) >= 3:
        temp_list = [all_comments[j].text for j in range(3)]

    else:
        temp_list = [all_comments[j].text for j in range(len(all_comments))]
    data[urls[i]] = temp_list
    print(temp_list)
    # WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="content-text"]')))
    # doc = BeautifulSoup(driver.page_source, 'html.parser')
    # print(doc.prettify())

with open('data.json', 'w') as fp:
    json.dump(data, fp)

driver.quit()