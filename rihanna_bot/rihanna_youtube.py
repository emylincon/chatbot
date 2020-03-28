import requests
from bs4 import BeautifulSoup
import config
from rihanna_bot import hot100
import json
from multiprocessing.pool import ThreadPool

url = "https://www.youtube.com/results?search_query="


def selector(message):
    if message[:len('youtube loop')] == "youtube loop":
        message_ = message[len("youtube loop") + 1:]
        return search_youtube_loop(message_)
    elif message[:len('youtube playlist')] == "youtube playlist":
        message_ = message[len("youtube playlist") + 1:]
        return artist_playlist(message_)
    elif message == 'youtube a random song':
        return random_song()
    elif message[:len('youtube choose playlist')] == "youtube choose playlist":
        message_ = message[len("youtube choose playlist") + 1:]
        return choose_playlist(message_)
    elif message == 'youtube popular songs playlist':
        return hot_100_playlist()
    elif message == 'youtube songs chart':
        return youtube_playlist()
    elif message[:len('youtube popular songs playlist')] == "youtube popular songs playlist":
        no = message.split()[-1]
        return hot_100_playlist(no)
    elif message[:len('youtube')] == "youtube":
        message_ = message[len("youtube") + 1:]
        return search_youtube(message_)
    else:
        reply = "Youtube is offline at the moment. refer to man youtube"
        return {'display': reply, 'say': reply}


def search_youtube(query):
    try:
        req = url + query
        page = requests.get(req, headers=config.header)
        soup = BeautifulSoup(page.content, 'html.parser')
        load = soup.find("div", {"id": "img-preload"})
        li = load.find_all("img")
        vid = li[0].get("src").split('/')[4]
        # link = "https://www.youtube.com/watch?v=" + vid
        display = f'<iframe width="560" height="315"\
                src="https://www.youtube.com/embed/{vid}?rel=0" allow="autoplay" frameborder="0" allowfullscreen>\
                </iframe>'
        say = f"playing {query} video from youtube"
        reply = {'display': display, 'say': say}
        return reply
    except Exception as e:
        return {'display': e, 'say': e}


def search_youtube_loop(query):
    try:
        req = url + query
        page = requests.get(req, headers=config.header)
        soup = BeautifulSoup(page.content, 'html.parser')
        load = soup.find("div", {"id": "img-preload"})
        li = load.find_all("img")
        vid = li[0].get("src").split('/')[4]
        # link = "https://www.youtube.com/watch?v=" + vid
        display = f'<iframe width="560" height="315"\
                src="https://www.youtube.com/embed/{vid}?playlist={vid}&loop=1" frameborder="0" allowfullscreen>\
                </iframe>'
        say = f"playing {query} video from youtube in a loop"
        reply = {'display': display, 'say': say}
        return reply
    except Exception as e:
        return {'display': str(e), 'say': str(e)}


def artist_playlist(query):
    try:
        req = url + query
        page = requests.get(req, headers=config.header)
        soup = BeautifulSoup(page.content, 'html.parser')
        load = soup.find("div", {"id": "img-preload"})
        playlist = ''
        li = load.find_all("img")
        # print(li)
        for link in li:
            try:
                ink = link.get("src")
                if ink[:2] != '//':
                    playlist += ink.split('/')[4]+','
            except Exception:
                pass
        # link = "https://www.youtube.com/watch?v=" + vid
        display = f'<iframe width="560" height="315"\
                src="https://www.youtube.com/embed/{playlist.split(",")[0]}?' \
                  f'playlist={playlist[playlist.index(",")+1:-1]}&loop=1" frameborder="0" allowfullscreen>\
                </iframe>'
        say = f"playing a {query} playlist video from youtube"
        reply = {'display': display, 'say': say}
        # print(reply['display'])
        return reply
    except Exception as e:
        return {'display': str(e), 'say': str(e)}


def find(search):
    req = url + search
    page = requests.get(req, headers=config.header)
    soup = BeautifulSoup(page.content, 'html.parser')
    load = soup.find("div", {"id": "img-preload"})
    if load:
        li = load.find_all("img")
        try:
            return li[0].get("src").split('/')[4]
        except IndexError:
            return None
    else:
        return None


def choose_playlist(query):
    try:
        query_list = query.split(',')
        result_list = []
        pool = ThreadPool(processes=len(query_list))
        for i in query_list:
            result_list.append(pool.apply_async(find, (i,)))
        playlist = ''
        for i in result_list:
            item = i.get()
            if item:
                playlist += item + ','
        display = f'<iframe width="560" height="315"\
                        src="https://www.youtube.com/embed/{playlist.split(",")[0]}?' \
                  f'playlist={playlist[playlist.index(",")+1:-1]}&loop=1" frameborder="0" allowfullscreen>\
                </iframe>'
        say = f"playing a {query} playlist video from youtube"
        reply = {'display': display, 'say': say}
        return reply
    except Exception as e:
        return {'display': str(e), 'say': str(e)}


def random_song():
    song = hot100.Music().random_song()
    return search_youtube(song)


def hot_100_playlist(no=None):
    if no:
        try:
            no = int(no)
            playlist = hot100.Music().playlist(no)
            # print(playlist)
            return choose_playlist(playlist)
        except ValueError:
            playlist = hot100.Music().playlist()
            return choose_playlist(playlist)
    else:
        playlist = hot100.Music().playlist()
        # print(playlist)
        return choose_playlist(playlist)


def youtube_playlist():
    req = url + 'chart'
    page = requests.get(req, headers=config.header)
    soup = BeautifulSoup(page.content, 'lxml')

    load = soup.find_all("script")
    script = None
    for i in load:
        scr = i.string
        if scr:
            if 'window["ytInitialData"]' in scr:
                script = i
                break
    # script = load[-2].string
    if script:
        lscript = script.string.split(';')
        variable = lscript[0].strip().split(' = ')[1]

        obj = json.loads(variable)
        first_content = obj['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRend' \
                                                                                             'erer']['contents'][0]
        playlist_id = first_content['itemSectionRenderer']['contents'][0]['playlistRenderer']['playlistId']
        title = first_content['itemSectionRenderer']['contents'][0]['playlistRenderer']['title']['simpleText']
        # print(playlist_id, title)

        display = f'<iframe width="560" height="315" ' \
                  f'src="https://www.youtube.com/embed/videoseries?list={playlist_id}&loop=1 ' \
                  f'frameborder="0" allowfullscreen"></iframe>'
        say = f'Now playing {title}'
        return {'display': display, 'say': say}
    else:
        return {'display': '<iframe width="560" height="315" '
                           'src="https://www.youtube.com/embed/videoseries?'
                           'list=PLywWGW4ILrvpqqkgKRV8jpZMaUPohQipP&loop=1 frameborder="0" allowfullscreen"></iframe>',
                'say': 'Now playing Official UK Top 100 Singles Chart (Top 40 Songs) Week Ending 2nd April 2020'}


# https://www.w3schools.com/html/html_youtube.asp
# artist_playlist('drake')
# g = "Future Featuring Drake Life Is Good,Post Malone Circles,Arizona Zervas Roxanne,Harry Styles Adore You,Justin Bieber Featuring Quavo Intentions,Lewis Capaldi Someone You Loved,Billie Eilish everything i wanted,blackbear Hot Girl Bummer,Maroon 5 Memories,Lil Uzi Vert Myron"
# a = choose_playlist(g)
# print(a)
# a = youtube_playlist()
# print(a)
