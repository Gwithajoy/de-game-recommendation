from flask import Blueprint, render_template, request, jsonify
from .services import (
    get_mongo_games,
    get_genre_top15,
    recommend
)

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
@main_bp.route("/home/")
def home():
    return render_template("main_page.html")            

@main_bp.route("/games/")
def games():
    # 2nd 페이지: 장르별 top15 전달
    genres = ["action","adventure","casual","indie","racing","rpg","simulation","sports","strategy"]
    data = { f"{g}_top15": get_genre_top15(g) for g in genres }
    return render_template("game_list.html", **data)

@main_bp.route("/api/game_select/", methods=["GET"])
def api_game_select():
    genres = ["action","adventure","casual","indie","racing","rpg","simulation","sports","strategy"]
    data = { f"{g}_top15": get_genre_top15(g) for g in genres }
    return jsonify(data)

@main_bp.route("/recommendation/")
def recommendation_page():
    return render_template("recommendation.html")

@main_bp.route("/api/recommendation/", methods=["POST"])
def api_recommendation():
    appids = request.get_json()["game_list"]
    rec = recommend(appids, version=1)
    return jsonify([ dict(r) for r in rec ])

@main_bp.route("/api/recommendation2/", methods=["POST"])
def api_recommendation2():
    appids = request.get_json()["game_list"]
    rec = recommend(appids, version=2)
    return jsonify([ dict(r) for r in rec ])

@main_bp.route("/about_this_game/<int:appid>")
def about_this_game(appid):
    from .models import SteamGameInfo
    game = SteamGameInfo.query.get_or_404(appid)
    return render_template("game_detail.html", game=game)
