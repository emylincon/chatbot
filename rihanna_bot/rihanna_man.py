def selector(query):
    if query in man_dict:
        return man_dict[query]()
    else:
        reply = "I am sorry. I do not know which man page you want. \nUse 'man help' to view your options"
        return {'display': reply, 'say': reply}


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
                        <td><font color='blue'>{feature.replace('man ', '').capitalize()}</font></td>\
                        <td onclick='man_complete(" + f'"{feature}"' + f")'>{feature}</td>\
                    </tr>"
    reply += "</table>"
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
                        <td onclick='man_complete(" + f'"calculate 5 {i} 2"' + f")'>calculate 5 {i} 2</td>\
                    </tr>"
    display += "</table>"
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
            "show twitter hash tags associated with <b>query</b>",
            "search twitter <b>search_query</b>"]
    for i in func:
        j = i.replace('<b>', '[').replace('</b>', ']')
        display += f"<tr>\
                         <td onclick='man_complete(" + f'"{j}"' + f")'>{i}</td>\
                     </tr>"
    display += "</table>"
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
            "tfl find tube station on map",
            "tfl journey duration from <b>se1 5hp</b> to <b>se18 3px</b>",
            "tfl live arrivals for <b>53</b> at <b>dunton road</b>",
            "tfl live arrivals for <b>northern</b> at <b>bank underground station</b>"]
    for i in func:
        j = i.replace('<b>', '[').replace('</b>', ']')
        display += f"<tr>\
                         <td onclick='man_complete(" + f'"{j}"' + f")'>{i}</td>\
                     </tr>"
    display += "</table>"
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
                      <td onclick='man_complete(" + '"BBC news"' + ")'>BBC News</td>\
                </tr>"
    display += "</table>"
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
                      <td onclick='man_complete(" + '"send email"' + ")'>send email</td>\
                </tr>"
    display += "</table>"
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
                    <td onclick='man_complete(" + '"google [query]"' + ")'>google <b>what_to_google</b></td>\
                </tr>"
    display += "</table>"
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
            "skype show picture <b>friend_name</b>",
            "skype birthday for <b>friend_name</b>",
            "skype get last message to <b>friend_name</b>"]
    for i in func:
        j = i.replace('<b>', '[').replace('</b>', ']')
        display += f"<tr>\
                         <td onclick='man_complete(" + f'"{j}"' + f")'>{i}</td>\
                     </tr>"
    display += "</table>"
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
                    <td onclick='man_complete(" + '"what is [query]"' + ")'>what is <b>what_to_look_up></b></td>\
                </tr>"
    display += "</table>"
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
                         <td onclick='man_complete(" + f'"{i}"' + f")'>{i}</td>\
                     </tr>"
    display += "</table>"
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
        j = i.replace('<b>', '[').replace('</b>', ']')
        display += f"<tr>\
                         <td onclick='man_complete(" + f'"{j}"' + f")'>{i}</td>\
                     </tr>"
    display += "</table>"
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
                         <td onclick='man_complete(" + f'"{i}"' + f")'>{i}</td>\
                     </tr>"
    display += "</table>"
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
                         <td onclick='man_complete(" + f'"{i}"' + f")'>{i}</td>\
                     </tr>"
    display += "</table>"
    say = "Find below How to use the Date feature"
    reply = {'display': display, 'say': say}
    return reply


def man_weather():
    display = "<table id='t01'>\
                        <tr>\
                            <th>Weather Usage</th>\
                        </tr>\
                        "
    func = ("weather forecast today", "weather forecast <b>Lagos Nigeria</b>")
    for i in func:
        j = i.replace('<b>', '[').replace('</b>', ']')
        display += f"<tr>\
                         <td onclick='man_complete(" + f'"{j}"' + f")'>{i}</td>\
                     </tr>"
    display += "</table>"
    say = "Find below How to use the Weather feature"
    reply = {'display': display, 'say': say}
    return reply


