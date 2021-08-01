import requests
import pandas as pd
from os import path
import json


def selector(message: str):
    if message[:len('mma')] == 'mma':
        pass


class MMA:
    def __init__(self):
        self.params = dict(key="2ee8f4948b82470c82dd118017bab42d")
        self.data = self.load_fighters()
        self.base_url = "https://api.sportsdata.io/v3/mma"

    @staticmethod
    def load_fighters():
        current_dir = path.dirname(__file__)
        fighters = path.join(current_dir, 'Fighters.json')
        with open(fighters) as json_file:
            data = json.load(json_file)
            df = pd.DataFrame(data)
            df = df.fillna('missing')
            return df

    def fight_schedule(self, year=2021):  # hourly request
        url = f"{self.base_url}/scores/json/Schedule/ufc/{year}"
        response = requests.get(url=url, params=self.params)
        return response

    def event(self, event_id):  # Minute request
        url = f"{self.base_url}/scores/json/Event/ufc/{event_id}"
        response = requests.get(url=url, params=self.params)
        return response

    def find_fighter(self, firstname=None, lastname=None, nickname=None):
        if lastname:
            return self.data[self.data['LastName'].str.match(lastname, case=False)].to_dict('records')[:5]
        elif firstname:
            return self.data[self.data['FirstName'].str.match(firstname, case=False)].to_dict('records')[:5]
        elif nickname:
            return self.data[self.data['Nickname'].str.match(nickname, case=False)].to_dict('records')[:5]


if __name__ == '__main__':
    print(MMA.load_fighters())
