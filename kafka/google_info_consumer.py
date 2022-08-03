import pandas as pd
import numpy as np
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Keys
from selenium.webdriver.common.action_chains import ActionChains
import requests
import json, csv
import traceback
from kafka import KafkaConsumer
from numpy import result_type
from pymongo import MongoClient
import pymongo


USER = "admin2"
PWD = "1111"
HOST = "ec2-54-248-99-240.ap-northeast-1.compute.amazonaws.com"
PORT = "27017"
client = pymongo.MongoClient(f"mongodb://{USER}:{PWD}@{HOST}:{PORT}")
db = client['google']
collection = db['google_game_kafka']
BROKERS = ["localhost:9092"]
TOPIC_NAME = "google_games_topic"
consumer = KafkaConsumer(TOPIC_NAME, bootstrap_servers = BROKERS)
while True:
    for message in consumer:
        doc = json.loads(message.value.decode())
        collection.insert_one(doc)
        print(doc)