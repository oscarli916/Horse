from datetime import datetime

from odd_system.scrape import Scraper

from web.app import make_app

### Make Scraper Object
scrape = Scraper()
# scrape.get_win_odds()

### Start website
app, socketio = make_app(scrape)
socketio.run(app, debug=True)
