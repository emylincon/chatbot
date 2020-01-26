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
    display = "<table id='t01'>\
                    <tr>\
                        <th>Twitter Usage</th>\
                    </tr>\
                    "
    func = ["show global trending topics on twitter",
            "show global trending topics on twitter graph",
            "show trending topics on twitter",
            "show my twitter status",
            "show twitter status for <user_twitter_id>",
            "show my last tweet",
            "show last twitter status for <user_twitter_id>",
            "tweet <message>",
            "search twitter <search_query>"]
    for i in func:
        display += f"<tr>\
                        <td>{i}</td>\
                    </tr>"
    say = "Find below How to use the Twitter feature"
    reply = {'display': display, 'say': say}
    return reply


def man_tfl():
    display = "<table id='t01'>\
                        <tr>\
                            <th>TFL Usage</th>\
                        </tr>\
                        "
    func = ["tfl tube service report",
            "tfl journey duration from se1 5hp to se18 3px",
            "tfl live arrivals for 53 at dunton road",
            "tfl live arrivals for northern at bank underground station"]
    for i in func:
        display += f"<tr>\
                        <td>{i}</td>\
                    </tr>"
    say = "Find below How to use the TFL feature"
    reply = {'display': display, 'say': say}
    return reply


def man_news():
    display = "<table id='t01'>\
                    <tr>\
                        <th>News Usage</th>\
                    </tr>\
                            "
    display += f"<tr>\
                      <td>BBC News</td>\
                </tr>"
    say = "Find below How to use the News feature"
    reply = {'display': display, 'say': say}
    return reply


def man_email():
    display = "<table id='t01'>\
                    <tr>\
                        <th>Email Usage</th>\
                    </tr>\
                            "
    display += f"<tr>\
                      <td>send email</td>\
                </tr>"
    say = "Find below How to use the Email feature"
    reply = {'display': display, 'say': say}
    return reply


def man_google():
    display = "<table id='t01'>\
                        <tr>\
                            <th>Google Usage</th>\
                        </tr>\
                                "
    display += f"<tr>\
                    <td>google <what_to_google></td>\
                </tr>"
    say = "Find below How to use the google feature"
    reply = {'display': display, 'say': say}
    return reply


def man_skype():
    display = "<table id='t01'>\
                        <tr>\
                            <th>Skype Usage</th>\
                        </tr>\
                        "
    func = ["skype chat <friend_name> <message>",
            "show picture <friend_name>",
            "birthday for <friend_name>",
            "skype get last message to <friend_name>"]
    for i in func:
        display += f"<tr>\
                        <td>{i}</td>\
                    </tr>"
    say = "Find below How to use the Skype feature"
    reply = {'display': display, 'say': say}
    return reply


def man_wiki():
    display = "<table id='t01'>\
                        <tr>\
                            <th>Wikipedia Usage</th>\
                        </tr>\
                                "
    display += f"<tr>\
                    <td>what is <what_to_look_up></td>\
                </tr>"
    say = "Find below How to use the Wikipedia feature"
    reply = {'display': display, 'say': say}
    return reply


def man_facebook():
    display = "<table id='t01'>\
                        <tr>\
                            <th>Facebook Usage</th>\
                        </tr>\
                        "
    func = ["show my facebook posts",
            "show facebook pages i like",
            "how many facebook friends do i have"]
    for i in func:
        display += f"<tr>\
                        <td>{i}</td>\
                    </tr>"
    say = "Find below How to use the Facebook feature"
    reply = {'display': display, 'say': say}
    return reply


def man_football():
    display = "<table id='t01'>\
                        <tr>\
                            <th>Football Usage</th>\
                        </tr>\
                        "
    func = ["football match today",
            "football league start",
            "football league status",
            "football top scorers",
            "football top scorers graph",
            "football match schedules for match 11",
            ]
    for i in func:
        display += f"<tr>\
                        <td>{i}</td>\
                    </tr>"
    say = "Find below How to use the Football feature"
    reply = {'display': display, 'say': say}
    return reply