def man_youtube():
    display = "<table id='t01'>\
                        <tr>\
                            <th>Youtube Usage</th>\
                            <th>Description</th>\
                        </tr>\
                                "
    func = {"play <b>video_name</b>": "opens a new window to play video",
            "Youtube <b>video_name</b>": "plays embedded video within chat log",
            "Youtube loop <b>video_name</b>": "plays embedded video within chat log in a loop",
            "Youtube playlist <b>artist_name</b>": "plays embedded playlist video within chat log",
            "youtube choose playlist <b>omg usher, anaconda, going bad</b>":
                "plays embedded playlist video within chat log",
            'youtube a random song': 'plays a random song on billboard hot 100 from youtube',
            "youtube popular songs playlist": "plays top 5 popular songs",
            "youtube popular songs playlist top <b>10</b>": "plays top 10 popular songs",
            "youtube songs chart": "plays chart playlist"
            }
    for i in func:
        j = i.replace('<b>', '[').replace('</b>', ']')
        display += f"<tr>\
                         <td onclick='man_complete(" + f'"{j}"' + f")'>{i}</td>\
                         <td onclick='man_complete(" + f'"{j}"' + f")'>{func[i]}</td>\
                     </tr>"
    display += "</table>"
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
        j = i.replace('<b>', '[').replace('</b>', ']')
        display += f"<tr>\
                         <td onclick='man_complete(" + f'"{j}"' + f")'>{i}</td>\
                     </tr>"
    display += "</table>"
    say = "Find below How to use the Amazon feature"
    reply = {'display': display, 'say': say}
    return reply


def man_dictionary():
    display = "<table id='t01'>\
                        <tr>\
                            <th>Dictionary Usage</th>\
                        </tr>\
                        "
    func = ["dictionary definition <em><b>word</b></em>",
            "dictionary synonym for <em><b>word</b></em>",
            "dictionary antonym for <em><b>word</b></em>",
            "dictionary translate <em><b>sentence</b></em> to <em><b>language</b></em>"
            ]
    for i in func:
        j = i.replace('<b>', '[').replace('</b>', ']').replace('<em>', '').replace('</em>', '')
        display += f"<tr>\
                             <td onclick='man_complete(" + f'"{j}"' + f")'>{i}</td>\
                         </tr>"
    display += "</table>"
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
        j = i.replace('<b>', '[').replace('</b>', ']')
        display += f"<tr>\
                         <td onclick='man_complete(" + f'"{j}"' + f")'>{i}</td>\
                     </tr>"
    display += "</table>"
    say = "Find below How to use the Internet of Things feature"
    reply = {'display': display, 'say': say}
    return reply


def man_word_cloud():
    display = "<table id='t01'>\
                        <tr>\
                            <th>Word Cloud Usage</th>\
                        </tr>\
                        "
    func = ["word cloud <em><b>word</b></em>",
            "word cloud antonyms and synonyms <em><b>word</b></em>",
            "word cloud twitter <em><b>word</b></em>",
            "word cloud twitter user <em><b>word</b></em>"
            ]
    for i in func:
        j = i.replace('<b>', '[').replace('</b>', ']').replace('<em>', '').replace('</em>', '')
        display += f"<tr>\
                         <td onclick='man_complete(" + f'"{j}"' + f")'>{i}</td>\
                     </tr>"
    display += "</table>"
    say = "Find below How to use the Word Cloud feature"
    reply = {'display': display, 'say': say}
    return reply


def man_job_search():
    display = "<table id='t01'>\
                            <tr>\
                                <th>Job Search Usage</th>\
                            </tr>\
                            "
    func = ["job search average salary for <b>job</b> in <b>place</b>",
            "job search min salary for <b>job</b> in <b>place</b>",
            "job search max salary for <b>job</b> in <b>place</b>",
            "job search average salary graph for <b>job</b>"
            ]
    for i in func:
        j = i.replace('<b>', '[').replace('</b>', ']')
        display += f"<tr>\
                            <td onclick='man_complete(" + f'"{j}"' + f")'>{i}</td>\
                        </tr>"
    display += "</table>"
    say = "Find below How to use the Job search feature"
    reply = {'display': display, 'say': say}
    return reply


def man_image():
    display = "<table id='t01'>\
                            <tr>\
                                <th>Image Usage</th>\
                                <th>Description</th>\
                            </tr>\
                            "
    func = ["show image <b>image_query</b>",
            "show images <b>image_query</b>",
            ]
    des = ["returns a single image to match search query", "returns at least 10 images to match search query"]
    for i in func:
        j = i.replace('<b>', '[').replace('</b>', ']')
        display += f"<tr>\
                            <td onclick='man_complete(" + f'"{j}"' + f")'>{i}</td>\
                            <td onclick='man_complete(" + f'"{j}"' + f")'>{des[func.index(i)]}</td>\
                        </tr>"
    display += "</table>"
    say = "Find below How to use the image feature"
    reply = {'display': display, 'say': say}
    return reply


