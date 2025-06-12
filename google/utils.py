from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from kafka import KafkaProducer
import pymongo
import json

class SeleniumHelper:
    """Headless Chrome 드라이버를 생성합니다."""
    @staticmethod
    def get_driver(headless: bool = True, window_size: str = "1920,1080"):
        options = Options()
        if headless:
            options.add_argument("--headless")
        options.add_argument(f"--window-size={window_size}")
        service = Service(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=options)


class KafkaHelper:
    """Kafka Producer 생성 및 메시지 전송 래퍼"""
    def __init__(self, brokers: list[str]):
        self.producer = KafkaProducer(
            bootstrap_servers=brokers,
            value_serializer=lambda v: json.dumps(v).encode("utf-8")
        )

    def send(self, topic: str, record: dict):
        self.producer.send(topic, record)
        self.producer.flush()


class MongoConnector:
    """MongoDB 커넥터"""
    def __init__(self, user, pwd, host, port, db_name):
        uri = f"mongodb://{user}:{pwd}@{host}:{port}"
        self.client = pymongo.MongoClient(uri)
        self.db = self.client[db_name]

    def collection(self, name: str):
        return self.db[name]