def man_time():
    display = "<table id='t01'>\
                        <tr>\
                            <th>Time Usage</th>\
                        </tr>\
                        "
    func = ("what is the time", "time", "what is the current time", "current time")
    for i in func:
        display += f"<tr>\
                        <td>{i}</td>\
                    </tr>"
    say = "Find below How to use the Time feature"
    reply = {'display': display, 'say': say}
    return reply


def man_date():
    display = "<table id='t01'>\
                        <tr>\
                            <th>Date Usage</th>\
                        </tr>\
                        "
    func = ("what is the date", "what is todays date", "todays date", "current date", "date")
    for i in func:
        display += f"<tr>\
                        <td>{i}</td>\
                    </tr>"
    say = "Find below How to use the Date feature"
    reply = {'display': display, 'say': say}
    return reply


def man_weather():
    display = "<table id='t01'>\
                        <tr>\
                            <th>Weather Usage</th>\
                        </tr>\
                        "
    func = ("weather forecast today", "weather forecast Lagos Nigeria")
    for i in func:
        display += f"<tr>\
                        <td>{i}</td>\
                    </tr>"
    say = "Find below How to use the Weather feature"
    reply = {'display': display, 'say': say}
    return reply


def man_youtube():
    display = "<table id='t01'>\
                        <tr>\
                            <th>Youtube Usage</th>\
                        </tr>\
                                "
    display += f"<tr>\
                    <td>play <video_name></td>\
                </tr>"
    say = "Find below How to use the Youtube feature"
    reply = {'display': display, 'say': say}
    return reply


def man_amazon():
    display = "<table id='t01'>\
                        <tr>\
                            <th>Amazon Usage</th>\
                        </tr>\
                        "
    func = ["amazon least price for <item_name>",
            "amazon max price for <item_name>",
            "amazon sort price for speakers at 11",
            "amazon sort rating for speakers at 4.5"
            ]
    for i in func:
        display += f"<tr>\
                        <td>{i}</td>\
                    </tr>"
    say = "Find below How to use the Amazon feature"
    reply = {'display': display, 'say': say}
    return reply


def man_dictionary():
    display = "<table id='t01'>\
                        <tr>\
                            <th>Dictionary Usage</th>\
                        </tr>\
                        "
    func = ["dictionary definition for <word>",
            "dictionary synonym for <word>",
            "dictionary antonym for <word>",
            "dictionary translate <sentence> to <language>"
            ]
    for i in func:
        display += f"<tr>\
                        <td>{i}</td>\
                    </tr>"
    say = "Find below How to use the Dictionary feature"
    reply = {'display': display, 'say': say}
    return reply


def man_iot():
    display = "<table id='t01'>\
                    <tr>\
                        <th>IoT Usage</th>\
                    </tr>\
                    "
    func = ["iot graph from <ip_address>",
            "iot light off for <ip_address>",
            "iot light on for <ip_address>",
            "iot temperature for <ip_address>",
            "iot cpu for <ip_address>",
            "iot memory for <ip_address>",
            "iot humidity for <ip_address>"]
    for i in func:
        display += f"<tr>\
                        <td>{i}</td>\
                    </tr>"
    say = "Find below How to use the I.o.T feature"
    reply = {'display': display, 'say': say}
    return reply


def man_word_cloud():
    display = "<table id='t01'>\
                        <tr>\
                            <th>Word Cloud Usage</th>\
                        </tr>\
                        "
    func = ["word cloud <word>",
            "word cloud antonyms and synonyms <word>",
            "word cloud twitter <word>"
            ]
    for i in func:
        display += f"<tr>\
                        <td>{i}</td>\
                    </tr>"
    say = "Find below How to use the Word Cloud feature"
    reply = {'display': display, 'say': say}
    return reply


man_dict = {'man help': man_help, 'man maths': man_maths, 'man twitter': man_twitter, 'man tfl': man_tfl,
            'man news': man_news, 'man email': man_email, 'man skype': man_skype, 'man facebook': man_facebook,
            'man football': man_football, 'man time': man_time, 'man date': man_date, 'man weather': man_weather,
            'man youtube': man_youtube, 'man google': man_google, 'man wikipedia': man_wiki, 'man wiki': man_wiki,
            'man amazon': man_amazon, 'man dictionary': man_dictionary, 'man iot': man_iot, 'man word cloud': man_word_cloud}

