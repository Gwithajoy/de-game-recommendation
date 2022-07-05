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


def get_bundle_info(appidlist):
    USER = "admin2"
    PWD = "1111"
    HOST = "ec2-54-248-99-240.ap-northeast-1.compute.amazonaws.com"
    PORT = "27017"
    client = pymongo.MongoClient(f"mongodb://{USER}:{PWD}@{HOST}:{PORT}")

    
    game_title  = []
    bundles_id = []
    bundles_count= []
    final_price = []


    params = {'json' : 1,
            'filter' : 'all',
            'language' : 'english'}
    
        # app ID로 게임 정보 가져오기
    for keyid in appidlist:
        url = f"https://store.steampowered.com/api/appdetails?appids={keyid}"
        res = requests.get(url, params=params).json()
        try:
            # title 확인
            title = res[f"{keyid}"]['data']['name']
            game_title.append(title)
            # 번들 정보 확인
            other_bundle = res[f"{keyid}"]['data']['dlc']
            bundles_id.append(other_bundle)
            # 번들 개수 
            count_bundle = len(res[f"{keyid}"]['data']['dlc'])
            bundles_count.append(count_bundle)
            # 최종 가격도 확인가능
            price = int(res[f"{keyid}"]['data']["price_overview"]['final']/100)
            final_price.append(price)
        except:
            pass
        
        db = client['steam']
        collection = db['steam_test']
        doc = {'title': title, 'bundle_info' : other_bundle, 'bundle_count' : count_bundle, 'final_price':price}
        collection.insert_one(doc)
    

