from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import requests
import wikipedia
import pyttsx3
from selenium import webdriver
from rihanna_bot import rihanna_football, rihanna_speak, rihanna_tweet, rihanna_news, rihanna_skype, rihanna_one_char, \
    rihanna_time, rihanna_maths as calc, rihanna_email, rihanna_tfl, rihanna_spell, rihanna_facebook, rihanna_amazon, \
    rihanna_dict, rihanna_iot, rihanna_wc, rihanna_sound_cloud, ri_news, rihanna_science, rihanna_maps, \
    rihanna_man, rihanna_job, ri_youtube, ri_image, rihanna_windows, rihanna_docker, rihanna_nhs, hot100, \
    rihanna_movies, rihanna_lyrics
import config
import random as r

bot = ChatBot('Bot', storage_adapter='chatterbot.storage.SQLStorageAdapter',
              logic_adapters=[
                  {'import_path': 'chatterbot.logic.BestMatch'},
                  {'import_path': 'chatterbot.logic.LowConfidenceAdapter',
                   'threshold': 0.50,
                   'default_response': 'I am sorry. I am not allowed to answer that question'
                   }
              ],
              trainer='chatterbot.trainers.ListTrainer')
bot.set_trainer(ListTrainer)

break_words = ["yes", "no", "okay", "yeah", "ok", "nah", "alright", "i see"]
_date = ("what is the date", "what is todays date", "todays date", "current date", "date")
_time = ("what is the time", "time", "what is the current time", "current time")
email = {'msg': '', 'address': '', 'subject': '', 'run': 0}
run_email = {1: 'which email address do you want to send to?', 2: 'what is the subject?',
             3: 'what do you wish to send to '}
laugh = ["haha", "lol", "hahaha", "ha", "lool"]


def email_thread(message):
    global email

    if email['run'] == 4:
        msg = message
        address = email['address']
        subject = email['subject']
        email = {'msg': '', 'address': '', 'subject': '', 'run': 0}
        return rihanna_email.send_email(subject=subject, msg=msg, _send_email=address)

    elif email['run'] == 3:
        email['subject'] = message
        reply = run_email[3] + email['address']
        return {'display': reply, 'say': reply}

    elif email['run'] == 1:
        reply = run_email[1]
        return {'display': reply, 'say': reply}

    elif email['run'] == 2:
        if rihanna_email.check(message) == 'valid':
            email['address'] = message
            reply = run_email[2]
            return {'display': reply, 'say': reply}
        elif message in rihanna_email.contact:
            email['address'] = rihanna_email.contact[message]
            reply = run_email[2]
            return {'display': reply, 'say': reply}
        else:
            email['run'] -= 1
            reply = f"{message} is an invalid email, please give a valid mail"
            return {'display': reply, 'say': reply}


def rihanna_voice(word_speech):
    engine = pyttsx3.init()
    engine.say(word_speech)
    engine.runAndWait()


def google_search(query):
    try:
        driver = webdriver.Chrome(executable_path=r"C:\Program Files\chrome driver\chromedriver.exe")
        google = "https://www.google.com/search?q="
        search = google + query
        driver.get(search)
        return driver
    except Exception as e:
        return "Web Driver Failed"


def play_song(song):
    driver = webdriver.Chrome(executable_path=r"C:\Program Files\chrome driver\chromedriver.exe")
    query = "https://www.youtube.com/results?search_query="
    search = query + song
    driver.get(search)
    driver.find_element_by_xpath(xpath='//*[@id="dismissable"]').click()

heart_effect = 0


def add_heart_effect():
    global heart_effect
    say = 'I am not programmed to love. However, your mouse cursor is'

    if heart_effect == 0:
        display = f'<script>putMouse()</script> {say}'

        heart_effect = 1
    else:
        display = "<img src='img/heart.png' width='70px'>"
        say = 'I know, you have already mentioned it'
    return {'display': display, 'say': say}


def remove_heart_effect():
    global heart_effect
    say = 'Oh well. It was good while it lasted. Mouse, Deactivate!'

    if heart_effect == 1:
        display = f'<script>removeMouse()</script> {say}'

        heart_effect = 0
    else:
        display = say = f"That doesnt hurt my feelings. Because, I dont have one"
    return {'display': display, 'say': say}


def format_string(string):
    d = "!?\|:;@'][<>"

    for c in d:
        if c in string:
            string = string.replace(c, '')
    return string


def weather(place):
    try:
        api_address = f'http://api.openweathermap.org/data/2.5/weather?appid={config.weather_id}='
        word = place.split(' ')
        if len(word) == 1:
            city = word[0]
        else:
            city = word[0] + ',' + word[1]

        url = api_address + city

        json_data = requests.get(url).json()
        desc = json_data['weather'][0]['description']
        temp_f = json_data['main']['temp']
        wind = json_data['wind']['speed']

        temp_c = round(temp_f - 273)

        forecast = f"{desc} in {city}. The temperature is {temp_c}° celcius with wind speed of {wind}"

    except:
        forecast = 'Sorry could not find location {}'.format(place)

    return forecast


