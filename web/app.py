from flask import Flask, render_template

def make_app(scraper):
    app = Flask(__name__)

    @app.route("/")
    def home():
        return render_template("index.html")

    @app.route("/horse_odds")
    def horse_odds():
        return render_template("horse_odds.html", raceno=scraper.races)

    @app.route("/horse_odds/race<string:race>")
    def horse_odds_race(race):
        return render_template(f"horse_odds_{race}.html", race=race)
    
    return app