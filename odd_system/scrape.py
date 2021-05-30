from selenium import webdriver
from bs4 import BeautifulSoup
import json

from odd_system.constants import DATE, HTML_LINK, WIN_JSON_LINK


class Scraper:
    def __init__(self):
        self.date = DATE    # datetime.date type
        self.driver = webdriver.PhantomJS()    # Selenium Driver
        self.venue = self.scrape_venue()    # str type
        self.races = self.scrape_races()    # int type
        self.all_racetime = self.scrape_all_racetime()  # ['12:30', 'xx:xx' , ...]
        
    ### Scrape venue from HTML (selenium: PhantomJS)
    ### Return "ST" / "HV"
    ### str type
    def scrape_venue(self):
        ## Get page source
        self.driver.get(HTML_LINK) # page_source = self.driver.page_source

        ## Scrape venue
        while True:
            try:
                venue = self.driver.find_element_by_xpath("""//*[@id="divMeetingInfo"]/div[1]/div[3]/nobr[2]""").text
                if venue == "沙田":
                    print("[INFO]: Today's venue: ST")
                    return "ST"
                elif venue == "跑馬地":
                    print("[INFO]: Today's venue: HV")
                    return "HV"
                else:
                    # try except? if selenium does not work for the first time?
                    print("[ERROR]: 場地不是 沙田/跑馬地 請到 " + HTML_LINK + " 確認")
                break
            except:
                print("[ERROR]: Element(venue) not found. XPath: //*[@id='divMeetingInfo']/div[1]/div[3]/nobr[2]")
                print("Start Rescrapping...")

    ### Scrape number of races from HTML (selenium: Phantom JS)
    ### Return number of races that day have
    ### int type
    def scrape_races(self):
        ## Get page source
        self.driver.get(HTML_LINK)

        ## Scrape races
        ## Try from race 11 to race 8
        for race in range(11,7,-1):
            try:
                self.driver.find_element_by_xpath("//*[@id='raceSel" + str(race) + "']")
                break
            except:
                pass
        print("[INFO]: Today's number of races: " + str(race))
        return race

    ### Scrape all races' racetime
    ### Return a list of racetime in ascending order
    ### ['xx:xx', 'xx:xx' , ...]
    def scrape_all_racetime(self):
        all_racetime = []
        for race in range(1, self.races+1):
            racetime = self.scrape_racetime(race)
            all_racetime.append(racetime)
        print("[INFO]: All racetime have been scraped Successfully")
        return all_racetime

    ### Scrape racetime by inputing race number from HTML (selenium: Phantom JS)
    ### Return racetime for that race 
    ### str 'xx:xx' type
    def scrape_racetime(self, raceno):
        ## Get page source
        self.driver.get(HTML_LINK + "&venue=" + self.venue + "&raceno=" + str(raceno))

        ## Scrape racetime
        try:
            racetime = self.driver.find_element_by_xpath("""//*[@id="container"]/div/div/div[2]/div[3]/div[1]/span[2]/nobr[2]""").text
            print("[INFO]: Race " + str(raceno) + " racetime scraped successfully")
            return racetime
        except:
            print("[ERROR]: Element(racetime raceno: " + raceno + ") not found. XPath: //*[@id='container']/div/div/div[2]/div[3]/div[1]/span[2]/nobr[2]")

    ### Get win odds json from HTML (selenium: Phantom JS)
    ### Return win odds json
    ### dict type
    def get_win_odds_json(self):
        ## Get page source
        while True:
            try:
                self.driver.get(WIN_JSON_LINK + "&venue=" + self.venue + "&start=1&end=" + str(self.races))
                print("[INFO]: Win Odds Json scrapped Successfully")
                break
            except:
                print("[ERROR]: Scrapping Win Odds Json Failed")
                print("Start Rescrapping...")

        ## Get json content
        win_json = self.driver.find_element_by_tag_name('pre').text
        ## Parse with JSON
        win_json = json.loads(win_json)

        return win_json

    ### Json to an array. Get "OUT" value, split "@@@" and pop the first unrelated element
    ### Return an array with length of number of races
    ### list type, length: number of races
    def win_json_to_list(self, win_json):
        arr = win_json.get("OUT")
        arr = arr.split("@@@")
        arr.pop(0)  # Remove the first unrelated element
        return arr

    def get_win_odds(self):
        ## Get JSON
        win_json = self.get_win_odds_json()
       
        ## JSON to 1Dlist
        win_list = self.win_json_to_list(win_json)
        print(win_list)

        
        for race in range(self.races):
            win_list[race] = win_list[race].split("#")
            win_list[race] = {
                "win": win_list[race][0],
                "pla": win_list[race][1]
            }
        print(win_list)

    # [{"win":[],
    #   "pla":[]},
    # {},
    # {},
    # ...,
    # {}]

    # [
    #     [[],[]],
    #     [[],[]],
    #     [],
    #     ...,
    #     [[],[]]
    # ]