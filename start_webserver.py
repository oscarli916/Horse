from odd_system.scrape import Scraper
from web.app import make_app

app = make_app(Scraper())
app.run(debug=True)