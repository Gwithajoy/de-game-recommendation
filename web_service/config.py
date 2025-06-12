import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "change_this")
    MONGO_URI = os.getenv(
        "MONGO_URI",
        "mongodb://admin2:1111@ec2-54-248-99-240.ap-northeast-1.compute.amazonaws.com:27017/google"
    )
    MYSQL_URI = os.getenv(
        "MYSQL_URI",
        "mysql+pymysql://admin:1111@ec2-54-248-99-240.ap-northeast-1.compute.amazonaws.com:3306/gentleman?charset=utf8mb4"
    )
