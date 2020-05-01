import itunespy

# https://github.com/sleepyfran/itunespy


def selector(query):
    if query[:len('album details for ')] == 'album details for ':
        msg = query[len('album details for '):].strip()
        return Albums(msg).track_list_()
    elif query[:len('albums for ')] == 'albums for ':
        msg = query[len('albums for '):]
        return Albums(msg).artist_albums()
    else:
        reply = 'itunespy cannot resolve this query'
        return {'display': reply, 'say': reply}


class Albums:
    def __init__(self, query):
        self.query = query

    def track_list(self):
        tracks_ = ''
        album = itunespy.search_album(self.query)  # Returns a list
        tracks = album[0].get_tracks()  # Get tracks from the first result
        for track in tracks:
            tracks_ += track.artist_name + ' ' + track.track_name + ','
        return tracks_[:-1]

    def track_list_(self):
        album = itunespy.search_album(self.query)  # Returns a list
        album_name = album[0].__dict__['collection_name']
        artist = album[0].__dict__['artist_name']
        img = album[0].__dict__['artwork_url_100']
        r_date = album[0].release_date.split('T')[0]
        length = album[0].get_album_time()
        tracks = album[0].get_tracks()  # Get tracks from the first result
        display = f'<div>' \
                  f'<img src="{img}" alt="image" style="float:left; height:100px"> ' \
                  f'<div style="float:left; height:100px; width:500px; background-color:black; color:white;">' \
                  f'<span style="font-size:30px;">{album_name} by {artist} </span>' \
                  f'<p style="font-size:15px;">Released on {r_date}</p>' \
                  f'<p style="font-size:15px;">Runtime of {length} minutes</p></div></div>'
        display += "<table id='t01' style='width:600px;'>"

        for song in tracks:
            preview = self.audio_tag(song.preview_url)
            display += f"<tr onclick='open_link(" + f'"{song.track_view_url}"' + f")'>\
                        <td><p style='font-size:12px; color:#3C6BD3; font-family:verdana;'>{song.track_number}</p></td>\
                        <td><p style='font-size:12px; color:#3C6BD3; font-family:verdana;'>{song.track_name}</p></td>\
                        <td><p style='font-size:12px; color:#769EF8; font-family:verdana;'>{preview}</p></td>\
                    </tr> \
                   "
        display += '</table>'
        say = f'find details for album {album_name} by {artist}'
        return {'display': display, 'say': say}

    def artist_albums(self):
        artist = itunespy.search_artist(self.query)  # Returns a list
        albums = artist[0].get_albums()  # Get albums from the first result
        display = ''
        for album in albums:
            album_name = album.collection_name
            artist = album.artist_name
            img = album.artwork_url_100
            r_date = album.release_date.split('T')[0]
            length = album.get_album_time()
            # border-style: solid;
            #   border-color: coral;
            display += f'<div>' \
                          f'<img src="{img}" alt="image" style="float:left; height:100px"> ' \
                          f'<div style="float:left; height:100px; width:500px; background-color:black; color:white; ' \
                       f'border-style: solid; border-color: white;">' \
                          f'<span style="font-size:20px;">{album_name} by {artist} </span>' \
                          f'<p style="font-size:15px;">Released on {r_date}</p>' \
                          f'<p style="font-size:15px;">Runtime of {length} minutes</p></div></div>'
        say = f'find displayed albums for {self.query}'
        return {'display': display, 'say': say}

    @staticmethod
    def audio_tag(link):
        tag = f'<audio controls>' \
              f'<source src="{link}">' \
              f'</audio>'
        return tag


# Albums('drake').artist_albums()