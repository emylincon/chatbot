import json
import os
from os import path

import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

from rihanna_bot.download_chrome_driver import get_driver


def selector(message: str):
    if message[:len('fighter')] == 'fighter':
        names = message[len('fighter'):].strip().split()
        lastname, firstname, nickname = None, None, None
        for k, v in enumerate(names):
            if v == "_":
                names[k] = None
        if len(names) == 3:
            lastname, firstname, nickname = names
        elif len(names) == 2:
            lastname, firstname = names
        elif len(names) == 1:
            lastname = names[0]
        else:
            reply = 'please do add lastname, firstname, or nickname'
            return {'display': reply, 'say': reply}
        return MMA().display_fighter(firstname=firstname, lastname=lastname, nickname=nickname)


class FighterPicture:
    def __init__(self):
        self.driver = self.get_driver()
        self.base_url = "https://www.espn.co.uk/search/_/q/"

    @staticmethod
    def get_driver():
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        if os.getcwd().split("\\")[-1] == "rihanna_bot":
            driver_path = '../chrome_driver/chromedriver.exe'
        else:
            driver_path = 'chrome_driver/chromedriver.exe'
        try:
            driver = webdriver.Chrome(executable_path=driver_path, options=options)
        except Exception as e:
            print(e)
            get_driver()
            driver = webdriver.Chrome(executable_path=driver_path, options=options)
        return driver

    def get_picture(self, query):
        self.driver.get(self.base_url + query)
        self.driver.find_element_by_xpath('//*[@id="onetrust-close-btn-container"]/button').click()
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        load = soup.find("section", {"class": "Card"})
        img = load.find("img").get('src')
        return img.split("&")[0]


class MMA:
    def __init__(self):
        self.params = dict(key="2ee8f4948b82470c82dd118017bab42d")
        self.data = self.load_fighters()
        self.base_url = "https://api.sportsdata.io/v3/mma"
        self.fightPic = FighterPicture()

    @staticmethod
    def load_fighters():
        try:
            current_dir = path.dirname(__file__)
        except NameError:
            current_dir = ""
        fighters = path.join(current_dir, 'Fighters.json')
        with open(fighters) as json_file:
            data = json.load(json_file, encoding="utf-8")
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

    def __find_fighter(self, firstname=None, lastname=None, nickname=None):
        response = []
        if lastname:
            response = self.data[self.data['LastName'].str.match(lastname, case=False)].to_dict('records')[:5]
        elif firstname:
            response = self.data[self.data['FirstName'].str.match(firstname, case=False)].to_dict('records')[:5]
        elif nickname:
            response = self.data[self.data['Nickname'].str.match(nickname, case=False)].to_dict('records')[:5]
        if len(response) == 0:
            return None
        return response

    @staticmethod
    def __convert_int(text):
        try:
            val = int(text)
            return val
        except ValueError:
            return text

    def display_fighter(self, firstname=None, lastname=None, nickname=None):
        fighter = self.__find_fighter(firstname, lastname, nickname)
        if fighter:
            fighter = fighter[0]
        else:
            reply = f"I am sorry, I could not find fighter"
            return {'display': reply, 'say': reply}
        face = self.fightPic.get_picture(f"{fighter['FirstName'].lower()} {fighter['LastName'].lower()}")
        record = f"{self.__convert_int(fighter['Wins'])}-" \
                 f"{self.__convert_int(fighter['Losses'])}-" \
                 f"{self.__convert_int(fighter['Draws'])}-" \
                 f"{self.__convert_int(fighter['NoContests'])}"
        display_block = f"""
        <div class="card" style="width: 18rem;">
        <img src="{face}" class="card-img-top"
            alt="face">
        <div class="card-body">
            <h5 class="card-title text-center">{fighter['FirstName']} <em>'{fighter['Nickname']}'</em> {fighter['LastName']}</h5>
            <h5 class="card-title text-center"> {record} </h5>
            <p class="text-center">{fighter['WeightClass']}</p>
        </div>

        <table class="table table-hover table-bordered">
        """

        for title in ['Height', 'Reach', 'TechnicalKnockouts', 'TechnicalKnockoutLosses', 'Submissions',
                      'SubmissionLosses', 'TitleWins', 'TitleLosses']:
            display_block += f"""
            <tr>
                <td><b>{title}</b></td>
                <td>{fighter[title]}</td>
            </tr>
            """

        if fighter['CareerStats'] != 'missing':
            for title in ['SigStrikesLandedPerMinute', 'SigStrikeAccuracy', 'TakedownAverage', 'SubmissionAverage',
                          'KnockoutPercentage', 'TechnicalKnockoutPercentage', 'DecisionPercentage']:
                display_block += f"""
                            <tr>
                                <td><b>{title}</b></td>
                                <td>{fighter['CareerStats'][title]}</td>
                            </tr>
                            """

        display_block += """
            </table>
        </div>
        """
        say = f'find below MMA fighter details for {fighter["FirstName"]} {fighter["LastName"]}'
        reply = {'display': display_block, 'say': say}
        return reply


if __name__ == '__main__':
    # print(FighterPicture().get_picture('max holloway'))
    # a = MMA().find_fighter(lastname='holloway')
    # print(json.dumps(a))
    # print(MMA().display_fighter(lastname="holloway"))
    print(MMA().display_fighter(lastname='usman'))
