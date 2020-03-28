import requests
from bs4 import BeautifulSoup
import config
from rihanna_bot import hot100


def selector(message):
    if message == 'sound cloud play a random song':
        return random_song()
    elif message == 'sound cloud play song cloud playlist':
        return playlist()
    elif message[:len('sound cloud play')] == "sound cloud play":
        message_ = message[len("sound cloud play") + 1:]
        return sound_cloud(message_)
    else:
        reply = "Sound cloud is offline at the moment. Man sound cloud"
        return {'display': reply, 'say': reply}


def sound_cloud(query):
    # step 1: Get the song link
    req = "https://soundcloud.com/search?q=" + query
    page = requests.get(req, headers=config.header)
    soup = BeautifulSoup(page.content, 'html.parser')
    ul_list = soup.find_all("ul")
    song_href = ul_list[1].find('a').get('href')

    # step 2: get the track id of the song
    req=f"https://soundcloud.com{song_href}"
    page = requests.get(req, headers=config.header)
    soup = BeautifulSoup(page.content, 'html.parser')
    track = soup.find("meta", {"property": "twitter:player"}).get('content')
    track_id = track.split('.')[-1].split('&')[0].split('%')[-1]
    for i in track_id:
        if i.isalpha():
            track_id = track_id.split(i)[-1]

    # step 3: pass the track_id into the sound cloud media frame
    frame = f'<iframe width="100%" height="166" scrolling="no" frameborder="no" allow="autoplay" ' \
            f'src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/{track_id}' \
            f'&color=%237900ff&auto_play=true&hide_related=false&show_comments=true&' \
            f'show_user=true&show_reposts=false&show_teaser=true"></iframe>'
    return {'display': frame, 'say': 'Playing music...'}


def playlist():
    display = '<iframe width="100%" height="160" scrolling="no" frameborder="no" allow="autoplay" ' \
              'src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/playlists/320899357' \
              '&color=%237900ff&auto_play=false&hide_related=false&show_comments=true&show_user=true' \
              '&show_reposts=false&show_teaser=true&visual=true"></iframe>'
    return {'display': display, 'say': 'Playing music...'}


def random_song():
    song = hot100.Music().random_song()
    return sound_cloud(song)


f'<iframe width="100%" height="300" scrolling="no" frameborder="no" allow="autoplay" ' \
f'src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/723315721' \
f'&color=%237900ff&auto_play=false&hide_related=false&show_comments=true&' \
f'show_user=true&show_reposts=false&show_teaser=true&visual=true"></iframe>'