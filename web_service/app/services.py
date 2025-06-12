from flask import current_app
from . import mongo, db
from .models import SteamGameInfo
from gensim.models.doc2vec import Doc2Vec
import pymysql

# Mongo 로부터 게임 목록 가져오기
def get_mongo_games():
    col = mongo.cx.get_default_database()["google_game_kafka"]
    cursor = col.find({}, {"_id":0, "name":1, "rating":1})
    return list(cursor)

# MySQL 로부터 top15 장르별 게임 조회
def get_genre_top15(genre_name):
    sql = f"SELECT appid, title, image_link FROM steam_game_info WHERE genre LIKE '%{genre_name}%' ORDER BY rating DESC LIMIT 15"
    conn = pymysql.connect(
        host=current_app.config["MYSQL_URI"].split("@")[1].split("/")[0],
        user=current_app.config["MYSQL_URI"].split("//")[1].split(":")[0],
        passwd=current_app.config["MYSQL_URI"].split(":")[2].split("@")[0],
        db=current_app.config["MYSQL_URI"].split("/")[-1].split("?")[0],
        charset="utf8mb4"
    )
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute(sql)
    data = cur.fetchall()
    conn.close()
    return data

# 추천 엔진 래퍼
def recommend(appids: list[int], version: int = 1):
    # gensim Doc2Vec 모델 로딩 (사전에 학습된 .model 파일 경로)
    model = Doc2Vec.load("models/gentleman_ver{}.model".format(version))
    # 벡터 유사도로 top6 appid 계산 (가정)
    inferred = [model.infer_vector([str(a)]) for a in appids]
    sims = model.docvecs.most_similar(positive=inferred, topn=6)
    rec_ids = [int(docid) for docid, _ in sims]
    # MySQL에서 상세 정보 가져오기
    engine = db.get_engine(current_app)
    return engine.execute(
        SteamGameInfo.__table__.select().where(SteamGameInfo.appid.in_(rec_ids))
    ).fetchall()
