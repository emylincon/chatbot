import twitter
from selenium import webdriver
import time
import ast
import config
import re
import matplotlib.pyplot as plt
import numpy as np
import urllib.request
import urllib.parse
import json
from textblob import TextBlob


def embed_tweet(query):
    request_headers = {
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"
    }

    url = f"https://publish.twitter.com/oembed?url={query}"
    request = urllib.request.Request(url, headers=request_headers)
    contents = json.loads(urllib.request.urlopen(request).read())
    return contents['html']


api = twitter.Api(consumer_key=config.consumer_key,
                  consumer_secret=config.consumer_secret,
                  access_token_key=config.access_token,
                  access_token_secret=config.access_token_secret)


def google_search(query):
    try:
        driver = webdriver.Chrome(executable_path=r"C:\Program Files\chrome driver\chromedriver.exe")
        google = "https://www.google.com/search?q="
        search = google + query
        driver.get(search)
        return driver
    except Exception as e:
        return "Web Driver Failed"


def twitter(message):
    if {"global", "trending", "twitter", "topics", "graph"} - set(message.split()) == set():
        reply = twitter_global_trends_graph()
        return reply
    elif {"global", "trending", "twitter", "topics"} - set(message.split()) == set():
        reply = twitter_global_trends()
        return reply

    elif {"trending", "twitter", "topics"} - set(message.split()) == set():
        reply = twitter_trend()
        return reply

    elif message == 'show my twitter status':
        reply = twitter_status()
        return reply

    elif message[:23] == 'show twitter status for':
        user = message.strip()[24:]
        reply = twitter_status_others(user)
        return reply

    elif message == 'show my last tweet':
        reply = last_tweet()
        return reply

    elif message[:len('twitter sentiment for ')] == 'twitter sentiment for ':
        query = message[len('twitter sentiment for '):].strip()
        reply = sentiment_report(query)
        return reply

    elif message[:28] == 'show last twitter status for':
        user = message.strip()[29:]
        reply = display_last_tweet(user)
        return reply

    elif message[:5] == 'tweet':
        try:
            tweet = message.strip()[6:]
            reply = post_tweet(tweet)
            #display_twitter()
            return reply
        except Exception as e:
            reply = "Error occurred in twitter"
            return {'display': reply, 'say': reply}

    elif message[:14] == 'search twitter':
        search = message[15:].strip()
        #reply = twitter_search_(search)
        reply = search_twitter(query=search)
        return reply

    elif message[:len('show twitter hash tags associated with')] == 'show twitter hash tags associated with':
        x = len('show twitter hash tags associated with')
        query = message[x+1:]
        return twitter_hash_tags(query)

    else:
        display = google_search(message)
        reply = "Googling . . ."
        return {'display': reply, 'say': reply}


def twitter_status_others(user):
    try:
        followers_count = len(api.GetFollowers(screen_name=user))
        friends_count = len(api.GetFriends(screen_name=user))
        reply = f"{user} have {followers_count} followers and {friends_count} friends following you on twitter"
        return {'display': reply, 'say': reply}
    except Exception as e:
        reply = "Due to Twitter Restrictions, You have reached your lookup limit. Try again in 15 minutes"
        return {'display': reply, 'say': reply}


def twitter_status():
    followers_count = len(api.GetFollowers())
    friends_count = len(api.GetFriends())
    reply = f"You have {followers_count} followers and {friends_count} friends following you on twitter"
    return {'display': reply, 'say': reply}


def display_last_tweet(user):
    try:
        reply = api.GetUserTimeline(screen_name=user)[0].text
        status = api.GetUserTimeline(screen_name=user)[0].id
        url = f"https://twitter.com/{user}/status/{status}"
        display = embed_tweet(query=url)
        return {'display': display, 'say': reply}
    except Exception as e:
        reply = "Due to Twitter Restrictions, You have reached your lookup limit. Try again in 15 minutes"
        return {'display': reply, 'say': reply}


def last_tweet():
    reply = api.GetUserTimeline()[0].text
    status = api.GetUserTimeline(screen_name='jamesemyking')[0].id
    url = f"https://twitter.com/jamesemyking/status/{status}"
    display = embed_tweet(query=url)
    return {'display': display, 'say': reply}


def post_tweet(tweet):
    api.PostUpdates(tweet)
    status = api.GetUserTimeline(screen_name='jamesemyking')[0].id
    url = f"https://twitter.com/jamesemyking/status/{status}"
    display = embed_tweet(query=url)
    say = "Tweet posted"
    return {'display': display, 'say': say}


def display_twitter():
    # chromedriver = "C:\Program Files\chrome driver"
    # driver = webdriver.Chrome(chromedriver)
    driver = webdriver.Chrome(executable_path=r"C:\Program Files\chrome driver\chromedriver.exe")
    query = "https://twitter.com/jamesemyking"
    driver.get(query)
    time.sleep(10)