def stop_words():
    response = ["okay", "ok", "alright", "great", "Thought as much", "Good"]

    reply = response[r.randrange(len(response))]
    return {'display': reply, 'say': reply}


def funny():
    response = ["its not that funny", "lol", "i am surprised you have a sense of humor",
                "funny eh?", "I know, I am hilarious", "haha"]

    reply = response[r.randrange(len(response))]
    return {'display': reply, 'say': reply}


def rihanna(message):
    if (message[:len("dictionary translate")] != "dictionary translate") and (
            rihanna_dict.detect_lang(message) != 'en'):
        config.lang_code = rihanna_dict.detect_lang(message)
        message = rihanna_dict.translate_sentence_code(query=message, lang='en')['display']

        # print(f'trans: {message} \n l_code: {lang_code}')

        # Formatting message input
    if email['run'] == 0:
        if message.lower()[:3] == 'tfl':
            message = format_string(message).lower().strip()

        elif message.lower()[:5] == 'skype':
            return rihanna_skype.selector(format_string(message[6:]).lower().strip())
        elif message.lower()[:len('solve')] == 'solve':
            return rihanna_science.selector(message)
        elif message.lower()[:len('rihanna ')] == 'rihanna ':
            msg = message.lower()[len('rihanna '):]
            return rihanna_science.selector(msg)
        elif message[:len('map')] == 'map':
            return rihanna_maps.selector(format_string(message))
        elif message[:len('lyrics')] == 'lyrics':
            return rihanna_lyrics.selector(format_string(message))
        elif message[:len('billboard')] == 'billboard':
            return hot100.selector(message)
        elif message.lower()[:len('iot')] == 'iot':
            return rihanna_iot.selector(format_string(message).lower().strip())
        elif message.lower()[:len('man')] == 'man':
            return rihanna_man.selector(format_string(message).lower().strip())
        elif message[-len('movies'):] == 'movies':
            return rihanna_movies.selector(format_string(message))
        elif message.lower()[:len('amazon')] == 'amazon':
            return rihanna_amazon.selector(format_string(message).lower().strip())
        elif message.lower()[:len('youtube')] == 'youtube':
            msg = format_string(message).lower().strip()
            return ri_youtube.selector(msg)
        elif message.lower()[:len('sound cloud')] == 'sound cloud':
            msg = format_string(message).lower().strip()
            return rihanna_sound_cloud.selector(msg)
        elif message.lower()[:len('dictionary')] == 'dictionary':
            return rihanna_dict.selector(format_string(message).lower().strip())
        elif message.lower()[:len('job search')] == 'job search':
            return rihanna_job.selector(format_string(message).lower().strip())
        elif message.lower()[:len('docker')] == 'docker':
            return rihanna_docker.selector(message.lower().strip())
        elif message.strip().lower() in laugh:
            return funny()
        else:
            message = rihanna_spell.auto_correct(format_string(message).lower().strip())
    else:
        message = rihanna_spell.auto_correct(message.lower().strip())

    # Main Decision Thread
    if email['run'] != 0:
        email['run'] += 1
        return email_thread(message)

    elif rihanna_football.football_key['status'] == 1:
        return rihanna_football.football_switch(message)

    elif {"send", "email"} - set(message.split()) == set():
        email['run'] += 1
        return email_thread(message)

    elif (len(message) == 1) or message.isdigit():
        return rihanna_one_char.main(message)

    elif message == 'i love you':
        return add_heart_effect()

    elif message == 'i hate you':
        return remove_heart_effect()

    elif message[:len('word cloud')] == 'word cloud':
        return rihanna_wc.selector(message)

    elif message[:len('nhs')] == 'nhs':
        return rihanna_nhs.selector(message)

    elif message[:len('hot 100')] == 'hot 100':
        return hot100.selector(message)

    elif message[:len('show image')] == 'show image':
        return ri_image.selector(message)

    elif message[:len('windows')] == 'windows':
        return rihanna_windows.selector(message)

    elif ("twitter" in message) or ("tweet" in message):
        return rihanna_tweet.twitter(message)

    elif message in break_words:
        reply = stop_words()
        if config.lang_code != 'en':
            reply = rihanna_dict.translate_sentence_code(reply, config.lang_code)
            config.lang_code = 'en'
        return reply

    elif message == 'why':
        reply = "Sorry, I cant tell you. Its a secret"
        if config.lang_code != 'en':
            reply = rihanna_dict.translate_sentence_code(reply, config.lang_code)
            config.lang_code = 'en'
        return reply

    elif message == 'what is your name':
        reply = "My name is Rihanna"
        if config.lang_code != 'en':
            reply = rihanna_dict.translate_sentence_code(reply, config.lang_code)
            config.lang_code = 'en'
            return reply
        return {'display': reply, 'say': reply}

    elif message in _date:
        reply = rihanna_time.rihanna_date()
        return reply

    elif message in _time:
        reply = rihanna_time.rihanna_time()
        return reply

    elif message[0:7] == 'what is':
        try:
            reply = wikipedia.summary(message.strip()[7:], sentences=1)
            if config.lang_code != 'en':
                reply = rihanna_dict.translate_sentence_code(reply, config.lang_code)
                config.lang_code = 'en'
                return reply
            return {'display': reply, 'say': reply}

        except:
            reply = "{}? hmm.. I know what it is but I can not tell you".format(message.strip()[7:])
            if config.lang_code != 'en':
                reply = rihanna_dict.translate_sentence_code(reply, config.lang_code)
                config.lang_code = 'en'
                return reply
            return {'display': reply, 'say': reply}

    elif {"bbc", "news"} - set(message.split()) == set():
        reply = rihanna_news.bbc()
        return reply

    elif message[:len('news')] == 'news':
        return ri_news.selector(message)

    elif message == 'weather forecast today':
        reply = weather('london,uk')
        # rihanna_voice(reply)
        if config.lang_code != 'en':
            reply = rihanna_dict.translate_sentence_code(reply, config.lang_code)
            config.lang_code = 'en'
            return reply
        return {'display': reply, 'say': reply}

    elif "facebook" in message:
        return rihanna_facebook.fb(message)

    elif message[:8] == 'football':
        reply = rihanna_football.football(message)
        return reply

    elif message[:9] == 'calculate':
        data = message.strip()[10:]
        reply = calc.calculate(data)
        return reply

    elif message[:6] == 'google':
        search = message.strip()[7:]
        display = google_search(search)
        reply = "Googling . . ."
        if config.lang_code != 'en':
            reply = rihanna_dict.translate_sentence_code(reply, config.lang_code)
            config.lang_code = 'en'
        return reply

    elif message[:3] == 'tfl':
        return rihanna_tfl.tfl(message)

    elif message[0:16] == 'weather forecast':
        reply = weather(message.strip()[16:].strip())
        if config.lang_code != 'en':
            reply = rihanna_dict.translate_sentence_code(reply, config.lang_code)
            config.lang_code = 'en'
            return reply
        return {'display': reply, 'say': reply}

    elif message[0:4] == 'play':
        critic = ['that is a lovely song', 'that is a terrible song', "don't like that song",
                  "that's my jam", "someone turn the music up", "you have a terrible song taste"]
        # rihanna_voice('Searching for {}'.format(message.strip()[5:]))
        play_song(message.strip()[5:])
        reply = critic[r.randrange(len(critic))]
        if config.lang_code != 'en':
            reply = rihanna_dict.translate_sentence_code(reply, config.lang_code)
            config.lang_code = 'en'
            return reply
        return {'display': reply, 'say': reply}

    elif len([i for i in calc.opp_code if i in message]) > 0:
        reply = calc.calculate(message)
        return reply

    elif message == 'lock screen':
        import ctypes
        ctypes.windll.user32.LockWorkStation()

    elif message != 'Bye':
        reply = str(bot.get_response(message)).replace('-', '')

        if config.lang_code != 'en':
            reply = rihanna_dict.translate_sentence_code(reply, config.lang_code)
            config.lang_code = 'en'
            return reply
        return {'display': reply, 'say': reply}


