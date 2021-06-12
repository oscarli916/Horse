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

    def update_horse_odds_api(self, win_place_odds: dict) -> None:
        self.update_each_horse_odds_api(win_place_odds)
        
        self.update_all_horse_odds_api(win_place_odds)

    ### Update each race
    def update_each_horse_odds_api(self, win_place_odds: dict) -> None:
        for race_odds in win_place_odds:
            print(f"[INFO]: Updating {race_odds}.json file")
            horse_odds_file = self.get_horse_odds_json_file_path(race_odds)
            with open(horse_odds_file, "w") as f:
                json.dump(win_place_odds[race_odds], f)
    
    ### Update all race
    def update_all_horse_odds_api(self, win_place_odds: dict) -> None:
        print(f"[INFO]: Updating all.json file")
        horse_odds_file = self.get_horse_odds_json_file_path()
        with open(horse_odds_file, "w") as f:
            json.dump(win_place_odds, f)

if __name__ == "__main__":
    # api = API()
    api = HorseOddsAPI()
    print(api.get_horse_odds_file_path("Race1"))
    