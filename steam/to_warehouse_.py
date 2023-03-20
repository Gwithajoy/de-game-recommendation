import pandas as pd
from pymongo import MongoClient
import pymongo
import mysql.connector as mysql
import re
from sqlalchemy import create_engine
from steam_review import get_mongodb_conn

def to_mysql_conn(engine):
    '''
        mysql로 engine을 반환하는 함수
	'''
    HOST ="ec2-**-248-**-**0.ap-northeast-1.compute.amazonaws.com"
    USER = "a***"
    PWD= "****"
    engine = create_engine(f"mysql+mysqlconnector://{USER}:{PWD}@{HOST}:3306/gentleman")
    return engine

def trans_for_warehouse(engine):
    '''
        몽고디비에서 받아온 데이터를 데이터 웨어하우스의 형식에 맞게 전처리 진행하여 to_sql로 적재처리 하는 함수
        :params
            appid : mysql에서 생성한 engine
        :return
            to_sql으로 최종 전처리된(warehouse를 위한) 데이터를 전송처리
	'''
    mycol= get_mongodb_conn('steam_review')
    reviews = []
    for j in range(1,5):
        if j == 1:
            # limit() : 한번에 조회 할 갯수 제한
            for d in mycol.find({},{"_id":0}).limit(500):
                    reviews.append(d)
        else:
            # skip() : 조회할때 원하는 갯수만큼 건너뛰고 조회할 수 있다.
            for d in mycol.find({},{"_id":0}).skip((j-1)*500).limit(500):
                reviews.append(d)
        playtime = []
        #reviews['author']에 steamid, num_games_owned, num_reviews, playtime_forever 등 분석에 필요한 값들을 for loop을 돌며 꺼내줌
        for i in range(len(reviews)):
            steamid = reviews[i]['author']['steamid']
            num_games_owned = reviews[i]['author']['num_games_owned']
            num_reviews = reviews[i]['author']['num_reviews']
            playtime_forever = reviews[i]['author']['playtime_forever']
            #플레이 타임의 경우 값이 없는 경우에는 0을 부여 / 그렇지 않은 경우에는 int 형식으로 값을 부여
            if playtime_forever == None:
                playtime.append(0)
            else:
                playtime.append(int(playtime_forever))
            reviews[i]['steamid'] = steamid
            reviews[i]['num_games_owned'] = num_games_owned
            reviews[i]['num_reviews'] = num_reviews
            reviews[i]['playtime_forever'] = playtime[i]
        # # read the data
            df = pd.DataFrame(reviews)
            df1 = df.copy()
            df1 = df1.astype({'weighted_vote_score':float})
            df1 = df1.astype({'appid':str})
            df1['appid'] = df1['appid'].apply(lambda x : x.split(",")[0])
            df1 = df1.astype({'appid':int})
            df1 = df1.dropna(axis=0)
            df2 = df1.drop(['received_for_free', 'timestamp_created','received_for_free','steam_purchase'
                            ,'written_during_early_access','timestamp_updated'
                            ,'recommendationid', 'comment_count', 'author'], axis=1)
            # 리뷰상의 이모티콘과 특수문자를 걸러주도록 패턴을 적용
            pattern = '[^a-z^A-Z^0-9^\s^\-^=^+^,^#^/^?^:^\^^.^@^*^~^!^(^)^\[^\]^<^>]'
            df2['review'] = df2['review'].apply(lambda x: re.sub(pattern, '', x))
            df2 = df2[['appid','steamid','review','num_games_owned','num_reviews',
                    'playtime_forever','votes_funny','votes_up','voted_up','weighted_vote_score']]
        
            if i % 100 == 0:
                df2 = df2.drop_duplicates(['steamid','review'])
                df2.to_sql(name ='steam_test', con = engine, if_exists='replace', index=False)
        