def get_response(usrText):
    bot = ChatBot('Bot',
                  storage_adapter='chatterbot.storage.SQLStorageAdapter',
                  logic_adapters=[
                      {
                          'import_path': 'chatterbot.logic.BestMatch'
                      },
                      {
                          'import_path': 'chatterbot.logic.LowConfidenceAdapter',
                          'threshold': 0.50,
                          'default_response': 'I am sorry. I am not allowed to give an answer to that question.'
                      }
                  ],
                  trainer='chatterbot.trainers.ListTrainer')
    bot.set_trainer(ListTrainer)
    while True:
        if usrText.strip() == 'click':
            text = rihanna_speak.speech_recog()
            print(f'speech: {text.strip()}')
            if text == 'sorry, could not recognize your voice':
                reply = str(text)
                return str({'display': reply, 'say': reply})
            else:
                result = rihanna(text.strip())
                if type(result).__name__ == 'dict':
                    result['user_said'] = text.strip()
                    reply = str(result)
                    return reply
                else:
                    print('Not dict', result)
                    result = f"{text};{result}"
                    reply = str(result)
                    return reply
                # return str({'user_said': text, 'reply': result, 'voice_check': 0, 'say': ''})

        elif usrText.strip() != 'Bye':
            result = rihanna(usrText)
            reply = str(result)
            #print(result)
            return reply  # reply should be string else it wont work
        elif usrText.strip() == 'Bye':
            reply = 'Bye'
            return str({'display': reply, 'say': reply})


# d = google_search("when is the wilder fight date")
# print('hello')
# print(rihanna('journey duration from se18 3px to se1 5hp'))
# print(rihanna("amazon least price for external hard drive 2tb"))
# print(get_response("jugar drake va mal"))
