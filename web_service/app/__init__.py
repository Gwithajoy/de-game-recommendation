from flask import Flask
from flask_pymongo import PyMongo
from flask_sqlalchemy import SQLAlchemy

mongo = PyMongo()
db    = SQLAlchemy()

def create_app():
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.config.from_object("config.Config")

    # DB 초기화
    mongo.init_app(app)
    db.init_app(app)

    # 블루프린트 등록
    from .routes import main_bp
    app.register_blueprint(main_bp)

    return app
