from . import db

class SteamGameInfo(db.Model):
    __tablename__ = "steam_game_info"
    appid        = db.Column(db.Integer, primary_key=True)
    title        = db.Column(db.String(255))
    image_link   = db.Column(db.String(512))
    grade        = db.Column(db.String(50))
    release_date = db.Column(db.Date)
    genre        = db.Column(db.String(100))
    description  = db.Column(db.Text)
    video_link   = db.Column(db.String(512))
