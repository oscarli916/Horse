# from datetime import datetime

from odd_system.scrape import Scraper

from web.app import make_app

from api.api import HorseOddsAPI

### Make Scraper Object
scrape = Scraper()
win_place_odds = scrape.get_win_place_odds()
print(win_place_odds)

### Make API Object
api = HorseOddsAPI()
api.update_horse_odds_api(win_place_odds)

### Start website + api
app = make_app(scrape)
app.run(debug=True)
