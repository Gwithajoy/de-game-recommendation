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
from steam_bundle_info import get_bundle_info
from steam_review  import get_reviews, get_n_reviews


if __name__ == '__main__':
    appidlist = get_appids()
    get_bundle_info(appidlist)
    get_n_reviews(appidlist, n=100)
