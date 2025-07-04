# Steam Game Recommendation Service

국내 PC 게임 시장의 성장과 Steam 추천 시스템의 한계를 보완하기 위해, 사용자 리뷰기반 및 협업 필터링 추천 모델을 개발하여 제공하는 풀스택 프로젝트입니다.

## 1. 프로젝트 개요

### 1.1. 배경 및 목표
- 국내 PC 게임 시장 점유율: 35.7%, Steam 플랫폼 비중 37%.
- 기존 Steam 추천은 할인·인기 위주로 정확도가 낮음.
- 사용자 리뷰와 협업 필터링 알고리즘을 융합한 2가지 버전의 추천 모델 구현 및 서비스 제공.

### 1.2. 역할
- 팀 리더 및 풀스택 개발
- Steam appID, 리뷰, 번들 정보 크롤링 → Kafka 기반 데이터 파이프라인
- 데이터 마트(MySQL) 설계 및 구축
- Flask 웹 서비스 프론트·백엔드 개발

## 2. 기술 스택
- 언어: Python, JavaScript
- 데이터 수집: Selenium, BeautifulSoup, Scrapy, Steam API, Kafka
- 저장: MongoDB, MySQL
- 처리: Pandas, SparkSQL
- 웹: Flask, SQLAlchemy
- 컨테이너·배포: Docker, docker-compose, Gunicorn

## 3. 시스템 구조

```
3rd_project/
├── conf/                   # 환경 설정 및 .env 예시
├── google/                 # Google Play 크롤러
├── kafka/                  # Kafka producer/consumer
├── steam/                  # Steam 크롤러 및 파이프라인
├── warehouse/              # Data Warehouse Loader
├── web_service/            # Flask 웹 서비스
├── tests/                  # 단위 테스트
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## 4. 데이터 파이프라인
1. **Extract**
   - Steam appID 수집: Scrapy + HTTPClient
   - Steam Review/Bundles: Steam API 호출
   - Google Play: Selenium 크롤링
2. **Stream**
   - Kafka producer/consumer로 실시간 스트리밍
3. **Load**
   - MongoDB: 원시 데이터 저장
   - MySQL: 데이터 마트 테이블 저장
4. **Transform**
   - Pandas / SparkSQL로 마트용 전처리
   - 리뷰 기반 및 사용자 기반 협업 필터링용 테이블 생성

## 5. 데이터베이스 모델
```sql
-- steam_game_info (PK: appid)
-- steam_bundle_info (FK→steam_game_info)
-- steam_reviews (FK→steam_game_info)
-- metacritic_info / meta / user
-- google_games / google_review
```

## 6. 추천 모델
- **아이템 기반 협업 필터링** (Surprise SVD, Cosine 유사도)
- **리뷰 기반 추천** (Doc2Vec + 리뷰 유사도)
- 하이퍼파라미터 튜닝: GridSearch, Bayesian Optimization
- 평가: 입력/출력 게임 태그 유사도 기준

## 7. 웹 서비스
- **Flask API**
  - `GET /api/game_select/`: 장르별 Top15 게임
  - `POST /api/recommendation/`: 모델1 추천 결과
  - `POST /api/recommendation2/`: 모델2 추천 결과
  - `GET /about_this_game/<appid>`: 게임 상세 정보
- **프론트엔드**
  - 순수 HTML/CSS/JS 슬라이더 UI
  - 3개 선택 시 버튼 활성화 → 추천 결과 페이지 이동

## 8. 설치 및 실행
1. 환경 변수 설정(.env):
   ```env
   FLASK_ENV=production
   SECRET_KEY=...
   MONGO_URI=...
   MYSQL_URI=...
   ```
2. 의존성 설치:
   ```bash
   pip install -r requirements.txt
   ```
3. 컨테이너 실행:
   ```bash
   docker-compose up --build
   ```
4. 웹 접속: `http://localhost:5000`

