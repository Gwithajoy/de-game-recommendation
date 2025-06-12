import time
from selenium.webdriver.common.by import By
from google.utils import SeleniumHelper, KafkaHelper

class GooglePlayScraper:
    LIST_URL = "https://play.google.com/store/games"
    CARD_SELECTOR = ".Si6A0c.Gy4nib"
    MORE_BUTTON_XPATH = '//*[@id="yDmH0d"]/c-wiz[2]/div/div/div[1]/c-wiz/div/c-wiz/div/div/span'

    def __init__(self, kafka_brokers: list[str], topic_info: str):
        self.driver = SeleniumHelper.get_driver()
        self.kafka = KafkaHelper(kafka_brokers)
        self.topic = topic_info

    def scroll_to_end(self):
        prev_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == prev_height:
                break
            prev_height = new_height

    def collect_game_links(self) -> list[str]:
        self.driver.get(self.LIST_URL)
        time.sleep(3)
        self.driver.maximize_window()
        self.scroll_to_end()
        # "더보기" 버튼 반복 클릭
        try:
            while True:
                btn = self.driver.find_element(By.XPATH, self.MORE_BUTTON_XPATH)
                btn.click()
                time.sleep(1)
        except:
            pass
        cards = self.driver.find_elements(By.CSS_SELECTOR, self.CARD_SELECTOR)
        return [c.get_attribute("href") for c in cards]

    def parse_and_send(self, url: str):
        self.driver.get(url)
        time.sleep(2)
        # 예시: 이름
        name = self.driver.find_element(By.CSS_SELECTOR, "h1 span").text
        # 예시: 등급
        grade = self.driver.find_element(By.CSS_SELECTOR, ".g1rdde span").text
        # 예시: 평점
        raw = self.driver.find_element(By.CSS_SELECTOR, '[aria-label*="stars"]').get_attribute("aria-label")
        rating = float(raw.split()[0])
        # 예시: 카테고리
        category = self.driver.find_element(By.CSS_SELECTOR, "c-wiz:nth-of-type(3) section div:nth-of-type(3)").text.split("\n")
        # 예시: 소개
        intro = self.driver.find_element(By.CSS_SELECTOR, "c-wiz:nth-of-type(3) section div:nth-of-type(1)").text

        doc = {
            "url": url,
            "name": name,
            "grade": grade,
            "rating": rating,
            "category": category,
            "introduction": intro
        }
        print("[GameInfo]", doc)
        self.kafka.send(self.topic, doc)

    def run(self):
        links = self.collect_game_links()
        for link in links:
            try:
                self.parse_and_send(link)
            except Exception as e:
                print("Error parsing", link, e)
