from scrapy.http import TextResponse
from steam.utils import HTTPClient

class SteamAppIDCrawler:
    """Steam 검색 페이지 순회하며 appid 목록 수집"""
    BASE_URL = 'https://store.steampowered.com/search/?page={}'

    def __init__(self, max_page=4863):
        self.http = HTTPClient()
        self.max_page = max_page

    def fetch_page_appids(self, page):
        url = self.BASE_URL.format(page)
        html = self.http.session.get(url).text
        resp = TextResponse(url=url, body=html, encoding='utf-8')
        return resp.xpath('//*[@id="search_resultsRows"]/a/@data-ds-appid').getall()

    def get_appids(self):
        appids = []
        for p in range(1, self.max_page+1):
            print(f"Fetching page {p}/{self.max_page}")
            appids.extend(self.fetch_page_appids(p))
        return appids
