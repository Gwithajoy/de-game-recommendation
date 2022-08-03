import pandas as pd
import numpy as np
import time
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Keys
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import requests
import json, csv
import traceback
from kafka import KafkaProducer
from numpy import result_type
import warnings
from selenium import webdriver
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager




BROKERS = ['localhost:9092']
TOPIC_NAME = "google_games_topic"
TOPIC_NAME2 = "google_review_topic"
producer = KafkaProducer(bootstrap_servers=BROKERS)

# def get_chrome_driver():
#     chrome_options = webdriver.ChromeOptions()

#     driver = webdriver.Chrome(
#         service=Service(ChromeDriverManager().install()),
#         options=chrome_options, )
    
#     return driver


# 워닝 무시
options = Options()
options.headless = True
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
warnings.filterwarnings('ignore')
# driver = get_chrome_driver()
driver.get("https://play.google.com/store/games")
driver.implicitly_wait(10)

# 창 크기 최대화
driver.maximize_window()
##스크롤 끝까지 내리기
#스크롤 내리기 이동 전 위치
scroll_location = driver.execute_script("return document.body.scrollHeight")

while True:
    #현재 스크롤의 가장 아래로 내림
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    #전체 스크롤이 늘어날 때까지 대기
    time.sleep(2)
    #늘어난 스크롤 높이
    scroll_height = driver.execute_script("return document.body.scrollHeight")
    #늘어난 스크롤 위치와 이동 전 위치 같으면(더 이상 스크롤이 늘어나지 않으면) 종료
    if scroll_location == scroll_height:
          break
    #같지 않으면 스크롤 위치 값을 수정하여 같아질 때까지 반복
    else:
    #스크롤 위치값을 수정
        scroll_location = driver.execute_script("return document.body.scrollHeight")

    # 더보기 버튼 누르기
    try:
        time.sleep(2)
        driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/c-wiz[2]/div/div/div[1]/c-wiz/div/c-wiz/div/div/span').click()
        time.sleep(2)
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    except:
        continue

# link 추출
elements = driver.find_elements(By.CSS_SELECTOR, '.Si6A0c.Gy4nib')
link_lst = []
for element in elements:
    link = element.get_attribute('href')
    print(link)
    link_lst.append(link)


for link in link_lst:
        driver.get(link)
        time.sleep(2)

        # 이름
        name=driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/c-wiz[2]/div/div/div[1]/div[1]/div/div/c-wiz/div[2]/div[1]/div/h1/span').text
        # 등급(나이제한)
        g_class = driver.find_elements(By.CSS_SELECTOR, '.g1rdde')
        if len(g_class) == 4:
            grade = driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/c-wiz[2]/div/div/div[1]/div[1]/div/div/c-wiz/div[2]/div[2]/div/div/div[4]/div[2]/span/span').text
        elif len(g_class) == 3:
            grade = driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/c-wiz[2]/div/div/div[1]/div[1]/div/div/c-wiz/div[2]/div[2]/div/div/div[3]/div[2]/span/span').text

        elif len(g_class) == 2:
            grade = driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/c-wiz[2]/div/div/div[1]/div[1]/div/div/c-wiz/div[2]/div[2]/div/div/div[2]/div[2]/span/span').text
        else:
            grade = driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/c-wiz[2]/div/div/div[1]/div[1]/div/div/c-wiz/div[2]/div[2]/div/div/div/div[2]/span/span').text
            
        # 게임 평점
        try:
            rating = driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/c-wiz[2]/div/div/div[1]/div[1]/div/div/c-wiz/div[2]/div[2]/div/div/div[1]/div[1]/div/div').text
            rating = float(rating[0:3])
        except:
            continue

        # 장르
        category=driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/c-wiz[2]/div/div/div[1]/div[2]/div/div[1]/c-wiz[2]/div/section/div/div[3]').text
        category=category.split('\n')

        # 게임소개
        introduction = driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/c-wiz[2]/div/div/div[1]/div[2]/div/div[1]/c-wiz[2]/div/section/div/div[1]').text
        
        DOC = {"name":name, "grade":grade, "rating":rating, "category":category, "introduction":introduction}
        print(DOC)
        producer.send(TOPIC_NAME, json.dumps(DOC).encode("utf-8"))
        producer.flush()

        
        # db.google_games.insert_one(DOC)
        # print(name, len(reviews))
        # del name, grade, rating, category, introduction
        
        ## 리뷰
        # 리뷰 더보기 버튼 클릭
        try:
            driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/c-wiz[2]/div/div/div[1]/div[2]/div/div[1]/c-wiz[4]/section/div/div/div[5]/div/div/button/span').click()
        except:
            continue

        # 리뷰 스크롤 내리기 
        time.sleep(4)
        driver.find_element(By.CSS_SELECTOR, '.fysCi').click()
        try:
            panel = driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/div[4]/div[2]/div/div/div/div/div[2]')       
        except:
            continue
        while True:
            pre_height = driver.execute_script('return arguments[0].scrollHeight;', panel)
            driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight;', panel)
            time.sleep(3)
            next_height = driver.execute_script('return arguments[0].scrollHeight;', panel)
            reviews = driver.find_elements(By.CSS_SELECTOR, '.h3YV2d')
            time.sleep(4)
            if pre_height == next_height:
                break
            if len(reviews) > 4000:
                break
                
        # 리뷰 가져오기
        time.sleep(2)
        reviews = driver.find_elements(By.CSS_SELECTOR, '.h3YV2d')
        reviews = [review.text for review in reviews]

        ##개인 평점
        #속성값 추출하기
        evaluation = driver.find_elements_by_xpath('//div[@class="Jx4nYe"]/div[@role="img"]')
        #가져온 속성에서 별점 부분 추출
        star=[int(i.get_attribute("aria-label").split()[3][0]) for i in evaluation]

        DOC2 = {"name" : name ,'reviews' : reviews, "star" : star}
        producer.send(TOPIC_NAME2, json.dumps(DOC2).encode("utf-8"))
        producer.flush()

        # 더보기 끄기
        driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/div[4]/div[2]/div/div/div/div/div[1]/button').click()
        time.sleep(2)
