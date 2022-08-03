import pyspark
from sqlalchemy import create_engine
from pyspark.sql import SparkSession
from pyspark import SparkContext
from pyspark import SparkConf
from pyspark.sql import SQLContext
import random
from sqlalchemy.engine import create_engine
from sqlalchemy.pool import NullPool
import pandas as pd


# spark session 설정
MAX_MEMORY="4g"
spark = SparkSession.builder.appName("mart")\
                .config("spark.executor.memory", MAX_MEMORY)\
                .config("spark.driver.memory", MAX_MEMORY)\
                .getOrCreate()

# mysql 정보
HOST = "ec2-54-248-99-240.ap-northeast-1.compute.amazonaws.com"
DB_USER   = "admin"
DB_PASSWD = "1111"
DB_NAME = "gentleman"
conn = f"mysql://{DB_USER}:{DB_PASSWD}@{HOST}/{DB_NAME}?charset=utf8"

# 테이블 읽어오기
for_m=pd.read_sql('SELECT * FROM steam_review', conn)
info_m= pd.read_sql('SELECT * FROM steam_info', conn)

#pandas dataframe을 spark dataframe으로 전환
for_m = spark.createDataFrame(for_m)
info_m = spark.createDataFrame(info_m)

#로컬
for_m.createOrReplaceTempView("data_for_m")
info_m.createOrReplaceTempView("info_m")              

# for review 
query ="""
SELECT data_for_m.appid, voted_up,weighted_vote_score,title,review, steamid
FROM data_for_m
INNER JOIN info_m ON data_for_m.appid = info_m.appid
"""
data_mart =spark.sql(query)
df1 = data_mart.toPandas()
df1_1 = df1[df1['voted_up'].isin(['True', 'False'])]
df1_2 = df1[df1['voted_up'].isna()]
total = pd.DataFrame()
total = pd.concat([total, df1_1, df1_2])


#for item
query ="""
SELECT data_for_m.appid, title, steamid,voted_up
FROM data_for_m
INNER JOIN info_m ON data_for_m.appid = info_m.appid
"""
seh = spark.sql(query)
df = seh.toPandas()
df['userscore'] = df['voted_up'].apply(lambda x : random.randint(8, 10)if x == 'True' else random.randint(1,3))
df = df.drop("voted_up", axis=1)


spark.stop()



