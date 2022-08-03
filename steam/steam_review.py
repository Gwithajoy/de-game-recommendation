  # 기본 설정
import time
import requests
import pymongo

# 리뷰 api 가져오기
def get_mongodb_conn(collection_name):
    '''
	    몽고디비 컬렉션 객체를 반환하는 함수
	    :params : 몽고디비 컬렉션 이름
	'''
    USER = "*****"
    PWD = "*****"
    HOST = "ec2-**-**-**-**.ap-northeast-1.compute.amazonaws.com"
    PORT = "27017"
    client = pymongo.MongoClient(f"mongodb://{USER}:{PWD}@{HOST}:{PORT}")
    db = client['steam']
    collection = db[collection_name]
    
    return collection

def get_reviews(appid):
    '''
        리뷰를 받아올 steam review url에 정보를 요청과 응답을 받는 함수
        :params
            appid : 스팀게임의 고유번호 
        :return
            json 형식으로 요청한 데이터 전부를 받아옴. 추후 get_n_reviews에서 정보를 불러오는 데 쓰일 예정.
	'''
    url = 'https://store.steampowered.com/appreviews/'
    response = requests.get(url=url+appid, headers={'User-Agent': 'Mozilla/5.0'})
    
    return response.json()

def get_n_reviews(appidlist, n=100):
    '''
        :params
            appid : steam_get_appids 에서 return된 게임의 appid list
            n=100 : 한번에 크롤러를 통해 리뷰 100개씩 가져오도록 설정
        :return 
            파라미터로 지정해준 사항에 맞는 데이터를 가져와서 몽고디비로 바로 인서트 처리
        : API 참고 링크
            https://partner.steamgames.com/doc/webapi_overview#1
	''' 
    reviews = [] 
    collection = get_mongodb_conn('steam_review')       
    cursor = '*'
    params = {
            'filter' : 'all',
            'language' : 'english',
            'day_range' : 9223372036854775807,
            'review_type' : 'all',
            'purchase_type' : 'all'
            }
    
    for appid in appidlist:
        for i in range(100):
            params['cursor'] = cursor.encode()
            params['num_per_page'] = min(100, n)
            # n -= 100
            response_i = get_reviews(appid, params)
            time.sleep(2)
            cursor = response_i['cursor']
            new = response_i['reviews']
            for i in new:
                    i['appid']= appid
            collection.insert_many(new)
            if len(response_i['reviews']) < 100: break