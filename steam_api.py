# 기본 설정
import selenium
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import re
import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import requests
import requests
import scrapy
from scrapy.http import TextResponse
from fake_useragent import UserAgent
from bs4 import BeautifulSoup


# bundle 정보를 가져오기 위해, 각 게임별 appid 불러오기 
def get_appids():
    
    fakeuser = UserAgent(verify_ssl=False).chrome
    header = {'User-Agent':fakeuser}

    appidlist = []
    BASE_URL = 'https://store.steampowered.com/search/?page='

    for i in range(1,2) : # 지금 4863페이지까지 있어서 이건 유동적으로 수정하시면 될 듯 !
        url = BASE_URL+str(i)
        req = requests.get(url, headers=header)
        res = TextResponse(req.url, body = req.text, encoding = 'utf-8')
        templist = res.xpath('//*[@id="search_resultsRows"]/a/@data-ds-appid').extract()
    
        appidlist=+ templist
    
           
            

# 리뷰 api 가져오기 
def get_reviews(appid, params={'json':1}):
        url = 'https://store.steampowered.com/appreviews/'
        response = requests.get(url=url+appid, params=params, headers={'User-Agent': 'Mozilla/5.0'})
        return response.json()

def get_n_reviews(appid, n=10):
    reviews = []
    cursor = '*'
    params = {
            'json' : 1,
            'filter' : 'all',
            'language' : 'english',
            'day_range' : 9223372036854775807,
            'review_type' : 'all',
            'purchase_type' : 'all'
            }
    
    while n > 0:
        
        for i in range(100):
            params['cursor'] = cursor.encode()
            params['num_per_page'] = min(100, n)
            n -= 100

            response_i = get_reviews(appid, params)
            cursor = response_i['cursor']
            reviews += response_i['reviews']
        
            if len(response_i['reviews']) < 100: break

    return reviews
        
def get_bundle_info(appid):
    
    params = {'json' : 1,
            'filter' : 'all',
            'language' : 'english'}
 
    # app ID로 게임 정보 가져오기
    url = f"https://store.steampowered.com/api/appdetails?appids={appid}"
    res = requests.get(url, params=params).json()
    # title 확인
    res[appid]['data']['name']
    # 번들 정보 확인
    res[appid]['data']['dlc']
    # Don't Starve Together 스팀 페이지에서 
    # CONTENT FOR THIS GAME 부분에 보면 Browse all (35)라고 표시되어있는것 확인
    len(res[appid]['data']['dlc'])
    # 최종 가격도 확인가능
    res[appid]['data']["price_overview"]['final']/100

