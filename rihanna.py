from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import requests
import wikipedia
import pyttsx3
from selenium import webdriver
import rihanna_tweet
import rihanna_tfl

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
        print('')


def play_song(song):
    driver = webdriver.Chrome(executable_path=r"C:\Program Files\chrome driver\chromedriver.exe")
    query = "https://www.youtube.com/results?search_query="
    search = query + song
    driver.get(search)
    driver.find_element_by_xpath(xpath='//*[@id="dismissable"]').click()


def weather(place):
    try:
        api_address = 'http://api.openweathermap.org/data/2.5/weather?appid=adaf7aa8e77b0dd6f92d6e86091fba1b&q='
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


def rihanna(message):
    if {"trending", "twitter", "topics"} - set(message.strip().lower().split()) == set():
        reply = rihanna_tweet.twitter_trend()
        return reply

    elif message.strip().lower() == ('what is your name' or 'what is your name?'):
        reply = "My name is Rihanna"
        # rihanna_voice(reply)
        return reply
    elif message.strip()[0:7] == 'what is':
        try:
            reply = wikipedia.summary(message.strip()[7:], sentences=1)
            # rihanna_voice(reply)
            return reply

        except:
            # rihanna_voice("{}? hmm.. I know what it is but I can not tell you".format(message.strip()[7:]))
            return '{}? hmm.. I know what it is but I can not tell you'.format(message.strip()[7:])

    elif message.strip() == 'weather forecast today':
        reply = weather('london,uk')
        # rihanna_voice(reply)
        return reply

    elif message.strip() == 'show my twitter status':
        reply = rihanna_tweet.twitter_status()
        return reply

    elif message.strip()[:23] == 'show twitter status for':
        user = message.strip()[24:]
        reply = rihanna_tweet.twitter_status_others(user)
        return reply

    elif message.strip() == 'show my last tweet':
        reply = rihanna_tweet.last_tweet()
        return reply

    elif message.strip()[:28] == 'show last twitter status for':
        user = message.strip()[29:]
        reply = rihanna_tweet.display_last_tweet(user)
        return reply

    elif message.strip()[:5] == 'tweet':
        tweet = message.strip()[6:]
        reply = rihanna_tweet.post_tweet(tweet)
        rihanna_tweet.display_twitter()
        return reply

    elif message.strip().lower()[:6] == 'google':
        search = message.strip()[7:]
        display = google_search(search)
        reply = "Googling . . ."
        return reply

    elif message.strip().lower()[:19] == 'tube service report':
        reply = rihanna_tfl.tfl_tube_status()
        return reply

    elif message.strip().lower()[:21] == 'journey duration from':  # e.g journey duration from se1 5hp to se18 3px
        detail = message.strip().lower()[22:].split('to')
        reply = rihanna_tfl.journey_duration(detail[0], detail[1])
        return reply

    elif message.strip().lower()[:17] == 'live arrivals for':     # e.g live arrivals for 53 at dunton road
        detail = message.strip().lower()[18:].split('at')
        reply = rihanna_tfl.get_timetable(detail[0], detail[1])
        return reply

    elif message.strip()[0:16] == 'weather forecast':
        reply = weather(message.strip()[16:].strip())
        # rihanna_voice(reply)
        return reply

    elif message.strip()[0:4] == 'play':
        # rihanna_voice('Searching for {}'.format(message.strip()[5:]))
        play_song(message.strip()[5:])
        return '{} is a lovely song'.format(message.strip()[5:])

    elif message.strip() != 'Bye':
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
                          'threshold': 0.70,
                          'default_response': 'I am sorry. I am not allowed to give an answer to that question.'
                      }
                  ],
                  trainer='chatterbot.trainers.ListTrainer')
    bot.set_trainer(ListTrainer)
    while True:
        if usrText.strip() != 'Bye':
            result = rihanna(usrText)
            reply = str(result)
            return reply
        elif usrText.strip() == 'Bye':
            return 'Bye'
            break

#d = google_search("when is the wilder fight date")
#print('hello')