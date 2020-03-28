import requests
from bs4 import BeautifulSoup
import config

url = "https://www.youtube.com/results?search_query="


def selector(message):
    if message[:len('youtube loop')] == "youtube loop":
        message_ = message[len("youtube loop") + 1:]
        return search_youtube_loop(message_)
    elif message[:len('youtube playlist')] == "youtube playlist":
        message_ = message[len("youtube playlist") + 1:]
        return artist_playlist(message_)
    elif message[:len('youtube choose playlist')] == "youtube choose playlist":
        message_ = message[len("youtube choose playlist") + 1:]
        return choose_playlist(message_)
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
        return {'display': e, 'say': e}


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
        return {'display': e, 'say': e}


def find(search):
    req = url + search
    page = requests.get(req, headers=config.header)
    soup = BeautifulSoup(page.content, 'html.parser')
    load = soup.find("div", {"id": "img-preload"})
    li = load.find_all("img")
    return li[0].get("src").split('/')[4]


def choose_playlist(query):
    try:
        query_list = query.split(',')
        playlist = ''
        for i in query_list:
            playlist += find(i)+','
        display = f'<iframe width="560" height="315"\
                        src="https://www.youtube.com/embed/{playlist.split(",")[0]}?' \
                  f'playlist={playlist[playlist.index(",")+1:-1]}&loop=1" frameborder="0" allowfullscreen>\
                </iframe>'
        say = f"playing a {query} playlist video from youtube"
        reply = {'display': display, 'say': say}
        return reply
    except Exception as e:
        return {'display': e, 'say': e}


# https://www.w3schools.com/html/html_youtube.asp
# artist_playlist('drake')