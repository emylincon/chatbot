import itunespy


def selector(query):
    if query[:len('album details for ')] == 'album details for ':
        msg = query[len('album details for '):].strip()
        return Albums(msg).track_list_()
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
        display = f'<div><img src="{img}" alt="image"> <span>{album_name} by {artist}. ' \
                  f'Released on {r_date} with a runtime of {length} minutes</span></div>'
        display += "<table id='t01'>"

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
        pass

    @staticmethod
    def audio_tag(link):
        tag = f'<audio controls>' \
              f'<source src="{link}">' \
              f'</audio>'
        return tag
