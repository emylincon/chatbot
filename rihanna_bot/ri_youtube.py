import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import SessionNotCreatedException
import config
from rihanna_bot import youtube_data
from rihanna_bot.download_chrome_driver import get_driver
import json
import random
from rihanna_bot.youtube_sim import youtube_sim_main
from multiprocessing.pool import ThreadPool
from rihanna_bot import hot100_data
from rihanna_bot.rihanna_itunes import Albums
import sys, traceback
import os
import re

def selector(message):
    if message[:len('youtube loop')] == "youtube loop":
        message_ = message[len("youtube loop") + 1:]
        return Youtube().search_youtube_loop(message_)
    elif message[:len('youtube playlist')] == "youtube playlist":
        message_ = message[len("youtube playlist") + 1:]
        return Youtube().artist_playlist(message_)
    elif message == 'youtube a random song':
        return Youtube().random_song()
    elif message[:len('youtube choose playlist')] == "youtube choose playlist":
        message_ = message[len("youtube choose playlist") + 1:]
        return Youtube().choose_playlist(message_)
    elif message == 'youtube popular songs playlist':
        return Youtube().hot_100_playlist()
    elif message == 'youtube songs chart':
        return Youtube().youtube_playlist()
    elif message == 'youtube rihanna playlist':
        return Youtube().rihanna_playlist()
    elif message[:len('youtube popular songs playlist')] == "youtube popular songs playlist":
        no = message.split()[-1]
        return Youtube().hot_100_playlist(no)
    elif message[:len('youtube views for ')] == 'youtube views for ':
        msg = message[len('youtube views for '):]
        return Youtube().youtube_views(msg)
    elif message[:len('youtube album play ')] == 'youtube album play ':
        msg = message[len('youtube album play '):]
        return Youtube().choose_playlist(Albums(msg).track_list())
    elif message[:len('youtube')] == "youtube":
        message_ = message[len("youtube") + 1:]
        return Youtube().search_youtube(message_)
    else:
        reply = "Youtube is offline at the moment. refer to man youtube"
        return {'display': reply, 'say': reply}