def twitter_trend():
    results = api.GetTrendsWoeid(woeid=23424975)

    reply = "Top UK Trends in Twitter: <br>"
    say = "Top UK Trends in Twitter \n"
    for _location in results[:5]:
        reply += f"<a href='{_location.url}' target='_blank'><font color='blue'>{_location.name}</font></a><br>"
        say += f"{_location.name}\n"
    #print(results)
    return {'display': reply, 'say': say.replace('#', 'hash tag ')}


def plot_tweet(tweet_data):     #tweet_data = {tweets: tweet_volume}
    try:
        tweets = tweet_data.keys()
        y_pos = np.arange(len(tweets))
        plt.rcdefaults()
        fig, ax = plt.subplots()
        ax.grid(True)
        ax.barh(y_pos, tweet_data.values(), align='center', color='b', alpha=0.3)
        ax.set_yticks(y_pos)
        ax.set_yticklabels(tweets)
        plt.xticks(rotation=45)
        ax.invert_yaxis()  # labels read top-to-bottom
        ax.set_xlabel('Tweet Volume')
        ax.set_title('Global Twitter Trends Plot')
        plt.subplots_adjust(left=0.3)
        #plt.show()
        plt.savefig(r'C:\Users\emyli\PycharmProjects\Chatbot_Project\tweet.png')
    except Exception as e:
        print(f'error in plot_tweet: {e}')


def twitter_global_trends_graph():
    try:
        result = api.GetTrendsCurrent()[:5]
        tweet_data = {}

        for trend in result:
            _trend = ast.literal_eval(str(trend))
            name = _trend['name']
            try:
                volume = int(_trend['tweet_volume'])
            except KeyError:
                if len(tweet_data) == 0:
                    volume = 1000
                else:
                    k = min(tweet_data, key=tweet_data.get)
                    volume = tweet_data[k] + 1000
            tweet_data[name] = volume
        plot_tweet(tweet_data)
        picture = f'<img src="tweet.png?{time.time()}" alt="Graph of Top Global Trends in Twitter" width="65%" height="65%">'
        # time.sleep(1)
        reply_ = {'display': picture,
                  'say': f"Find below a graph of Top Global Trends in Twitter"}

        return reply_
    except Exception as e:
        '''
        return 'Twitter is currently withholding this information | ' \
               '<a href="https://trends24.in/" target="_blank">view</a>'
        '''
        reply = f'error in plot_tweet_graph: {e}'
        return {'display': reply, 'say': reply}


def twitter_global_trends():
    try:
        result = api.GetTrendsCurrent()[:5]
        reply = "Top Global Trends in Twitter: <br>"
        say = "Top Global Trends in Twitter: \n"
        for trend in result:
            _trend = ast.literal_eval(str(trend))
            #print(_trend)
            name = _trend['name']
            try:
                volume = _trend['tweet_volume']
            except KeyError:
                volume = 20000
            url = _trend['url']

            reply += f'{name} ({volume} Tweets) <a href={url} target="_blank">view</a> <br>'
            say += f'{name} ({volume} Tweets). \n'

        return {'display': reply, 'say': say.replace('#', 'hash tag ')}
    except Exception as e:
        reply = 'Twitter is currently withholding this information ' \
               '<a href="https://trends24.in/" target="_blank">view</a>'
        return {'display': reply, 'say': 'Twitter is currently withholding this information'}


def twitter_search_(query):
    #result = str(api.GetSearch(term=query, count=5)).replace('Status', '').replace("'", "")[:-2].split('), (')
    result = api.GetSearch(term=query, count=5)
    say = f"Top 5 Search Results for {query}"
    display = f"<table id='t01'>\
                                    <tr>\
                                        <th style='text-align:center'>User</th>\
                                        <th style='text-align:center'>Tweet</th>\
                                        <th>Retweets</th>\
                                    </tr>\
                                    "

    for status in result:
        user = status.user.screen_name  #use
        name = status.user.name
        pic = status.user.profile_image_url
        retweet_count = status.retweet_count
        tweet = status.text
        links = re.findall(r'(https?://\S+)', tweet)
        #print(status.media[0].display_url)
        #print('l:', links)
        if links:
            for i in links:
                link = f'<a href={i} target="_blank">link</a>'
                #print(i, link)
                tweet = tweet.replace(i, link)

        display += f"<tr>\
                        <td style='text-align:center'><img src='{pic}' alt='user pic'> <p>{name} @<b>{user}</b></p></td>\
                        <td style='text-align:center'>{tweet}</td>\
                        <td style='text-align:center'>{retweet_count}</td>\
                    </tr>"
    reply = {'display': display.replace(';', ''), 'say': say}
    return reply


