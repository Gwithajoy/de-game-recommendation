from steam.utils import HTTPClient

class SteamReviewAPI:
    """Steam 리뷰 Web API 호출기"""
    BASE_URL = 'https://store.steampowered.com/appreviews/'

    def __init__(self):
        self.http = HTTPClient()

    def fetch_reviews(self, appid, cursor='*', num=100):
        params = {
            'filter':'all',
            'language':'english',
            'day_range':9223372036854775807,
            'review_type':'all',
            'purchase_type':'all',
            'cursor': cursor,
            'num_per_page': num
        }
        return self.http.get_json(self.BASE_URL + str(appid), params=params)
