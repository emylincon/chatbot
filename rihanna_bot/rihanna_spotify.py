import requests
import json
import config

# get token for new release from this link =
#  https://developer.spotify.com/console/get-new-releases/?country=&limit=&offset=


def selector(query):
    if (query == 'spotify new releases') or (query == 'whats new on spotify'):
        return SpotifyMusic().new_release()


class SpotifyMusic:
    def __init__(self):
        self.header = config.spotify_header
        self.baseURL = 'https://api.spotify.com/v1/'

    def new_release(self):
        url = self.baseURL+'browse/new-releases'
        response = requests.get(url, headers=self.header)
        data = json.loads(response.content)
        # print(data)
        display = "<table id='t01'>\
                      <tr>\
                        <th></th>\
                        <th><p style='font-size:15px; color:#5985E9; font-family:verdana;'>Artist</p></th>\
                        <th><p style='font-size:15px; color:#5985E9; font-family:verdana;'>Name</p></th>\
                        <th><p style='font-size:15px; color:#5985E9; font-family:verdana;'>Type</p></th>\
                        <th><p style='font-size:15px; color:#5985E9; font-family:verdana;'>Release date</p></th>\
                      </tr>\
                    "
        for item in data['albums']['items']:
            display += f"<tr onclick='open_link(" + f'"{item["external_urls"]["spotify"]}"' + f")'>\
                        <td><img src='{item['images'][0]['url']}' alt='{item['artists'][0]['name']} image' width='80px'></td>\
                        <td><p style='font-size:12px; color:#3C6BD3; font-family:verdana;'>{item['artists'][0]['name']}</p></td>\
                        <td><p style='font-size:12px; color:#3C6BD3; font-family:verdana;'>{item['name']}</p></td>\
                        <td><p style='font-size:12px; color:#769EF8; font-family:verdana;'>{item['album_type']}</p></td>\
                        <td><p style='font-size:12px; color:#769EF8; font-family:verdana;'>{item['release_date']}</p></td>\
                    </tr> \
                   "
        display += '</table>'
        return {'display': display, 'say': 'find displayed new releases on spotify'}


# print(SpotifyMusic().new_release())
