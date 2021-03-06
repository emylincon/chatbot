import config


def selector(query):
    if query[:len('map ')] == 'map ':
        message = query[len('map '):]
        return google_locate(message)


def google_locate(message):
    query = message.replace(' ', '+')
    display = f'<iframe\
                  width="800"\
                  height="450"\
                  frameborder="0" style="border:0"\
                  src="https://www.google.com/maps/embed/v1/place?key={config.google_api}\
                    &q={query}" allowfullscreen>\
                </iframe>'
    say = f'find displayed the map location for {message}'
    return {'display': display, 'say': say}
