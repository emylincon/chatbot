from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import requests
import wikipedia
import pyttsx3
from selenium import webdriver
from rihanna_bot import rihanna_football, rihanna_speak, rihanna_tweet, rihanna_news, rihanna_skype, rihanna_one_char, \
    rihanna_time, rihanna_maths as calc, rihanna_email, rihanna_tfl, rihanna_spell, rihanna_facebook
import config
import random as r

bot = ChatBot('Bot', storage_adapter='chatterbot.storage.SQLStorageAdapter',
              logic_adapters=[
                  {'import_path': 'chatterbot.logic.BestMatch'},
                  {'import_path': 'chatterbot.logic.LowConfidenceAdapter',
                   'threshold': 0.50,
                   'default_response': 'I am sorry. I am not allowed to give an answer to that question.'
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
        return run_email[3] + email['address']

    elif email['run'] == 1:
        return run_email[1]

    elif email['run'] == 2:
        if rihanna_email.check(message) == 'valid':
            email['address'] = message
            return run_email[2]
        elif message in rihanna_email.contact:
            email['address'] = rihanna_email.contact[message]
            return run_email[2]
        else:
            email['run'] -= 1
            return f"{message} is an invalid email, please give a valid mail"


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


def format_string(string):
    d = "!?\|:;@'"

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
        forecast = 'Sorry could not find {}'.format(place)

    return forecast


def stop_words():
    response = ["okay", "ok", "alright", "great", "Thought as much", "Good"]

    return response[r.randrange(len(response))]


def rihanna(message):

    # Formatting message input
    if email['run'] == 0:
        if message[:3] == 'tfl':
            message = format_string(message).lower().strip()
        elif message[:12] == 'show picture':
            return rihanna_skype.show_picture(message[13:].strip())
        elif message[:len('birthday for')] == 'birthday for':
            return rihanna_skype.birthday(message[len('birthday for') + 1:].strip())
        elif message[:5] == 'skype':
            return rihanna_skype._skype(message[6:])
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

    elif ("twitter" in message) or ("tweet" in message):
        return rihanna_tweet.twitter(message)

    elif message in break_words:
        reply = stop_words()
        return reply

    elif message == 'why':
        return "Sorry, I cant tell you. Its a secret"

    elif message == 'what is your name':
        reply = "My name is Rihanna"
        # rihanna_voice(reply)
        return reply

    elif message in _date:
        reply = rihanna_time.rihanna_date()
        return reply

    elif message in _time:
        reply = rihanna_time.rihanna_time()
        return reply

    elif message[0:7] == 'what is':
        try:
            reply = wikipedia.summary(message.strip()[7:], sentences=1)
            # rihanna_voice(reply)
            return reply

        except:
            # rihanna_voice("{}? hmm.. I know what it is but I can not tell you".format(message.strip()[7:]))
            return '{}? hmm.. I know what it is but I can not tell you'.format(message.strip()[7:])

    elif {"bbc", "news"} - set(message.split()) == set():
        reply = rihanna_news.bbc()
        return reply

    elif message == 'weather forecast today':
        reply = weather('london,uk')
        # rihanna_voice(reply)
        return reply

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
        return reply

    elif message[:3] == 'tfl':
        return rihanna_tfl.tfl(message)

    elif message[0:16] == 'weather forecast':
        reply = weather(message.strip()[16:].strip())
        # rihanna_voice(reply)
        return reply

    elif message[0:4] == 'play':
        critic = ['that is a lovely song', 'that is a terrible song', "don't like that song",
                  "that's my jam", "someone turn the music up", "you have a terrible song taste"]
        # rihanna_voice('Searching for {}'.format(message.strip()[5:]))
        play_song(message.strip()[5:])
        return critic[r.randrange(len(critic))]

    elif len([i for i in calc.opp_code if i in message]) > 0:
        reply = calc.calculate(message)
        return reply

    elif message != 'Bye':
        reply = bot.get_response(message)

        if str(reply)[:3] == '- -':
            # rihanna_voice(str(reply)[3:])
            reply = str(reply)[3:]
        elif str(reply)[0] == '-':
            # rihanna_voice(str(reply)[1:])
            reply = str(reply)[1:]
        else:
            # rihanna_voice(reply)
            pass
        return reply


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
            if text == 'sorry could not recognize your voice':
                reply = str(text)
                return reply
            else:
                result = rihanna(text.strip())
                result = f"{text};{result}"
                reply = str(result)
                return reply
        elif usrText.strip() != 'Bye':
            result = rihanna(usrText)
            reply = str(result)
            return reply
        elif usrText.strip() == 'Bye':
            return 'Bye'


# d = google_search("when is the wilder fight date")
# print('hello')
# print(rihanna('journey duration from se18 3px to se1 5hp'))
