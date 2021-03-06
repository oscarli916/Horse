from selenium import webdriver
import json
from datetime import datetime, timedelta
import time

from odd_system.constants import DATE, HTML_LINK, WIN_JSON_LINK
from api.api import HorseOddsAPI

def str_racetime_to_datetime(str_racetime : str) -> datetime:
    now = datetime.now()
    return datetime(now.year, now.month, now.day, int(str_racetime[:2]), int(str_racetime[3:]))

class Scraper:

    update_time = [1,2,3,4,5,6,7,8,9,10,15]

    def __init__(self):
        self.date = DATE    # datetime.date type
        self.driver = webdriver.PhantomJS()    # Selenium Driver
        self.venue = self.scrape_venue()    # str type
        self.races = self.scrape_races()    # int type
        self.all_racetime = self.scrape_all_racetime()  # ['12:30', 'xx:xx' , ...]
        self.all_horses = self.scrape_all_horses() # [14,14,13,...]
        self.api = HorseOddsAPI()

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
            print("[ERROR]: Element(racetime raceno: " + str(raceno) + ") not found. XPath: //*[@id='container']/div/div/div[2]/div[3]/div[1]/span[2]/nobr[2]")

    ### Scrape all races' number of horses
    ### Return a list of number of horses
    ### [14, 14, 13, ...]
    def scrape_all_horses(self):
        all_horses = []
        for race in range(1, self.races+1):
            horses = self.scrape_horses(race)
            all_horses.append(horses)
        print("[INFO]: All horses have been scraped Successfully")
        return all_horses

    ### Scrape number of horses by inputing race number from HTML (selenium: Phantom JS)
    ### Return number of horses for that race 
    ### int type
    def scrape_horses(self, raceno):
        ## Get page source
        self.driver.get(HTML_LINK + "&venue=" + self.venue + "&raceno=" + str(raceno))

         ## Scrape horses
        try:
            tbody = self.driver.find_element_by_xpath("""//*[@id="horseTable"]/tbody""")
            horses = len(tbody.find_elements_by_tag_name("tr")) - 1           
            print("[INFO]: Race " + str(raceno) + " no. of horses scraped successfully")
            return int(horses)
        except:
            print("[ERROR]: Element(horses raceno: " + str(raceno) + ") not found. XPath: //*[@id='horseTable']/tbody")

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
        ## Check JSON is empty
        if win_json["OUT"] == "":
            print("[ERROR]: JSON is empty. Please check the link.")
            return
        return win_json

    ### Json to an array. Get "OUT" value, split "@@@" and pop the first unrelated element.
    ### Then split "#" and ";"
    ### Return a 3D array with length of number of races
    ### list type, length: number of races
    def win_json_to_list(self, win_json):
        arr = win_json["OUT"]
        arr = arr.split("@@@")
        arr.pop(0)  # Remove the first unrelated element

        for race in range(self.races):
            arr[race] = arr[race].split("#")
            arr[race][0] = arr[race][0].split(";")
            arr[race][1] = arr[race][1].split(";")
            arr[race][0].pop(0)
            arr[race][1].pop(0)

        return arr

    ### Put each horse odd into "race_win_odds" and then combine all "race_win_odds"
    ### Return a list. Inside the list have each race's horse's win odd
    ### list type, length: number of races
    def win_odds(self, win_list):
        win_odds = []
        for race in range(self.races):
            race_win_odds = []
            for horse in range(self.all_horses[race]):
                win_list[race][0][horse] = win_list[race][0][horse].split("=")
                win_odd = win_list[race][0][horse][1]
                race_win_odds.append(win_odd)
            win_odds.append(race_win_odds)
        return win_odds

    def place_odds(self, place_list):
        place_odds = []
        for race in range(self.races):
            race_place_odds = []
            for horse in range(self.all_horses[race]):
                place_list[race][1][horse] = place_list[race][1][horse].split("=")
                place_odd = place_list[race][1][horse][1]
                race_place_odds.append(place_odd)
            place_odds.append(race_place_odds)
        return place_odds

    ### Split "=" already. If [2] == "1" then hottest and append
    ### Return a list. Inside the list have each race's hottest horse
    ### list type, length: numnber of races
    def win_hot(self, win_list):
        win_hot = []
        for race in range(self.races):
            for horse in range(self.all_horses[race]):
                horse_hot = win_list[race][0][horse][2]
                horse_num = win_list[race][0][horse][0]
                if horse_hot == "1":
                    win_hot.append(horse_num)
        return win_hot

    def place_hot(self, place_list):
        place_hot = []
        for race in range(self.races):
            for horse in range(self.all_horses[race]):
                horse_hot = place_list[race][1][horse][2]
                horse_num = place_list[race][1][horse][0]
                if horse_hot == "1":
                    place_hot.append(horse_num)
        return place_hot

    ### If [2] == "2" then greenbox and append
    ### If [2] == "3" then brownbox and append
    ### Return 2 list. Inside the list have each race's green/brown box horse number
    ### list type, length: number of races
    def win_green_brown_box(self, win_list):
        win_green_box = []
        win_brown_box = []
        for race in range(self.races):
            green_box = []
            brown_box = []
            for horse in range(self.all_horses[race]):
                horse_colour = win_list[race][0][horse][2]
                horse_num = win_list[race][0][horse][0]
                if horse_colour == "2":
                    green_box.append(horse_num)
                if horse_colour == "3":
                    brown_box.append(horse_num)
            win_green_box.append(green_box)
            win_brown_box.append(brown_box)
        return win_green_box, win_brown_box

    def place_green_brown_box(self, place_list):
        place_green_box = []
        place_brown_box = []
        for race in range(self.races):
            green_box = []
            brown_box = []
            for horse in range(self.all_horses[race]):
                horse_colour = place_list[race][1][horse][2]
                horse_num = place_list[race][1][horse][0]
                if horse_colour == "2":
                    green_box.append(horse_num)
                if horse_colour == "3":
                    brown_box.append(horse_num)
            place_green_box.append(green_box)
            place_brown_box.append(brown_box)
        return place_green_box, place_brown_box

    ### Return each races' win odds, place odds, win hot, place hot, win green box, place green box
    ### dict type
    def get_win_place_odds(self):
        ## Get JSON
        win_json = self.get_win_odds_json()
       
        ## JSON to 3Dlist
        win_list = self.win_json_to_list(win_json)
        # print(win_list)

        ## Get win/place odds
        win_odds = self.win_odds(win_list)
        place_odds = self.place_odds(win_list)

        ## Get win/place hot
        win_hot = self.win_hot(win_list)
        place_hot = self.place_hot(win_list)

        ## Get win/place green box
        win_green_box, win_brown_box = self.win_green_brown_box(win_list)
        place_green_box, place_brown_box = self.place_green_brown_box(win_list)

        win_place_odds = {}
        for race in range(self.races):
            win_place_odds["Race" + str(race + 1)] = {
                "win_odds": win_odds[race],
                "place_odds": place_odds[race],
                "win_hot": win_hot[race],
                "place_hot": place_hot[race],
                "win_green_box": win_green_box[race],
                "place_green_box": place_green_box[race],
                "win_brown_box": win_brown_box[race],
                "place_brown_box": place_brown_box[race],
            }

        # print(win_place_odds)
        return win_place_odds

    def get_q_pla_odds(self):
        pass

    def get_q_pla_odds_race(self, race: int):
        pass

    def auto_scrape(self):
        ### Set []
        all_racetime = self.all_racetime.copy()
        ## Check if [][0] is < now
        now = datetime.now()
        for race in range(len(all_racetime)-1, -1, -1):
            racetime = str_racetime_to_datetime(all_racetime[race])
            racetime = racetime-timedelta(minutes=15)
            if racetime < now:
                all_racetime.pop(race)
        ### Last racetime
        last_racetime = str_racetime_to_datetime(all_racetime[-1])
        
        ### While True/ While now < last racetime + 5
        while now < last_racetime+timedelta(minutes=5):
            print(all_racetime)
            ## If now = [][0] - 15 mins
            upcoming_racetime = str_racetime_to_datetime(all_racetime[0])
            upcoming_scrapetime = upcoming_racetime-timedelta(minutes=15)
            stop_scrapetime = upcoming_racetime+timedelta(minutes=5)
            win_place_odds = self.get_win_place_odds()
            
            ## Get race number
            race_num = self.all_racetime.index(all_racetime[0]) + 1
            print("Race number", race_num)

            if now >= upcoming_scrapetime:
                ## Start insert update: run function (update database)
                minutes_diff = upcoming_racetime - now
                minutes_diff = divmod(minutes_diff.seconds, 60)[0] + 1
                ## If minute difference in update_time, update json
                if minutes_diff in self.update_time:
                    ## Update json
                    self.api.update_horse_odds_api(win_place_odds, count_down=minutes_diff, race_num=race_num)
                else:
                    ## Update realtime odds
                    self.api.update_horse_odds_api(win_place_odds)
            else:
                ## Update realtime odds
                self.api.update_horse_odds_api(win_place_odds)

            ## Update now time
            now = datetime.now()
            ## If now = [][0] + 5 , [].pop(0)
            if now >= stop_scrapetime:
                all_racetime.pop(0)

            time.sleep(5)
            
        ### Remove all json files
        print("[INFO]: Removing all json files")
        self.api.remove_all_json_files()