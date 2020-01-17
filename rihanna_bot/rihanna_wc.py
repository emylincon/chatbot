#rihanna world cloud
import sys
from os import path
import numpy as np
from PIL import Image
import wikipedia
from wordcloud import WordCloud, STOPWORDS
from rihanna_bot import rihanna_dict
import time
import os

# get path to script's directory
currdir = path.dirname(__file__)


def selector(msg):

    if msg[:len('word cloud antonyms and synonyms')] == 'word cloud antonyms and synonyms':
        query = msg[len('word cloud antonyms and synonyms')+1:]
        return word_cloud_syn_ant(query)
    elif msg[:len('word cloud')] == 'word cloud':
        query = msg[len('word cloud')+1:]
        return word_cloud(query)


def get_wiki(query):
    # get best matching title for given query
    title = wikipedia.search(query)[0]

    # get wikipedia page for selected title
    page = wikipedia.page(title)
    return page.content


def create_wordcloud(text):
    # create numpy araay for wordcloud mask image
    mask = np.array(Image.open(path.join(currdir, "cloud.png")))

    # create set of stopwords
    stopwords = set(STOPWORDS)

    # create wordcloud object
    wc = WordCloud(background_color="white",
                   max_words=200,
                   mask=mask,
                   stopwords=stopwords)

    # generate wordcloud
    wc.generate(text)

    # save wordcloud
    wc.to_file(path.join(currdir, r"C:\Users\emyli\PycharmProjects\Chatbot_Project\wc.png"))


def word_cloud_syn_ant(query):
    path = rf'C:\Users\emyli\PycharmProjects\Chatbot_Project\wc.png'
    try:
        os.remove(path)
    except Exception as e:
        pass
    text = rihanna_dict.ant_syn(query)
    # generate wordcloud
    create_wordcloud(text)
    time.sleep(3)

    reply = {'display': f'<img src="wc.png?{time.time()}" alt="Test image" width="65%" height="65%">',
             'say': f'find word cloud for {query}'}

    return reply


def word_cloud(query):
    path = rf'C:\Users\emyli\PycharmProjects\Chatbot_Project\wc.png'
    try:
        os.remove(path)
    except Exception as e:
        pass
    # get text for given query
    text = get_wiki(query)
    # generate wordcloud
    create_wordcloud(text)
    time.sleep(3)

    reply = {'display': f'<img src="wc.png?{time.time()}" alt="Test image" width="65%" height="65%">',
             'say': f'find word cloud for {query}'}

    return reply