def man_windows():
    display = "<table id='t01'>\
                            <tr>\
                                <th>Windows Usage</th>\
                                <th>Description</th>\
                            </tr>\
                            "
    func = ["windows lock screen",
            "windows sort download folder",
            ]
    des = ["Lock your windows screen", "sort the files in the download folder by file type"]
    for i in func:
        display += f"<tr>\
                            <td onclick='man_complete(" + f'"{i}"' + f")'>{i}</td>\
                            <td onclick='man_complete(" + f'"{i}"' + f")'>{des[func.index(i)]}</td>\
                        </tr>"
    display += "</table>"
    say = "Find below How to use the Rihanna windows functionality"
    reply = {'display': display, 'say': say}
    return reply


def man_hot100():
    display = "<table id='t01'>\
                            <tr>\
                                <th>Feature</th>\
                                <th>Description</th>\
                            </tr>\
                            "
    func = ["hot 100 chart",
            ]
    des = ["displays chart",]
    for i in func:
        display += f"<tr>\
                            <td onclick='man_complete(" + f'"{i}"' + f")'>{i}</td>\
                            <td onclick='man_complete(" + f'"{i}"' + f")'>{des[func.index(i)]}</td>\
                        </tr>"
    display += "</table>"
    say = "Find hot 100 functionality"
    reply = {'display': display, 'say': say}
    return reply


def man_docker():
    display = "<table id='t01'>\
                            <tr>\
                                <th>Docker Usage</th>\
                                <th>Description</th>\
                            </tr>\
                            "

    func = {'docker image list': 'list images',
            'docker container list': 'list all containers',
            'docker container network': 'list container network setting',
            'docker container utilization': 'list container utilization',
            'docker run <b>image</b>': 'runs given image as container',
            'docker multi run <no of containers> <b>image</b>': 'runs multiple containers from a given image',
            'docker start <b>container</b>': 'starts given container',
            'docker stop <b>container</b>': 'stops given container',
            'docker pull <b>image</b>': 'adds image to repository',
            'docker image delete <b>image</b>': 'delete given image',
            'docker container delete <b>container</b>': 'delete given container',
            }
    for i in func:
        j = i.replace('<b>', '[').replace('</b>', ']')
        display += f"<tr>\
                             <td onclick='man_complete(" + f'"{j}"' + f")'>{i}</td>\
                             <td onclick='man_complete(" + f'"{j}"' + f")'>{func[i]}</td>\
                         </tr>"
    display += "</table>"
    say = "Find below How to use the Rihanna docker functionality"
    reply = {'display': display, 'say': say}
    return reply


def man_nhs():
    display = "<table id='t01'>\
                            <tr>\
                                <th>NHS Usage</th>\
                            </tr>\
                            "
    func = ['nhs review on <b>condition</b>',
            'nhs prevention for <b>condition</b>',
            'nhs overview for <b>condition</b>',
            'nhs symptoms for <b>condition</b>',
            'nhs treatments overview for <b>condition</b>',
            'nhs self care advice for <b>condition</b>',
            'nhs other treatments for <b>condition</b>',
            'nhs causes for <b>condition</b>',
            'nhs health news',
            'nhs medicine information on <b>drug</b>',
            'nhs search <b>query</b>']
    for i in func:
        j = i.replace('<b>', '[').replace('</b>', ']')
        display += f"<tr>\
                            <td onclick='man_complete(" + f'"{j}"' + f")'>{i}</td>\
                        </tr>"
    display += "</table>"
    say = "Find below How to use the NHS feature"
    reply = {'display': display, 'say': say}
    return reply


def man_sound_cloud():
    display = "<table id='t01'>\
                            <tr>\
                                <th>Sound cloud Usage</th>\
                                <th>Description</th>\
                            </tr>\
                            "

    func = {'sound cloud play <b>song</b>': 'plays sound from sound cloud',
            'sound cloud play song cloud playlist': 'plays a playlist',
            'sound cloud play a random song': 'plays a random song'
            }
    for i in func:
        j = i.replace('<b>', '[').replace('</b>', ']')
        display += f"<tr>\
                             <td onclick='man_complete(" + f'"{j}"' + f")'>{i}</td>\
                             <td onclick='man_complete(" + f'"{j}"' + f")'>{func[i]}</td>\
                         </tr>"
    display += "</table>"
    say = "Find below How to use the sound cloud functionality"
    reply = {'display': display, 'say': say}
    return reply


def man_map():
    display = "<table id='t01'>\
                            <tr>\
                                <th>Map Usage</th>\
                                <th>Description</th>\
                            </tr>\
                            "

    func = {'map <b>London bridge UK</b>': 'displays location on map',
            }
    for i in func:
        j = i.replace('<b>', '[').replace('</b>', ']')
        display += f"<tr>\
                             <td onclick='man_complete(" + f'"{j}"' + f")'>{i}</td>\
                             <td onclick='man_complete(" + f'"{j}"' + f")'>{func[i]}</td>\
                         </tr>"
    display += "</table>"
    say = "Find below How to use the map functionality"
    reply = {'display': display, 'say': say}
    return reply


