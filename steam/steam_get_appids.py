# 기본 설정
import time
import re
import pandas as pd
import requests
import scrapy
from scrapy.http import TextResponse
from fake_useragent import UserAgent



# bundle 정보를 가져오기 위해, 각 게임별 appid 불러오기 
def get_appids():
    '''
		스팀 각 게임마다 있는 고유의 id값을 data-ds-appid에서 게임 appid를 가져오는 함수.
        스팀의 모든 게임들은 1 ~ 4863 페이지에 걸쳐 있으므로 각 페이지에 있는 각 게임링크에 있는 appid를 가져옴.
		:return
		1 ~ 4863 페이지에 있는 모든 게임의 appid가 list형식으로 리턴
	'''
    
    fakeuser = UserAgent(verify_ssl=False).chrome
    header = {'User-Agent':fakeuser}

    appidlist = []
    BASE_URL = 'https://store.steampowered.com/search/?page='

    for i in range(1,4863) : # 지금 4863페이지까지 있어서 이건 유동적으로 수정하시면 될 듯 !
        print(i)
        url = BASE_URL+str(i)
        req = requests.get(url, headers=header)
        res = TextResponse(req.url, body = req.text, encoding = 'utf-8')
        
        templist = res.xpath('//*[@id="search_resultsRows"]/a/@data-ds-appid').extract()
    
        appidlist += templist
    
    return appidlist
    
 