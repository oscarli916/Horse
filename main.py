from datetime import datetime

from odd_system.scrape import Scraper

from web.app import make_app

### Make Scraper Object
scrape = Scraper()
win_place_odds = scrape.get_win_place_odds()
print(win_place_odds)

### Start website
app = make_app(scrape)
app.run(debug=True)
