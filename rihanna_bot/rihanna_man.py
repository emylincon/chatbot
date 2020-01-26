def selector(query):
    if query in man_dict:
        return man_dict[query]()
    else:
        return "I am sorry. I do not know which man page you want. \nUse 'man help' to view your options"


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
            "show twitter status for <b>user_twitter_id</b>",
            "show my last tweet",
            "show last twitter status for <b>user_twitter_id</b>",
            "tweet <b>message</b>",
            "search twitter <b>search_query</b>"]
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
            "tfl journey duration from <b>se1 5hp</b> to <b>se18 3px</b>",
            "tfl live arrivals for <b>53</b> at <b>dunton road</b>",
            "tfl live arrivals for <b>northern</b> at <b>bank underground station</b>"]
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
                    <td>google <b>what_to_google</b></td>\
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
    func = ["skype chat <b>friend_name</b> <b>message</b>",
            "show picture <b>friend_name</b>",
            "birthday for <b>friend_name</b>",
            "skype get last message to <b>friend_name</b>"]
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
                    <td>what is <b>what_to_look_up></b></td>\
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
            "football match schedules for match <b>11</b>",
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
                    <td>play <em>video_name></em></td>\
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
    func = ["amazon least price for <b>item_name</b>",
            "amazon max price for <b>item_name</b>",
            "amazon sort price for <b>speakers</b> at <b>11</b>",
            "amazon sort rating for <b>speakers</b> at <b>4.5</b>"
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
    func = ["dictionary definition for <em>word</em>",
            "dictionary synonym for <em>word</em>",
            "dictionary antonym for <em>word</em>",
            "dictionary translate <em>sentence</em> to <em>language</em>"
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
    func = ["iot graph from <em><b>ip_address</b></em>",
            "iot light off for <b>ip_address</b>",
            "iot light on for <b>ip_address</b>",
            "iot temperature for <b>ip_address</b>",
            "iot cpu for <b>ip_address</b>",
            "iot memory for <b>ip_address</b>",
            "iot humidity for <b>ip_address</b>"]
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
    func = ["word cloud <em>word</em>",
            "word cloud antonyms and synonyms <em>word</em>",
            "word cloud twitter <em>word</em>"
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

