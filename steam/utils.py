import requests
import pymongo
from fake_useragent import UserAgent

class MongoConnector:
    """MongoDB 연결 관리"""
    def __init__(self, user, pwd, host, port, db_name):
        uri = f"mongodb://{user}:{pwd}@{host}:{port}"
        self.client = pymongo.MongoClient(uri)
        self.db = self.client[db_name]

    def collection(self, name):
        return self.db[name]


class HTTPClient:
    """Requests 래퍼 + UserAgent 관리"""
    def __init__(self):
        self.session = requests.Session()
        ua = UserAgent(verify_ssl=False).chrome
        self.session.headers.update({'User-Agent': ua})

    def get_json(self, url, params=None):
        resp = self.session.get(url, params=params, timeout=10)
        resp.raise_for_status()
        return resp.json()
