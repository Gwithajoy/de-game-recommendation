# 기본 설정
import time
import re
import os
import pandas as pd
import requests
import scrapy
from scrapy.http import TextResponse
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from steam_get_appids import get_appids
# from pymongo import MongoClient
import pymongo
import traceback
import pandas as pd

def get_bundle_info(appid):
    USER = "유저"
    PWD = "패스워드"
    HOST = "서버"
    PORT = "포트"
    client = pymongo.MongoClient(f"mongodb://{USER}:{PWD}@{HOST}:{PORT}")
   


    
    game_title  = []
    bundles_id = []
    bundles_count= []
    final_price = []


    params = {'json' : 1,
            'filter' : 'all',
            'language' : 'english'}
    

        # app ID로 게임 정보 가져오기
    url = f"https://store.steampowered.com/api/appdetails?appids={appid}"
    res = requests.get(url, params=params).json()
    try:
        # title 확인
        title = res[f"{appid}"]['data']['name']
        game_title.append(title)
        # 번들 정보 확인
        try:
            other_bundle = res[f"{appid}"]['data']['dlc']
            bundles_id.append(other_bundle)
        except:
            bundles_id.append('0')
        # 번들 개수 
        try:
            count_bundle = len(res[f"{appid}"]['data']['dlc'])
            bundles_count.append(count_bundle)
        except:
            bundles_count.append("0")
        # 최종 가격도 확인가능
        try:
            price = int(res[f"{appid}"]['data']["price_overview"]['final']/100)
            final_price.append(price)
        except:
            final_price("0")
    except:
        game_title.append('o')
        bundles_id.append('0')
        bundles_count.append("0")
        final_price.append("0")

    db = client['steam']
    collection = db['steam_bundle_info']
    doc = {'title': game_title, 'bundle_info' : bundles_id, 'bundle_count' : bundles_count, 'final_price':final_price}
    print(doc)
    collection.insert_one(doc)


appids = pd.read_csv('/Users/glebang/Downloads/appid.csv')
appids = appids['0']
appidlist = []

for keyid in appids:
    appidlist.append(keyid)
   
appidlist = appidlist[:12000]


for i in range(len(appidlist)):
    print(appidlist[i])
    temp = get_bundle_info(appidlist[i])
