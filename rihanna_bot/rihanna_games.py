from bs4 import BeautifulSoup
from selenium import webdriver
url = "https://www.miniclip.com/games/search/en/?query=bounce#privacy-consents"
# search for class='game-icon-component game-icon'. within the class find the link
# find loader-scene


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

    def search_games(self):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')

        driver = webdriver.Chrome(options=options)
        driver.get(self.url)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        game_list = soup.find_all("div", {"class": "game-icon-component game-icon"})
        for game in game_list:
            link = game.find('a').get('href')
            game_obj = self.__get_game_url(link)
            if game_obj:
                return {'display': game_obj, 'say': f'You now play {self.query}. enjoy!'}
        reply = f'Sorry I cannot find {self.query}'
        return {'display': reply, 'say': reply}

    def __get_game_url(self, link):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')

        driver = webdriver.Chrome(options=options)
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
    return {'display': game, 'say': 'You now play tetris. enjoy!'}


def bouncy_dunk():
    game = """<Object width="380px" height="680px"
            <param name="movie" value="https://games.gamepix.com/play/40407?sid=30166">
            <embed SRC="https://games.gamepix.com/play/40264?sid=30166" width="380px" height="680px"
            </embed>
            </object>
            """
    return {'display': game, 'say': f'You now play bouncy dunk. enjoy!'}


# a = selector('game play snake')
# print(a)
