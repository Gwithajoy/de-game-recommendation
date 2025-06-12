import time
from selenium.webdriver.common.by import By
from google.utils import SeleniumHelper, KafkaHelper

class GoogleReviewScraper:
    """개별 게임 페이지에서 리뷰를 모두 긁어와 Kafka로 전송"""
    MORE_REVIEWS_XPATH = '//*[contains(@aria-label, "Show All Reviews")]//button'
    PANEL_CSS = 'div[role="region"]'
    REVIEW_CSS = '.h3YV2d'
    CLOSE_XPATH = '//button[@aria-label="Close"]'

    def __init__(self, kafka_brokers: list[str], topic_reviews: str):
        self.driver = SeleniumHelper.get_driver()
        self.kafka = KafkaHelper(kafka_brokers)
        self.topic = topic_reviews

    def open_reviews_panel(self):
        try:
            btn = self.driver.find_element(By.XPATH, self.MORE_REVIEWS_XPATH)
            btn.click()
            time.sleep(2)
        except:
            return False
        return True

    def scroll_reviews(self):
        panel = self.driver.find_element(By.CSS_SELECTOR, self.PANEL_CSS)
        prev = panel.get_attribute("scrollHeight")
        while True:
            self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", panel)
            time.sleep(1)
            curr = panel.get_attribute("scrollHeight")
            if curr == prev:
                break
            prev = curr

    def collect_reviews(self, game_name: str):
        if not self.open_reviews_panel():
            return
        self.scroll_reviews()
        elems = self.driver.find_elements(By.CSS_SELECTOR, self.REVIEW_CSS)
        texts = [e.text for e in elems]
        # 예: 별점 속성 추출
        stars = [int(e.get_attribute("aria-label").split()[3][0]) for e in
                 self.driver.find_elements(By.CSS_SELECTOR, 'div[role="img"]')]
        doc = {"name": game_name, "reviews": texts, "stars": stars}
        print("[Reviews]", game_name, len(texts))
        self.kafka.send(self.topic, doc)
        # 닫기
        try:
            self.driver.find_element(By.XPATH, self.CLOSE_XPATH).click()
            time.sleep(1)
        except:
            pass

    def run_for_game(self, game_url: str):
        self.driver.get(game_url)
        time.sleep(2)
        name = self.driver.find_element(By.CSS_SELECTOR, "h1 span").text
        self.collect_reviews(name)
