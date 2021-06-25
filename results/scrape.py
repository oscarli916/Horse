from os import scandir
from selenium import webdriver
import pandas as pd
import logging
from typing import List

from constants import RESULT_URL

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s [%(levelname)s]: %(message)s",)


class ResultScraper():
    def __init__(self, date) -> None:
        self.driver = webdriver.PhantomJS()
        self.date = date
        self.venue = self.scrape_venue()
        self.races = self.scrape_races()


    def scrape_venue(self) -> str:
        """
        Return venue of the result date: (one of three)
            * "ST",
            * "HV",
            * "" 

        XPath:
            /html/body/div/div[2]/table/tbody/tr/td[1]/span
            /html/body/div/div[2]/table/tbody/tr[1]/td[1]/span
        """
        logging.info("Scrapping venue")
        ### Get page
        result_url = RESULT_URL + "RaceDate=" + self.date
        self.driver.get(result_url)

        ### Scrape venue
        while True:
            ## Try except to prevent find element have error
            try:
                venue = self.driver.find_element_by_xpath("""/html/body/div/div[2]/table/tbody/tr/td[1]/span""").text
                if venue == "沙田:":
                    logging.info("Venue is ST")
                    return "ST"
                elif venue =="跑馬地:":
                    logging.info("Venue is HV")
                    return "HV"
                else:
                    logging.error("場地不是 沙田/跑馬地 請到 " + result_url + " 確認")
                    return ""
            except:
                logging.error("Element(venue) not found. XPath: /html/body/div/div[2]/table/tbody/tr/td[1]/span")
                logging.info("Start Rescrapping...")

    def scrape_races(self) -> int:
        """
        Return number of races of the result date

        XPath:
        /html/body/div/div[2]/table/tbody/tr/td[VARIABLE]
        """
        logging.info("Scrapping number of races")
        ### Get page
        result_url = RESULT_URL + "RaceDate=" + self.date + "&Racecourse=" + self.venue
        self.driver.get(result_url)

        ### Scrape number of races
        ## For loop from race 11 to race 8
        for race in range(12,9,-1):
            ## Try except to prevent find element have error
            try:
                self.driver.find_element_by_xpath(f"""/html/body/div/div[2]/table/tbody/tr/td[{str(race)}]""")
                break
            except:
                pass
        logging.info("Number of races is " + str(race-2))
        return race-2

    def scrape_race_result(self, race: int):
        """
        """
        logging.info("Scrapping Race%s result", race)

        ### Get page
        result_url = RESULT_URL + "RaceDate=" + self.date + "&Racecourse=" + self.venue + "&RaceNo=" + str(race)
        self.driver.get(result_url)

        ### Get 總場次

        ### Get race info
        race_info = self.scrape_race_info(xpath="""/html/body/div/div[4]/table/tbody/tr[2]/td[1]""")
        class_, distance, apply_score1, apply_score2 = self.split_race_info(race_info)
        apply_score = self.combine_apply_score(s1=apply_score1, s2=apply_score2)
        print(apply_score)

    def scrape_race_info(self, xpath: str) -> str:
        """
        Return race info

        e.g. "第四班 - 1200米 - (60-40)"
        """
        logging.info("Scrapping race info")
        return self.driver.find_element_by_xpath(xpath).text

    def split_race_info(self, race_info: str) -> List[str]:
        """
        Return splitted race info and remove spaces
        """
        logging.info("Splitting race info")
        split = race_info.split("-")
        for i in range(len(split)):
            split[i] = split[i].strip()
        return split

    def combine_apply_score(self, s1: str, s2: str) -> str:
        """
        Return combined 報名評分

        Args:
            s1: e.g. '(60'
            s2: e.g. '40)'
        """
        s1_index = s1.index("(")
        s2_index = s2.index(")")
        return s2[:s2_index] + "-" + s1[s1_index+1:]

if __name__ == "__main__":
    date = input("Please Enter Result Date (e.g. 2021/06/23): ")
    scraper = ResultScraper(date)
    scraper.scrape_race_result(race=1)