def man_news_():
    display = "<table id='t01'>\
                            <tr>\
                                <th>News feature</th>\
                                <th>Description</th>\
                            </tr>\
                            "

    func = {'news headline in <b>uk</b>': 'displays top 10 news headlines in a selected country',
            'news headline search <b>trump</b> in <b>uk</b>': 'search for top news in a country',
            'news headline with category <b>business</b> in <b>uk</b>':
                'find for top news in a country with diff categories',
            'news categories': 'shows the categories options',
            'news headline': 'shows the headlines in the default country uk',
            }
    for i in func:
        j = i.replace('<b>', '[').replace('</b>', ']')
        display += f"<tr>\
                             <td onclick='man_complete(" + f'"{j}"' + f")'>{i}</td>\
                             <td onclick='man_complete(" + f'"{j}"' + f")'>{func[i]}</td>\
                         </tr>"
    display += "</table>"
    say = "Find below How to use the News functionality"
    reply = {'display': display, 'say': say}
    return reply


def man_alpha():
    display = "<table id='t01'>\
                            <tr>\
                                <th>feature</th>\
                                <th>Description</th>\
                            </tr>\
                            "

    func = {'solve <b>x + 5 = 10</b>': 'solves equation',
            'solve <b>x + 5 = 10</b> show working': 'solves equation with workings',
            'rihanna tell me a dirty joke': 'says a joke',
            'rihanna tell me a computer science joke': 'says a joke',
            'rihanna tell me a physics joke': 'says a joke',
            'solve x^4 - 4x^3 + 8x + 1': 'solves equation',
            'solve 1/(1+sqrt(2))': 'solves equation',  # truth table p xor q xor r xor s
            'solve truth table p xor q xor r xor s': 'solves equation',
            'solve area of a circle with radius 2': 'finds area',
            'rihanna polar plot r=1+cos theta': 'plots graph',
            'rihanna plot 1,2,3,4,5,6,7': 'plots graph',
            'rihanna {25, 35, 10, 17, 29, 14, 21, 31}': 'data analysis',
            'rihanna 5, 12, 13 triangle': 'triangle details',
            'rihanna sequence of Fibonacci numbers': 'details',
            'rihanna integrate x^2': 'displays solution',
            'rihanna 1, 4, 9, 16, 25, ...': 'computes',
            'rihanna H2SO4': 'chemistry knowledge',
            'rihanna how many elements in the periodic table': 'chemistry knowledge',
            'rihanna carbon': 'chemistry knowledge',
            'rihanna 10 densest elements': 'chemistry knowledge',
            "rihanna Newton's laws": 'physics knowledge',
            'rihanna Brownian motion': 'physics knowledge',
            'rihanna speed of light': 'physics knowledge',
            'rihanna Oscar for best actress 1982': 'entertainment knowledge',
            'rihanna bible john 3:16': 'bible verses',
            }
    for i in func:
        j = i.replace('<b>', '[').replace('</b>', ']')
        display += f"<tr>\
                             <td onclick='man_complete(" + f'"{j}"' + f")'>{i}</td>\
                             <td onclick='man_complete(" + f'"{j}"' + f")'>{func[i]}</td>\
                         </tr>"
    display += "</table>"
    say = "Find below How to use the rihanna alpha functionality"
    reply = {'display': display, 'say': say}
    return reply


man_dict = {'man help': man_help, 'man maths': man_maths, 'man twitter': man_twitter, 'man tfl': man_tfl,
            'man news': man_news, 'man email': man_email, 'man skype': man_skype, 'man facebook': man_facebook,
            'man football': man_football, 'man time': man_time, 'man date': man_date, 'man weather': man_weather,
            'man youtube': man_youtube, 'man google': man_google, 'man wikipedia': man_wiki, 'man wiki': man_wiki,
            'man amazon': man_amazon, 'man dictionary': man_dictionary, 'man iot': man_iot, 'man windows': man_windows,
            'man word cloud': man_word_cloud, 'man job search': man_job_search, 'man image': man_image,
            'man docker': man_docker, 'man nhs': man_nhs, 'man sound cloud': man_sound_cloud,
            'man rihanna news': man_news_, 'man rihanna': man_alpha, 'man hot 100': man_hot100, 'man map': man_map}
