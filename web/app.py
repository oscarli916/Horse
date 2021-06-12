from flask import Flask, render_template, jsonify
from api.api import HorseOddsAPI
import json

def make_app(scraper):
    app = Flask(__name__)
    api = HorseOddsAPI()

    ### Website
    @app.route("/")
    def home():
        return render_template("index.html")

    @app.route("/horse_odds")
    def horse_odds():
        return render_template("horse_odds.html", raceno=scraper.races)

    @app.route("/horse_odds/race<string:race>")
    def horse_odds_race(race):
        return render_template(f"horse_odds_{race}.html", race=race)
    
    ### API
    @app.route("/api/horse_odds", defaults={"race":""})
    @app.route("/api/horse_odds/<string:race>")
    def api_horse_odds(race):
        if race == "":
            horse_odds_file = api.get_horse_odds_json_file_path()
        else:
            horse_odds_file = api.get_horse_odds_json_file_path(race)
        with open(horse_odds_file, "r") as f:
            data = json.load(f)
        return jsonify(data)

    return app