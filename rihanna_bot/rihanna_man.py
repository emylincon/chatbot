def selector(query):
    if query in man_dict:
        return man_dict[query]()
    else:
        return "I am sorry. I do not know which man page you want. \nUse 'man page' to view your options"


def man_help():
    reply = ''
    reply += "<table id='t01'>\
                <tr>\
                    <th>Feature</th>\
                    <th>Manual Page</th>\
                </tr>\
                "
    for feature in man_dict:
        reply += f"<tr>\
                        <td>{feature.replace('man ', '').upper()}</td>\
                        <td>{feature}</td>\
                    </tr>"
    reply_ = {'display': reply, 'say': 'Please find below the features and manual pages'}
    return reply_


def man_maths():
    display = "<table id='t01'>\
                <tr>\
                    <th>Maths Usage</th>\
                </tr>\
                "
    m = ['+', '*', '-', '/']
    for i in m:
        display += f"<tr>\
                        <td>calculate 5 {i} 2</td>\
                    </tr>"

    say = "Find below How to use the Maths feature"
    reply = {'display': display, 'say': say}
    return reply


def man_twitter():
    pass


def man_tfl():
    pass


def man_news():
    pass


def man_email():
    pass


def man_google():
    pass


def man_skype():
    pass

def man_wiki():
    pass


def man_facebook():
    pass


def man_football():
    pass


def man_time():
    pass


def man_weather():
    pass


def man_youtube():
    pass


def man_amazon():
    pass


def man_dictionary():
    pass


def man_iot():
    pass


def man_word_cloud():
    pass


man_dict = {'man help': man_help, 'man maths': man_maths, 'man twitter': man_twitter, 'man tfl': man_tfl,
            'man news': man_news, 'man email': man_email, 'man skype': man_skype, 'man facebook': man_facebook,
            'man football': man_football, 'man time': man_time, 'man date': man_time, 'man weather': man_weather,
            'man youtube': man_youtube, 'man google': man_google, 'man wikipedia': man_wiki, 'man wiki': man_wiki,
            'man amazon': man_amazon, 'man dictionary': man_dictionary, 'man iot': man_iot, 'man word cloud': man_word_cloud}

