import time
import re
import os
from matplotlib.font_manager import json_dump
import pandas as pd
import requests
from pymongo import MongoClient
import pymongo
from fake_useragent import UserAgent
from bs4 import BeautifulSoup  
import json, csv
import traceback
from kafka import KafkaProducer
from numpy import result_type


BROKERS = ['localhost:9092']
TOPIC_NAME = "steam_reviews_topic"

producer = KafkaProducer(bootstrap_servers=BROKERS)



def get_reviews(appid, params={'json':1}):
    
        url = 'https://store.steampowered.com/appreviews/'
        response = requests.get(url=url+str(appid), params=params,headers={'User-Agent': 'Mozilla/5.0'})
        return response.json()
        time.sleep(2)
              

def get_n_reviews(appid, n=10000):
    USER = "admin2"
    PWD = "1111"
    HOST = "ec2-54-248-99-240.ap-northeast-1.compute.amazonaws.com"
    PORT = "27017"
    client = pymongo.MongoClient(f"mongodb://{USER}:{PWD}@{HOST}:{PORT}")
    db = client['steam']
    collection = db['steam_review']
        
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
            try:
                params['cursor'] = cursor.encode()
                params['num_per_page'] = min(100, n)
                n -= 100
                response = get_reviews(appid, params)
                cursor = response['cursor']
                new = response['reviews']
                for h in new:
                    h['appid']= appid
                    print(new)
                #reviews += response['reviews']
                if len(new) < 1:
                    continue
                producer.send(TOPIC_NAME, json.dumps(new).encode("utf-8"))
                producer.flush()
                # collection.insert_many(new)
            
                if len(response['reviews']) < 100: break
            except:
                continue



appids = pd.read_csv('/home/ubuntu/kafka_2.13-3.2.0/kafka_test/appid.csv')
appids = appids['0']
appidlist = []


for keyid in appids:
    appidlist.append(keyid)

appidlist = appidlist[4000:]


for i in range(len(appidlist)):
    temp = get_n_reviews(appidlist[i])
    
    
 