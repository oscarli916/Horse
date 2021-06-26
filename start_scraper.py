import logging

from odd_system.scrape import Scraper

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s [%(levelname)s]: %(message)s",)

scrape = Scraper()
logging.info("Starting Auto Scrape")
scrape.auto_scrape()