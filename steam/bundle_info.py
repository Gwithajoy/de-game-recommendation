from steam.utils import HTTPClient, MongoConnector

class SteamBundleInfoService:
    """Steam API로 bundle & price 정보 수집 후 MongoDB 저장"""
    API_URL = 'https://store.steampowered.com/api/appdetails'

    def __init__(self, mongo_cfg):
        self.http = HTTPClient()
        self.mongo = MongoConnector(**mongo_cfg)
        self.collection = self.mongo.collection('steam_bundle_info')

    def fetch_bundle_data(self, appid):
        params = {'appids': appid, 'json':1, 'filter':'all', 'language':'english'}
        data = self.http.get_json(self.API_URL, params=params).get(str(appid), {}).get('data', {})
        return {
            'title': data.get('name', None),
            'bundle_ids': data.get('dlc', []),
            'bundle_count': len(data.get('dlc', [])),
            'final_price': data.get('price_overview', {}).get('final', 0) // 100
        }

    def save(self, appid):
        doc = self.fetch_bundle_data(appid)
        print(f"[BundleInfo] {appid} → {doc}")
        self.collection.insert_one(doc)
