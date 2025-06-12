import re
import pandas as pd
from sqlalchemy import create_engine
from steam.review_api import SteamReviewAPI
from steam.utils import MongoConnector

class WarehouseLoader:
    """Mongo에서 읽어와 전처리 후 MySQL 테이블에 적재"""
    def __init__(self, mongo_cfg, mysql_url):
        self.mongo = MongoConnector(**mongo_cfg)
        self.engine = create_engine(mysql_url)

    def transform_reviews(self, docs):
        df = pd.DataFrame(docs)
        # author 필드 분해
        df['steamid'] = df['author'].apply(lambda a: a.get('steamid'))
        df['num_games_owned'] = df['author'].apply(lambda a: a.get('num_games_owned'))
        df['num_reviews'] = df['author'].apply(lambda a: a.get('num_reviews'))
        df['playtime_forever'] = df['author'].apply(lambda a: a.get('playtime_forever') or 0)
        df = df.drop(columns=['author', '_id'])
        # 텍스트 전처리
        pat = r'[^a-zA-Z0-9\s\-\=\+\,\#\/\?\:\^\.\@\*\~\!\(\)\[\]\<\>]'
        df['review'] = df['review'].apply(lambda x: re.sub(pat, '', x))
        return df

    def load(self, collection_name, table_name, batch_size=500):
        col = self.mongo.collection(collection_name)
        cursor = col.find({}, {'_id':0}).batch_size(batch_size)
        buffer = []
        for doc in cursor:
            buffer.append(doc)
            if len(buffer) >= batch_size:
                df = self.transform_reviews(buffer)
                df.to_sql(table_name, con=self.engine, if_exists='append', index=False)
                buffer.clear()
        # 남은 데이터 적재
        if buffer:
            df = self.transform_reviews(buffer)
            df.to_sql(table_name, con=self.engine, if_exists='append', index=False)
