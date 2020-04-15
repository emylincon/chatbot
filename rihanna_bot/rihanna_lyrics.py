import lyricsgenius
import config
import json


def selector(query):    # lyrics to in my feelings by drake
    if query[:len('lyrics to ')] == 'lyrics to ':
        msg = query[len('lyrics to '):].split('by')
        if len(msg) == 2:
            return lyrics_finder(song=msg[0], artist=msg[1])
        else:
            return lyrics_finder(song=msg[0])


def lyrics_finder(song, artist=None):
    if artist:
        genius = lyricsgenius.Genius(config.lyrics_key)
        song_obj = genius.search_song(song, artist)

        style_m = f"style='background-image:url('{song_obj._body['header_image_url']}'); width:900px;'"
        style_i = f"style='float:left;'"
        style_l = f"style='background-color:#e6e4e1; font-size:14px; width:900px;'"
        title = song_obj.title
        artist = song_obj.artist
        display = f'<div {style_m}>' \
                  f'<div {style_i}><img src="{song_obj._body["song_art_image_thumbnail_url"]}" width="100px"></div>' \
                  f'<div {style_i}>{title}<p>{artist}</p></div>' \
                  '</div>' \
                  f'<div {style_l}>{song_obj.lyrics}</div>'
        return {'display': display, 'say': f'find displayed the lyrics for {title}', 'lyrics': song_obj.lyric}
    else:
        genius = lyricsgenius.Genius(config.lyrics_key)
        song_obj = genius.search_song(song)

        style_m = f"style='background-image:url('{song_obj._body['header_image_url']}'); width:900px;'"
        style_i = f"style='float:left;'"
        style_l = f"style='background-color:#e6e4e1; font-size:14px; width:900px;'"
        title = song_obj.title
        artist = song_obj.artist
        display = f'<div {style_m}>' \
                  f'<div {style_i}><img src="{song_obj._body["song_art_image_thumbnail_url"]}" width="100px"></div>' \
                  f'<div {style_i}>{title}<p>{artist}</p></div>' \
                  '</div>' \
                  f'<div {style_l}>{song_obj.lyrics}</div>'
        return {'display': display, 'say': f'find displayed the lyrics for {title}', 'lyrics': song_obj.lyrics}

