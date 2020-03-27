import urllib.request
import urllib.parse
import json
import random
import config

# documentation = https://unsplash.com/documentation


def selector(message):
    if message[:len("show images")] == "show images":
        msg = message[len("show images")+1:]
        return Picture(msg).user_many_image()
    elif message[:len("show image")] == "show image":
        msg = message[len("show image")+1:]
        return Picture(msg).user_one_image()

    else:
        return "rihanna cannot help with your query, use man help to navigate"


class Picture:
    def __init__(self, pic):
        request_headers = {
            "Authorization": f"Client-ID {config.unsplash_key}",
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"
        }
        self.pic = pic
        pageURL = f'https://api.unsplash.com/search/photos?query={self.pic}'
        request = urllib.request.Request(pageURL, headers=request_headers)
        self.contents = json.loads(urllib.request.urlopen(request).read())
        self.results = self.contents['results']

    def one_image(self):
        img = random.choice(self.results)
        return img['urls']['small']

    def user_one_image(self):
        load = self.one_image()
        reply = {'display': f'<img src="{load}" alt=f"{self.pic} image " width="60%" height="60%">',
                 'say': f'find displayed of {self.pic}'}
        return reply

    def many_image(self):
        return [img['urls']['small'] for img in self.results[:10]]

    def user_many_image(self):
        load = self.many_image()
        display = ""
        for image in load:
            display += f"<div style = 'width:300px; word-wrap: break-word'> " \
                       f'<img src="{image}" alt=f"{self.pic} image " width="300px" ></div>'
        reply = {'display': f'{display}',
                 'say': f'find displayed images of {self.pic}'}
        return reply