def search_twitter(query):
    result = api.GetSearch(term=query, count=5)
    say = f"Find displayed the Top 5 Search Results for {query}"
    display = ''
    for status in result:
        user = status.user.screen_name  #use
        _id_ = status.id
        url = f"https://twitter.com/{user}/status/{_id_}"
        display += embed_tweet(query=url)
    reply = {'display': display, 'say': say}
    return reply


# this function is for word cloud
def twitter_search_cloud(query):
    result = api.GetSearch(term=query, count=30)
    answer = ''
    for status in result:
        tweet = status.text
        links = re.findall(r'(https?://\S+)', tweet)
        if links:
            for i in links:

                tweet = tweet.replace(i, '')
        answer += f'{tweet} '
    return answer.lower().replace(query, '')


def twitter_hash_tags(query):
    tweet_count = 30
    result = api.GetSearch(term=query, count=tweet_count)
    answer = []
    display = ''
    for status in result:
        if len(status.hashtags) > 0:
            for hash in status.hashtags:
                answer.append(hash.text)
    if len(answer) == 0:
        say = f'no hashtags associated with {query} in top {tweet_count} tweets'
        display += say
    else:
        say = f'<b>Hash Tags Associated with {query} in top {tweet_count} tweets</b>'
        display += say
        for hashtag in answer:
            display += f'<br><font color="blue">#{hashtag}</font>'
    reply = {'display': display, 'say': say}
    return reply


# this feature is only for word cloud
def twitter_search_cloud_user(query):
    result = api.GetSearch(term=query, count=50)
    answer = ''
    for status in result:
        answer += f'{status.user.description} '

    return answer


def sentiment_report(query):
    result = api.GetSearch(term=query, count=15)
    tweets = {}
    plot_data = {'Happy': 0, 'Neutral': 0, 'Sad': 0}
    for status in result:
        user = status.user.screen_name  # use
        _id_ = status.id
        url = f"https://twitter.com/{user}/status/{_id_}"
        display = embed_tweet(query=url)
        tweet = status.text
        links = re.findall(r'(https?://\S+)', tweet)

        if links:
            for i in links:
                tweet = tweet.replace(i, '')
        tweet = " ".join(re.findall("[a-zA-Z]+", tweet)).replace('RT', '')
        score = TextBlob(tweet).polarity
        if score > 0:
            percent, senti_ = f'{round(score*100, 1)}%', 'Happy'
        elif score < 0:
            percent, senti_ = f'{round(score*-100, 1)}%', 'Sad'
        else:
            percent, senti_ = '0%', 'Neutral'
        plot_data[senti_] += 1
        tweets[tweet] = {'score': score, 'sentiment': senti_, 'percentage': percent, 'display': display}
    plot_sentiment(plot_data, query)
    display = sentiment_display(tweets) + \
              f'<br><img src="tweet_image/sentiment.png?{time.time()}" alt="Sentiment graph" width="">'
    return {'display': display, 'say': 'find displayed the sentiment analysis for the top 15 tweets'}


def sentiment_display(report):
    display = f'<table id="t01">'
    for tweet in report.values():
        display += f'<tr style="background-color:#15202b">\
                        <td>{tweet["display"]}</td>\
                        <td><div style="color:white; font-size:30px; border-style: solid; border-color:white; ' \
                   f'text-align:center; float:center; background-color:#15202b">' \
                   f'{tweet["percentage"]}</div>'\
                   f'<br><div style="float:center;">' \
                   f'<img src="tweet_image/{tweet["sentiment"].lower()}.png" width="80px">' \
                   f'</div>' \
                   f'</td>\
                      </tr>'
    display += '</table>'
    return display


def plot_sentiment(data, query):
    fig, ax = plt.subplots()
    ax.bar([1,2,3], data.values(), align='center', color=['g','b','r'], alpha=0.3)
    ax.set_xticks([1,2,3])
    ax.set_xticklabels(data.keys())
    ax.set_title(f'Sentiment Analysis for {query.capitalize()}')
    plt.savefig(r'C:\Users\emyli\PycharmProjects\Chatbot_Project\tweet_image\sentiment.png')

#print(twitter_global_trends())
#print(twitter_search_("drake"))
#twitter("tweet test in 2")
#print(twitter_global_trends_graph())
#plot_tweet({'this is not you and me okay but yes': 20, 'no':50})
#print(twitter_search_cloud('microsoft'))
#twitter_search_cloud_user('microsoft')
#print(twitter_hash_tags('microsoft'))
#print(twitter_trend())
# a = "https://twitter.com/BleacherReport/status/1236526501073281029"
# print(embed_tweet(a))
# print(search_twitter(query='drake'))
# print(sentiment_report('drake'))