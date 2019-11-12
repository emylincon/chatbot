from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import requests
import wikipedia
import pyttsx3
from selenium import webdriver
import re


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


def play_song(song):
    # chromedriver = "C:\Program Files\chrome driver"
    # driver = webdriver.Chrome(chromedriver)
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
    if message.strip()[0:7] == 'what is':
        try:
            reply = wikipedia.summary(message.strip()[7:], sentences=1)
            #rihanna_voice(reply)
            return(reply)

        except:
            #rihanna_voice("{}? hmm.. I know what it is but I can not tell you".format(message.strip()[7:]))
            return('{}? hmm.. I know what it is but I can not tell you'.format(message.strip()[7:]))

    
    elif message.strip() == 'weather forecast today':
        reply = weather('london,uk')
        #rihanna_voice(reply)
        return(reply)

    elif message.strip().lower() == 'what is your name' or 'what is your name?':
        reply = "My name is Rihanna"
        #rihanna_voice(reply)
        return(reply)


    elif message.strip()[0:16] == 'weather forecast':
        reply = weather(message.strip()[16:].strip())
        #rihanna_voice(reply)
        return(reply)


    elif message.strip()[0:4] == 'play':
        #rihanna_voice('Searching for {}'.format(message.strip()[5:]))
        play_song(message.strip()[5:])
        return ('{} is a lovely song'.format(message.strip()[5:]))

    elif message.strip() != 'Bye':
        reply = bot.get_response(message)

        if str(reply)[:3] == '- -':
            #rihanna_voice(str(reply)[3:])
            reply = str(reply)[3:]
        elif str(reply)[0] == '-':
            #rihanna_voice(str(reply)[1:])
            reply = str(reply)[1:]
        else:
            #rihanna_voice(reply)
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
        if usrText.strip()!= 'Bye':
            result = rihanna(usrText)
            reply = str(result)
            return(reply)
        elif usrText.strip() == 'Bye':
            return('Bye')
            break
        

        
