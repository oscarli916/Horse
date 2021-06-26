import os
import json

class API:
    
    def __init__(self):
        self.api_folder = os.path.dirname(os.path.abspath(__file__))

class HorseOddsAPI(API):

    def __init__(self):
        super().__init__()
        self.api_horse_odds_folder = os.path.join(self.api_folder, r"horse_odds")
        
    ### raceno: str or empty
    def get_horse_odds_json_file_path(self, race: str = "") -> str:
        if race == "":
            return os.path.join(self.api_horse_odds_folder, "all.json")
        return os.path.join(self.api_horse_odds_folder, race + ".json")

    def update_horse_odds_api(self, win_place_odds: dict, count_down: int=0, race_num: int=0) -> None:
        self.update_each_horse_odds_api(win_place_odds, count_down, race_num)
        
        self.update_all_horse_odds_api(win_place_odds, count_down, race_num)

    ### Update each race
    def update_each_horse_odds_api(self, win_place_odds: dict, count_down: int=0, race_num: int=0) -> None:
        for race_odds in win_place_odds:
            print(f"[INFO]: Updating {race_odds}.json file")
            horse_odds_file = self.get_horse_odds_json_file_path(race_odds)
            if os.path.exists(horse_odds_file):
                with open(horse_odds_file, "r") as f:
                    data = json.load(f)
                data["realtime"] = win_place_odds[race_odds]
                if count_down != 0 and race_odds == "Race" + str(race_num):
                    data[str(count_down)] = win_place_odds[race_odds]
            else:
                data = {"realtime":win_place_odds[race_odds]}

            with open(horse_odds_file, "w") as f:
                json.dump(data, f)
    
    ### Update all race
    def update_all_horse_odds_api(self, win_place_odds: dict, count_down: int=0, race_num: int=0) -> None:
        print(f"[INFO]: Updating all.json file")
        horse_odds_file = self.get_horse_odds_json_file_path()
        if os.path.exists(horse_odds_file):
            with open(horse_odds_file, "r") as f:
                data = json.load(f)
            data["realtime"] = win_place_odds
            if count_down != 0:
                data[count_down] = win_place_odds
        else:
            data = {"realtime":win_place_odds}
        with open(horse_odds_file, "w") as f:
            json.dump(data, f)
        
    def remove_all_json_files(self):
        path = self.api_horse_odds_folder
        for f in os.listdir(path):
            file_path = os.path.join(path, f)
            os.remove(file_path)

if __name__ == "__main__":
    # api = API()
    api = HorseOddsAPI()
    print(api.get_horse_odds_file_path("Race1"))
    