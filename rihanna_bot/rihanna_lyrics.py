import lyricsgenius
import config
import json


def selector(query):  # lyrics to in my feelings by drake
    if query[:len('lyrics to ')] == 'lyrics to ':
        msg = query[len('lyrics to '):].split('by')
        if len(msg) == 2:
            return lyrics_finder(song=msg[0], artist=msg[1])
        else:
            return lyrics_finder(song=msg[0])


def format_lyrics(song_obj):
    style_m = f"style='background-image: url({song_obj._body['header_image_url']}); " \
              f"width:600px; background-size: cover; background-repeat: no-repeat; " \
              f"background-color: #c75858; height: 150px;'"
    style_i = "style='float:left;'"
    style_p = 'color:yellow; margin:0; padding:0; margin-bottom:0; margin-top:0;'
    style_l = f"style='background-color:#e6e4e1; font-size:17px; width:600px; text-align: center;'"
    title = song_obj.title
    artist = song_obj.artist
    a = '\n'
    display = f'<div {style_m}>' \
              f'<div {style_i}><img src="{song_obj._body["song_art_image_thumbnail_url"]}" width="150px"></div>' \
              f'<div {style_i}>' \
              f'<p style="{style_p} font-size:45px; ">{title}</p>' \
              f'<p style="{style_p} font-size:40px; ">{artist}</p>' \
              f'</div>' \
              '</div>' \
              f'<div {style_l}>{song_obj.lyrics.replace(a, "<br>").replace("[", "<br>[")}</div>'
    return display


def lyrics_finder(song, artist=None):
    if artist:
        genius = lyricsgenius.Genius(config.lyrics_key)
        song_obj = genius.search_song(song, artist)
        display = format_lyrics(song_obj)

        return {'display': display, 'say': f'find displayed the lyrics for {song_obj.title}', 'lyrics': song_obj.lyrics}
    else:
        genius = lyricsgenius.Genius(config.lyrics_key)
        song_obj = genius.search_song(song)
        display = format_lyrics(song_obj)

        return {'display': display, 'say': f'find displayed the lyrics for {song_obj.title}', 'lyrics': song_obj.lyrics}

# a =lyrics_finder('in my feelings', 'drake')['display']
# print(a)
