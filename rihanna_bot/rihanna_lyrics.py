import lyricsgenius
import config
from rihanna_bot.ri_youtube import Youtube
from multiprocessing.pool import ThreadPool
import traceback, sys


def selector(query):  # lyrics to in my feelings by drake
    if query[:len('lyrics to ')] == 'lyrics to ':
        msg = query[len('lyrics to '):].split('by')
        if len(msg) == 2:
            return lyrics_finder(song=msg[0], artist=msg[1])
        else:
            return lyrics_finder(song=msg[0])
    elif query[:len('lyrics and video to ')] == 'lyrics and video to ':
        msg = query[len('lyrics and video to '):].split('by')
        if len(msg) == 2:
            return lyrics_video(song=msg[0], artist=msg[1])
        else:
            return lyrics_video(song=msg[0])#
    elif query[:len('lyrics with video to ')] == 'lyrics with video to ':
        msg = query[len('lyrics with video to '):]
        return youtube_lyrics_2(msg)


def format_lyrics(song_obj):
    style_m = f"style='background-image: url({song_obj._body['header_image_url']}); " \
              f"width:600px; background-size: cover; background-repeat: no-repeat; " \
              f"background-color: #c75858; height: 150px;'"
    style_i = "style='float:left;'"
    style_p = 'color:yellow; margin:0; padding:0; margin-bottom:0; margin-top:0;'
    style_l = f"style='background-color:#e6e4e1; font-size:17px; width:600px; text-align: center;'"
    style_lyrics = "style='color:#58638E; font-size:35px; font-family: Comic Sans MS;'"
    title = song_obj.title
    artist = song_obj.artist
    a = '\n'
    display = f'<div {style_m}>' \
              f'<div {style_i}><img src="{song_obj._body["song_art_image_thumbnail_url"]}" width="150px"></div>' \
              f'<div {style_i}>' \
              f'<p style="{style_p} font-size:45px; ">{title}</p>' \
              f'<p style="{style_p} font-size:40px; ">{artist}</p>' \
              f'</div>' \
              f'</div><div {style_l}>'
    tail = f'<span {style_lyrics}>Song Lyrics<br></span>' \
           f'{song_obj.lyrics.replace(a, "<br>").replace("[", "<br>[")}</div>'
    return display,tail


def lyrics_finder(song, artist=None):
    try:
        if artist:
            genius = lyricsgenius.Genius(config.lyrics_key)
            song_obj = genius.search_song(song, artist)
            display = format_lyrics(song_obj)

            return {'display': display[0]+display[1],
                    'say': f'find displayed the lyrics for {song_obj.title}',
                    'lyrics': song_obj.lyrics}
        else:
            genius = lyricsgenius.Genius(config.lyrics_key)
            song_obj = genius.search_song(song)
            display = format_lyrics(song_obj)

            return {'display': display[0]+display[1],
                    'say': f'find displayed the lyrics for {song_obj.title}',
                    'lyrics': song_obj.lyrics}
    except:
        traceback.print_exc()
        exc_type, exc_value, exc_traceback = sys.exc_info()
        reply = f'rihanna detected a bug in lyrics.lyrics_finder: {exc_value}'
        return {'display': reply, 'say': reply, 'lyrics': 'NOT FOUND'}


def lyrics_video(song, artist=None):
    if artist:
        genius = lyricsgenius.Genius(config.lyrics_key)
        song_obj = genius.search_song(song, artist)
        display = format_lyrics(song_obj)
        vid = Youtube().search_youtube(song+' '+artist)

        return {'display': display[0]+vid['display']+display[1],
                'say': f'find displayed the lyrics for {song_obj.title}',
                'lyrics': song_obj.lyrics}
    else:
        genius = lyricsgenius.Genius(config.lyrics_key)
        song_obj = genius.search_song(song)
        display = format_lyrics(song_obj)
        vid = Youtube().search_youtube(song)

        return {'display': display[0]+vid['display']+display[1],
                'say': f'find displayed the lyrics for {song_obj.title}',
                'lyrics': song_obj.lyrics}


def youtube_lyrics(query):
    a = '\n'
    lyrics = lyrics_finder(query)['lyrics'].replace(a, "<br>").replace("[", "<br>[")
    video_div = Youtube().search_youtube(query)['display']
    say = 'find displayed the video and lyrics'
    script = '<script>\
                        var coll = document.getElementsByClassName("collapsible");\
                        var i;\
                        for (i = 0; i < coll.length; i++) {\
                          coll[i].addEventListener("click", function() {\
                            this.classList.toggle("active");\
                            var content = this.nextElementSibling;\
                            if (content.style.maxHeight){\
                              content.style.maxHeight = null;\
                            } else {\
                              content.style.maxHeight = content.scrollHeight + "px";\
                            } \
                          });\
                        }\
                        </script>'
    lyrics_button = f'<br><button type="button" class="collapsible">Song Lyrics</button>'
    lyrics_button += f' <div class="content"><div style="text-align:center;">{lyrics}</div></div>'
    main_div = "<div style='width:600px;'>"

    video_div += lyrics_button + script
    main_div += video_div + '</div>'
    return {'display': main_div, 'say': say}


