import time
from steam.utils import MongoConnector
from steam.review_api import SteamReviewAPI

class SteamReviewPipeline:
    """appid 리스트 순회하며 n개 리뷰 가져와 MongoDB 저장"""
    def __init__(self, mongo_cfg, batch_size=100):
        self.api = SteamReviewAPI()
        self.mongo = MongoConnector(**mongo_cfg)
        self.collection = self.mongo.collection('steam_review')
        self.batch_size = batch_size

    def run_for_appid(self, appid, total_n=10000):
        remaining = total_n
        cursor = '*'
        while remaining > 0:
            data = self.api.fetch_reviews(appid, cursor, min(self.batch_size, remaining))
            cursor = data.get('cursor', cursor)
            reviews = data.get('reviews', [])
            if not reviews:
                break
            for r in reviews:
                r['appid'] = appid
            self.collection.insert_many(reviews)
            remaining -= len(reviews)
            print(f"[Reviews] {appid}: saved {len(reviews)} reviews, remaining {remaining}")
            time.sleep(1)  # rate limit

    def run(self, appid_list, per_app_n=1000):
        for aid in appid_list:
            self.run_for_appid(aid, total_n=per_app_n)
