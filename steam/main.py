from steam.get_appids import SteamAppIDCrawler
from steam.bundle_info import SteamBundleInfoService
from steam.review_pipeline import SteamReviewPipeline
from warehouse.loader import WarehouseLoader

# 설정 예시
mongo_cfg = {
    'user':'admin2', 'pwd':'1111',
    'host':'ec2-54-248-99-240.ap-northeast-1.compute.amazonaws.com',
    'port':'27017', 'db_name':'steam'
}
mysql_url = 'mysql+mysqlconnector://user:pwd@host:3306/gentleman'

if __name__ == '__main__':
    # 1) appid 수집
    crawler = SteamAppIDCrawler(max_page=2)  
    appids = crawler.get_appids()

    # 2) 번들 정보 저장
    bundle_srv = SteamBundleInfoService(mongo_cfg)
    for aid in appids[:100]:
        bundle_srv.save(aid)

    # 3) 리뷰 파이프라인 실행
    review_pipe = SteamReviewPipeline(mongo_cfg, batch_size=100)
    review_pipe.run(appids[:50], per_app_n=500)

    # 4) Data Warehouse 로드
    loader = WarehouseLoader(mongo_cfg, mysql_url)
    loader.load('steam_review', 'steam_test')