class Youtube:
    def __init__(self):
        self.url = "https://www.youtube.com/results?search_query="
        self.u_data = youtube_data.yt_data

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

    def __get_data(self, query):
        driver = self.get_driver()  # driver is used instead of requests because driver gets more output than requests
        req = self.url + query
        driver.get(req)
        driver.find_element_by_xpath(
            xpath='//*[@id="yDmH0d"]/c-wiz/div/div/div/div[2]/div[1]/div[4]/form/div[1]/div/button').click()
        soup = BeautifulSoup(driver.page_source, 'lxml')
        # print(soup)
        load = soup.find_all("script")
        script = None
        for i in load:
            scr = i.string
            # print(scr)
            if scr:
                # if 'window["ytInitialData"]' in scr:
                if 'ytInitialData' in scr:
                    script = i
                    break
        obj = None
        if script:
            variable = re.findall("{.+?(?=;)", script.string)[0]
            try:
                obj = json.loads(variable)
            except json.decoder.JSONDecodeError:
                print('cant decode this')

        else:
            print('no script')
        return obj

    def test_me(self, query):
        print(self.__get_data(query))

    def get_data(self, query):
        obj = self.__get_data(query)
        if obj:
            set_id = 0  # 0 or 1 controls if video has been found
            changed = 0  # 0 or 1 controls if youtube data content has changed
            result = ''
            contents = \
                obj['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents'][
                    0][
                    'itemSectionRenderer']['contents']
            for data in contents:
                if 'videoRenderer' in data:
                    vid_data = data['videoRenderer']
                    if set_id == 0:
                        result = vid_data['title']['runs'][0]['text'].replace('- ', '').lower()
                        vid = vid_data['videoId']
                        vid_name = vid_data['title']['runs'][0]['text'].replace('- ', '').lower()
                        vid_length = vid_data['lengthText']['accessibility']['accessibilityData']['label']
                        vid_views = vid_data['viewCountText']['simpleText']
                        if vid_name not in self.u_data:
                            self.u_data[vid_name] = {'videoID': vid, 'videoTitle': vid_name.title(),
                                                     'videoLength': vid_length, 'videoViews': vid_views}
                            changed = 1
                        set_id = 1
                        break
                    else:
                        vid_name = vid_data['title']['runs'][0]['text'].replace('- ', '').lower()
                        if vid_name not in self.u_data:
                            vid_data = data['videoRenderer']
                            vid_ = vid_data['videoId']
                            vid_length = vid_data['lengthText']['accessibility']['accessibilityData']['label']
                            vid_views = vid_data['viewCountText']['simpleText']
                            self.u_data[vid_name] = {'videoID': vid_, 'videoTitle': vid_name.title(),
                                                     'videoLength': vid_length, 'videoViews': vid_views}
                            changed = 1

            if changed == 1:
                path = r'C:\Users\emyli\PycharmProjects\Chatbot_Project\rihanna_bot\youtube_data.py'
                file = open(path, 'w', encoding='utf-8')
                file.write(f'yt_data = {self.u_data}\n')
                file.write(f'data_length = {len(self.u_data)}\n')
                file.close()
            if result in self.u_data:
                return self.u_data[result]
            else:
                print('result not in data')
                return None
        else:
            return None

    def get_artist_data(self, query):
        obj = self.__get_data(query)
        # print(json.dumps(obj))
        if obj:
            changed = 0  # 0 or 1 controls if youtube data content has changed
            data_ = ''
            cont = obj['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents']
            length = len(cont)
            for i in range(length):
                contents = cont[i]['itemSectionRenderer']['contents']
                for data in contents:
                    if 'videoRenderer' in data:
                        vid_data = data['videoRenderer']
                        result = vid_data['title']['runs'][0]['text'].replace('- ', '').lower()
                        vid = vid_data['videoId']
                        vid_name = vid_data['title']['runs'][0]['text'].replace('- ', '').lower()
                        vid_length = vid_data['lengthText']['accessibility']['accessibilityData']['label']
                        vid_views = vid_data['viewCountText']['simpleText']
                        if vid_name not in self.u_data:
                            self.u_data[vid_name] = {'videoID': vid, 'videoTitle': vid_name.title(),
                                                     'videoLength': vid_length, 'videoViews': vid_views}
                            changed = 1
                        data_ += f'{vid},'
                if data_ != '':
                    break
            if changed == 1:
                file = open('youtube_data.py', 'w', encoding='utf-8')
                file.write(f'yt_data = {self.u_data}\n')
                file.write(f'data_length = {len(self.u_data)}\n')
                file.close()
            return data_[:-1]
        else:
            return None

    def search_youtube(self, query):
        try:
            sim_dict = youtube_sim_main(query)
            if sim_dict == 0:
                you_dict = self.get_data(query)
                if you_dict:

                    display = f'<iframe width="600" height="335"\
                                    src="https://www.youtube.com/embed/{you_dict["videoID"]}?rel=0" ' \
                              f'allow="autoplay" frameborder="0" allowfullscreen>\
                                    </iframe>'
                    say = f"playing {you_dict['videoTitle']} video from youtube"
                    reply = {'display': display, 'say': say}
                    return reply

                else:
                    reply = f"Sorry, I couldn't find {query}"
                    return {'display': reply, 'say': reply}
            else:
                # link = "https://www.youtube.com/watch?v=" + vid
                display = f'<iframe width="600" height="335"\
                                                src="https://www.youtube.com/embed/{sim_dict["videoID"]}?rel=0" ' \
                          f'allow="autoplay" frameborder="0" allowfullscreen>\
                                                </iframe>'
                say = f"playing {sim_dict['videoTitle']} video from youtube"
                reply = {'display': display, 'say': say}
                return reply
        except:
            traceback.print_exc()
            exc_type, exc_value, exc_traceback = sys.exc_info()
            reply = f'rihanna detected a bug in choose playlist: {exc_value}'
            return {'display': reply, 'say': reply}

    def search_youtube_loop(self, query):
        sim_dict = youtube_sim_main(query)
        if sim_dict == 0:
            you_dict = self.get_data(query)
            if you_dict:
                display = f'<iframe width="560" height="315" src="https://www.youtube.com/embed/{you_dict["videoID"]}?' \
                          f'playlist={you_dict["videoID"]}&loop=1" frameborder="0" allowfullscreen>\
                                                </iframe>'
                say = f"playing {you_dict['videoTitle']} video from youtube in a loop"
                reply = {'display': display, 'say': say}
                return reply

            else:
                reply = f"Sorry, I couldn't find {query}"
                return {'display': reply, 'say': reply}
        else:
            # link = "https://www.youtube.com/watch?v=" + vid
            display = f'<iframe width="560" height="315"\
                                src="https://www.youtube.com/embed/{sim_dict["videoID"]}?' \
                      f'playlist={sim_dict["videoID"]}&loop=1" frameborder="0" allowfullscreen>\
                                </iframe>'
            say = f"playing {sim_dict['videoTitle']} video from youtube in a loop"
            reply = {'display': display, 'say': say}
            return reply

    def artist_playlist(self, query):
        try:
            playlist = self.get_artist_data(query)
            # print('playlist:', playlist)
            if playlist:
                display = f'<iframe width="560" height="315" src="https://www.youtube.com/embed/{playlist.split(",")[0]}?' \
                          f'playlist={playlist[playlist.index(",") + 1:]}&loop=1" frameborder="0" allowfullscreen>\
                                                </iframe>'
                say = f"playing a {query} playlist video from youtube"
                reply = {'display': display, 'say': say}
                return reply

            else:
                reply = f"Sorry, I couldn't find {query}"
                return {'display': reply, 'say': reply}
        except:
            traceback.print_exc()
            exc_type, exc_value, exc_traceback = sys.exc_info()
            reply = f'rihanna detected a bug in Youtube.artist_playlist: {exc_value}'
            return {'display': reply, 'say': reply}

    def choose_playlist(self, query):
        try:
            query_list = query.split(',')
            result_list = []
            pool = ThreadPool(processes=len(query_list))
            for i in query_list:
                sim_dict = youtube_sim_main(i)
                if sim_dict == 0:
                    result_list.append(pool.apply_async(self.get_data, (i,)))
                else:
                    result_list.append(sim_dict)
            playlist = ''
            for i in result_list:
                if type(i).__name__ == 'dict':
                    playlist += f"{i['videoID']},"
                else:
                    item = i.get()
                    if item:
                        playlist += item['videoID'] + ','
            display = f'<iframe width="560" height="315"\
                            src="https://www.youtube.com/embed/{playlist.split(",")[0]}?' \
                      f'playlist={playlist[playlist.index(",") + 1:-1]}&loop=1" frameborder="0" allowfullscreen>\
                    </iframe>'
            say = f"playing a {query} playlist video from youtube"
            reply = {'display': display, 'say': say}
            return reply
        except:
            traceback.print_exc()
            exc_type, exc_value, exc_traceback = sys.exc_info()
            reply = f'rihanna detected a bug in choose playlist: {exc_value}'
            return {'display': reply, 'say': reply}

    def youtube_playlist(self):
        req = self.url + 'chart'
        page = requests.get(req, headers=config.header)
        soup = BeautifulSoup(page.content, 'lxml')

        load = soup.find_all("script")
        script = None
        for i in load:
            scr = i.string
            if scr:
                # if 'window["ytInitialData"]' in scr:
                if 'ytInitialData' in scr:
                    script = i
                    break
        # script = load[-2].string
        if script:
            lscript = script.string.split(';')
            variable = lscript[0].strip().split(' = ')[1]

            obj = json.loads(variable)
            contents = \
                obj['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents'][
                    0][
                    'itemSectionRenderer']['contents']
            for data in contents:
                if 'playlistRenderer' in data:
                    # print(data.keys())
                    vid_data = data['playlistRenderer']
                    playlist_id = vid_data['playlistId']
                    title = vid_data['title']['simpleText']
                    display = f'<iframe width="560" height="315" ' \
                              f'src="https://www.youtube.com/embed/videoseries?list={playlist_id}&loop=1 ' \
                              f'frameborder="0" allowfullscreen"></iframe>'
                    say = f'Now playing {title}'
                    return {'display': display, 'say': say}
                else:
                    return {'display': '<iframe width="560" height="315" '
                                       'src="https://www.youtube.com/embed/videoseries?list=PLywWGW4ILrvpqqkgKRV8jpZ'
                                       'MaUPohQipP&loop=1 frameborder="0" allowfullscreen"></iframe>',
                            'say': 'Now playing Official UK Top 100 Singles Chart (Top 40 Songs) '
                                   'Week Ending 16th April 2020'}

        else:
            return {'display': '<iframe width="560" height="315" '
                               'src="https://www.youtube.com/embed/videoseries?list=PLywWGW4ILrvpqqkgKRV8jpZ'
                               'MaUPohQipP&loop=1 frameborder="0" allowfullscreen"></iframe>',
                    'say': 'Now playing Official UK Top 100 Singles Chart (Top 40 Songs) '
                           'Week Ending 16th April 2020'}

    @staticmethod
    def rihanna_playlist():
        return {'display': '<iframe width="560" height="315" '
                           'src="https://www.youtube.com/embed/videoseries?'
                           'list=PL2oLK9yB8WKVahzI1Akf1_zwPnmmAbFow&loop=1 frameborder="0" allowfullscreen"></iframe>',
                'say': 'Now playing Rihanna Demo playlist on youtube'}

    def random_song(self):
        song = random.choice(list(self.u_data.values()))
        display = f'<iframe width="560" height="315"\
                                                    src="https://www.youtube.com/embed/{song["videoID"]}?rel=0" ' \
                  f'allow="autoplay" frameborder="0" allowfullscreen>\
                                        </iframe>'
        say = f"playing selected random song {song['videoTitle']} video from youtube"
        reply = {'display': display, 'say': say}
        return reply

    @staticmethod
    def hot_100_playlist(no=None):
        if no:
            try:
                no = int(no)
                play = list(hot100_data.hot_songs.values())[:no]
                playlist = ''
                for vid in play:
                    playlist += vid['url'].split('v=')[1] + ','

                display = f'<iframe width="560" height="315"\
                                            src="https://www.youtube.com/embed/{playlist.split(",")[0]}?' \
                          f'playlist={playlist[playlist.index(",") + 1:-1]}&loop=1" frameborder="0" allowfullscreen>\
                        </iframe>'
                say = f"playing hot 100 songs from youtube"
                reply = {'display': display, 'say': say}
                return reply

            except ValueError:
                play = list(hot100_data.hot_songs.values())[:no]
                playlist = ''
                for vid in play:
                    playlist += vid['url'].split('v=')[1] + ','

                display = f'<iframe width="560" height="315"\
                            src="https://www.youtube.com/embed/{playlist.split(",")[0]}?' \
                          f'playlist={playlist[playlist.index(",") + 1:-1]}&loop=1" frameborder="0" allowfullscreen>\
                        </iframe>'
                say = f"playing hot 100 songs from youtube"
                reply = {'display': display, 'say': say}
                return reply
        else:
            play = list(hot100_data.hot_songs.values())[:no]
            playlist = ''
            for vid in play:
                if 'v=' in vid['url']:
                    playlist += vid['url'].split('v=')[1] + ','
                else:
                    print(vid)

            display = f'<iframe width="560" height="315"\
                        src="https://www.youtube.com/embed/{playlist.split(",")[0]}?' \
                      f'playlist={playlist[playlist.index(",") + 1:-1]}&loop=1" frameborder="0" allowfullscreen>\
                    </iframe>'
            say = f"playing hot 100 songs from youtube"
            reply = {'display': display, 'say': say}
            return reply

    def youtube_views(self, query):
        driver = self.get_driver()      # driver is used instead of requests because driver gets more output than requests
        req = self.url + query
        driver.get(req)
        soup = BeautifulSoup(driver.page_source, 'lxml')

        load = soup.find_all("script")
        script = None
        # print(load)
        for i in load:
            scr = i.string
            if scr:
                # if 'window["ytInitialData"]' in scr:
                if 'ytInitialData' in scr:
                    script = i
                    break

        if script:
            lscript = script.string.split(';')
            variable = lscript[0].strip().split(' = ')[1]
            try:
                obj = json.loads(variable)
            except json.decoder.JSONDecodeError:
                return None
            set_id = 0  # 0 or 1 controls if video has been found
            changed = 0  # 0 or 1 controls if youtube data content has changed
            result = ''
            vid_time = ''
            contents = \
                obj['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents'][
                    0][
                    'itemSectionRenderer']['contents']
            for data in contents:
                if 'videoRenderer' in data:
                    vid_data = data['videoRenderer']
                    if set_id == 0:
                        result = vid_data['title']['runs'][0]['text'].replace('- ', '').lower()
                        vid = vid_data['videoId']
                        vid_name = vid_data['title']['runs'][0]['text'].replace('- ', '').lower()
                        vid_length = vid_data['lengthText']['accessibility']['accessibilityData']['label']
                        vid_views = vid_data['viewCountText']['simpleText']
                        vid_time = vid_data['publishedTimeText']['simpleText']
                        if vid_name not in self.u_data:
                            self.u_data[vid_name] = {'videoID': vid, 'videoTitle': vid_name.title(),
                                                     'videoLength': vid_length, 'videoViews': vid_views}
                            changed = 1
                        set_id = 1
                        break

            if changed == 1:
                file = open('youtube_data.py', 'w', encoding='utf-8')
                file.write(f'yt_data = {self.u_data}\n')
                file.write(f'data_length = {len(self.u_data)}\n')
                file.close()
            if vid_time != '':
                reply = f"{vid_name.title()} has accumulated {vid_views} since it was posted {vid_time}"
                return {'display': reply, 'say': reply}
            else:
                reply = 'I cannot find video'
                return {'display': reply, 'say': reply}
        else:
            reply = 'I cannot find video'
            return {'display': reply, 'say': reply}

# https://www.w3schools.com/html/html_youtube.asp
# artist_playlist('drake')
# g = "Future Featuring Drake Life Is Good,Post Malone Circles,Arizona Zervas Roxanne,Harry Styles Adore You,Justin Bieber Featuring Quavo Intentions,Lewis Capaldi Someone You Loved,Billie Eilish everything i wanted,blackbear Hot Girl Bummer,Maroon 5 Memories,Lil Uzi Vert Myron"
# a = choose_playlist(g)
# print(a)
# a = youtube_playlist()
# a = Youtube().search_youtube('drake one dance')
# a = Youtube().artist_playlist('post malone')
# a = Youtube().random_song()
# a = Youtube().choose_playlist('drake club paradise, drake draft day, drake 5pm in toronto, drake war, drake do not disturb, drake mob ties')
# a = Youtube().hot_100_playlist()
# a = Youtube().search_youtube_loop('6ix9ine gooba')
# # a = Youtube().youtube_playlist()
# a = Youtube().youtube_views('toosie slide drake')
# print(a)


if __name__ == "__main__":
    # a = Youtube().search_youtube('love yours')
    a = Youtube().artist_playlist('post malone')
    print('Reply ->', a)
    # Youtube().test_me('post malone')