def youtube_lyrics_2(query):
    try:
        genius = lyricsgenius.Genius(config.lyrics_key)
        result_list = []
        pool = ThreadPool(processes=2)
        result_list.append(pool.apply_async(genius.search_song, (query,)))
        result_list.append(pool.apply_async(Youtube().search_youtube, (query,)))

        song_obj = result_list[0].get()
        a = '\n'
        lyrics = song_obj.lyrics.replace(a, "<br>").replace("[", "<br>[")
        style_text = "style ='background-color: rgb(0,0,0); background-color: rgba(0,0,0, 0.4); color: white; " \
                     "font-weight: bold; border: 3px solid #f1f1f1; transform: translate(-0%, -0%);" \
                     "z-index: 2; height: 100%; padding: 20px; text-align: center;'"
        video_div = result_list[1].get()['display']
        say = 'find displayed the video and lyrics'
        script = '<script>\
                            var coll = document.getElementsByClassName("collapsible");\
                            var i;\
                            for (i = 0; i < coll.length; i++) {\
                              coll[i].addEventListener("click", function() {\
                                this.classList.toggle("active");\
                                var lyrics = this.nextElementSibling;\
                                if (lyrics.style.maxHeight){\
                                  lyrics.style.maxHeight = null;\
                                } else {\
                                  lyrics.style.maxHeight = lyrics.scrollHeight + "px";'
        script += f'lyrics.style.backgroundImage = "url(' + f"'" + f'{song_obj._body["header_image_url"]}' + "')" + '";'
        script += ' \
                                } \
                              });\
                            }\
                            </script>'
        lyrics_button = f'<br><button type="button" class="collapsible">Song Lyrics</button>'
        lyrics_button += f' <div class="lyrics"><div {style_text}>{lyrics}</div></div>'
        main_div = "<div style='width:600px;'>"

        video_div += lyrics_button
        main_div += video_div + '</div>' + script
        return {'display': main_div, 'say': say}
    except:
        traceback.print_exc()
        exc_type, exc_value, exc_traceback = sys.exc_info()
        reply = f'rihanna detected a bug in lyrics.youtube_lyrics_2: {exc_value}'
        return {'display': reply, 'say': reply}


# does not work
def youtube_lyrics_1(query):
    genius = lyricsgenius.Genius(config.lyrics_key)
    song_obj = genius.search_song(query)
    a = '\n'
    style_m = f"style='background-image: url({song_obj._body['header_image_url']}); " \
              f"background-size: cover; background-repeat: no-repeat; " \
              f"background-position: center; height: 1500px;" \
              f"filter: blur(8px); -webkit-filter: blur(8px);'"
    style_text = "style ='background-color: rgb(0,0,0); background-color: rgba(0,0,0, 0.4); color: white; " \
                 "font-weight: bold; border: 3px solid #f1f1f1; transform: translate(-0%, -97%);" \
                 "z-index: 2; height: 100%; padding: 20px; text-align: center;'"
    lyrics = song_obj.lyrics.replace(a, "<br>").replace("[", "<br>[")
    video_div = Youtube().search_youtube(query)['display']
    say = 'find displayed the video and lyrics'
    script = '<script>\
                        var coll = document.getElementsByClassName("collapsible");\
                        var i;\
                        for (i = 0; i < coll.length; i++) {\
                          coll[i].addEventListener("click", function() {\
                            this.classList.toggle("active");\
                            var content = this.nextElementSibling;\
                            if (content.style.maxHeight){\
                              content.style.maxHeight = null;\
                            } else {\
                              content.style.maxHeight = content.scrollHeight + "px";\
                            } \
                          });\
                        }\
                        </script>'
    lyrics_button = f'<br><button type="button" class="collapsible">Song Lyrics</button>'
    lyrics_button += f' <div class="content" style="max-height: 1550px;"><div {style_m}></div><div {style_text}>{lyrics}</div></div>'
    main_div = "<div style='width:600px;'>"

    video_div += lyrics_button + script
    main_div += video_div + '</div>'
    return {'display': main_div, 'say': say}


def sound_cloud_lyrics(query):
    genius = lyricsgenius.Genius(config.lyrics_key)
    song_obj = genius.search_song(query)
    a = '\n'
    lyrics = song_obj.lyrics.replace(a, "<br>").replace("[", "<br>[")
    style_text = "style ='background-color: rgb(0,0,0); background-color: rgba(0,0,0, 0.4); color: white; " \
                 "font-weight: bold; border: 3px solid #f1f1f1; transform: translate(-0%, -0%);" \
                 "z-index: 2; height: 100%; padding: 20px; text-align: center;'"
    script = '<script>\
                            var coll = document.getElementsByClassName("collapsible");\
                            var i;\
                            for (i = 0; i < coll.length; i++) {\
                              coll[i].addEventListener("click", function() {\
                                this.classList.toggle("active");\
                                var lyrics = this.nextElementSibling;\
                                if (lyrics.style.maxHeight){\
                                  lyrics.style.maxHeight = null;\
                                } else {\
                                  lyrics.style.maxHeight = lyrics.scrollHeight + "px";'
    script += f'lyrics.style.backgroundImage = "url(' + f"'" + f'{song_obj._body["header_image_url"]}' + "')" + '";'
    script += ' \
                                } \
                              });\
                            }\
                            </script>'
    lyrics_button = f'<br><button type="button" class="collapsible">Song Lyrics</button>'
    lyrics_button += f' <div class="lyrics"><div {style_text}>{lyrics}</div></div>'

    return {'lyrics': lyrics_button, 'script': script}

# a =lyrics_finder('in my feelings', 'drake')['display']
# print(a)
# a = youtube_lyrics_2('kendrick humble')
# print(a)
