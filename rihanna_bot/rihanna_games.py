from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import SessionNotCreatedException
from rihanna_bot.download_chrome_driver import get_driver
import os


def selector(query):
    if query == 'game play tetris':
        return tetris()
    elif query == 'game play bouncy dunk':
        return bouncy_dunk()
    elif query[:len('game play ')] == 'game play ':
        name = query[len('game play '):]
        return Games(name).search_games()


class Games:
    def __init__(self, query):
        self.query = query
        self.url = f"https://www.miniclip.com/games/search/en/?query={query}#privacy-consents"

    @staticmethod
    def __game_link(link):
        return f"https://www.miniclip.com{link}#privacy-consents"

    @staticmethod
    def get_driver():
        options = webdriver.ChromeOptions()
        options.add_argument('headless')

        try:
            chrome_p = os.listdir('chrome_driver/')[0]
            chrome_path = f'chrome_driver/{chrome_p}'
        except FileNotFoundError:
            chrome_p = os.listdir('../chrome_driver/')[0]
            chrome_path = f'../chrome_driver/{chrome_p}'

        try:
            driver = webdriver.Chrome(chrome_path, options=options)
        except SessionNotCreatedException:
            get_driver()
            driver = webdriver.Chrome(chrome_path, options=options)

        return driver

    def search_games(self):
        driver = self.get_driver()
        driver.get(self.url)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        game_list = soup.find_all("div", {"class": "game-icon-component game-icon"})
        for game in game_list:
            link = game.find('a').get('href')
            game_obj = self.__get_game_url(link)
            if game_obj:
                return {'display': game_obj, 'say': f'You can now play {self.query}. enjoy!'}
        reply = f'Sorry I cannot find {self.query}'
        return {'display': reply, 'say': reply}

    def __get_game_url(self, link):
        driver = self.get_driver()
        req = self.__game_link(link)
        driver.get(req)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        load = soup.find("div", {"class": "loader-scene"})
        try:
            value = load.find('form').get('action')
            div_style = soup.find("div", {"class": "loader-container"}).get('style')
            return self.game_frame(value=value, style=div_style)
        except:
            return None

    @staticmethod
    def game_frame(value, style):
        game = f"""<Object style="{style}"
                    <param name="movie" value="{value}">
                    <embed SRC="{value}" style="{style}"
                    </embed>
                    </object>
                    """
        return game


def tetris():
    game = """<Object width="350px" height="600px"
            <param name="movie" value="https://games.gamepix.com/play/40264?sid=30166">
            <embed SRC="https://games.gamepix.com/play/40264?sid=30166" width="350px" height="600px"
            </embed>
            </object>
            """
    return {'display': game, 'say': 'You can now play tetris. enjoy!'}


def bouncy_dunk():
    game = """<Object width="380px" height="680px"
            <param name="movie" value="https://games.gamepix.com/play/40407?sid=30166">
            <embed SRC="https://games.gamepix.com/play/40407?sid=30166" width="380px" height="680px"
            </embed>
            </object>
            """
    return {'display': game, 'say': f'You can now play bouncy dunk. enjoy!'}


# a = selector('game play snake')
# print(a)
# https://www.miniclip.com/games/strike-force-heroes/en/#privacy-consents

# a = 'https://www.miniclip.com/games/strike-force-heroes/en/#privacy-consents'
# options = webdriver.ChromeOptions()
# options.add_argument('headless')
#
# driver = webdriver.Chrome(options=options)
# req = a
# driver.get(req)
# soup = BeautifulSoup(driver.page_source, 'lxml')
# load = soup.find("div", {"class": "loader-scene"})
# try:
#     value = load.find('form').get('action')
#     div_style = soup.find("div", {"class": "loader-container"}).get('style')
#     g = Games('yes')
#     print(g.game_frame(value=value, style=div_style))
# except:
#     print('no')