import pymongo
import json
from kafka import KafkaConsumer

#broker목록은 모두 설정하는 것이 좋다!
BROKERS = ['localhost:9092']
TOPIC_NAME = "steam_reviews_topic"

USER = "admin2"
PWD = "1111"
HOST = "ec2-54-248-99-240.ap-northeast-1.compute.amazonaws.com"
PORT = "27017"
client = pymongo.MongoClient(f"mongodb://{USER}:{PWD}@{HOST}:{PORT}")
db = client['steam']
collection = db['steam_review_kafka']
consumer = KafkaConsumer(TOPIC_NAME, bootstrap_servers=BROKERS)


while True:
    for message in consumer:
        doc = json.loads(message.value.decode())
        collection.insert_many(doc)
        print(doc)